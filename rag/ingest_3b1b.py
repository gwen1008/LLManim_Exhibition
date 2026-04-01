"""
3b1b Videos → ManimCE RAG Ingestion Pipeline
============================================
將 3Blue1Brown 的 ManimGL 場景翻譯成 ManimCE，索引進 Weaviate。

前置條件：
1. docker-compose up -d （Weaviate 要跑起來）
2. python rag/ingest_code.py （先建好 ManimGoldenPair schema）
3. .env 裡有 DEEPSEEK_API_KEY

Usage:
    python rag/ingest_3b1b.py --source ~/Desktop/3b1b_videos
    python rag/ingest_3b1b.py --source ~/Desktop/3b1b_videos --years _2019 _2020
    python rag/ingest_3b1b.py --source ~/Desktop/3b1b_videos --dry-run
"""

import ast
import sys
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# Allow importing from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

import weaviate
from agents.core.llm_client import LLMClient

# ─── Config ───────────────────────────────────────────────────────────────────

DEFAULT_YEARS = ["_2018", "_2019", "_2020", "_2021", "_2022", "_2023", "_2024"]

# 這些 keyword 出現代表 file 依賴外部 data，跳過
EXTERNAL_DATA_SIGNALS = [
    "DATA_DIR",
    "load_from_disk",
    "datasets.load",
    "Path(get_output_dir()",
    "image_net",
    "OWL3",
]

# MaminGL 的 Scene 基底類別（CE 只有 Scene 這些）
GL_SCENE_BASES = {
    "Scene",
    "GraphScene",
    "MovingCameraScene",
    "ZoomedScene",
    "ThreeDScene",
    "SpecialThreeDScene",
    "SampleSpaceScene",
    "TeacherStudentsScene",
    "PiCreatureScene",
    "LinearTransformationScene",
    "NumberLineScene",
}

# 用來提取 used_modules 的 CE class set（與 ingest_code.py 保持一致）
MANIM_CE_CLASSES = {
    "Circle", "Square", "Rectangle", "Triangle", "Dot", "Line", "Arrow", "Vector",
    "Polygon", "RegularPolygon", "Ellipse", "Annulus", "Arc", "Sector",
    "ArcBetweenPoints", "CurvedArrow", "DoubleArrow", "DashedLine",
    "Brace", "BraceLabel", "SurroundingRectangle", "Cross", "Underline",
    "Text", "MathTex", "Tex", "MarkupText", "DecimalNumber", "Integer",
    "NumberLine", "Axes", "NumberPlane", "ComplexPlane",
    "FunctionGraph", "ParametricFunction", "ImplicitFunction",
    "VGroup", "Group", "Mobject", "VMobject", "Angle", "RightAngle",
    "Create", "Uncreate", "Write", "Unwrite", "DrawBorderThenFill",
    "FadeIn", "FadeOut", "FadeTransform",
    "GrowFromCenter", "GrowArrow", "GrowFromPoint", "GrowFromEdge",
    "Transform", "ReplacementTransform", "TransformMatchingTex", "TransformMatchingShapes",
    "Rotate", "ScaleInPlace", "MoveToTarget",
    "Indicate", "Flash", "Circumscribe", "Wiggle", "ApplyWave",
    "ShowPassingFlash", "AnimationGroup", "LaggedStart", "LaggedStartMap", "Succession",
    "ValueTracker", "always_redraw",
    "Scene", "MovingCameraScene", "ZoomedScene", "ThreeDScene",
}

# ─── Prompts ──────────────────────────────────────────────────────────────────

