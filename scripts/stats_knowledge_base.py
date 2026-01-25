"""
統計 knowledge_base 中的檔案數量與資訊
"""
from pathlib import Path
from collections import defaultdict
import re

def count_lines_and_comments(file_path: Path) -> dict:
    """統計檔案的行數和註解數"""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        total_lines = len(lines)
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif stripped.startswith('#'):
                comment_lines += 1
            else:
                code_lines += 1
        
        return {
            "total": total_lines,
            "code": code_lines,
            "comments": comment_lines,
            "blank": blank_lines
        }
    except Exception as e:
        return {"total": 0, "code": 0, "comments": 0, "blank": 0}

def extract_manim_imports(file_path: Path) -> set:
    """提取 Manim 相關的 import"""
    try:
        content = file_path.read_text(encoding='utf-8')
        imports = set()
        
        # 尋找 from manim import 或 import manim
        patterns = [
            r'from\s+manim\s+import\s+([^\n]+)',
            r'import\s+manim[^\n]*',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, str):
                    imports.add(match.strip())
        
        return imports
    except:
        return set()

def analyze_knowledge_base(knowledge_base_dir: str = "knowledge_base") -> dict:
    """分析知識庫"""
    kb_path = Path(knowledge_base_dir)
    if not kb_path.exists():
        print(f"❌ 找不到知識庫資料夾: {kb_path}")
        return {}
    
    stats = {
        "total_files": 0,
        "categories": defaultdict(lambda: {
            "files": 0,
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "manim_imports": set()
        })
    }
    
    # 遍歷所有 .py 檔案
    for py_file in kb_path.rglob("*.py"):
        category = py_file.parent.name
        if category == "knowledge_base":  # 跳過根目錄的檔案
            category = "root"
        
        stats["total_files"] += 1
        cat_stats = stats["categories"][category]
        cat_stats["files"] += 1
        
        # 統計行數
        line_stats = count_lines_and_comments(py_file)
        cat_stats["total_lines"] += line_stats["total"]
        cat_stats["code_lines"] += line_stats["code"]
        cat_stats["comment_lines"] += line_stats["comments"]
        
        # 收集 imports
        imports = extract_manim_imports(py_file)
        cat_stats["manim_imports"].update(imports)
    
    return stats

def print_stats(stats: dict):
    """列印統計結果"""
    print("\n" + "="*70)
    print("📊 知識庫統計報告")
    print("="*70)
    
    print(f"\n📁 總檔案數: {stats['total_files']}")
    
    if stats['categories']:
        print("\n📂 分類詳細統計:")
        print("-"*70)
        
        for category, cat_stats in sorted(stats['categories'].items()):
            print(f"\n🔹 {category.upper()}")
            print(f"   檔案數: {cat_stats['files']}")
            print(f"   總行數: {cat_stats['total_lines']}")
            print(f"   代碼行: {cat_stats['code_lines']}")
            print(f"   註解行: {cat_stats['comment_lines']}")
            
            comment_ratio = (cat_stats['comment_lines'] / cat_stats['total_lines'] * 100) if cat_stats['total_lines'] > 0 else 0
            print(f"   註解比例: {comment_ratio:.1f}%")
            
            if cat_stats['manim_imports']:
                print(f"   常用 Manim 組件: {', '.join(list(cat_stats['manim_imports'])[:5])}")
        
        # 目標進度
        print("\n" + "-"*70)
        print("🎯 目標進度:")
        total = stats['total_files']
        target = 20
        progress = min(100, (total / target) * 100)
        print(f"   目前: {total} / {target} 個檔案 ({progress:.1f}%)")
        
        if total < target:
            needed = target - total
            print(f"   ⚠️  還需要 {needed} 個檔案才能達到目標")
        else:
            print(f"   ✅ 已達到目標！")
    
    print("="*70)

if __name__ == "__main__":
    stats = analyze_knowledge_base()
    if stats:
        print_stats(stats)
