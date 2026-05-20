from manim import *

class ScientificNotationBacterialLength(Scene):
    """
    Exponent scientific notation 指數與科學記號: Visualizes the "unit-conversion-then-scientific-notation-multiplication" workflow.

    動畫手法範本：單位換算 + 科學記號相乘
    ----------
    適用場景：
    - 應用題涉及微觀單位（微米、奈米）換算為公尺、克等基本單位
    - 數量級懸殊的數字相乘（如極小數 × 極大數）
    - 結果須以「標準科學記號」表示（1 ≤ |a| < 10）

    視覺要點（六步驟）：
    1. 單一物體尺度 → 用 10^n 換算為基本單位
    2. 數量（百萬/億）→ 轉成 10^m
    3. 列出總量算式（兩科記相乘）
    4. 分離「數字部分」與「指數部分」分別運算
    5. 合併兩部分結果
    6. 調整為標準科學記號（檢查係數範圍）

    注意：本範本用「8 奈米 × 4 千萬」作為示意例（避開 Q101 的 3.2 微米 × 5 百萬），
    使用者套用時須**自行替換**真實題目的尺度與數量，並重新計算指數加總。
    """
    def get_glow_rect(self, mobject, color="#3A86FF", buff=0.15):

        return RoundedRectangle(

            corner_radius=0.15,

            color=color,

            stroke_width=3,

            fill_color=color,

            fill_opacity=0.15

        ).surround(mobject, buff=buff)


    def construct(self):

        # 🌌 Set sleek deep-dark slate background

        self.camera.background_color = "#0B0F19"


        # 📐 Add modern thin background coordinate grid

        grid = NumberPlane(

            x_range=[-7, 7, 1], y_range=[-4, 4, 1],

            background_line_style={"stroke_color": "#1E293B", "stroke_opacity": 0.4, "stroke_width": 1}

        )

        self.add(grid)

        # 標題：描述手法
        title = Text("Technique: Unit Conversion + Scientific Notation Multiplication", font_size=28).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: 單一物體尺度換算（用 8 奈米作為示意，避開 Q101 的 3.2 微米）
        step1 = Text("Step 1: Convert per-item size to base unit", font_size=24).next_to(title, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(step1))

        size_orig = MathTex(r"\text{size} = 8 \text{ nm}")
        size_factor = MathTex(r"1 \text{ nm} = 10^{-9} \text{ m}")
        size_grp = VGroup(size_orig, size_factor).arrange(DOWN, buff=0.4).next_to(step1, DOWN, buff=0.3).align_to(step1, LEFT)
        self.play(Write(size_grp))
        self.wait(0.5)

        size_m = MathTex(r"8 \text{ nm} = 8 \times 10^{-9} \text{ m}", color="#FFBE0B")
        size_m.next_to(size_factor, DOWN, buff=0.4).align_to(step1, LEFT)
        self.play(TransformMatchingTex(size_orig, size_m), FadeOut(size_factor))
        self.wait(0.5)

        # Step 2: 數量轉科學記號
        step2 = Text("Step 2: Convert quantity to scientific form", font_size=24).next_to(size_m, DOWN, buff=0.6).to_edge(LEFT)
        self.play(Write(step2))

        qty_orig = MathTex(r"\text{count} = 4 \times 10^7")
        qty_orig.next_to(step2, DOWN, buff=0.3).align_to(step2, LEFT)
        self.play(Write(qty_orig))
        self.wait(0.5)

        # 移到上方準備計算
        self.play(
            FadeOut(step1), FadeOut(step2),
            size_m.animate.shift(UP * 2.5).to_edge(LEFT).set_color(WHITE),
            qty_orig.animate.shift(UP * 2.5).next_to(size_m, RIGHT, buff=1).set_color(WHITE),
        )

        # Step 3: 總量算式
        step3 = Text("Step 3: Set up the product", font_size=24).next_to(size_m, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(step3))
        total_eq = MathTex(
            r"\text{total} =",
            r"(8 \times 10^{-9})",
            r"\times",
            r"(4 \times 10^7)",
            font_size=42,
        ).move_to(ORIGIN)
        self.play(Write(total_eq))
        self.wait(1)

        # Step 4: 分離數字與指數部分
        step4 = Text("Step 4: Group coefficients and exponents separately", font_size=24).next_to(total_eq, UP, buff=0.4)
        self.play(Transform(step3, step4))

        rearranged = MathTex(
            r"\text{total} =",
            r"(8 \times 4)",
            r"\times",
            r"(10^{-9} \times 10^7)",
            font_size=42,
        ).move_to(ORIGIN)
        self.play(TransformMatchingTex(total_eq, rearranged))
        self.wait(1)

        num_prod = MathTex(r"8 \times 4 = 32", color="#3A86FF").next_to(rearranged, DOWN, buff=0.5).to_edge(LEFT)
        exp_prod = MathTex(r"10^{-9} \times 10^7 = 10^{-2}", color="#06D6A0").next_to(num_prod, RIGHT, buff=1)
        self.play(Write(num_prod), Write(exp_prod))
        self.wait(1)

        # Step 5: 合併
        step5 = Text("Step 5: Combine", font_size=24).next_to(rearranged, UP, buff=0.4)
        self.play(Transform(step3, step5))

        combined = MathTex(r"\text{total} = 32 \times 10^{-2}", font_size=42, color="#FFBE0B").move_to(ORIGIN)
        self.play(
            TransformMatchingTex(rearranged, combined),
            FadeOut(num_prod), FadeOut(exp_prod),
        )
        self.wait(1)

        # Step 6: 標準科學記號（係數須在 [1, 10) 內）
        step6 = Text("Step 6: Normalize to standard scientific notation (1 ≤ |a| < 10)",
                     font_size=22).next_to(combined, UP, buff=0.4)
        self.play(Transform(step3, step6))

        normalize = MathTex(r"32 \times 10^{-2} = 3.2 \times 10^1 \times 10^{-2} = 3.2 \times 10^{-1}",
                            font_size=38, color="#06D6A0").next_to(combined, DOWN, buff=0.6)
        self.play(Write(normalize))
        self.wait(1.5)

        # 最終答案
        final = MathTex(r"\text{Result: } 3.2 \times 10^{-1} \text{ m}", font_size=44).move_to(ORIGIN)
        self.play(
            FadeOut(VGroup(size_m, qty_orig, combined, normalize, step3)),
            Write(final),
        )
        box = self.get_glow_rect(final, color="#06D6A0", buff=0.3)
        self.play(Create(box))
        self.wait(2)

        hint = Text("To apply: replace the numbers above; the six-step skeleton stays identical.",
                    font_size=20, color=GRAY).to_edge(DOWN, buff=0.4)
        self.play(Write(hint))
        self.wait(2)
        self.play(FadeOut(VGroup(title, final, box, hint)))
