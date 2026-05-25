# 08 — QR Code + 致謝 + 參考文獻

**位置**：海報最下方（區塊 ⑩），60 × 5 cm
- **致謝 + 參考文獻**：左側，約 30 × 5 cm（小字 12pt）
- **QR codes**：右側，並排 3 個（每個約 5×5 cm）

---

## QR Code 區（右下，v2 改為 3 個）

```
   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
   │             │    │             │    │             │
   │   [QR 1]    │    │   [QR 2]    │    │   [QR 3]    │
   │             │    │             │    │             │
   └─────────────┘    └─────────────┘    └─────────────┘
    Demo Video         GitHub Repo        Paper (AIED LBR)
    （示範影片）        （程式碼）          （論文 PDF）
```

### 📌 三個 URL 由廖振廷之後提供

| QR | 內容 | 狀態 |
|---|---|---|
| 1 | Demo 影片 | ⏳ 廖振廷之後給（YouTube unlisted） |
| 2 | GitHub Repo | ⏳ 廖振廷之後給（會先設 public） |
| 3 | AIED 2026 LBR 論文 | ⏳ 廖振廷之後給（會議報告後才有正式連結） |

**🛠️ 你現在可以做的事**：
先在海報 QR 位置放 **3 個灰色佔位方框**（5×5 cm，深灰底白色問號），下方標籤「Demo / Code / Paper」。
等廖振廷給 URL 後，用 `qrencode` 一次生成 3 個 PNG 直接替換佔位即可，不影響整體排版。

**🌟 進階加分項（可選）**：
加第 4 個 QR — **Live Demo**（Streamlit / HuggingFace Space），標示 `🔴 Try it now`，讓評審當場輸入題目試跑。這在 AIED poster session 殺傷力極大。

### 生成方式
**選項 A（命令列，最快）**：
```bash
# 安裝（macOS）：brew install qrencode
qrencode -o demo_video.png -s 12 "https://youtu.be/XXXXX"
qrencode -o github_repo.png -s 12 "https://github.com/USER/REPO"
```

**選項 B（線上）**：
- https://www.qr-code-generator.com/
- https://www.the-qrcode-generator.com/

**參數建議**：解析度 ≥ 600×600 px，避免列印模糊；error correction level 設 M 或 Q。

---

## 致謝（左下，14pt）

```
本研究感謝國立臺灣師範大學電機工程學系專題經費支持，
並感謝賴以威副教授於研究方向與系統設計上的指導。
```

---

## 參考文獻（左下，14pt）

```
Mayer, R. E. (2009). Multimedia Learning (2nd ed.). Cambridge University Press.
Shinn, N., et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. NeurIPS 2023.
Manim Community. (2024). Manim Community Edition. https://www.manim.community/
```

> ⚠️ 如書面報告有引用其他關鍵文獻（CoT、RAG、Tree-of-Thought 等），請組員補上 2-3 篇代表作。
