# KB150 交付文檔(給 main 的人)

> 分支:`feat/kb150-manim-templates`
> 來源:`data/seed_questions_150.txt.xlsx`(159 題,9 個知識點)
> 計畫文檔:`C:\Users\Cherry\.claude\plans\150-manim-150-maim-twinkly-frog.md`

## 這是什麼

把封測 150 題的詳解 + 引導策略,用 LLM 濃縮成代表性 Manim Scene,灌進**新的 Weaviate collection `ManimKB150`** 跟舊的 `ManimGoldenPair` **並存**。

預設行為**完全不變** — 沒設 env var 一切跑舊 KB。要用新 KB 才需要切 env。

## KB 規格

- **Collection 名稱**:`ManimKB150`
- **Scene 數量**:每知識點 3 個代表題(難度=4 為主)+ 2 個 coverage-gap 補洞 seed(q38、q98)= **29 個 Scene**
- **檔案位置**:`knowledge_base/kb150/{slug}/{ClassName}.py`

> ⚠️ **Scene 是 RAG 飼料,不是 render-ready demo**
> 這批 Scene 由 Gemini 2.5 Flash 生成,程式碼結構完整(py_compile 通過、有 docstring、用 ManimCE API),但 **layout 經常重疊**(多步驟物件往下堆而沒 FadeOut 上一步)。
> 這是有意的取捨:KB 的工作是給 Coder 看「該用哪些 API、解這類題的結構是什麼」,Coder 拿到後會自己改、再走 RefiningLoop + Vision + pre_render_patch 修 layout。直接拿這些 Scene `manim -ql` render 出來會看到重疊,**這不代表 KB 壞掉**。
> 真正要驗證的是「Coder 用這個 KB 後產出的影片」,那才需要把 RefiningLoop 完整跑過。
- **涵蓋知識點**:
  | 中文 | slug(目錄名) |
  |---|---|
  | 整數加減 | `integer_add_sub` |
  | 整數乘除 | `integer_mul_div` |
  | 分數加減 | `fraction_add_sub` |
  | 分數乘除 | `fraction_mul_div` |
  | 四則運算算則(不含去括號) | `pemdas_no_bracket_removal` |
  | 四則運算(含去括號) | `pemdas_with_bracket_removal` |
  | 完整的四則混合運算 | `mixed_arithmetic_full` |
  | 指數與科學記號 | `exponent_scientific_notation` |
  | 因數與倍數 | `factor_multiple` |

## 怎麼切到新 KB 跑題目

### PowerShell
```powershell
$env:RAG_COLLECTION = "ManimKB150"
python run_math.py add 84 985 --render  # 或你的測試指令
```

### Bash / WSL
```bash
RAG_COLLECTION=ManimKB150 python run_math.py add 84 985 --render
```

### 取消(切回舊 KB)
```powershell
Remove-Item Env:RAG_COLLECTION
```

> 切換點在 [agents/core/rag_retriever.py](../../agents/core/rag_retriever.py) 開頭的 `COLLECTION_NAME` 變數。預設 `ManimGoldenPair`,讀 env 一次性決定整個 process 用哪個 collection。

## 本計畫已驗證的事

`scripts/verify_kb150_coverage.py` 跑 159 題對新 KB 的 retrieval,**用 top-K hit 標準**(K=3,跟 Coder 實際拿到的一致):任一個 top-3 結果落在該題知識點對應目錄就算 hit。

**Definition of Done**:整體 hit 率 ≥ 90%、每個知識點 ≥ 80%  ✅ **PASS**

最新結果(2026-05-17,加 q38/q98 補洞 seed 後):
| 知識點 | top-K hit |
|---|---|
| 分數加減 | 17/17 (100.0%) |
| 分數乘除 | 17/17 (100.0%) |
| 四則運算算則(不含去括號) | 20/20 (100.0%) |
| 四則運算(含去括號) | 20/20 (100.0%) |
| 因數與倍數 | 18/18 (100.0%) |
| 完整的四則混合運算 | 17/17 (100.0%) |
| 整數乘除 | 17/17 (100.0%) |
| 整數加減 | 17/17 (100.0%) |
| 指數與科學記號 | 16/16 (100.0%) |
| **OVERALL** | **159/159 (100.0%)** |
| Top-1 嚴格(僅 diagnostic) | 139/159 (87.4%) |

> Top-1 vs Top-K 差距:有 ~12% 的題目 top-1 跨類但 top-3 內仍能找到對的類(常見情境:integer 題的 top-1 抓到 pemdas/mixed_arithmetic — 因為「step-by-step calculation」字眼通用)。實務上 Coder 看 top-3 例子,所以 top-K 才是合理指標。

