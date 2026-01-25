"""
為知識庫中的檔案自動生成功能描述
使用 LLM 來分析代碼並生成描述
"""
import sys
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.llm_client import LLMClient

def generate_file_description(file_path: Path) -> str:
    """為單個檔案生成描述"""
    try:
        code_content = file_path.read_text(encoding='utf-8')
        
        # 限制代碼長度（避免超出 token 限制）
        if len(code_content) > 3000:
            code_content = code_content[:3000] + "\n... (代碼已截斷)"
        
        client = LLMClient()
        
        prompt = f"""請為以下 Manim 代碼生成簡短的功能描述。

要求：
1. 用繁體中文描述
2. 功能描述在 50 字以內
3. 列出 2-3 個關鍵的 Manim 技巧或組件
4. 說明這個範例適合用於什麼教學場景

代碼：
```python
{code_content}
```

請以以下格式輸出：
**功能**: [描述]
**關鍵技巧**: [列出2-3個主要 Manim 技巧]
**適用場景**: [教學場景]
"""
        
        description = client.generate(prompt)
        return description
    except Exception as e:
        return f"生成描述時發生錯誤: {e}"

def update_readme_with_description(category_dir: Path, file_name: str, description: str):
    """更新分類 README，添加檔案描述"""
    readme_path = category_dir / "README.md"
    
    if readme_path.exists():
        content = readme_path.read_text(encoding='utf-8')
        
        # 檢查是否已有該檔案的描述
        if file_name in content:
            # 更新現有描述
            pattern = f"## {file_name}.*?(?=##|$)"
            import re
            new_section = f"## {file_name}\n{description}\n"
            content = re.sub(pattern, new_section, content, flags=re.DOTALL)
        else:
            # 添加到檔案列表後
            if "## 檔案列表" in content:
                # 在檔案列表後添加
                insert_pos = content.find("## 檔案列表") + len("## 檔案列表")
                if "\n\n" in content[insert_pos:]:
                    insert_pos = content.find("\n\n", insert_pos) + 2
                new_section = f"\n## {file_name}\n{description}\n"
                content = content[:insert_pos] + new_section + content[insert_pos:]
            else:
                # 添加到檔案末尾
                content += f"\n## {file_name}\n{description}\n"
    else:
        # 建立新的 README
        content = f"""# {category_dir.name.capitalize()} Examples

## 檔案列表

## {file_name}
{description}
"""
    
    readme_path.write_text(content, encoding='utf-8')
    print(f"✅ 已更新: {readme_path}")

def generate_descriptions_for_category(category: str, interactive: bool = True):
    """為某個分類的所有檔案生成描述"""
    kb_path = Path("knowledge_base")
    category_dir = kb_path / category
    
    if not category_dir.exists():
        print(f"❌ 找不到分類資料夾: {category_dir}")
        return
    
    py_files = list(category_dir.glob("*.py"))
    
    if not py_files:
        print(f"⚠️  在 {category_dir} 中未找到任何 .py 檔案")
        return
    
    print(f"\n📝 為 {category} 分類生成描述...")
    print(f"找到 {len(py_files)} 個檔案\n")
    
    for py_file in py_files:
        file_name = py_file.stem
        print(f"處理: {file_name}.py", end=" ... ")
        
        if interactive:
            response = input("生成描述？(y/n): ").strip().lower()
            if response != 'y':
                print("跳過")
                continue
        
        try:
            description = generate_file_description(py_file)
            update_readme_with_description(category_dir, file_name, description)
            print("✅")
        except Exception as e:
            print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        category = sys.argv[1]
        interactive = "--auto" not in sys.argv
        generate_descriptions_for_category(category, interactive=interactive)
    else:
        print("用法: python generate_description.py <category> [--auto]")
        print("範例: python generate_description.py geometry")
        print("      python generate_description.py algebra --auto")
