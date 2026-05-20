"""Strip system-specific code from generated Scene .py files.

Converts `runs/<timestamp>/<case_id>/code.py` into clean RAG examples
suitable for `knowledge_base/kb150_v2/<chapter>/<SceneName>.py`.

Strip targets (verified stable across 3 stable_outputs samples, see plan):
  - `class SubtitleManager:` block
  - `class SceneInstrumentor:` block
  - construct() init lines:
      self._instrumentor = SceneInstrumentor(...)
      self._sm = SubtitleManager(self)
      self.set_subtitle = self._sm.show
  - `self.set_subtitle(...)` calls
  - `self.add_sound(...)` calls (with `# [auto-injected]` comment)
  - `_audio_dur_N = X.XX` variable lines
  - `remaining_N = max(...)` + corresponding `self.wait(...)` lines
  - `class GeneratedScene(Scene)` → `class <SceneName>(Scene)`

Usage:
  python rag/strip_system_code.py \
      --runs-dir runs/<timestamp> \
      --topics evaluation/kb150_v2_topics.json \
      --out knowledge_base/kb150_v2

  # dry-run (preview)
  python rag/strip_system_code.py --runs-dir runs/<ts> --topics ... --out ... --dry-run

  # single file
  python rag/strip_system_code.py --single runs/<ts>/KB150V2_X/code.py \
      --scene-name X --chapter Y --topics evaluation/kb150_v2_topics.json --out knowledge_base/kb150_v2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


# ── Strip regexes (line-based unless noted) ────────────────────────────
RE_SET_SUBTITLE_CALL = re.compile(r"^\s*self\.set_subtitle\(.*?\)\s*(?:#.*)?$")
RE_ADD_SOUND = re.compile(r"^\s*self\.add_sound\(.*?\)\s*(?:#.*)?$")
RE_AUDIO_DUR = re.compile(r"^(\s*)_audio_dur_(\d+)\s*=\s*([\d.]+)\s*(?:#.*)?$")
# Generic: `remaining_N = max(<anything>)` — formula varies, parsed via eval()
RE_REMAINING_VAR = re.compile(r"^(\s*)remaining_(\d+)\s*=\s*(max\(.+\))\s*(?:#.*)?$")
RE_WAIT_REMAINING = re.compile(r"^(\s*)self\.wait\(\s*max\(\s*([\d.]+)\s*,\s*remaining_(\d+)\s*\)\s*\)\s*(?:#.*)?$")
RE_WAIT_REMAINING2 = re.compile(r"^(\s*)self\.wait\(remaining_(\d+)\)\s*(?:#.*)?$")
RE_INSTRUMENTOR_INIT = re.compile(r"^\s*self\._instrumentor\s*=\s*SceneInstrumentor\(.*\)\s*$")
RE_SM_INIT = re.compile(r"^\s*self\._sm\s*=\s*SubtitleManager\(self\)\s*$")
RE_SET_SUBTITLE_BIND = re.compile(r"^\s*self\.set_subtitle\s*=\s*self\._sm\.show\s*$")
RE_GENERATED_SCENE_CLASS = re.compile(r"^(class\s+)GeneratedScene(\s*\(Scene\)\s*:)\s*$")
# Also: anim_time_N = X.X — used by remaining_N calc; keep for our recompute then delete
RE_ANIM_TIME = re.compile(r"^(\s*)anim_time_(\d+)\s*=\s*([\d.]+)\s*(?:#.*)?$")


RE_IF_REMAINING = re.compile(r"^(\s*)if\s+remaining_\d+\s*>\s*0\s*:\s*$")
RE_INDENTED_WAIT_REMAINING = re.compile(r"^\s+self\.wait\(remaining_\d+\)\s*(?:#.*)?$")


def _is_strip_line(line: str) -> bool:
    """Return True if this line should be removed (system code, NOT animation timing).

    Note: WAIT_REMAINING / REMAINING_VAR / AUDIO_DUR are NOT in this list — they're
    handled by _recompute_waits() which converts them to fixed-time self.wait() calls
    to preserve animation pacing for teaching examples.
    """
    return any(
        rx.match(line)
        for rx in (
            RE_SET_SUBTITLE_CALL,
            RE_ADD_SOUND,
            RE_INSTRUMENTOR_INIT,
            RE_SM_INIT,
            RE_SET_SUBTITLE_BIND,
        )
    )


def _recompute_waits(lines: list[str]) -> list[str]:
    """Strategy C: replace `self.wait(max(0.1, remaining_N))` with `self.wait(<computed>)`.

    Computes the original remaining time using the formula seen in generated code:
        remaining_N = max(min_wait, _audio_dur_K - anim_time_K + slack)
    Then emits `self.wait(round(remaining_N, 2))` so animation pacing is preserved
    without leaking audio_dur / anim_time / remaining variables into the RAG example.

    Process:
      1. First pass: collect _audio_dur_N and anim_time_N values
      2. Second pass: when seeing `remaining_N = max(...)`, compute concrete value
      3. Third pass: replace `self.wait(max(.., remaining_N))` with the concrete wait
      4. Drop the original _audio_dur / remaining_ assignments
    """
    # Pass 1+2: build lookup from variable name → concrete value
    audio_dur: dict[str, float] = {}
    anim_time: dict[str, float] = {}
    remaining_val: dict[str, float] = {}

    for ln in lines:
        m = RE_AUDIO_DUR.match(ln)
        if m:
            audio_dur[m.group(2)] = float(m.group(3))
            continue
        m = RE_ANIM_TIME.match(ln)
        if m:
            anim_time[m.group(2)] = float(m.group(3))
            continue
        m = RE_REMAINING_VAR.match(ln)
        if m:
            # Generic: eval the max() expression with collected variables in scope.
            # Supports all variants:
            #   max(0.1, _audio_dur_K - anim_time_K + 0.5)
            #   max(0.1, _audio_dur_K - anim_time_K - 1.0 + 0.5)
            #   max(0.1, _audio_dur_K - (1.2 + 0.3 + anim_time_K) + 0.5)
            scope = {f"_audio_dur_{k}": v for k, v in audio_dur.items()}
            scope.update({f"anim_time_{k}": v for k, v in anim_time.items()})
            scope["max"] = max
            try:
                computed = eval(m.group(3), {"__builtins__": {}}, scope)
                remaining_val[m.group(2)] = round(float(computed), 2)
            except Exception:
                pass  # leave as-is; will fall back to wait(1.5)

    # Pass 3: rewrite lines
    out: list[str] = []
    for ln in lines:
        # Replace `self.wait(max(min, remaining_N))` with `self.wait(<value>)`
        m = RE_WAIT_REMAINING.match(ln)
        if m:
            indent = m.group(1)
            min_wait = float(m.group(2))
            n = m.group(3)
            if n in remaining_val:
                final = max(min_wait, remaining_val[n])
                out.append(f"{indent}self.wait({round(final, 2)})")
            else:
                # fallback: use a sensible default (1.5s teaching pause)
                out.append(f"{indent}self.wait(1.5)")
            continue
        m = RE_WAIT_REMAINING2.match(ln)
        if m:
            indent = m.group(1)
            n = m.group(2)
            if n in remaining_val:
                out.append(f"{indent}self.wait({remaining_val[n]})")
            else:
                out.append(f"{indent}self.wait(1.5)")
            continue
        # Drop _audio_dur_N and remaining_N assignment lines
        if RE_AUDIO_DUR.match(ln) or RE_REMAINING_VAR.match(ln):
            continue
        # Keep anim_time_N — it's referenced by `run_time=anim_time_N` in self.play() calls
        out.append(ln)
    return out


def _strip_if_remaining_blocks(lines: list[str]) -> list[str]:
    """Remove `if remaining_N > 0:` + body until dedent."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = RE_IF_REMAINING.match(ln)
        if m:
            base_indent = len(m.group(1))
            # skip the if line + all subsequent indented lines
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "" or (len(nxt) - len(nxt.lstrip())) > base_indent:
                    i += 1
                else:
                    break
            continue
        out.append(ln)
        i += 1
    return out