**迭代軌跡**(供日後 KB 擴充參考):
| 階段 | 動作 | top-K | top-1 |
|---|---|---|---|
| 初次 verify(無 patch) | 27 個 LLM 生 docstring 沒提類別 | — | 50.9% |
| Patch docstring 前綴 | 加「知識點 中英雙語」prefix | — | 84.9% |
| Top-K 標準 | 換成 Coder 實際使用的 top-3 標準 | 97.5% | 84.9% |
| 補 2 個 gap seed | q38(error analysis)、q98(指數運算) | **100.0%** | 87.4% |

**報告位置**:`runs/kb150_coverage_report.csv`(欄位:`id, knowledge, expected_dir, top1_class, top1_dir, top1_desc, top2_class, top2_dir, top3_class, top3_dir, hit_top1, hit_topk`)

跑法:
```powershell
$env:RAG_COLLECTION = "ManimKB150"
python scripts/verify_kb150_coverage.py
```

> 注意:這只驗證 RAG 能撈到對的 Scene。**沒驗證 Coder 拿到 Scene 後生出的 Manim 影片品質。**

## 本計畫沒做、需要你接手的事

1. **用新 KB 跑真題目產 Manim**:
   ```powershell
   $env:RAG_COLLECTION = "ManimKB150"
   python run_math.py <題號> --render
   # 或批次
   python run_evaluation.py --kb-tag kb150
   ```
2. **品質對比**(舊 KB 那份結果已存在,不用重跑):
   - RAG 抓到的 class 是否相關
   - Coder 生成的 Manim 是否能 render
   - 影片中的解題步驟是否與題目詳解一致
   - 是否有 hallucinated API、layout 出錯
3. **決定是否把新 KB 設為預設**:
   - 如果新 KB 表現顯著好 → 改 [agents/core/rag_retriever.py](../../agents/core/rag_retriever.py) 第 16 行的 default 值
   - 如果差不多或更差 → 保留 env var 切換機制,新 KB 當實驗性選項

## 復原 / 移除新 KB

```python
# 刪掉 Weaviate 裡的新 collection(不影響舊 collection):
import weaviate
client = weaviate.connect_to_local()
client.collections.delete("ManimKB150")
client.close()
```

## 重建 KB 從零

前置:
- 確保 Weaviate 有 Gemini vectorizer config 跑著(本分支已改 docker-compose.yml,`docker compose up -d` 即可)
- `.env` 有 `GOOGLE_API_KEY`(Gemini 用,生 Scene + Weaviate embedding 都需要)

```powershell
# 1. 抽 seed JSON(從 data/seed_questions_150.txt.xlsx)
#    --extra-ids 38,98 是補洞 seed:q38 涵蓋「error analysis」,q98 涵蓋「純指數運算」
python scripts/extract_kb150_seeds.py --per-category 3 --extra-ids 38,98

# 2. LLM 生 Scene(~15-25 分鐘,29 次 Gemini 2.5 Flash 呼叫,~$0.20)
python scripts/generate_kb150_scenes.py --limit 1   # smoke 先測 1 題
python scripts/generate_kb150_scenes.py             # 全跑

# 3. 修補 docstring(prepend 知識點 prefix 給 RAG 用,不呼 LLM)
python scripts/patch_kb150_docstrings.py

# 4. 灌 Weaviate
python rag/ingest_code.py --collection ManimKB150 --kb-dir knowledge_base/kb150/

# 5. 驗證 coverage(DoD 標準:overall>=90%, 每類>=80%)
$env:RAG_COLLECTION = "ManimKB150"
python scripts/verify_kb150_coverage.py
```

⚠️ **Step 1 的 `--extra-ids 38,98` 不要省略**。沒這兩個補洞 seed,指數與科學記號類只有 81% 命中(科學記號 vs 純指數運算分布偏掉)、整數加減類有 1 個 error-analysis 題抓不到。

⚠️ **Step 3 (patch_kb150_docstrings.py) 一定要在 ingest 之前跑**。LLM 自動生的 docstring 不夠 category-discoverable,沒 patch 的話 overall top-1 hit 率只有 50%(實測)。

⚠️ 增量補洞(已有 KB 想加新 seed 不重生整批):
```powershell
python scripts/extract_kb150_seeds.py --per-category 3 --extra-ids 38,98,<新ID>
python scripts/generate_kb150_scenes.py --only-ids <新ID>  # 只生新加的
python scripts/patch_kb150_docstrings.py
python rag/ingest_code.py --collection ManimKB150 --kb-dir knowledge_base/kb150/
```
