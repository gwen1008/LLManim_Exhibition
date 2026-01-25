"""
建立知識庫資料夾結構
"""
import os
from pathlib import Path

def setup_knowledge_base():
    """建立 knowledge_base 資料夾結構"""
    base_dir = Path("knowledge_base")
    
    # 主要分類資料夾
    categories = ["geometry", "algebra", "calculus", "arithmetic", "statistics"]
    
    for category in categories:
        category_dir = base_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # 為每個分類建立 README.md
        readme_path = category_dir / "README.md"
        if not readme_path.exists():
            readme_content = f"""# {category.capitalize()} Examples

這個資料夾包含 {category} 相關的 Manim 範例代碼。

## 檔案列表

（待補充）

## 分類說明

（待補充）
"""
            readme_path.write_text(readme_content, encoding='utf-8')
            print(f"✅ 建立: {category_dir}/README.md")
    
    # 建立總 README
    main_readme = base_dir / "README.md"
    if not main_readme.exists():
        main_readme_content = """# Manim 知識庫 (Knowledge Base)

這個資料夾包含高品質的 Manim 代碼範例，用於訓練 RAG 系統。

## 資料夾結構

- `geometry/`: 幾何相關範例
- `algebra/`: 代數相關範例
- `calculus/`: 微積分相關範例
- `arithmetic/`: 算術相關範例
- `statistics/`: 統計相關範例

## 使用方式

這些範例將被用於：
1. RAG 系統的檢索增強生成
2. AI Coder 的參考資料
3. 教學與學習資源

## 品質標準

每個範例檔案應：
- ✅ 可以正常運行
- ✅ 有清晰的註解
- ✅ 展示明確的數學概念
- ✅ 使用現代 Manim Community 語法

## 統計

（使用 `python scripts/stats_knowledge_base.py` 查看詳細統計）
"""
        main_readme.write_text(main_readme_content, encoding='utf-8')
        print(f"✅ 建立: {base_dir}/README.md")
    
    print(f"\n📁 知識庫結構已建立於: {base_dir.absolute()}")
    print(f"📊 已建立 {len(categories)} 個分類資料夾")

if __name__ == "__main__":
    setup_knowledge_base()
