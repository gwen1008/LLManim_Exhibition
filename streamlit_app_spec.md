# Streamlit Web 介面規格書

> 目標：在瀏覽器完成「輸入數學主題 → 即時看 log → 看影片」，無需碰觸 VS Code 終端機。

---

## 1. 環境與依賴

- **Python**：與專案相同 (3.10+)
- **新增套件**：
  - `streamlit`（必要）
  - `watchdog`（可選，見 4.2）
- 安裝：`pip install streamlit watchdog`  
  建議同步加入 `requirements.txt` 或 `requirements-streamlit.txt`

---

## 2. 入口與工作目錄

- 啟動：`streamlit run app.py`（預設從執行 `streamlit` 的 `cwd` 找 `.env`、`agents/`、`media/`、`stable_outputs/`）
- **要求**：`app.py` 必須在專案根目錄，且 `streamlit run app.py` 時 `cwd` 為專案根；若在別處執行，需在 `app.py` 開頭 `os.chdir(專案根)` 或等效處理，以正確載入 `.env` 與模組。

---

## 3. UI 基本元素

- **Math Topic 輸入框**：`st.text_input("動畫主題", ...)` 或 `st.text_area`
- **生成按鈕**：`st.button("生成動畫")`
- **即時 Log 區**：`st.code(...)` 或 `st.text(...)` 或 `st.markdown`，需能**即時追加**新輸出（見 4）
- **影片播放器**：生成成功後顯示 `stable_outputs/{safe_name}.mp4`（見 5）

---

## 4. 即時 Log 串流（核心）

### 4.1 與 main 的整合方式（二選一）

| 選項 | 作法 | 對 main.py 的影響 | 備註 |
|------|------|-------------------|------|
| **A) subprocess** | `subprocess.Popen(["python", "main.py"], stdin=PIPE, stdout=PIPE, stderr=STDOUT, text=True, bufsize=1, cwd=專案根)`；另開 thread 讀 `proc.stdout`，把每行/每塊寫入 Streamlit log 區 | 需改 `main`：支援「由 stdin 或 argv 取得 topic」，不再僅用 `input()` | 改動小，但須處理 `input()` 與 stdin |
| **B) 直接呼叫** | 在 `main.py` 抽出 `run_ema(topic, output_callback=print)`，`print` 改為 `output_callback(...)`；`app.py` 做 `run_ema(topic, lambda s: log_placeholder.write(s))` | 需重構 `main` 與 `SessionLogger` | 完全掌控輸出，利於擴充 |

**建議**：若本版以「最小改動、先跑起來」為準，可選 **A**；若預期會加進度條、取消按鈕等，可選 **B**。

### 4.2 若選 A：main 的輸入方式

- 必須能** non-interactive** 取得 topic，例如：
  - 優先：`sys.argv[1]` 若存在則為 topic，否則再 `input()`；或
  - 若 `stdin` 非 TTY 且可讀，則 `sys.stdin.readline().strip()` 為 topic，否則 `input()`。
- `app.py` 使用 `Popen(..., stdin=PIPE)`，啟動後立即：
  - `proc.stdin.write(f"{topic}\n")`
  - `proc.stdin.flush()`
- 確保 `main` 只呼叫一次取得 topic 的邏輯，避免 blocking。

### 4.3 若選 B：output_callback

- 簽名：`output_callback(text: str) -> None`
- `main` 內所有 `print(...)` 改為 `output_callback(str(...))`，或 `print` 再被 `SessionLogger` 包一層時，由 `run_ema` 提供自訂 `TeeOutput` 之一端為 callback。
- `SessionLogger`：可改為「若未提供 log 檔路徑則不寫檔、只走 callback」，或保留寫檔，由 `run_ema` 決定是否啟用。

### 4.4 Streamlit 端顯示

- 使用 `st.empty()` 或 `st.container()` 作為 log 佔位，在讀到 stdout 新內容時：
  - `log_placeholder.markdown(log_content)` 或 `log_placeholder.code(log_content, language="text")`
  - 適度做 `st.rerun()` 或在 thread 內用 `st.session_state` 累積字串再更新，避免高頻 rerun。  
  （Streamlit 無原生 WebSocket，通常以「累積字串 + 定時或事件驅動 rerun」模擬即時感。）

### 4.5 watchdog（可選）

- **用途**：若僅為「偵測 `stable_outputs/` 新 mp4 以觸發播放器更新」，可用 `watchdog` 監聽該目錄，在 `on_created` / `on_modified` 時更新 `st.session_state` 並 `st.rerun()`。
- **替代**：若採「生成流程在 `app.py` 內跑完才回傳」，可直接在 `run_ema` 或 subprocess `wait()` 後檢查 `stable_outputs/{safe_name}.mp4` 是否存在，不需 `watchdog`。
- 本版可先不實作 `watchdog`，在 Spec 保留為進階選項。

---

## 5. 影片路徑與播放器

### 5.1 路徑規則（須與 main.py 一致）

- `main` 內：`safe_name = user_topic.replace(" ", "_").replace(".", "_").replace("/", "_").replace("*", "x")`
- 影片：`stable_outputs/{safe_name}.mp4`
- **要求**：`app.py` 應有共用函式，例如 `topic_to_safe_name(topic: str) -> str`，規則與 `main` 相同，避免兩邊分叉。

### 5.2 播放

- `st.video(path)` 或 `st.video(open(path, "rb"))`；若路徑不存在則不顯示或顯示「尚無影片」。
- 若用 `watchdog`，僅在**與本次 topic 對應之 `{safe_name}.mp4` 出現或更新**時才刷新播放器，避免誤用他次生成之檔。

---

## 6. 流程與錯誤處理

- **主流程**：輸入 topic → 點「生成」→ 即時 log 更新 → 成功後顯示影片。
- **`.py` 直接播放**：本版可**不實作**；若實作，需另加 UI（例如第二輸入或勾選）並只跑 `run_manim_task`，與「數學主題」流程分開。
- **長時間執行**：`auto_fix_loop` 最多 10 次嘗試，單次可能很長。建議：
  - 顯示 `st.spinner("生成中...")` 或明確「執行中」狀態；
  - 可選：**停止**按鈕，對 subprocess `proc.terminate()` 或對 `run_ema` 以 `Event` 中斷。
- **失敗**：log 區應可看到 `main` 的錯誤輸出；影片區顯示「本次未產生影片」或留空。

---

## 7. Definition of Done（DoD）

- [ ] 執行 `streamlit run app.py` 後，**不需再開 VS Code 終端**即可完成一次完整動畫生成。
- [ ] **即時 Log**：生成過程中，於 Web UI 即時看到 `main` / `ema` 之 log（Planner、Coder、Review、Manim 等）。
- [ ] **影片**：成功後，同一頁面自動顯示並可播放 `stable_outputs/{safe_name}.mp4`。
- [ ] Demo 情境：網頁輸入例如 `Pythagorean theorem` → 看到即時 log → 看到影片。

---

## 8. 待團隊決定

- [ ] **4.1**：採用 **A) subprocess** 或 **B) 直接呼叫 `run_ema`**？
- [ ] **4.5**：本版是否實作 `watchdog`？（建議先不做）
- [ ] **6**：是否要「停止」按鈕與 `.py` 直播？

---

## 9. 檔案結構建議

```
LLManim_Agent/
├── app.py              # Streamlit 入口
├── streamlit_app_spec.md
├── main.py             # 若選 A：小改輸入；若選 B：抽出 run_ema
├── ...
```

若之後有 `run_ema`，可放在 `main.py` 或 `core.py`，由 `app.py` import。
