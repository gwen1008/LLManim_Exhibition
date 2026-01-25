"""
快速開始腳本 - 一鍵設置知識庫
"""
import sys
from pathlib import Path

# 添加專案根目錄到路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    print("="*70)
    print("🚀 知識庫快速設置")
    print("="*70)
    
    # Step 1: 建立資料夾結構
    print("\n📁 Step 1: 建立資料夾結構...")
    from scripts.setup_knowledge_base import setup_knowledge_base
    setup_knowledge_base()
    
    # Step 2: 檢查 Manim
    print("\n🔍 Step 2: 檢查 Manim 環境...")
    import subprocess
    try:
        result = subprocess.run(["manim", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Manim 已安裝")
            print(f"   版本: {result.stdout.strip()}")
        else:
            print("⚠️  Manim 可能未正確安裝")
    except FileNotFoundError:
        print("❌ 找不到 manim 命令")
        print("   請先安裝 Manim: pip install manim")
    
    # Step 3: 顯示統計（如果有檔案）
    print("\n📊 Step 3: 檢查現有檔案...")
    kb_path = Path("knowledge_base")
    if kb_path.exists():
        py_files = list(kb_path.rglob("*.py"))
        if py_files:
            print(f"   找到 {len(py_files)} 個 Python 檔案")
            print("   執行 'python scripts/stats_knowledge_base.py' 查看詳細統計")
        else:
            print("   ⚠️  尚未有範例檔案")
            print("   請參考 DATA_COLLECTION_GUIDE.md 開始收集資料")
    
    # Step 4: 顯示下一步建議
    print("\n" + "="*70)
    print("✅ 設置完成！")
    print("="*70)
    print("\n📋 下一步建議：")
    print("   1. 閱讀 DATA_COLLECTION_GUIDE.md 了解數據來源")
    print("   2. 開始收集 Manim 範例代碼")
    print("   3. 將檔案放入對應的分類資料夾")
    print("   4. 使用 'python scripts/verify_examples.py' 驗證檔案")
    print("   5. 使用 'python scripts/stats_knowledge_base.py' 查看進度")
    print("\n💡 實用命令：")
    print("   - 驗證檔案: python scripts/verify_examples.py")
    print("   - 查看統計: python scripts/stats_knowledge_base.py")
    print("   - 生成描述: python scripts/generate_description.py <category>")
    print("="*70)

if __name__ == "__main__":
    main()
