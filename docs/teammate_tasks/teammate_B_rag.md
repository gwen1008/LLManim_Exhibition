# 組員 B 任務說明 — RAG 系統優化

> 這份文件是你的完整工作說明，不需要看其他文件也能執行。
> 有問題直接問 @liaozhenting。

---

## 你在做什麼

這個專案會把數學題目自動轉成教育動畫影片。整條流程：

```
題目 → [Planner] → JSON blueprint → [Coder] → Manim code → 影片
```

RAG（Retrieval-Augmented Generation）的工作是：在 Coder 生成程式碼前，從向量資料庫撈出「最相關的 Manim 範例程式碼」，讓 Coder 有好的參考資料，減少 API 用法錯誤。

**目前問題**：

| 問題 | 現狀 | 後果 |
|---|---|---|
| Query 太粗 | 直接把題目文字丟進 RAG，例如 "Pythagorean theorem" | 撈出的範例命中率低 |
| limit 硬編碼 = 2 | 不管 score 多低，就是只撈 2 筆 | 品質差的範例也進去了 |
| Planner 拿不到 RAG | RAG context 只傳給 Coder | Planner 設計 layout 時沒有參考範例 |

**你的任務**：讓 RAG 撈得更準、讓撈到的東西真的有用、讓 Planner 也能受益。

**你不需要懂 Manim 動畫渲染，不需要看影片輸出。** 你的工作在 Python + 向量資料庫層面。

---

## 環境 Setup（30-45 分鐘）

### 1. Clone 專案

```bash
git clone <repo_url>
cd LLManim_Agent
```

### 2. 安裝依賴

```bash
pip install -r requirements.txt
```

### 3. 設定 .env

跟 @liaozhenting 要 `.env` 檔，放到專案根目錄。你至少需要：

```
OPENAI_API_KEY=...        # Weaviate text2vec-openai 模組用（向量化 query）
```

> 注意：Weaviate host/port 在 `rag_retriever.py` 寫死為 `localhost:8080`，不用改 env。
> 你不需要 AZURE_SPEECH_KEY、PLANNER_MODEL、CODER_MODEL、OPENROUTER_API_KEY。

### 4. 起 Weaviate（Docker）

```bash
docker compose up -d weaviate
```

等到出現 `✅ RAG System: Connected to Weaviate.` 再繼續。

### 5. 確認知識庫有資料

```bash
python rag/check_weaviate.py
```

如果顯示 `ManimGoldenPair` collection 有資料（> 0 objects），代表 OK。

如果是空的，執行 ingest：

```bash
python rag/ingest_code.py       # 匯入 knowledge_base/examples/
python rag/ingest_rules.py      # 匯入 knowledge_base/manim_ce_rules/
```

### 6. 驗證 RAG 可以跑

```bash
python rag/test_retrieval.py
```

看到 4 個測試各有結果（不一定要有 score 很高，但不能全部是空的）就 OK。

---

## 你要改的檔案（只有這幾個）

| 檔案 | 你可以改什麼 |
|---|---|
| `agents/core/rag_retriever.py` | `retrieve_examples()` 的 limit / threshold 邏輯、`retrieve_rules()` |
| `main.py` | `_rag_task()` 函數（第 200-215 行附近）的 query 設計 |
| `knowledge_base/examples/` | 新增 `.py` 範例檔案（知識庫擴充） |

**嚴禁改動的檔案**：
- `agents/orchestrator/refining_loop.py`
- `agents/core/llm_client.py`
- `agents/coder/`（整個目錄）
- `agents/planner/`（整個目錄）
- `run_evaluation.py` 的 judge 邏輯

---

## 三個子任務

### 子任務 B1：量測 Baseline（先做這個）

**目的**：知道現在 RAG 有多爛，才知道改完有多好。

**步驟**：

```bash
python rag/relevance_audit_20.py
```

這個腳本會對 20 個題目各跑一次 RAG，印出每題撈到什麼。

你需要手動統計：
- 有幾題的 `best_score < 0.65`（走空 RAG，完全沒有範例進去）
- 有幾題的 `best_score >= 0.65` 但描述跟題目毫無關係（false positive）

把結果填進這個表格（PR 描述用）：

| 指標 | Baseline |
|---|---|
| 空 RAG 題數（best_score < 0.65 / 20 題） | ? |
| False positive 估計（目測不相關） | ? |
| `best_score` 中位數 | ? |

---

### 子任務 B2：Query 分解（核心改動）

**問題**：現在 query 直接用題目文字，例如：
```
"Pythagorean theorem"
```

