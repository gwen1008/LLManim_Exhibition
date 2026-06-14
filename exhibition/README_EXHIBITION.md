# 數學動畫展覽網頁 — 本機開啟教學

這是「AI 數學動畫生成系統」的展覽網頁，包含：

- **Gallery**：系統能力展示（6 部）＋ Opus 裸跑 vs 本系統對比（5 部）
- **Tech**：系統技術數據（150 部 benchmark、成本、品質、Pipeline 流程）

> 註：原本的「Live 即時生成」功能需要 Claude / OpenAI / Azure 等私鑰，**此公開版本已移除**。網頁為純瀏覽，影片皆已預先生成內附。

---

## 怎麼在自己電腦開（3 步）

需求：Python 3.9+

```bash
# 1. clone 專案
git clone <這個 repo 的網址>
cd LLManim_Agent

# 2. 安裝兩個套件（只需要這兩個）
pip install -r exhibition/requirements-serve.txt

# 3. 啟動網頁伺服器
python -m uvicorn exhibition.api:app --port 8090
```

開啟瀏覽器 → **http://localhost:8090**

關閉：終端按 `Ctrl + C`

---

## 常見問題

- **Port 8090 被占用？** 換一個：`--port 8000`，網址也跟著改成 `http://localhost:8000`
- **影片打不開 / 空白？** 確認 clone 時影片有完整下載（`exhibition/static/` 下應有 `videos/`、`batch_20/`、`retry_cap20/`、`retry_hsat20/`）
- **要讓同網段其他裝置看？** 加 `--host 0.0.0.0`，別人用 `http://你的IP:8090` 連
