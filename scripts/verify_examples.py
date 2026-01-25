"""
驗證 knowledge_base 中的 Manim 檔案是否可以正常運行
"""
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

def extract_scene_name(file_path: Path) -> str:
    """從檔案中提取 Scene 類別名稱（簡化版）"""
    try:
        content = file_path.read_text(encoding='utf-8')
        # 尋找 class XxxScene(Scene) 或 class Xxx(Scene)
        import re
        matches = re.findall(r'class\s+(\w+)\s*\(.*Scene\)', content)
        if matches:
            return matches[0]
        # 如果找不到，嘗試找第一個類別
        matches = re.findall(r'class\s+(\w+)', content)
        if matches:
            return matches[0]
        return "Scene"  # 預設
    except Exception as e:
        print(f"⚠️  無法讀取 {file_path}: {e}")
        return None

def verify_manim_file(file_path: Path, scene_name: str = None, timeout: int = 60) -> Tuple[bool, str]:
    """
    驗證 Manim 檔案是否可以正常運行
    
    Args:
        file_path: 檔案路徑
        scene_name: Scene 類別名稱（如果為 None 則自動提取）
        timeout: 超時時間（秒）
    
    Returns:
        (是否成功, 錯誤訊息)
    """
    if scene_name is None:
        scene_name = extract_scene_name(file_path)
        if scene_name is None:
            return False, "無法提取 Scene 名稱"
    
    try:
        # 使用 -pql 參數（preview, quality low, 最後一幀）
        # 這樣可以快速驗證而不會渲染完整動畫
        result = subprocess.run(
            ["manim", "-pql", str(file_path), scene_name],
            capture_output=True,
            timeout=timeout,
            text=True
        )
        
        if result.returncode == 0:
            return True, ""
        else:
            error_msg = result.stderr[:500] if result.stderr else result.stdout[:500]
            return False, error_msg
    except subprocess.TimeoutExpired:
        return False, f"執行超時（>{timeout}秒）"
    except FileNotFoundError:
        return False, "找不到 manim 命令，請確認 Manim 已正確安裝"
    except Exception as e:
        return False, str(e)

def verify_all_examples(knowledge_base_dir: str = "knowledge_base", verbose: bool = True) -> dict:
    """
    驗證所有範例檔案
    
    Returns:
        統計字典
    """
    kb_path = Path(knowledge_base_dir)
    if not kb_path.exists():
        print(f"❌ 找不到知識庫資料夾: {kb_path}")
        return {}
    
    stats = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "categories": {}
    }
    
    # 遍歷所有 .py 檔案
    py_files = list(kb_path.rglob("*.py"))
    stats["total"] = len(py_files)
    
    if py_files:
        print(f"\n🔍 找到 {len(py_files)} 個 Python 檔案，開始驗證...\n")
    else:
        print(f"⚠️  在 {kb_path} 中未找到任何 .py 檔案")
        return stats
    
    for py_file in py_files:
        # 取得分類名稱
        category = py_file.parent.name
        if category not in stats["categories"]:
            stats["categories"][category] = {"total": 0, "passed": 0, "failed": 0}
        
        stats["categories"][category]["total"] += 1
        
        if verbose:
            print(f"📄 驗證: {py_file.relative_to(kb_path)}", end=" ... ")
        
        scene_name = extract_scene_name(py_file)
        success, error = verify_manim_file(py_file, scene_name)
        
        if success:
            stats["passed"] += 1
            stats["categories"][category]["passed"] += 1
            if verbose:
                print("✅")
        else:
            stats["failed"] += 1
            stats["categories"][category]["failed"] += 1
            if verbose:
                print(f"❌")
                if error:
                    print(f"   錯誤: {error[:200]}")
    
    return stats

def print_stats(stats: dict):
    """列印統計結果"""
    print("\n" + "="*60)
    print("📊 驗證結果統計")
    print("="*60)
    print(f"總檔案數: {stats['total']}")
    print(f"✅ 通過: {stats['passed']}")
    print(f"❌ 失敗: {stats['failed']}")
    
    if stats['categories']:
        print("\n📁 分類統計:")
        for category, cat_stats in stats['categories'].items():
            pass_rate = (cat_stats['passed'] / cat_stats['total'] * 100) if cat_stats['total'] > 0 else 0
            print(f"  {category}: {cat_stats['passed']}/{cat_stats['total']} ({pass_rate:.1f}%)")
    
    print("="*60)

if __name__ == "__main__":
    verbose = "--quiet" not in sys.argv
    stats = verify_all_examples(verbose=verbose)
    
    if stats:
        print_stats(stats)
        
        # 如果失敗數 > 0，返回非零退出碼
        if stats["failed"] > 0:
            sys.exit(1)
