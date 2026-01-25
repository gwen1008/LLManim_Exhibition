"""
為已下載的檔案添加或更新說明
"""
import sys
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.download_from_github import add_description_to_readme

def add_description_interactive():
    """互動式添加說明"""
    print("="*70)
    print("📝 為檔案添加說明")
    print("="*70)
    
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("❌ 找不到 knowledge_base 資料夾")
        print("   請先執行: python scripts/quick_start.py")
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
    
    # 檢查是否已有說明
    readme_path = category_dir / "README.md"
    existing_desc = None
    if readme_path.exists():
        content = readme_path.read_text(encoding='utf-8')
        file_section = f"## {selected_file.stem}"
        if file_section in content:
            import re
            match = re.search(f"{re.escape(file_section)}\\s*\\*\\*說明\\*\\*:\\s*(.+?)(?=\\n\\n|## |$)", content, re.DOTALL)
            if match:
                existing_desc = match.group(1).strip()
                print(f"\n⚠️  此檔案已有說明: {existing_desc}")
                update = input("是否要更新？(y/n): ").strip().lower()
                if update != 'y':
                    return
    
    # 輸入新說明
    print(f"\n請輸入檔案說明（簡短描述 {selected_file.name} 的功能）:")
    if existing_desc:
        print(f"目前說明: {existing_desc}")
        print("（直接 Enter 保持不變，或輸入新說明覆蓋）")
    
    description = input("說明: ").strip()
    
    if not description:
        if existing_desc:
            print("保持原有說明不變")
            return
        else:
            print("❌ 未輸入說明")
            return
    
    # 添加說明
    add_description_to_readme(category, selected_file.name, description)
    print(f"\n✅ 已為 {selected_file.name} 添加說明！")

def add_description_batch():
    """批量為檔案添加說明"""
    kb_path = Path("knowledge_base")
    if not kb_path.exists():
        print("❌ 找不到 knowledge_base 資料夾")
        return
    
    categories = [d.name for d in kb_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    print("="*70)
    print("📝 批量添加說明")
    print("="*70)
    
    for category in categories:
        category_dir = kb_path / category
        py_files = list(category_dir.glob("*.py"))
        
        if not py_files:
            continue
        
        print(f"\n📁 {category.upper()}")
        print("-"*70)
        
        for py_file in py_files:
            # 檢查是否已有說明
            readme_path = category_dir / "README.md"
            has_desc = False
            if readme_path.exists():
                content = readme_path.read_text(encoding='utf-8')
                if f"## {py_file.stem}" in content:
                    has_desc = True
            
            if has_desc:
                print(f"  ✓ {py_file.name} (已有說明)")
            else:
                print(f"  - {py_file.name}")
                desc = input(f"    請輸入說明（直接 Enter 跳過）: ").strip()
                if desc:
                    add_description_to_readme(category, py_file.name, desc)
                    print(f"    ✅ 已添加說明")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        add_description_batch()
    else:
        add_description_interactive()