def _strip_class_block(src: str, class_name: str) -> str:
    """Remove a top-level `class <class_name>:` block (until next top-level def/class)."""
    lines = src.split("\n")
    out: list[str] = []
    in_class = False
    for line in lines:
        if not in_class:
            if re.match(rf"^class\s+{re.escape(class_name)}\s*:", line):
                in_class = True
                continue
            out.append(line)
        else:
            # leave block when hitting a non-indented non-blank line
            if line and not line.startswith((" ", "\t")):
                in_class = False
                out.append(line)
    return "\n".join(out)


def strip_source(src: str, target_scene_name: str) -> str:
    """Apply all strip operations to a generated Scene .py source."""
    # 1. Remove SubtitleManager + SceneInstrumentor class blocks
    src = _strip_class_block(src, "SubtitleManager")
    src = _strip_class_block(src, "SceneInstrumentor")

    # 2. Line-based strips
    lines = src.split("\n")
    # 2a. Remove `if remaining_N > 0:` blocks (multi-line)
    lines = _strip_if_remaining_blocks(lines)
    # 2b. Recompute wait() with concrete values (Strategy C — preserve teaching pace)
    lines = _recompute_waits(lines)
    # 2c. Remove single-line strip patterns (subtitle/audio/init only — NOT wait)
    kept = [ln for ln in lines if not _is_strip_line(ln)]

    # 3. Rename GeneratedScene → target_scene_name
    renamed = []
    for ln in kept:
        m = RE_GENERATED_SCENE_CLASS.match(ln)
        if m:
            renamed.append(f"{m.group(1)}{target_scene_name}{m.group(2)}")
        else:
            renamed.append(ln)

    # 4. Collapse runs of >2 blank lines
    final: list[str] = []
    blank_run = 0
    for ln in renamed:
        if ln.strip() == "":
            blank_run += 1
            if blank_run <= 2:
                final.append(ln)
        else:
            blank_run = 0
            final.append(ln)

    return "\n".join(final).rstrip() + "\n"


