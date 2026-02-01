"""
Video Ingestion Pipeline: VLM-Based Captioning for Manim Animations
====================================================================
This script processes MP4 video files, extracts keyframes, uses GPT-4o to generate
detailed visual descriptions, and links them to the corresponding code chunks in Weaviate.

Key Features:
- Keyframe extraction (1 frame per second)
- VLM-based "narration" generation
- Synthetic code hypothesis (bridging visual-to-code gap)
"""

import os
import base64
from pathlib import Path
from typing import List, Dict
import cv2
from openai import OpenAI
import weaviate
from dotenv import load_dotenv

load_dotenv()


class VideoFrameExtractor:
    """Extracts keyframes from MP4 videos."""
    
    def extract_frames(self, video_path: Path, fps: int = 1) -> List[str]:
        """Extract frames at specified FPS and return as base64 strings."""
        cap = cv2.VideoCapture(str(video_path))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(video_fps / fps)
        
        frames_b64 = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                # Encode frame to base64
                _, buffer = cv2.imencode('.jpg', frame)
                frame_b64 = base64.b64encode(buffer).decode('utf-8')
                frames_b64.append(frame_b64)
            
            frame_count += 1
        
        cap.release()
        return frames_b64


class VLMCaptioner:
    """Uses GPT-4o to generate visual descriptions of Manim animations."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_caption(self, frames_b64: List[str], video_name: str) -> str:
        """Generate a detailed narration of the animation."""
        
        # Prepare messages with multiple frames
        content = [
            {
                "type": "text",
                "text": f"""You are analyzing a Manim mathematical animation video titled "{video_name}".

Your task:
1. Describe the sequence of events chronologically.
2. Identify geometric shapes, their colors, and positions.
3. Describe transformations (rotation, translation, scaling, fading).
4. If text or math formulas appear, transcribe them.
5. **Hypothesize the Manim code**: Based on what you see, suggest which Manim classes were likely used (e.g., Create, FadeIn, Rotate, ReplacementTransform).

Format your response as a detailed paragraph suitable for semantic search.
"""
            }
        ]
        
        # Add frames (limit to 5 to avoid token overflow)
        for i, frame_b64 in enumerate(frames_b64[:5]):
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame_b64}"
                }
            })
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
            max_tokens=500
        )
        
        caption = response.choices[0].message.content
        return caption


class WeaviateVideoLinker:
    """Links video descriptions to existing code chunks in Weaviate."""
    
    def __init__(self, url: str = "http://localhost:8080"):
        self.client = weaviate.connect_to_local(host=url.replace("http://", ""))
    
    def update_chunk_with_video(self, source_file: str, video_description: str):
        """Find the code chunk by source_file and add video description."""
        collection = self.client.collections.get("ManimGoldenPair")
        
        # Query for the matching code chunk
        result = collection.query.fetch_objects(
            filters=weaviate.classes.query.Filter.by_property("source_file").equal(source_file),
            limit=1
        )
        
        if result.objects:
            obj = result.objects[0]
            # Update the object with video description
            collection.data.update(
                uuid=obj.uuid,
                properties={"video_description": video_description}
            )
            print(f"✅ Updated {source_file} with video description")
        else:
            print(f"⚠️  No code chunk found for {source_file}")
    
    def close(self):
        self.client.close()


if __name__ == "__main__":
    # Configuration
    VIDEO_DIR = Path("./knowledge_base/videos")  # Where Team Member C stores MP4 files
    
    print("🚀 Starting Video Ingestion Pipeline...")
    
    extractor = VideoFrameExtractor()
    captioner = VLMCaptioner()
    linker = WeaviateVideoLinker()
    
    for video_file in VIDEO_DIR.glob("*.mp4"):
        print(f"🎬 Processing: {video_file.name}")
        
        # Step 1: Extract frames
        frames = extractor.extract_frames(video_file, fps=1)
        print(f"   Extracted {len(frames)} frames")
        
        # Step 2: Generate caption
        caption = captioner.generate_caption(frames, video_file.stem)
        print(f"   Caption: {caption[:100]}...")
        
        # Step 3: Link to code chunk (assumes video name matches .py file)
        source_file = f"{video_file.stem}.py"
        linker.update_chunk_with_video(source_file, caption)
    
    linker.close()
    print("🎉 Video ingestion complete!")
