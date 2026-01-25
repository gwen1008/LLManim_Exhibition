"""
從 GitHub 下載 Manim 範例檔案
支援多種方式：單個檔案 URL、倉庫路徑、或批量下載
"""
import sys
import requests
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def download_file_from_raw_url(raw_url: str, save_path: Path) -> bool:
    """從 GitHub raw URL 下載單個檔案"""
    try:
        print(f"📥 下載: {raw_url}")
        response = requests.get(raw_url, timeout=30)
        
        if response.status_code == 200:
            # 確保目錄存在
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 寫入檔案
            save_path.write_text(response.text, encoding='utf-8')
            print(f"✅ 已保存: {save_path}")
            return True
        else:
            print(f"❌ 下載失敗 (狀態碼: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def convert_github_url_to_raw(github_url: str) -> str:
    """將 GitHub 網頁 URL 轉換為 raw URL"""
    # 處理不同的 GitHub URL 格式
    patterns = [
        r'github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)',  # 標準格式
        r'github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)',  # 目錄格式
    ]
    
    for pattern in patterns:
        match = re.search(pattern, github_url)
        if match:
            user, repo, branch, path = match.groups()
            return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
    
    # 如果已經是 raw URL，直接返回
    if 'raw.githubusercontent.com' in github_url:
        return github_url
    
    return None

def suggest_category(filename: str, content: str = "") -> str:
    """根據檔名和內容建議分類"""
    filename_lower = filename.lower()
    content_lower = content.lower() if content else ""
    
    # 幾何相關關鍵詞
    geometry_keywords = ['circle', 'square', 'triangle', 'polygon', 'pythagorean', 
                        'angle', 'geometry', 'shape', 'transform', 'rotate', 'scale']
    
    # 代數相關關鍵詞
    algebra_keywords = ['equation', 'algebra', 'quadratic', 'polynomial', 'function',
                       'solve', 'factor', 'expand', 'simplify', 'tex', 'math']
    
    # 微積分相關關鍵詞
    calculus_keywords = ['derivative', 'integral', 'calculus', 'limit', 'riemann',
                        'differentiate', 'integrate', 'slope', 'tangent']
    
    # 算術相關關鍵詞
    arithmetic_keywords = ['addition', 'subtraction', 'multiplication', 'division',
                          'arithmetic', 'number', 'digit', 'add', 'subtract']
    
    # 檢查檔名
    all_text = filename_lower + " " + content_lower
    
    if any(kw in all_text for kw in calculus_keywords):
        return "calculus"
    elif any(kw in all_text for kw in geometry_keywords):
        return "geometry"
    elif any(kw in all_text for kw in algebra_keywords):
        return "algebra"
    elif any(kw in all_text for kw in arithmetic_keywords):
        return "arithmetic"
    else:
        return "geometry"  # 預設

def add_description_to_readme(category: str, filename: str, description: str):
    """將檔案說明添加到分類的 README.md"""
    kb_path = Path("knowledge_base")
    category_dir = kb_path / category
    readme_path = category_dir / "README.md"
    
    # 確保 README 存在
    if not readme_path.exists():
        readme_content = f"""# {category.capitalize()} Examples

這個資料夾包含 {category} 相關的 Manim 範例代碼。

## 檔案列表

"""
    else:
        readme_content = readme_path.read_text(encoding='utf-8')
    
    # 檢查是否已有該檔案的說明
    file_section = f"## {filename.replace('.py', '')}"
    if file_section in readme_content:
        # 更新現有說明
        import re
        pattern = f"{re.escape(file_section)}.*?(?=## |$)"
        new_section = f"{file_section}\n**說明**: {description}\n\n"
        readme_content = re.sub(pattern, new_section, readme_content, flags=re.DOTALL)
    else:
        # 添加到檔案列表
        if "## 檔案列表" in readme_content:
            # 在檔案列表後添加
            insert_pos = readme_content.find("## 檔案列表") + len("## 檔案列表")
            if "\n\n" in readme_content[insert_pos:]:
                insert_pos = readme_content.find("\n\n", insert_pos) + 2
            new_section = f"\n{file_section}\n**說明**: {description}\n\n"
            readme_content = readme_content[:insert_pos] + new_section + readme_content[insert_pos:]
        else:
            # 添加到末尾
            readme_content += f"\n{file_section}\n**說明**: {description}\n\n"
    
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"✅ 已更新說明到: {readme_path}")

