"""
整理 AI 研究相關檔案到 research/ 資料夾
"""
from pathlib import Path
import shutil
import sys

def organize_research_files(force=False):
    """將 AI 研究相關檔案移動到 research/ 資料夾"""
    project_root = Path(__file__).parent.parent
    research_dir = project_root / "research"
    
    # 建立 research 資料夾（如果不存在）
    research_dir.mkdir(exist_ok=True)
    
    # 定義要移動的檔案
    files_to_move = [
        "deep_research_rag.md",
        "manimator_paper_extract.txt"
    ]
    
    moved_files = []
    skipped_files = []
    not_found_files = []
    
    for filename in files_to_move:
        source = project_root / filename
        destination = research_dir / filename
        
        if not source.exists():
            # 檢查是否已經在 research 資料夾中
            if destination.exists():
                print(f"[INFO] 檔案已在 research/ 資料夾: {filename}")
                continue
            else:
                not_found_files.append(filename)
                continue
        
        if destination.exists() and not force:
            print(f"[SKIP] 檔案已存在: {destination.name}")
            skipped_files.append(filename)
            continue
        
        try:
            shutil.move(str(source), str(destination))
            moved_files.append(filename)
            print(f"[OK] 已移動: {filename} -> research/{filename}")
        except Exception as e:
            print(f"[ERROR] 移動失敗 {filename}: {e}")
    
    print("\n" + "="*60)
    print("整理結果")
    print("="*60)
    print(f"已移動: {len(moved_files)} 個檔案")
    if moved_files:
        for f in moved_files:
            print(f"  - {f}")
    
    if skipped_files:
        print(f"\n跳過: {len(skipped_files)} 個檔案")
        for f in skipped_files:
            print(f"  - {f}")
    
    if not_found_files:
        print(f"\n找不到: {len(not_found_files)} 個檔案")
        for f in not_found_files:
            print(f"  - {f}")
    
    print(f"\n研究資料夾位置: {research_dir.absolute()}")
    print("="*60)

if __name__ == "__main__":
    force = "--force" in sys.argv
    organize_research_files(force=force)