TRANSLATE_SYSTEM = """\
你是 Manim 專家，專門將 ManimGL 代碼翻譯成 ManimCE (manim community edition v0.19)。

翻譯規則：
1. import 統一改成 `from manim import *`，移除所有 manimlib / manim_imports_ext 相關 import
2. CONFIG dict 改成 __init__() 的預設參數：
   CONFIG = {"length": 3}  →  def __init__(self, length=3, **kwargs): super().__init__(**kwargs)
3. API 名稱替換：
   - ShowCreation          → Create
   - TextMobject           → Text（純文字）或 MathTex（含 LaTeX 公式）
   - TexMobject / OldTex   → MathTex
   - FadeInFromDown/Up     → FadeIn(shift=DOWN/UP)
   - GraphScene            → Scene，坐標軸改成 ax = Axes(...); self.add(ax)
   - setup_axes()          → 刪除，在 construct() 裡直接建 Axes
   - .highlight(color)     → .set_color(color)
   - .fade(factor)         → .set_opacity(1 - factor)
   - get_graph(func)       → ax.plot(func)
   - coords_to_point(x, y) → ax.c2p(x, y)
4. 動畫語法：
   - self.play() 裡的 .shift()/.move_to() 改成 .animate.shift()/.animate.move_to()
   - color= 不能傳給 Create/Write/FadeIn，先 .set_color() 再播放
5. 找不到對應的 MaminGL 方法：用最接近的 CE 實作替代，或略過不影響核心邏輯的部分
6. 保留數學邏輯和動畫結構，不要改變場景的視覺意圖

輸出格式（必須嚴格遵守）：
第一行：# DESCRIPTION: <一句自然語言，說明這個場景在視覺上展示什麼>
然後輸出翻譯後的代碼，包在 ```python ... ``` 中。

範例：
# DESCRIPTION: 展示正弦波在坐標軸上從左到右動態繪製的過程。
```python
from manim import *

class DrawSinWave(Scene):
    def construct(self):
        ax = Axes(x_range=[0, 4*PI], y_range=[-2, 2])
        self.add(ax)
        graph = ax.plot(np.sin, color=BLUE)
        self.play(Create(graph), run_time=3)
        self.wait()
```
"""

TRANSLATE_USER = """\
請翻譯以下 MaminGL 場景類別（來源：{filename}）：

```python
{source}
```
"""

# ─── Extraction ───────────────────────────────────────────────────────────────

def has_external_data_dep(source: str) -> bool:
    return any(signal in source for signal in EXTERNAL_DATA_SIGNALS)


def extract_gl_scenes(filepath: Path, source_root: Path) -> List[Dict]:
    """
    AST 解析 MaminGL 檔案，提取 Scene 子類別的原始代碼。
    回傳 list of raw chunk dicts（尚未翻譯）。
    """
    try:
        source = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    if has_external_data_dep(source):
        print(f"  ⏭️  Skip {filepath.name} (外部 data 依賴)")
        return []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        print(f"  ⚠️  SyntaxError: {filepath.name}")
        return []

    chunks = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        # 取得 base class 名稱
        base_names: set[str] = set()
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_names.add(base.id)
            elif isinstance(base, ast.Attribute):
                base_names.add(base.attr)

        if not base_names.intersection(GL_SCENE_BASES):
            continue

        class_code = ast.get_source_segment(source, node)
        if not class_code or len(class_code.splitlines()) < 6:
            continue

        # topic: 取年份資料夾的下一層目錄名稱（e.g. _2019/diffyq/... → "diffyq"）
        try:
            rel_parts = filepath.relative_to(source_root).parts
            topic = rel_parts[1] if len(rel_parts) > 2 else rel_parts[0]
        except ValueError:
            topic = filepath.parent.name

        chunks.append({
            "class_name": node.name,
            "raw_gl_code": class_code,
            "source_file": str(filepath.relative_to(source_root)),
            "topic": topic,
            "filename": filepath.name,
        })

    return chunks


# ─── Translation ──────────────────────────────────────────────────────────────

