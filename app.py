# streamlit run app.py
"""
EMA Streamlit Web 介面
在瀏覽器完成：輸入數學主題 → 即時 log → 影片播放
"""

import os
import subprocess
import sys

import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def topic_to_safe_name(topic: str) -> str:
    """與 main.py 一致：用於 stable_outputs/{safe_name}.mp4"""
    return topic.replace(" ", "_").replace(".", "_").replace("/", "_").replace("*", "x")


def run_main_stream(topic: str):
    """以 subprocess 執行 main.py，stdin 傳入 topic；產生即時 log 的 generator。"""
    proc = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=PROJECT_ROOT,
        env=os.environ.copy(),
    )
    try:
        proc.stdin.write(topic.strip() + "\n")
        proc.stdin.flush()
    finally:
        proc.stdin.close()

    for line in iter(proc.stdout.readline, ""):
        yield line
    proc.wait()


st.set_page_config(page_title="EMA – Manim 動畫生成", page_icon="🎬", layout="centered")
st.title("🎬 EMA：Manim 動畫生成")
st.caption("輸入數學主題，由系統規劃腳本、生成程式碼並渲染影片。")

topic = st.text_input(
    "動畫主題",
    placeholder="例如：Pythagorean theorem、二元一次方程式",
    label_visibility="collapsed",
)
generate = st.button("生成動畫", type="primary")

if generate:
    if not (topic and topic.strip()):
        st.warning("請輸入動畫主題。")
        st.stop()
    t = topic.strip()
    safe = topic_to_safe_name(t)

    with st.spinner("生成中，請稍候…"):
        try:
            st.write_stream(run_main_stream(t))
        except Exception as e:
            st.error(f"執行失敗：{e}")
            st.stop()

    video_path = os.path.join(PROJECT_ROOT, "stable_outputs", safe + ".mp4")
    st.subheader("📹 生成結果")
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.warning("本次未產生影片，請查看上方 log 排查錯誤。")
