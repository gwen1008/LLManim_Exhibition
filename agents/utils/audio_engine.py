import os
import subprocess
import contextlib
import wave
import time
from pathlib import Path
import requests
import threading
from pathlib import Path

# 移除 SDK 依賴，改用 REST API
speechsdk = None

class AudioEngine:
    @staticmethod
    def get_safe_dir_name(topic: str) -> str:
        """
        Canonical topic → filesystem-safe directory name.
        Used by both AudioEngine and RefiningLoop to ensure consistent audio_dir lookup.
        """
        import hashlib
        topic_hash = hashlib.md5(topic.encode('utf-8')).hexdigest()[:10]
        ascii_topic = "".join([c if c.isalnum() else "_" for c in topic])[:20]
        return f"{ascii_topic}_{topic_hash}"

    def __init__(self, output_dir="media/audio", topic=None):
        # 如果提供 topic，創建專屬子目錄
        # Sanitize topic for folder name (IMPORTANT: FFmpeg on some Macs fails with Unicode paths)
        if topic:
            safe_topic = AudioEngine.get_safe_dir_name(topic)
            self.output_dir = Path(output_dir) / safe_topic
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Azure 設定
        self.azure_key = os.getenv("AZURE_SPEECH_KEY")
        self.azure_region = os.getenv("AZURE_SPEECH_REGION")
        # 只要有 Key 和 Region 就可以使用 REST API
        self.azure_enabled = bool(self.azure_key and self.azure_region)
        self.voice_name = "zh-TW-HsiaoChenNeural"

    def generate_narration(self, steps: list):
        """
        輸入: 包含 'narrative' 的字典列表
        輸出: 更新後的列表 (新增 'audio_path' 和 'duration'), 以及合併後的總音檔路徑
        """
        audio_paths = [None] * len(steps)
        
        print(f"🎙️ 開始生成語音 (Azure: {self.azure_enabled})...")

        import concurrent.futures

        def _process_step(i, step):
            text = step.get("narrative", "")
            if not text:
                step["duration"] = 2.0
                return i, step, None

            ext = ".mp3" if self.azure_enabled else ".wav"
            filename = f"step_{i:02d}{ext}"
            out_path = self.output_dir / filename
            
            if self.azure_enabled:
                self._tts_azure(text, out_path)
            else:
                self._tts_local(text, out_path)
            
            duration = self._get_wav_duration(out_path)
            
            step["audio_path"] = str(out_path.resolve())
            step["duration"] = duration 
            
            print(f"  - 語音片段 {i}: {duration:.2f}s | {text[:15]}...")
            return i, step, out_path

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(steps), 8)) as executor:
            futures = [executor.submit(_process_step, i, step) for i, step in enumerate(steps)]
            for future in concurrent.futures.as_completed(futures):
                i, updated_step, out_path = future.result()
                steps[i] = updated_step
                audio_paths[i] = out_path

        # Filter out Nones
        valid_paths = [p for p in audio_paths if p is not None]

        # 4. 合併音檔 (給 FFmpeg 用)
        final_ext = ".mp3" if self.azure_enabled else ".wav"
        final_file = self.output_dir / f"final_narrative{final_ext}"
        self._concatenate_audio(valid_paths, final_file)
        
        return steps, str(final_file)

    def _tts_azure(self, text, out_path):
        # 確保使用絕對路徑
        abs_out_path = Path(out_path).resolve()
        
        url = f"https://{self.azure_region}.tts.speech.microsoft.com/cognitiveservices/v1"
        headers = {
            "Ocp-Apim-Subscription-Key": self.azure_key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-160kbitrate-mono-mp3",
            "User-Agent": "EMA_System"
        }
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">
            <voice name="{self.voice_name}">
                <prosody rate="-5.0%">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        try:
            # 加上 timeout 防止微軟伺服器卡住導致 Agent 永遠掛起
            response = requests.post(url, headers=headers, data=ssml.encode('utf-8'), timeout=15)
            if response.status_code == 200:
                if len(response.content) == 0:
                    print(f"❌ Azure TTS 回傳了 0 bytes (可能是語系不支援)")
                    return
                with open(abs_out_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"❌ Azure TTS 請求失敗: {response.status_code} - {response.text}")
        except Exception as e:
             print(f"❌ Azure TTS 連線錯誤: {e}")

    _pyttsx3_lock = threading.Lock()  # Class-level lock to serialize pyttsx3 calls

    def _tts_local(self, text, out_path):
        # pyttsx3 is NOT thread-safe (singleton runLoop).
        # Use a class-level lock to serialize calls when running in ThreadPoolExecutor.
        try:
            import pyttsx3
            with AudioEngine._pyttsx3_lock:
                engine = pyttsx3.init()
                engine.save_to_file(text, str(out_path))
                engine.runAndWait()
        except ImportError:
            print("❌ 錯誤: 缺少 pyttsx3 套件。若不使用 Azure TTS，請執行 pip install pyttsx3。")
            # 產生空音檔避免程式完全中斷
            with open(out_path, 'wb') as f:
                pass 

    def _get_wav_duration(self, wav_path):
        """Get audio duration without spawning ffprobe subprocess.

        - MP3 (Azure TTS CBR 160kbps): parse MPEG frame header for bitrate, compute from file size
        - WAV: use stdlib wave module
        - Fallback: ffprobe subprocess
        """
        abs_path = Path(wav_path).resolve()

        # 等待檔案完整寫入（替代 sleep，更穩定）
        for _ in range(6):
            if abs_path.exists() and abs_path.stat().st_size > 0:
                break
            time.sleep(0.05)

        try:
            if not abs_path.exists() or abs_path.stat().st_size == 0:
                return 2.0

            suffix = abs_path.suffix.lower()

            # WAV: use stdlib (zero overhead)
            if suffix == ".wav":
                with wave.open(str(abs_path), 'rb') as wf:
                    frames = wf.getnframes()
                    rate = wf.getframerate()
                    return frames / rate if rate > 0 else 2.0

            # MP3: parse MPEG frame header to get bitrate, then compute duration
            if suffix == ".mp3":
                import struct
                file_size = abs_path.stat().st_size
                with open(abs_path, "rb") as f:
                    # Skip ID3v2 tag if present
                    header = f.read(10)
                    if header[:3] == b'ID3':
                        # ID3v2 size is stored as synchsafe integer in bytes 6-9
                        tag_size = (header[6] << 21) | (header[7] << 14) | (header[8] << 7) | header[9]
                        f.seek(10 + tag_size)
                    else:
                        f.seek(0)

                    # Find first MPEG sync word (0xFF 0xE0+)
                    sync_data = f.read(4)
                    attempts = 0
                    while len(sync_data) == 4 and attempts < 8192:
                        if sync_data[0] == 0xFF and (sync_data[1] & 0xE0) == 0xE0:
                            break
                        f.seek(-3, 1)
                        sync_data = f.read(4)
                        attempts += 1

                    if len(sync_data) == 4 and sync_data[0] == 0xFF and (sync_data[1] & 0xE0) == 0xE0:
                        # MPEG version: bits 4-3 of byte 1
                        version_bits = (sync_data[1] >> 3) & 0x03
                        # Bitrate index: bits 7-4 of byte 2
                        bitrate_idx = (sync_data[2] >> 4) & 0x0F

                        # MPEG1 Layer III bitrate table (kbps)
                        _BITRATES_V1_L3 = [0, 32, 40, 48, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0, 0]
                        # MPEG2/2.5 Layer III bitrate table
                        _BITRATES_V2_L3 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0]

                        if version_bits == 3:  # MPEG1
                            bitrate_kbps = _BITRATES_V1_L3[bitrate_idx] if bitrate_idx < 16 else 0
                        else:  # MPEG2 or MPEG2.5
                            bitrate_kbps = _BITRATES_V2_L3[bitrate_idx] if bitrate_idx < 16 else 0

                        if bitrate_kbps > 0:
                            # For CBR: duration ≈ file_size * 8 / bitrate
                            # Subtract ID3 tag size for accuracy
                            audio_bytes = file_size - f.tell() + 4
                            duration = audio_bytes * 8 / (bitrate_kbps * 1000)
                            return max(0.1, duration)

            # Fallback: ffprobe (for edge cases)
            cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(abs_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)
            output = result.stdout.strip()
            return float(output) if output else 2.0
        except Exception as e:
            print(f"⚠️ 無法取得音檔長度: {abs_path} ({e})")
            return 2.0

    def _concatenate_audio(self, paths, output_path):
        # 簡單的 ffmpeg concat
        list_file = self.output_dir / "list.txt"
        with open(list_file, "w") as f:
            for p in paths:
                f.write(f"file '{p.resolve()}'\n")
        
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output_path), "-y"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)