import sys
import os
from pathlib import Path

# 加入專案根目錄到路徑
sys.path.append(str(Path(__file__).parent.parent))

from agents.core.rag_retriever import RAGRetriever

def test_rag():
    retriever = RAGRetriever()
    
    print("\n" + "="*50)
    print("🧪 測試 1: 基礎範例檢索 (應命中 Examples)")
    print("="*50)
    # 測試一個基礎範例中一定有的主題
    results_basic = retriever.retrieve_examples("Create a simple square and circle", limit=2)
    for i, res in enumerate(results_basic):
        print(f"[{i+1}] {res['description']} (來源: {res.get('source')})")

    print("\n" + "="*50)
    print("🧪 測試 2: 高階數學檢索 (應命中 3b1b)")
    print("="*50)
    # 測試傅立葉變換，這在 3b1b 中非常多
    results_math = retriever.retrieve_examples("Fourier series transformation animation", limit=2)
    for i, res in enumerate(results_math):
        print(f"[{i+1}] {res['description']} (來源: {res.get('source')})")

    print("\n" + "="*50)
    print("🧪 測試 3: API 規則檢索 (應命中 Rules)")
    print("="*50)
    # 測試關於 .animate 的規則
    results_rules = retriever.retrieve_rules("How to use .animate syntax correctly", limit=2)
    for i, res in enumerate(results_rules):
        print(f"[{i+1}] {res['description']}")

    print("\n" + "="*50)
    print("🧪 測試 4: 整合格式化 (模擬 AI 看到的 Prompt)")
    print("="*50)
    combined = results_basic + results_rules
    formatted = retriever.format_for_prompt(combined)
    print(formatted[:1000] + "..." if len(formatted) > 1000 else formatted)

    retriever.close()

if __name__ == "__main__":
    test_rag()
