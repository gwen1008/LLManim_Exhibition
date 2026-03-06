# streamlit run app.py
"""
EMA Streamlit Web 介面
在瀏覽器完成：輸入數學主題 → 即時 log → 影片播放
"""

import os
import subprocess
import sys
import time

import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def topic_to_safe_name(topic: str) -> str:
    """與 main.py 一致：用於 stable_outputs/{safe_name}.mp4"""
    return topic.replace(" ", "_").replace(".", "_").replace("/", "_").replace("*", "x").replace("+", "_plus_").replace("-", "_minus_")


def run_main_stream(topic: str):
    """以 subprocess 執行 main.py，stdin 傳入 topic；產生即時 log 的 generator。"""
    # Force output buffering for real-time streaming
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=PROJECT_ROOT,
        env=env,
    )
    # Store process in session state to allow stopping
    st.session_state["process"] = proc

    try:
        # 1. Send Topic
        proc.stdin.write(topic.strip() + "\n")
        proc.stdin.flush()

        
    except (BrokenPipeError, OSError):
        pass # Process might have exited early or finished
    finally:
        try:
            proc.stdin.close()
        except:
            pass

    for line in iter(proc.stdout.readline, ""):
        yield line
    proc.wait()
    # Clear process from session state when done
    if "process" in st.session_state:
        del st.session_state["process"]


st.set_page_config(page_title="EMA – Manim 動畫生成", page_icon="🎬", layout="centered")
st.title("🎬 EMA：Manim 動畫生成")
st.caption("輸入數學主題，由系統規劃腳本、生成程式碼並渲染影片。")

topic = st.text_input(
    "動畫主題",
    placeholder="例如：Pythagorean theorem、二元一次方程式",
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 1])
with col1:
    generate = st.button("生成動畫", type="primary", use_container_width=True)
with col2:
    stop = st.button("🔴 停止生成", type="secondary", use_container_width=True)

if stop:
    if "process" in st.session_state:
        proc = st.session_state["process"]
        proc.terminate()
        st.warning("已強制停止生成程序。")
        del st.session_state["process"]
        st.stop()
    else:
        st.info("目前沒有正在執行的生成程序。")

if generate:
    if not (topic and topic.strip()):
        st.warning("請輸入動畫主題。")
        st.stop()
    t = topic.strip()
    safe = topic_to_safe_name(t)

    with st.spinner(f"正在使用 {agent_mode} 生成中... 請稍候..."):
        try:
            import time
            start_time = time.time()
            st.write("🚀 正在啟動主程序...")
            
            # Stream output from main.py
            line_count = 0
            for line in run_main_stream(t):
                st.write(line.rstrip())
                line_count += 1
            
            elapsed = time.time() - start_time
            st.write(f"\n✅ 主程序執行完畢 (共 {line_count} 行輸出, 耗時 {elapsed:.1f}s)")
            
        except Exception as e:
            import traceback
            st.error(f"執行失敗：{e}")
            st.code(traceback.format_exc())
            st.stop()

    # Find video path (Support versioned files)
    output_folder = os.path.join(PROJECT_ROOT, "stable_outputs")
    
    # 1. Search for all files matching the pattern {safe_name}*.mp4
    candidates = []
    if os.path.exists(output_folder):
        for file in os.listdir(output_folder):
            if file.startswith(safe) and file.endswith(".mp4"):
                candidates.append(os.path.join(output_folder, file))
    
    # 2. Sort by modification time (newest first)
    video_path = None
    if candidates:
        candidates.sort(key=os.path.getmtime, reverse=True)
        # Default to the latest video
        video_path = candidates[0]
    
    # 3. Check if user selected a history version
    if "selected_video" in st.session_state and os.path.exists(st.session_state["selected_video"]):
        # Ensure the selected video still relates to the current search
        if st.session_state["selected_video"] in candidates:
            video_path = st.session_state["selected_video"]
    
    # 4. Render Video Player & History
    st.subheader("📹 生成結果")
    if video_path and os.path.exists(video_path):
        st.video(video_path)
        
        # Determine if we are watching the latest or an older version
        is_latest = (video_path == candidates[0])
        version_label = "🆕 最新版本" if is_latest else "📜 歷史版本"
        st.caption(f"📂 正在播放: {os.path.basename(video_path)} ({version_label})")
        
        # History List
        if len(candidates) > 1:
            with st.expander("📜 歷史版本 (點擊播放)", expanded=False):
                for path in candidates:
                    # Skip the currently playing video in the list? Or show all?
                    # Let's show all for clarity, but highlight current
                    col_h1, col_h2, col_h3 = st.columns([0.1, 0.7, 0.2])
                    
                    is_current = (path == video_path)
                    
                    with col_h1:
                        if is_current:
                            st.write("▶️")
                        else:
                            st.write("🎞️")
                    with col_h2:
                        st.caption(os.path.basename(path))
                        st.caption(f"📅 {time.ctime(os.path.getmtime(path))}")
                    with col_h3:
                        if not is_current:
                            if st.button("播放", key=path):
                                st.session_state["selected_video"] = path
                                st.rerun()
                        else:
                            st.button("播放中", key=path, disabled=True)
    else:
        st.warning("本次未產生影片，請查看上方 log 排查錯誤。")
