"""
RAG Relevance Judging: 20 題人工標注測試
輸出每一題的 Top 3 檢索結果的完整描述，供人工判斷相關性。
"""
import sys, json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agents.core.rag_retriever import RAGRetriever

def run_relevance_audit():
    # 20 題精選 (刻意涵蓋強項與弱項)
    queries = [
        # 算術 (4)
        ("K3", "Vertical addition with carrying 28 + 35"),
        ("K4", "Prime factorization tree for number 60"),
        ("K5", "Order of operations PEMDAS with parentheses example"),
        ("K6", "Negative numbers addition on a number line"),
        # 分數 (4)
        ("K4", "Fraction multiplication area model 1/2 times 1/3"),
        ("K5", "Converting fractions to decimals and percentages"),
        ("K6", "Ratio and proportion visualization with tape diagram"),
        ("K7", "Percentage discount calculation with bar model"),
        # 幾何 (5)
        ("K5", "Area of a triangle half base times height"),
        ("K7", "Reflection and symmetry of a shape across a line"),
        ("K8", "Pythagorean theorem proof with squares on sides"),
        ("K8", "Interior angles of a pentagon split into triangles"),
        ("K9", "Rotation of a triangle 90 degrees on coordinate plane"),
        # 代數 (4)
        ("K7", "Solving x + 5 = 12 using a balance scale"),
        ("K8", "Plotting y = 2x + 1 linear function on axes"),
        ("K9", "System of two linear equations finding intersection"),
        # 統計/生活 (3)
        ("K5", "Mean median and mode of a data set"),
        ("K4", "Clock showing 3:00 with 90 degree angle"),
        ("K3", "Counting coins and making change for a purchase"),
        ("K9", "Probability of rolling a 6 on a fair die"),
    ]

    retriever = RAGRetriever()

    all_results = []
    for grade, query in queries:
        examples = retriever.retrieve_examples(query, limit=3)
        rules = retriever.retrieve_rules(query, limit=1)

        entry = {
            "grade": grade,
            "query": query,
            "examples": [],
            "rules": []
        }
        for ex in examples:
            entry["examples"].append({
                "source": ex.get("source", "unknown"),
                "description": ex.get("description", "")[:120],
                "code_preview": ex.get("code", "")[:200] if ex.get("code") else "N/A"
            })
        for r in rules:
            entry["rules"].append({
                "description": r.get("description", "")[:120]
            })
        all_results.append(entry)

    retriever.close()

    # 輸出每一題的詳細結果
    for i, entry in enumerate(all_results, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/20] 年級: {entry['grade']} | 題目: {entry['query']}")
        print(f"{'='*60}")
        for j, ex in enumerate(entry["examples"], 1):
            print(f"  範例 {j} [{ex['source']}]: {ex['description']}")
            if ex["code_preview"] != "N/A":
                # 只印第一行 code
                first_lines = ex["code_preview"].replace("\r","").split("\n")[:3]
                for l in first_lines:
                    print(f"    > {l}")
        if entry["rules"]:
            print(f"  規則: {entry['rules'][0]['description']}")
        else:
            print(f"  規則: (無)")

if __name__ == "__main__":
    run_relevance_audit()
