"""為 30 題 benchmark_set 重生 TTS。

流程：
1. 從 code.py 抽出所有 set_subtitle 字串（依分鏡順序）
2. 對每條字串呼叫 Azure TTS（zh-TW），存到 raw/tts_step_NN.mp3
3. 用 ffprobe 量每個 mp3 實際長度
4. 改寫 code.py：
   - add_sound 路徑改成新 mp3
   - _audio_dur_N 值改成新 mp3 實際時長

用法:
  python evaluation/benchmark_set/regen_tts.py Q024 --apply
  python evaluation/benchmark_set/regen_tts.py --apply              # 全 30 題
  python evaluation/benchmark_set/regen_tts.py Q024 --voice zh-TW-YunJheNeural
"""
from __future__ import annotations
import re, os, sys, subprocess, argparse, time
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

BASE = Path(__file__).parent

AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION", "eastasia")
assert AZURE_KEY, "AZURE_SPEECH_KEY missing in .env"

DEFAULT_VOICE = "zh-TW-HsiaoChenNeural"  # 女聲，最常用
SUBTITLE_RE = re.compile(r'(self\.set_subtitle\(\s*["\'])(.+?)(["\'],\s*run_time=)', re.DOTALL)


def tts_azure(text: str, out_path: Path, voice: str = DEFAULT_VOICE, retries: int = 3) -> bool:
    """呼叫 Azure TTS，存 mp3。"""
    import requests
    url = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-160kbitrate-mono-mp3",
        "User-Agent": "BenchmarkSet_Regen",
    }
    # 保留 SSML 的 prosody rate（-5% 跟原 audio_engine 一致）
    # 注意：要 escape XML 特殊字元
    safe_text = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">
    <voice name="{voice}">
        <prosody rate="-5.0%">{safe_text}</prosody>
    </voice>
</speak>"""

    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, data=ssml.encode("utf-8"), timeout=60)
            if r.status_code == 200 and r.content:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(r.content)
                return True
            print(f"  ⚠ TTS HTTP {r.status_code}: {r.text[:120]}")
        except Exception as e:
            print(f"  ⚠ TTS error: {e}")
        time.sleep(1.5 * (attempt + 1))
    return False


def get_mp3_duration(mp3: Path) -> float:
    """用 ffprobe 取 mp3 時長（秒）。"""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
        capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def extract_subtitles(code_path: Path) -> list[tuple[int, str, int]]:
    """從 code.py 抽 set_subtitle，回傳 [(index, text, line_no)]"""
    src = code_path.read_text(encoding="utf-8")
    results = []
    for i, m in enumerate(SUBTITLE_RE.finditer(src)):
        text = m.group(2)
        line_no = src[:m.start()].count("\n") + 1
        results.append((i, text, line_no))
    return results


def process_qid(qid: str, voice: str, apply: bool) -> dict:
    qd = BASE / qid
    code = qd / "code.py"
    if not code.exists():
        return {"ok": False, "msg": "code.py 不存在"}

    subtitles = extract_subtitles(code)
    if not subtitles:
        return {"ok": False, "msg": "沒找到 set_subtitle"}

    print(f"\n▶ {qid}: {len(subtitles)} 條字幕")
    tts_dir = qd / "raw" / "tts_regen"
    tts_dir.mkdir(parents=True, exist_ok=True)

    durations = []
    for idx, text, _ in subtitles:
        mp3 = tts_dir / f"step_{idx:02d}.mp3"
        if mp3.exists() and mp3.stat().st_size > 1000:
            dur = get_mp3_duration(mp3)
            print(f"  [{idx}] cached: {dur:.2f}s — {text[:40]}...")
        else:
            print(f"  [{idx}] generating: {text[:40]}...", flush=True)
            ok = tts_azure(text, mp3, voice=voice)
            if not ok:
                return {"ok": False, "msg": f"TTS 失敗 idx={idx}"}
            dur = get_mp3_duration(mp3)
            print(f"      ✓ {dur:.2f}s")
        durations.append((idx, str(mp3.resolve()), dur))
        time.sleep(0.2)  # rate limit 保險

    # 改寫 code.py
    if apply:
        src = code.read_text(encoding="utf-8")
        for idx, mp3_path, dur in durations:
            # 替換 add_sound 路徑
            old_sound_re = re.compile(
                rf'self\.add_sound\("[^"]+"\)(\s*#[^\n]*duration=[\d.]+s)?',
                re.DOTALL,
            )
            # 替換每個 add_sound (按出現順序 N=idx)
            # 簡化：只替換第 (idx+1) 次出現
            occurrences = list(old_sound_re.finditer(src))
            if idx < len(occurrences):
                m = occurrences[idx]
                new_sound_line = f'self.add_sound("{mp3_path}")  # [regen] duration={dur:.2f}s'
                src = src[:m.start()] + new_sound_line + src[m.end():]

            # 替換 _audio_dur_N
            dur_re = re.compile(rf'(_audio_dur_{idx} = )[\d.]+(\s*#)')
            src = dur_re.sub(rf'\g<1>{dur:.2f}\2', src)

        # 備份
        bak = code.with_suffix(".py.tts-bak")
        if not bak.exists():
            bak.write_text(code.read_text(encoding="utf-8"), encoding="utf-8")
        code.write_text(src, encoding="utf-8")
        print(f"  ✓ code.py 改寫完成（備份 .py.tts-bak）")

    total_new = sum(d for _, _, d in durations)
    return {"ok": True, "msg": f"{len(durations)} 條，總長 {total_new:.1f}s"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qids", nargs="*")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    args = ap.parse_args()

    if args.qids:
        qids = args.qids
    else:
        qids = sorted(d.name for d in BASE.iterdir() if d.is_dir() and d.name.startswith("Q"))

    print(f"Voice: {args.voice}")
    print(f"Apply: {args.apply}")
    print(f"題數: {len(qids)}")

    for qid in qids:
        result = process_qid(qid, args.voice, args.apply)
        status = "✅" if result["ok"] else "❌"
        print(f"  {status} {qid}: {result['msg']}")


if __name__ == "__main__":
    main()
