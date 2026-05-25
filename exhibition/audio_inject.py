"""Standalone copy of _inject_audio_sync from main.py for use in exhibition runners."""
import re as _re


def inject_audio_sync(code: str, updated_sequence: list, final_audio_path: str) -> str:
    fake_audio_pattern = _re.compile(
        r'[ \t]*audio_step\w+\s*=\s*["\'][^"\']+["\'][^\n]*\n'
        r'(?:[ \t]*if\s+os\.path\.exists\([^\)]+\):[^\n]*\n'
        r'[ \t]*self\.add_sound\([^\)]+\)[^\n]*\n'
        r'(?:[ \t]*elif[^\n]*\n[ \t]*self\.add_sound\([^\)]+\)[^\n]*\n)?)?',
        _re.MULTILINE
    )
    cleaned, n_removed = fake_audio_pattern.subn('', code)
    if n_removed > 0:
        code = cleaned
        print(f"[Audio Inject] Removed {n_removed} fake audio blocks")

    audio_steps = [(i, s) for i, s in enumerate(updated_sequence) if s.get("audio_path")]
    if not audio_steps:
        return code

    step_pattern = _re.compile(r'^( +)(# Step \d+)', _re.MULTILINE)
    step_markers = list(step_pattern.finditer(code))

    injected = False
    if step_markers and audio_steps:
        n_inject = min(len(step_markers), len(audio_steps))
        for marker_idx in range(n_inject - 1, -1, -1):
            match = step_markers[marker_idx]
            indent = match.group(1)
            _, step_data = audio_steps[marker_idx]
            audio_path = step_data["audio_path"]
            duration = step_data.get("duration", 2.0)
            dur_var = f"_audio_dur_{marker_idx}"
            inject_lines = (
                f'{indent}self.add_sound("{audio_path}")  # [auto-injected]\n'
                f'{indent}{dur_var} = {duration:.2f}  # [audio-sync]\n'
            )
            code = code[:match.start()] + inject_lines + code[match.start():]

        def _patch_subtitle(seg, dur_var):
            anchor = 'self.set_subtitle('
            start = seg.find(anchor)
            if start == -1:
                return seg
            depth, end = 0, start + len(anchor) - 1
            for i, ch in enumerate(seg[start + len(anchor) - 1:], start + len(anchor) - 1):
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
            call = seg[start:end + 1]
            if 'run_time' in call:
                return seg
            return seg[:start] + seg[start:end] + f', run_time={dur_var})' + seg[end + 1:]

        step_markers2 = list(step_pattern.finditer(code))
        for marker_idx in range(n_inject - 1, -1, -1):
            match = step_markers2[marker_idx]
            dur_var = f"_audio_dur_{marker_idx}"
            seg_end = step_markers2[marker_idx + 1].start() if marker_idx + 1 < len(step_markers2) else len(code)
            seg = code[match.start():seg_end]
            code = code[:match.start()] + _patch_subtitle(seg, dur_var) + code[seg_end:]

        injected = True
        print(f"[Audio Inject] Injected {n_inject} add_sound() calls")

    if not injected:
        m = _re.search(r'(def construct\(self\):\s*\n)', code)
        if m and final_audio_path:
            pos = m.end()
            indent = _re.match(r'^(\s+)', code[pos:pos + 80])
            indent = indent.group(1) if indent else "        "
            code = code[:pos] + f'{indent}self.add_sound("{final_audio_path}")  # [fallback]\n' + code[pos:]
            print("[Audio Inject] Fallback: injected final_narrative at construct() start")

    return code