def has_residue(src: str) -> list[str]:
    """Return list of residue indicators (empty list = clean).

    Only checks executable code lines (skips `#` comment lines), since the
    Coder's `[VISUAL REASONING]` header often mentions `self.set_subtitle`
    in passing — those comments are harmless.

    Note: `anim_time_N` variables are kept (used by self.play(run_time=anim_time_N))
    and not considered residue.
    """
    keywords = ("set_subtitle", "_audio_dur", "remaining_", "SubtitleManager",
                "SceneInstrumentor", "add_sound", "_sm")
    issues: list[str] = []
    for line in src.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        for kw in keywords:
            if kw in line and kw not in issues:
                issues.append(kw)
    if "GeneratedScene" in src and not any(
        line.lstrip().startswith("#") and "GeneratedScene" in line
        for line in src.split("\n")
    ):
        # only flag if there's an executable mention
        for line in src.split("\n"):
            if "GeneratedScene" in line and not line.lstrip().startswith("#"):
                issues.append("GeneratedScene (rename failed)")
                break
    return issues


def process_one(code_path: Path, scene_name: str, chapter: str, out_root: Path,
                dry_run: bool = False) -> tuple[bool, str]:
    """Strip one generated code.py and write to kb150_v2/<chapter>/<scene>.py."""
    src = code_path.read_text(encoding="utf-8")
    cleaned = strip_source(src, scene_name)

    residue = has_residue(cleaned)
    status = "ok" if not residue else f"⚠️ residue: {residue}"

    if dry_run:
        return (not residue, f"[DRY-RUN] {scene_name}: {status} (out lines={cleaned.count(chr(10))})")

    out_dir = out_root / chapter
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{scene_name}.py"
    out_path.write_text(cleaned, encoding="utf-8")
    try:
        out_display = out_path.relative_to(REPO)
    except ValueError:
        out_display = out_path
    return (not residue, f"{scene_name} → {out_display} : {status}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runs-dir", type=Path, help="runs/<timestamp> directory with KB150V2_X/code.py subdirs")
    p.add_argument("--single", type=Path, help="Single code.py path (use with --scene-name --chapter)")
    p.add_argument("--scene-name", help="Required if --single")
    p.add_argument("--chapter", help="Required if --single")
    p.add_argument("--topics", type=Path, default=REPO / "evaluation" / "kb150_v2_topics.json",
                   help="kb150_v2_topics.json — used to map case_id → chapter/scene")
    p.add_argument("--out", type=Path, default=REPO / "knowledge_base" / "kb150_v2",
                   help="Output root (default: knowledge_base/kb150_v2)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    # Build scene_name → chapter lookup from topics
    topics = json.loads(args.topics.read_text(encoding="utf-8"))
    scene_to_chapter: dict[str, str] = {}
    for chapter, scenes in topics.items():
        if chapter.startswith("_"):
            continue
        for name in scenes:
            scene_to_chapter[name] = chapter

    # ── Single file mode ──
    if args.single:
        if not args.scene_name or not args.chapter:
            sys.exit("--single requires --scene-name and --chapter")
        ok, msg = process_one(args.single, args.scene_name, args.chapter, args.out, args.dry_run)
        print(("✅ " if ok else "❌ ") + msg)
        return 0 if ok else 1

    # ── Batch mode (runs-dir) ──
    if not args.runs_dir:
        sys.exit("Need either --runs-dir or --single")

    case_dirs = sorted(d for d in args.runs_dir.iterdir() if d.is_dir() and d.name.startswith("KB150V2_"))
    if not case_dirs:
        sys.exit(f"No KB150V2_* subdirs found in {args.runs_dir}")

    ok_count = fail_count = 0
    for d in case_dirs:
        scene = d.name.replace("KB150V2_", "", 1)
        chapter = scene_to_chapter.get(scene)
        if not chapter:
            print(f"⚠️ unknown scene (not in topics): {scene}")
            fail_count += 1
            continue
        code_path = d / "code.py"
        if not code_path.exists():
            print(f"⚠️ no code.py in {d}")
            fail_count += 1
            continue
        ok, msg = process_one(code_path, scene, chapter, args.out, args.dry_run)
        print(("✅ " if ok else "❌ ") + msg)
        if ok:
            ok_count += 1
        else:
            fail_count += 1

    print(f"\nDone. {ok_count} ok, {fail_count} fail.")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main() or 0)