但 knowledge_base 裡的範例是按「Manim 用什麼物件畫什麼」分類的，直接用題目命中率低。

**改法**：在 `main.py` 的 `_rag_task()` 裡，改成先做 query expansion：

```python
def _rag_task():
    # 原本：直接用 user_topic
    # _results = _rag.retrieve_examples(user_topic, limit=2)
    
    # 改成：兩階段 query
    # 第一階段：用題目撈
    _results = _rag.retrieve_examples(user_topic, limit=3)
    
    # 第二階段：用更具體的關鍵字再撈
    # 把題目拆成視覺關鍵字，例如：
    # "Pythagorean theorem" → "right triangle, square area, Polygon"
    # "linear equation graph" → "Axes, plot, MathTex"
    expanded_queries = _expand_rag_query(user_topic)
    for eq in expanded_queries:
        _results += _rag.retrieve_examples(eq, limit=2)
    
    # 去重（按 description 去重）
    seen = set()
    unique_results = []
    for r in _results:
        key = r["description"][:60]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    _results = unique_results
    ...
```

你需要實作 `_expand_rag_query(user_topic: str) -> list[str]`：

**選項 1（簡單版，推薦先做）**：用關鍵字規則 mapping

```python
TOPIC_TO_VISUAL_KEYWORDS = {
    "triangle": ["Polygon triangle", "right triangle sides"],
    "circle": ["Circle radius arc", "Dot center"],
    "graph": ["Axes plot MathTex", "number line"],
    "fraction": ["fraction bar MathTex", "rectangle split"],
    "equation": ["MathTex balance", "algebra steps"],
    "probability": ["bar chart histogram", "fraction probability"],
    # ...繼續擴充
}

def _expand_rag_query(topic: str) -> list[str]:
    topic_lower = topic.lower()
    expansions = []
    for keyword, queries in TOPIC_TO_VISUAL_KEYWORDS.items():
        if keyword in topic_lower:
            expansions.extend(queries)
    return expansions[:3]  # 最多 3 個
```

**選項 2（進階版，如果選項 1 效果不好）**：用 LLM 生成 expanded query

```python
def _expand_rag_query(topic: str) -> list[str]:
    prompt = f"""Given the math topic: "{topic}"
List 3 short visual search queries for finding Manim animation code examples.
Focus on: geometry objects used, visual strategy, Manim class names.
Output: JSON array of 3 strings. Example: ["circle radius arc", "Polygon vertices", "Axes plot line"]"""
    # 用 llm.ask() 呼叫便宜的模型（groq llama）
    ...
```

---

### 子任務 B3：動態 limit + Threshold 調整

**改 `agents/core/rag_retriever.py`**：

目前：
```python
def retrieve_examples(self, query: str, limit: int = 2) -> List[Dict]:
    response = collection.query.hybrid(query=query, limit=limit, ...)
```

改成：
```python
def retrieve_examples(self, query: str, limit: int = 5) -> List[Dict]:
    """撈 5 筆，依 score 過濾後最多回傳 3 筆品質好的"""
    response = collection.query.hybrid(query=query, limit=limit, ...)
    
    # 過濾低品質
    SCORE_THRESHOLD = 0.4
    RELEVANCE_THRESHOLD = 0.65
    MAX_RETURN = 3
    
    results = [r for r in ... if r["score"] >= SCORE_THRESHOLD]
    best_score = max((r["score"] for r in results), default=0.0)
    
    if best_score < RELEVANCE_THRESHOLD:
        return []  # 現有邏輯，保留
    
    # 按 score 排序，只回傳最好的 3 筆
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:MAX_RETURN]
```

---

## 評分方式

你沒有自動評分工具（不像組員 A 有 `run_planner_eval.py`），你需要手動量測：

### 量化指標（從 log 抓）

跑完 `rag/relevance_audit_20.py` 後，看 log：
```
🔍 RAG Examples: skipped (best=0.43 < 0.65) for 'Pythagorean theorem'
🔍 RAG Examples: 3 relevant (best=0.78) for 'area of triangle'
```

統計：
- 改前空 RAG 題數 vs 改後空 RAG 題數
- 改前 best_score 中位數 vs 改後中位數

### 質化評估（人工看）

把改後的 `relevance_audit_20.py` 結果截圖，每題對照：
- RAG 撈到的範例描述和題目有多相關（1-5 分自評）
- 有沒有明顯不相關的範例混進去

**驗收標準**：

