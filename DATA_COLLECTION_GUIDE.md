# 📚 數據收集指南 (Data Collection Guide)

## 🎯 任務目標
建立高品質的 Manim 代碼知識庫，用於後續的 RAG (檢索增強生成) 系統，提升 AI Coder 的準確性。

---

## 📍 數據來源 (Where to Find Data)

### 1. **Manim Community Examples** ⭐ 推薦
- **官方文檔**: https://docs.manim.community/
- **Example Gallery**: https://docs.manim.community/en/stable/examples.html
- **優點**: 官方維護，代碼品質高，註解完整
- **收集方式**: 直接從 GitHub 下載或複製代碼

### 2. **GitHub 倉庫**
推薦搜索關鍵詞：
- `manim-community-examples`
- `manim-tutorial`
- `manim-educational`
- `manim-math-animations`

**具體倉庫推薦**:
- `3b1b/manim` (原始倉庫，有大量範例)
- `ManimCommunity/manim` (社群版，範例更現代)
- `carykh/jumpcutter` (相關教學動畫)
- 搜索 `topic:manim` 和 `language:python`

### 3. **YouTube 教程**
- **3Blue1Brown**: 原始 Manim 創作者，代碼在 GitHub
- **Manim Community 官方頻道**: 教學影片通常附帶代碼連結
- **搜索關鍵詞**: "manim tutorial", "manim python tutorial"

### 4. **Reddit / Discord**
- `r/manim`: Reddit 社群，常有分享代碼
- Manim Community Discord: 活躍社群，可詢問範例

### 5. **論文與研究**
- 搜索 "manim educational animation" 相關論文
- 通常論文會附帶代碼倉庫連結

---

## 📂 專案結構設置

### Step 1: 建立知識庫資料夾結構

```
LLManim_Agent/
├── knowledge_base/
│   ├── geometry/          # 幾何相關
│   │   ├── README.md      # 分類說明
│   │   └── *.py           # 範例檔案
│   ├── algebra/           # 代數相關
│   │   ├── README.md
│   │   └── *.py
│   ├── calculus/          # 微積分相關
│   │   ├── README.md
│   │   └── *.py
│   ├── arithmetic/        # 算術相關 (可選)
│   ├── statistics/        # 統計相關 (可選)
│   └── README.md          # 知識庫總說明
```

---

## 🔄 逐步操作流程

### Phase 1: 環境準備 ✅

1. **確認 Manim 環境**
   ```bash
   # 測試 Manim 是否正常運作
   manim --version
   ```

2. **建立知識庫資料夾**
   ```bash
   mkdir -p knowledge_base/{geometry,algebra,calculus}
   ```

### Phase 2: 數據挖掘 🔍

#### 方法 A: 從 GitHub 下載 (推薦)

1. **搜索並克隆範例倉庫**
   ```bash
   # 範例：克隆 Manim Community 範例
   git clone https://github.com/ManimCommunity/manim.git
   cd manim/examples
   ```

2. **篩選高品質檔案**
   - 尋找有完整註解的檔案
   - 確認代碼結構清晰
   - 檢查是否有對應的影片輸出

#### 方法 B: 手動收集

1. **瀏覽官方文檔**
   - 訪問 https://docs.manim.community/en/stable/examples.html
   - 複製代碼到本地檔案

2. **從 YouTube 影片描述**
   - 許多教學影片會在描述中提供代碼連結
   - 下載並驗證

### Phase 3: 分類與整理 📁

#### 分類標準

**幾何 (geometry/)**:
- 形狀繪製 (Circle, Square, Polygon)
- 幾何變換 (Transform, Rotate, Scale)
- 座標系統 (Axes, NumberPlane)
- 範例: `draw_circle.py`, `pythagorean_theorem.py`

**代數 (algebra/)**:
- 方程式顯示 (MathTex, Equation)
- 代數運算動畫 (TransformMatchingTex)
- 函數圖形 (FunctionGraph)
- 範例: `solve_equation.py`, `quadratic_formula.py`

**微積分 (calculus/)**:
- 導數視覺化
- 積分動畫
- 極限概念
- 範例: `derivative_visualization.py`, `riemann_sum.py`

#### 檔案命名規範

建議格式: `主題_功能描述.py`

範例:
- `geometry_pythagorean_theorem.py`
- `algebra_quadratic_equation.py`
- `calculus_derivative_graph.py`

### Phase 4: 驗證與測試 ✅

#### 驗證清單 (每個檔案都要檢查)

- [ ] **語法正確**: 代碼可以正常執行，無語法錯誤
- [ ] **可運行**: 使用 `manim -pql <file.py> <SceneName>` 可以成功渲染
- [ ] **註解完整**: 關鍵步驟有中文或英文註解
- [ ] **結構清晰**: 代碼組織良好，易於理解
- [ ] **功能明確**: 每個檔案展示一個明確的數學概念或技巧

#### 測試腳本

建立 `verify_examples.py` 來批量驗證:

```python
import os
import subprocess
from pathlib import Path

def verify_manim_file(file_path):
    """驗證 Manim 檔案是否可以正常運行"""
    try:
        # 提取 Scene 類別名稱 (簡化版，可能需要調整)
        result = subprocess.run(
            ["manim", "-pql", str(file_path)],
            capture_output=True,
            timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error verifying {file_path}: {e}")
        return False

# 遍歷所有 .py 檔案
knowledge_base = Path("knowledge_base")
for py_file in knowledge_base.rglob("*.py"):
    if verify_manim_file(py_file):
        print(f"✅ {py_file}")
    else:
        print(f"❌ {py_file}")
```

