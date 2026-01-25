"""
運行 knowledge_base 中的 Manim 檔案生成影片
"""
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.verify_examples import extract_scene_name

def run_manim_file(file_path: Path, scene_name: str = None, quality: str = "ql", preview: bool = True) -> Tuple[bool, str]:
    """
    運行 Manim 檔案生成影片
    
    Args:
        file_path: 檔案路徑
        scene_name: Scene 類別名稱（如果為 None 則自動提取）
        quality: 畫質選項 (ql=低, qm=中, qh=高, qk=4K)
        preview: 是否自動播放影片
    
    Returns:
        (是否成功, 輸出訊息)
    """
    if scene_name is None:
        scene_name = extract_scene_name(file_path)
        if scene_name is None:
            return False, "無法提取 Scene 名稱"
    
    # 建立命令
    cmd = ["manim"]
    
    if preview:
        cmd.append("-p")  # 自動播放
    
    cmd.extend([f"-{quality}", str(file_path), scene_name])
    
    try:
        print(f"🚀 正在渲染: {file_path.name} ({scene_name})...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # 尋找生成的影片路徑
            output_lines = result.stdout.split('\n')
            video_path = None
            for line in output_lines:
                if '.mp4' in line or 'media' in line.lower():
                    # 嘗試提取路徑
                    if 'media' in line.lower():
                        parts = line.split()
                        for part in parts:
                            if '.mp4' in part or 'media' in part.lower():
                                video_path = part.strip()
                                break
            
            success_msg = f"✅ 渲染成功: {file_path.name}"
            if video_path:
                success_msg += f"\n   影片位置: {video_path}"
            return True, success_msg
        else:
            error_msg = result.stderr[:500] if result.stderr else result.stdout[:500]
            return False, f"渲染失敗: {error_msg}"
    except subprocess.TimeoutExpired:
        return False, "渲染超時（>5分鐘）"
    except FileNotFoundError:
        return False, "找不到 manim 命令，請確認 Manim 已正確安裝"
    except Exception as e:
        return False, f"錯誤: {str(e)}"

def run_single_file():
    """運行單個檔案"""
    print("="*70)
    print("🎬 運行 Manim 檔案生成影片")
    print("="*70)
    
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("❌ 找不到 knowledge_base 資料夾")
        return
    
    # 列出所有分類
    categories = [d.name for d in kb_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if not categories:
        print("❌ 找不到任何分類資料夾")
        return
    
    print("\n選擇分類:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    choice = input(f"\n請選擇 (1-{len(categories)}): ").strip()
    try:
        category = categories[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ 無效的選擇")
        return
    
    category_dir = kb_path / category
    py_files = list(category_dir.glob("*.py"))
    
    if not py_files:
        print(f"❌ 在 {category} 資料夾中找不到任何 .py 檔案")
        return
    
    print(f"\n找到 {len(py_files)} 個檔案:")
    for i, py_file in enumerate(py_files, 1):
        print(f"  {i}. {py_file.name}")
    
    file_choice = input(f"\n請選擇檔案 (1-{len(py_files)}): ").strip()
    try:
        selected_file = py_files[int(file_choice) - 1]
    except (ValueError, IndexError):
        print("❌ 無效的選擇")
        return
    
    # 選擇畫質
    print("\n選擇畫質:")
    print("  1. ql (低品質，快速)")
    print("  2. qm (中品質)")
    print("  3. qh (高品質)")
    print("  4. qk (4K，最慢)")
    
    quality_choice = input("請選擇 (1-4，預設 1): ").strip() or "1"
    quality_map = {"1": "ql", "2": "qm", "3": "qh", "4": "qk"}
    quality = quality_map.get(quality_choice, "ql")
    
    # 運行
    success, message = run_manim_file(selected_file, quality=quality, preview=True)
    
    print("\n" + "="*70)
    if success:
        print(message)
    else:
        print(f"❌ {message}")
    print("="*70)

def run_all_files():
    """批量運行所有檔案"""
    print("="*70)
    print("🎬 批量運行所有 Manim 檔案")
    print("="*70)
    print("⚠️  警告: 這可能需要很長時間！")
    confirm = input("是否繼續？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消")
        return
    
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("❌ 找不到 knowledge_base 資料夾")
        return
    
    categories = [d.name for d in kb_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    total_files = 0
    success_count = 0
    fail_count = 0
    
    for category in categories:
        category_dir = kb_path / category
        py_files = list(category_dir.glob("*.py"))
        
        if not py_files:
            continue
        
        print(f"\n📁 {category.upper()}")
        print("-"*70)
        
        for py_file in py_files:
            total_files += 1
            success, message = run_manim_file(py_file, quality="ql", preview=False)
            
            if success:
                success_count += 1
                print(f"  ✅ {py_file.name}")
            else:
                fail_count += 1
                print(f"  ❌ {py_file.name}: {message[:100]}")
    
    print("\n" + "="*70)
    print("📊 運行結果統計")
    print("="*70)
    print(f"總檔案數: {total_files}")
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失敗: {fail_count}")
    print("="*70)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        run_all_files()
    else:
        run_single_file()