| 指標 | 必須達到 |
|---|---|
| 空 RAG 題數 | 比 baseline 少 ≥ 30%（例如 baseline 10 題空 → 改後 ≤ 7 題） |
| best_score 中位數 | ≥ 0.65 |
| 無明顯 false positive | 目測相關性 ≥ 70%（每 10 題至少 7 題你覺得撈對了） |

---

## 執行步驟（Day by Day）

### Day 1 — Setup + 讀 code

1. 照上面 Setup 跑通 `python rag/test_retrieval.py`
2. 讀 `agents/core/rag_retriever.py`（162 行，全部讀）
3. 讀 `main.py` 第 200-215 行（`_rag_task()` 函數）
4. 跑 `python rag/relevance_audit_20.py`，看 20 題的結果，手動記下空 RAG 的題目

### Day 2 — Baseline 量化

把 `relevance_audit_20.py` 的輸出存起來：
```bash
python rag/relevance_audit_20.py 2>&1 | tee baseline_rag_audit.txt
```

統計空 RAG 題數和 best_score 中位數，填進上面的表格。

### Day 3-4 — 實作 B2 + B3

1. 先改 `retrieve_examples()` 的 dynamic limit（B3，改動小、風險低）
2. 再實作 `_expand_rag_query()`（B2，從 keyword mapping 版開始）
3. 改完後跑一次 `relevance_audit_20.py`：

```bash
python rag/relevance_audit_20.py 2>&1 | tee after_b2_b3_rag_audit.txt
diff baseline_rag_audit.txt after_b2_b3_rag_audit.txt
```

看看空 RAG 題數有沒有減少。

### Day 5 — 知識庫補充（可選，如果 B2+B3 還不夠）

如果某些題目領域完全沒有範例（best_score < 0.5），可以往 `knowledge_base/examples/` 新增範例：

範例格式（參考 `knowledge_base/examples/geometry/` 下的現有檔案）：
```python
"""
description: Pythagorean theorem proof with colored squares on each side
manim_modules: Polygon, Square, MathTex, Transform
"""
class PythagoreanProof(Scene):
    def construct(self):
        # ... Manim code
```

新增後需要重新 ingest：
```bash
python rag/ingest_code.py
```

### Day 6 — 開 PR

開 Pull Request，標題：
```
feat: RAG query expansion + dynamic limit (B1+B2+B3)
```

PR 描述必須附：
1. Baseline vs After 對比表（空 RAG 題數、best_score 中位數）
2. `_expand_rag_query()` 的設計選擇（為什麼選 keyword mapping 還是 LLM？）
3. 如果有新增知識庫範例，列出新增了哪些

---

## 常見問題

**Q：Weaviate 起不來怎麼辦？**
先跑 `docker compose ps` 看容器狀態，再跑 `docker compose logs weaviate` 看錯誤。常見問題是 port 8080 被占用。

**Q：ingest 完 check_weaviate.py 還是 0 objects？**
跑 `python rag/verify_index.py` 確認有沒有索引錯誤。

**Q：relevance_audit_20.py 所有題目都是空 RAG？**
代表 Weaviate 的 collection 可能是空的，重新 ingest 一次。

**Q：我可以改 retrieve_rules() 嗎？**
可以，規則跟範例的優化邏輯類似，動態 limit 和 threshold 也可以加進去。

**Q：我需要懂 Manim 嗎？**
不需要詳細懂，但你要知道 `Polygon`、`MathTex`、`Axes` 是什麼（Manim 的物件名稱），這樣你寫 keyword mapping 才有感覺。這些你可以直接查 `knowledge_base/manim_ce_rules/` 裡的 md 檔。

---

## 目錄結構（你需要關心的部分）

```
LLManim_Agent/
├── agents/
│   └── core/
│       └── rag_retriever.py        ← 主要改動
├── rag/
│   ├── test_retrieval.py           ← 功能驗證
│   ├── relevance_audit_20.py       ← Baseline 量測（你的主要武器）
│   ├── ingest_code.py              ← 重新 ingest 知識庫
│   ├── ingest_rules.py             ← ingest Manim API 規則
│   └── check_weaviate.py           ← 確認 Weaviate 狀態
├── knowledge_base/
│   ├── examples/                   ← 可新增範例的目錄
│   │   ├── arithmetic/
│   │   ├── geometry/
│   │   ├── algebra/
│   │   └── ...
│   └── manim_ce_rules/             ← Manim API 規則（唯讀）
├── main.py                         ← _rag_task() 函數（query 設計）
└── .env                            ← API keys（跟 @liaozhenting 要）
```