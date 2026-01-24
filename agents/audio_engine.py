import os
import subprocess
import contextlib
import wave
import time
from pathlib import Path
import requests

# 移除 SDK 依賴，改用 REST API
speechsdk = None

class AudioEngine:
    def __init__(self, output_dir="media/audio", topic=None):
        # 如果提供 topic，創建專屬子目錄
        if topic:
            safe_topic = topic.replace(" ", "_").replace(".", "_").replace("/", "_").replace("*", "x")
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
        audio_paths = []
        
        print(f"🎙️ 開始生成語音 (Azure: {self.azure_enabled})...")

        for i, step in enumerate(steps):
            text = step.get("narrative", "")
            if not text:
                step["duration"] = 2.0
                continue

            # 決定副檔名
            ext = ".mp3" if self.azure_enabled else ".wav"
            filename = f"step_{i:02d}{ext}"
            out_path = self.output_dir / filename
            
            # 1. 生成語音
            if self.azure_enabled:
                self._tts_azure(text, out_path)
            else:
                self._tts_local(text, out_path)
            
            # 2. 計算時長
            duration = self._get_wav_duration(out_path)
            
            # 3. 更新資料
            step["audio_path"] = str(out_path)
            step["duration"] = duration # 關鍵！
            audio_paths.append(out_path)
            
            print(f"  - 語音片段 {i}: {duration:.2f}s | {text[:15]}...")

        # 4. 合併音檔 (給 FFmpeg 用)
        final_ext = ".mp3" if self.azure_enabled else ".wav"
        final_file = self.output_dir / f"final_narrative{final_ext}"
        self._concatenate_audio(audio_paths, final_file)
        
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
            response = requests.post(url, headers=headers, data=ssml.encode('utf-8'))
            if response.status_code == 200:
                with open(abs_out_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"❌ Azure TTS 請求失敗: {response.status_code} - {response.text}")
        except Exception as e:
             print(f"❌ Azure TTS 連線錯誤: {e}")

    def _tts_local(self, text, out_path):
        engine = pyttsx3.init()
        engine.save_to_file(text, str(out_path))
        engine.runAndWait()

    def _get_wav_duration(self, wav_path):
        # 避免檔案還被佔用，稍作緩衝
        time.sleep(0.1)
        
        # 轉換為絕對路徑
        abs_path = Path(wav_path).resolve()
        
        try:
            cmd = [
                "ffprobe", 
                "-v", "error", 
                "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", 
                str(abs_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except Exception as e:
            print(f"⚠️ 無法透過 FFprobe 取得音檔長度: {abs_path}")
            print(f"錯誤詳情: {e}")
            return 2.0

    def _concatenate_audio(self, paths, output_path):
        # 簡單的 ffmpeg concat
        list_file = self.output_dir / "list.txt"
        with open(list_file, "w") as f:
            for p in paths:
                f.write(f"file '{p.resolve()}'\n")
        
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output_path), "-y"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)