"""
Generate the 3-layer self-repair funnel figure for the poster.

Usage:
    python paper/poster/figures/make_repair_funnel.py

Output:
    paper/poster/figures/figure_repair_funnel.png  (300 dpi, ~1800x1400 px)

⚠️ Note: intercept rates below are ILLUSTRATIVE estimates based on Layer
ordering rationale (cheap → expensive). Replace with real numbers from
session logs if available (search for 'linter_fail', 'layout_fail',
'vision_fail' counts across runs/).
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm

# Pick a CJK font available on macOS
for f in ["PingFang TC", "Heiti TC", "Hiragino Sans GB", "Arial Unicode MS"]:
    if any(f in font.name for font in fm.fontManager.ttflist):
        plt.rcParams["font.family"] = f
        break
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Color palette
COLOR_L1 = "#4caf50"   # green = free
COLOR_L2 = "#ffc107"   # amber = free but deeper
COLOR_L3 = "#e63946"   # red = expensive
COLOR_BOX = "#1f3a5f"  # deep blue text
COLOR_REFLEX = "#2e6fb8"

# Title
ax.text(5, 9.6, "三層自我修復迴圈 Three-Layer Self-Repair",
        ha="center", va="center", fontsize=20, fontweight="bold",
        color=COLOR_BOX)
ax.text(5, 9.15, "Cheap deterministic checks first, expensive vision last",
        ha="center", va="center", fontsize=11, style="italic", color="#666")

# Input box
ax.add_patch(FancyBboxPatch((3.5, 8.0), 3, 0.7,
             boxstyle="round,pad=0.05", linewidth=1.5,
             edgecolor=COLOR_BOX, facecolor="white"))
ax.text(5, 8.35, "Generated Manim Code", ha="center", va="center",
        fontsize=12, color=COLOR_BOX, fontweight="bold")

# Arrow down
ax.annotate("", xy=(5, 7.55), xytext=(5, 7.95),
            arrowprops=dict(arrowstyle="->", lw=1.5, color=COLOR_BOX))

# ---- Layer 1: AST Linter ----
y1 = 6.4
ax.add_patch(FancyBboxPatch((1.2, y1), 7.6, 1.05,
             boxstyle="round,pad=0.05", linewidth=2,
             edgecolor=COLOR_L1, facecolor="#e8f5e9"))
ax.text(1.5, y1 + 0.75, "Layer 1", fontsize=14, fontweight="bold",
        color=COLOR_L1, va="center")
ax.text(1.5, y1 + 0.3, "AST Linter", fontsize=10, color=COLOR_L1, va="center")

ax.text(5.0, y1 + 0.7, "30+ ManimCE 規則靜態掃描",
        fontsize=11, color=COLOR_BOX, va="center", fontweight="bold")
ax.text(5.0, y1 + 0.32, "棄用 API／幻覺方法／座標誤用／Updater 風險",
        fontsize=9, color="#555", va="center")

# Right side: cost + intercept
ax.text(8.55, y1 + 0.7, "零成本", fontsize=11, color=COLOR_L1,
        va="center", ha="right", fontweight="bold")
ax.text(8.55, y1 + 0.32, "攔截 ~50%*", fontsize=9, color="#555",
        va="center", ha="right")

ax.annotate("", xy=(5, 6.1), xytext=(5, 6.35),
            arrowprops=dict(arrowstyle="->", lw=1.5, color=COLOR_BOX))

# ---- Layer 2: Layout Auditor ----
y2 = 4.95
ax.add_patch(FancyBboxPatch((1.6, y2), 6.8, 1.05,
             boxstyle="round,pad=0.05", linewidth=2,
             edgecolor=COLOR_L2, facecolor="#fff8e1"))
ax.text(1.85, y2 + 0.75, "Layer 2", fontsize=14, fontweight="bold",
        color="#c89400", va="center")
ax.text(1.85, y2 + 0.3, "Layout Audit", fontsize=10, color="#c89400", va="center")

ax.text(5.0, y2 + 0.7, "確定性幾何 AABB 審計",
        fontsize=11, color=COLOR_BOX, va="center", fontweight="bold")
ax.text(5.0, y2 + 0.32, "物件重疊／文字遮擋／畫面擁擠／水平平衡",
        fontsize=9, color="#555", va="center")

ax.text(8.15, y2 + 0.7, "零成本", fontsize=11, color="#c89400",
        va="center", ha="right", fontweight="bold")
ax.text(8.15, y2 + 0.32, "攔截 ~30%*", fontsize=9, color="#555",
        va="center", ha="right")

ax.annotate("", xy=(5, 4.65), xytext=(5, 4.9),
            arrowprops=dict(arrowstyle="->", lw=1.5, color=COLOR_BOX))

# ---- Layer 3: Vision Auditor ----
y3 = 3.5
ax.add_patch(FancyBboxPatch((2.0, y3), 6.0, 1.05,
             boxstyle="round,pad=0.05", linewidth=2,
             edgecolor=COLOR_L3, facecolor="#ffebee"))
ax.text(2.25, y3 + 0.75, "Layer 3", fontsize=14, fontweight="bold",
        color=COLOR_L3, va="center")
ax.text(2.25, y3 + 0.3, "Vision Audit", fontsize=10, color=COLOR_L3, va="center")

ax.text(4.7, y3 + 0.7, "GPT-4o Chain-of-Visual-Thought",
        fontsize=10, color=COLOR_BOX, va="center", ha="center", fontweight="bold")
ax.text(4.7, y3 + 0.32, "題目一致性／概念忠實度／結構／時序／信心",
        fontsize=8.5, color="#555", va="center", ha="center")

ax.text(7.85, y3 + 0.7, "$0.02/題", fontsize=10, color=COLOR_L3,
        va="center", ha="right", fontweight="bold")
ax.text(7.85, y3 + 0.32, "攔截 ~20%*", fontsize=8.5, color="#555",
        va="center", ha="right")

ax.annotate("", xy=(5, 3.2), xytext=(5, 3.45),
            arrowprops=dict(arrowstyle="->", lw=1.5, color=COLOR_BOX))

# ---- Reflexion Loop ----
y4 = 2.1
ax.add_patch(FancyBboxPatch((2.5, y4), 5.0, 0.9,
             boxstyle="round,pad=0.05", linewidth=2,
             edgecolor=COLOR_REFLEX, facecolor="#e3f2fd",
             linestyle="--"))
ax.text(5, y4 + 0.6, "Reflexion 修正迴圈", fontsize=12,
        color=COLOR_REFLEX, ha="center", va="center", fontweight="bold")
ax.text(5, y4 + 0.25, "失敗→將教訓編入 prompt 前綴→重生成（主迭代上限 5 次）",
        fontsize=8.5, color="#555", ha="center", va="center")

# Curved arrow back from reflexion to top
ax.annotate("",
            xy=(1.2, 6.9), xytext=(2.5, 2.55),
            arrowprops=dict(arrowstyle="->", lw=1.2,
                            color=COLOR_REFLEX,
                            connectionstyle="arc3,rad=-0.4"))

# Final output
ax.add_patch(FancyBboxPatch((3.5, 0.6), 3, 0.7,
             boxstyle="round,pad=0.05", linewidth=2,
             edgecolor="#2e7d32", facecolor="#c8e6c9"))
ax.text(5, 0.95, "PASS → Render → Final Video",
        ha="center", va="center", fontsize=12, color="#1b5e20",
        fontweight="bold")

ax.annotate("", xy=(5, 0.55), xytext=(5, 2.05),
            arrowprops=dict(arrowstyle="->", lw=1.5, color="#2e7d32"))

# Footnote
ax.text(5, 0.05,
        "* 攔截率為各層架構設計分配示意；實際比例隨題目難度浮動",
        fontsize=7, color="#888", ha="center", style="italic")

plt.tight_layout()
out = "paper/poster/figures/figure_repair_funnel.png"
plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
print(f"saved: {out}")