def translate_chunk(chunk: Dict, llm: LLMClient) -> Optional[Dict]:
    """
    用 DeepSeek 將單一 GL chunk 翻譯成 ManimCE，回傳 Weaviate-ready dict。
    翻譯失敗或語法錯誤回傳 None。
    """
    try:
        response = llm.ask(
            system_prompt=TRANSLATE_SYSTEM,
            user_prompt=TRANSLATE_USER.format(
                source=chunk["raw_gl_code"],
                filename=chunk["filename"],
            ),
            role="coder",
            temperature=0,
        )
    except Exception as e:
        print(f"  ❌ LLM 錯誤 ({chunk['class_name']}): {e}")
        return None

    # 解析 description
    description = f"[3b1b translated] {chunk['class_name']} — {chunk['source_file']}"
    for line in response.splitlines():
        stripped = line.strip()
        if stripped.startswith("# DESCRIPTION:"):
            desc_text = stripped.replace("# DESCRIPTION:", "").strip()
            if desc_text:
                description = f"[3b1b translated] {desc_text}"
            break

    # 提取代碼
    translated_code = LLMClient.extract_code(response)

    # 語法驗證
    try:
        ast.parse(translated_code)
    except SyntaxError as e:
        print(f"  ⚠️  翻譯語法錯誤 ({chunk['class_name']}): {e} — 跳過")
        return None

    # 提取使用的 CE modules
    used_modules: set[str] = set()
    try:
        for node in ast.walk(ast.parse(translated_code)):
            if isinstance(node, ast.Name) and node.id in MANIM_CE_CLASSES:
                used_modules.add(node.id)
    except Exception:
        pass

    complexity = translated_code.count("self.play") + translated_code.count("self.add")

    return {
        "code_content": translated_code,
        "imports": "from manim import *",
        "complexity_score": complexity,
        "manim_modules": ", ".join(sorted(used_modules)),
        "source_file": f"3b1b/{chunk['source_file']}",
        "topic": chunk["topic"],
        "video_description": description,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Ingest 3b1b MaminGL → ManimCE into Weaviate RAG")
    parser.add_argument("--source", required=True, help="3b1b/videos repo 路徑，例如 ~/Desktop/3b1b_videos")
    parser.add_argument("--years", nargs="+", default=DEFAULT_YEARS, help="要處理的年份資料夾")
    parser.add_argument("--dry-run", action="store_true", help="只列出會處理的 Scene，不翻譯也不上傳")
    parser.add_argument("--save-local", action="store_true", help="同時將翻譯結果存到 knowledge_base/3b1b/")
    parser.add_argument("--checkpoint", default="rag/.3b1b_checkpoint.jsonl", help="斷點記錄檔路徑")
    args = parser.parse_args()

    source_dir = Path(args.source).expanduser().resolve()
    if not source_dir.exists():
        print(f"❌ 找不到來源目錄：{source_dir}")
        sys.exit(1)

    print(f"🚀 3b1b RAG Ingestion")
    print(f"   Source    : {source_dir}")
    print(f"   Years     : {args.years}")
    print(f"   Dry run   : {args.dry_run}")
    print(f"   Save local: {args.save_local}")
    print(f"   Checkpoint: {args.checkpoint}\n")

    # ── Step 0: 載入 checkpoint（已翻譯的）─────────────────────────────────
    checkpoint_path = Path(args.checkpoint)
    already_translated: List[Dict] = []
    done_keys: set[str] = set()  # "source_file::class_name"
    if checkpoint_path.exists():
        with checkpoint_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    chunk = json.loads(line)
                    already_translated.append(chunk)
                    done_keys.add(chunk["_key"])
        print(f"♻️  從 checkpoint 載入 {len(already_translated)} 個已翻譯 chunks，將跳過這些 Scene\n")

    # ── Step 1: 收集所有 GL Scene chunks ──────────────────────────────────
    all_raw: List[Dict] = []
    for year in args.years:
        year_dir = source_dir / year
        if not year_dir.exists():
            print(f"⚠️  找不到：{year_dir.name}")
            continue
        print(f"📂 {year}/")
        for py_file in sorted(year_dir.rglob("*.py")):
            chunks = extract_gl_scenes(py_file, source_dir)
            if chunks:
                print(f"  ✅ {py_file.relative_to(source_dir)}: {len(chunks)} scene(s)")
            all_raw.extend(chunks)

    print(f"\n📊 找到 {len(all_raw)} 個 GL Scene classes")

    if not all_raw:
        print("沒有可處理的 Scene，結束。")
        return

    if args.dry_run:
        print("\n🔍 Dry run 清單：")
        for c in all_raw:
            print(f"  [{c['topic']}] {c['source_file']} → {c['class_name']}")
        return

    # ── Step 2: LLM 翻譯 ──────────────────────────────────────────────────
    llm = LLMClient(debug=False)
    translated: List[Dict] = []
    failed = 0

    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    ckpt_file = checkpoint_path.open("a", encoding="utf-8")

    for i, chunk in enumerate(all_raw, 1):
        key = f"{chunk['source_file']}::{chunk['class_name']}"
        if key in done_keys:
            print(f"[{i}/{len(all_raw)}] ⏭️  跳過（已翻譯）{chunk['class_name']}")
            continue

        print(f"\n[{i}/{len(all_raw)}] {chunk['class_name']}  ({chunk['source_file']})")
        result = translate_chunk(chunk, llm)
        if result:
            result["_key"] = key
            translated.append(result)
            ckpt_file.write(json.dumps(result, ensure_ascii=False) + "\n")
            ckpt_file.flush()
            print(f"  ✅ {result['video_description'][:80]}")
        else:
            failed += 1
        time.sleep(0.3)  # DeepSeek rate limit buffer

    ckpt_file.close()

    # checkpoint 裡的舊資料也要上傳（如果是第一次跑到底）
    all_translated = already_translated + translated
    print(f"\n📊 翻譯結果：{len(translated)} 新增，{failed} 失敗，{len(already_translated)} 從 checkpoint 載入，共 {len(all_translated)} 個")

    if not all_translated:
        print("❌ 沒有成功翻譯的 chunk，不上傳。")
        print(llm.get_session_report())
        return

    # ── Step 3 (optional): 存到本地 knowledge_base/3b1b/ ─────────────────
    if args.save_local:
        kb_root = Path(__file__).parent.parent / "knowledge_base" / "3b1b"
        saved = 0
        for chunk in all_translated:
            # source_file 格式：3b1b/_2018/fourier.py → _2018/fourier.py
            rel_path = Path(chunk["source_file"].removeprefix("3b1b/"))
            # 每個 Scene 存成獨立 .py 檔：knowledge_base/3b1b/_2018/fourier/FourierScene.py
            out_dir = kb_root / rel_path.parent / rel_path.stem
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{chunk['topic']}_{chunk['code_content'].split('class ')[1].split('(')[0].strip()}.py"
            # 取 class name 更可靠的方式
            try:
                class_name = [
                    n.name for n in ast.walk(ast.parse(chunk["code_content"]))
                    if isinstance(n, ast.ClassDef)
                ][0]
            except Exception:
                class_name = "UnknownScene"
            out_file = out_dir / f"{class_name}.py"
            content = (
                f"# Source: {chunk['source_file']}\n"
                f"# Description: {chunk['video_description']}\n\n"
                f"{chunk['imports']}\n\n"
                f"{chunk['code_content']}\n"
            )
            out_file.write_text(content, encoding="utf-8")
            saved += 1
        print(f"💾 已存 {saved} 個檔案到 knowledge_base/3b1b/")

    # ── Step 4: 上傳到 Weaviate ───────────────────────────────────────────
    print(f"\n📤 上傳 {len(all_translated)} 個 chunks 到 Weaviate...")
    try:
        client = weaviate.connect_to_local()
        collection = client.collections.get("ManimGoldenPair")
        upload_chunks = [{k: v for k, v in c.items() if k != "_key"} for c in all_translated]
        with collection.batch.dynamic() as batch:
            for chunk in upload_chunks:
                batch.add_object(properties=chunk)
        client.close()
        print(f"✅ 上傳完成！ManimGoldenPair 現在有 3b1b 翻譯範例。")
        # 上傳成功後刪除 checkpoint，避免下次重複上傳
        if checkpoint_path.exists():
            checkpoint_path.unlink()
            print(f"🗑️  Checkpoint 已清除：{checkpoint_path}")
    except Exception as e:
        print(f"❌ Weaviate 上傳失敗：{e}")
        print("   確認 docker-compose up -d 有跑起來")
        print(f"   翻譯結果已保留在 checkpoint：{checkpoint_path}")

    print(llm.get_session_report())


if __name__ == "__main__":
    main()