### Phase 5: 添加功能描述 📝

#### 為每個檔案創建描述

建議在每個分類資料夾建立 `README.md`，格式如下:

```markdown
# Geometry Examples

## pythagorean_theorem.py
**功能**: 展示畢氏定理的視覺化證明，使用三個正方形來演示 a² + b² = c²
**關鍵技巧**: 
- 使用 `Square` 和 `VGroup` 組合形狀
- 使用 `Transform` 動畫展示面積關係
- 使用 `MathTex` 顯示公式

## draw_number_line.py
**功能**: 示範如何繪製帶有箭頭的數線，並標記特定數值
**關鍵技巧**:
- 使用 `NumberLine` 物件
- 使用 `Arrow` 添加方向指示
- 使用 `Dot` 和 `Label` 標記點
```

#### 進階: 自動生成描述

可以建立一個腳本，使用 LLM 自動為每個檔案生成描述:

```python
# generate_descriptions.py (範例)
from agents.llm_client import LLMClient

def generate_description(code_content):
    client = LLMClient()
    prompt = f"""
    請為以下 Manim 代碼生成簡短的功能描述（50字以內）：
    
    {code_content}
    
    格式：
    **功能**: [描述]
    **關鍵技巧**: [列出2-3個主要 Manim 技巧]
    """
    return client.generate(prompt)
```

---

## 📊 進度追蹤

### 目標: 至少 20 個高品質檔案

建議分配:
- **幾何 (geometry/)**: 7-8 個檔案
- **代數 (algebra/)**: 7-8 個檔案  
- **微積分 (calculus/)**: 5-6 個檔案

### 品質標準

✅ **高品質檔案應具備**:
1. 完整的類別定義 (`class MyScene(Scene)`)
2. 清晰的 `construct()` 方法
3. 適當的註解（至少關鍵步驟）
4. 使用現代 Manim Community 語法（避免舊版語法）
5. 單一明確的教學目標

❌ **應避免**:
- 過於複雜的檔案（包含太多概念）
- 使用已棄用的 API (`ShowCreation` → 應使用 `Create`)
- 缺少註解的代碼
- 無法運行的代碼

---

## 🛠️ 實用工具與腳本

### 1. 批量下載腳本

```python
# download_examples.py
import requests
import os
from pathlib import Path

def download_from_github_raw(url, save_path):
    """從 GitHub raw URL 下載檔案"""
    response = requests.get(url)
    if response.status_code == 200:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"✅ Downloaded: {save_path}")
    else:
        print(f"❌ Failed: {url}")
```

### 2. 代碼清理腳本

```python
# clean_code.py
def remove_comments_and_clean(code):
    """移除多餘註解，保留關鍵註解"""
    # 實作清理邏輯
    pass
```

### 3. 統計腳本

```python
# stats.py
from pathlib import Path

def count_examples():
    kb = Path("knowledge_base")
    stats = {}
    for category in ["geometry", "algebra", "calculus"]:
        count = len(list((kb / category).glob("*.py")))
        stats[category] = count
    print(f"總計: {sum(stats.values())} 個檔案")
    for cat, count in stats.items():
        print(f"  {cat}: {count} 個")
```

---

## ✅ Definition of Done (DoD) 檢查清單

完成標準：

- [ ] `knowledge_base/` 資料夾已建立
- [ ] 至少 3 個分類資料夾（geometry, algebra, calculus）
- [ ] 每個分類至少有 5 個 `.py` 檔案
- [ ] **總計至少 20 個檔案**
- [ ] 每個檔案都經過驗證，可以正常運行
- [ ] 每個分類都有 `README.md` 說明檔案
- [ ] 至少 50% 的檔案有功能描述
- [ ] 所有檔案使用現代 Manim Community 語法
- [ ] 代碼品質一致，註解清晰

---

## 🚀 快速開始命令

### 方法 A: 使用自動化腳本（推薦）✨

```bash
# 一鍵設置知識庫結構
python scripts/quick_start.py
```

這個腳本會自動：
- ✅ 建立所有必要的資料夾結構
- ✅ 檢查 Manim 環境
- ✅ 顯示現有檔案統計
- ✅ 提供下一步建議

### 方法 B: 手動設置

```bash
# 1. 建立資料夾結構
python scripts/setup_knowledge_base.py

# 2. 測試 Manim 環境
manim --version

# 3. 驗證現有檔案（如果有）
python scripts/verify_examples.py

# 4. 查看統計
python scripts/stats_knowledge_base.py
```

### 可用腳本總覽

| 腳本 | 功能 | 使用方式 |
|------|------|----------|
| `scripts/quick_start.py` | 一鍵設置 | `python scripts/quick_start.py` |
| `scripts/setup_knowledge_base.py` | 建立資料夾結構 | `python scripts/setup_knowledge_base.py` |
| `scripts/verify_examples.py` | 驗證所有檔案 | `python scripts/verify_examples.py` |
| `scripts/stats_knowledge_base.py` | 查看統計 | `python scripts/stats_knowledge_base.py` |
| `scripts/generate_description.py` | 生成檔案描述 | `python scripts/generate_description.py <category>` |

---

## 📞 需要幫助？

- 檢查 Manim 文檔: https://docs.manim.community/
- 查看專案 README: `README.md`
- 聯繫專案負責人: Liao Zhenting

---

**最後更新**: 2026-01-25
**負責人**: Team Member C