def download_from_github_url(github_url: str, target_category: str = None, 
                            custom_filename: str = None, add_description: bool = True) -> bool:
    """
    從 GitHub URL 下載檔案
    
    Args:
        github_url: GitHub 檔案或目錄 URL
        target_category: 目標分類 (geometry/algebra/calculus/arithmetic/statistics)
        custom_filename: 自訂檔名（可選）
    """
    # 轉換為 raw URL
    raw_url = convert_github_url_to_raw(github_url)
    
    if not raw_url:
        print(f"❌ 無法解析 GitHub URL: {github_url}")
        print("   請確認 URL 格式正確，例如:")
        print("   https://github.com/user/repo/blob/branch/path/to/file.py")
        return False
    
    # 取得檔名
    if custom_filename:
        filename = custom_filename
        if not filename.endswith('.py'):
            filename += '.py'
    else:
        filename = Path(raw_url).name
        if not filename.endswith('.py'):
            print("⚠️  警告: 檔案不是 .py 格式")
    
    # 決定分類
    if not target_category:
        # 先下載內容來判斷分類
        try:
            response = requests.get(raw_url, timeout=10)
            if response.status_code == 200:
                content = response.text[:1000]  # 只讀前1000字元
                target_category = suggest_category(filename, content)
                print(f"💡 自動建議分類: {target_category}")
        except:
            target_category = "geometry"  # 預設
    
    # 建立保存路徑
    kb_path = Path("knowledge_base") / target_category
    kb_path.mkdir(parents=True, exist_ok=True)
    save_path = kb_path / filename
    
    # 檢查檔案是否已存在
    if save_path.exists():
        response = input(f"⚠️  檔案已存在: {save_path}\n   是否覆蓋？(y/n): ").strip().lower()
        if response != 'y':
            print("跳過下載")
            return False
    
    # 下載檔案
    success = download_file_from_raw_url(raw_url, save_path)
    
    # 如果下載成功且需要添加說明
    if success and add_description:
        print("\n" + "-"*70)
        add_desc = input("是否要為此檔案添加簡短說明？(y/n，預設 n): ").strip().lower()
        if add_desc == 'y':
            description = input("請輸入檔案說明（簡短描述此檔案的功能）: ").strip()
            if description:
                add_description_to_readme(target_category, filename, description)
            else:
                print("未輸入說明，已跳過")
    
    return success

def interactive_download():
    """互動式下載模式"""
    print("="*70)
    print("📥 GitHub 檔案下載工具")
    print("="*70)
    print("\n支援的 URL 格式:")
    print("  - https://github.com/user/repo/blob/branch/path/file.py")
    print("  - https://raw.githubusercontent.com/user/repo/branch/path/file.py")
    print("\n輸入 'q' 或 'quit' 結束\n")
    
    while True:
        github_url = input("請輸入 GitHub URL: ").strip()
        
        if github_url.lower() in ['q', 'quit', 'exit']:
            print("再見！")
            break
        
        if not github_url:
            continue
        
        # 詢問分類
        print("\n選擇分類:")
        print("  1. geometry (幾何)")
        print("  2. algebra (代數)")
        print("  3. calculus (微積分)")
        print("  4. arithmetic (算術)")
        print("  5. statistics (統計)")
        print("  6. 自動判斷")
        
        choice = input("請選擇 (1-6，預設 6): ").strip() or "6"
        
        category_map = {
            "1": "geometry",
            "2": "algebra",
            "3": "calculus",
            "4": "arithmetic",
            "5": "statistics",
            "6": None  # 自動判斷
        }
        
        target_category = category_map.get(choice)
        
        # 詢問自訂檔名
        custom_name = input("自訂檔名（直接 Enter 使用原檔名）: ").strip()
        custom_name = custom_name if custom_name else None
        
        # 下載（互動模式下自動詢問說明）
        success = download_from_github_url(github_url, target_category, custom_name, add_description=True)
        
        if success:
            print("\n✅ 下載完成！")
            print("   建議執行: python scripts/verify_examples.py 來驗證檔案")
        
        print("\n" + "-"*70 + "\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 命令列模式
        github_url = sys.argv[1]
        category = sys.argv[2] if len(sys.argv) > 2 else None
        filename = sys.argv[3] if len(sys.argv) > 3 else None
        
        download_from_github_url(github_url, category, filename)
    else:
        # 互動模式
        interactive_download()
