from manim import *

class ScientificNotationSubtraction(Scene):
    """
    Exponent scientific notation 指數與科學記號: Visualizes the "unify-exponents" technique for scientific notation addition/subtraction.

    動畫手法範本：統一指數後加減
    ----------
    適用場景：
    - 科學記號加減運算（兩項 10^p 與 10^q 不同次方）
    - p ≠ q 時必須先把較小指數的項調整為較大指數
    - 再用分配律提出 10^max(p,q) → 數字部分加減 → 標準化

    視覺要點（四步驟）：
    1. 用 Indicate 標記兩個不同的指數，提示「指數不同不可直接相加減」
    2. 用 Arrow + 文字提示「小數點往左移、指數加 1」的調整規則
    3. 統一指數後，用 TransformMatchingTex 改寫為共享指數的形式
    4. 提出公因數 10^max → 算出數字部分 → 再標準化

    注意：本範本用 3.6 × 10^5 + 8 × 10^3 作為示意例（避開 Q102 的 4.5×10^5 + 7×10^4），
    使用者套用時須**自行**判斷哪個項要調整、移多少位、指數加減多少。
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

        title = Text("Technique: Unify Exponents Before Add/Subtract", font_size=32).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 示意題目：3.6 × 10^5 + 8 × 10^3
        problem = MathTex(
            "3.6 \\times 10^5",
            "+",
            "8 \\times 10^3",
        ).scale(1.2).next_to(title, DOWN, buff=1)
        self.play(Write(problem))
        self.wait(0.8)

        # Step 1: 標記兩個不同的指數
        exp1 = problem[0][5:7]  # 10^5
        exp2 = problem[2][3:5]  # 10^3
        label1 = Text("Exponents differ!", font_size=24, color="#FFBE0B").next_to(problem, DOWN, buff=0.5)
        self.play(Indicate(exp1, scale_factor=1.3), Indicate(exp2, scale_factor=1.3), Write(label1))
        self.wait(1)
        self.play(FadeOut(label1))

        # Step 2: 規則說明
        rule1 = Text("Step 1: Lift the smaller exponent to match the larger.", font_size=22).next_to(problem, DOWN, buff=0.4)
        rule2 = Text("Rule: shift decimal left by k → add k to the exponent.", font_size=22, color=GRAY).next_to(rule1, DOWN, buff=0.2)
        self.play(Write(rule1), Write(rule2))
        self.wait(1.5)

        # 演示調整：8 × 10^3 → 0.08 × 10^5（小數點往左移 2 位、指數加 2）
        adjust = MathTex(r"8 \times 10^3 = 0.08 \times 10^5", color="#FFBE0B").next_to(rule2, DOWN, buff=0.6)
        self.play(Write(adjust))
        self.wait(1.5)
        self.play(FadeOut(rule1), FadeOut(rule2))

        # Step 3: 改寫成統一指數的式子
        unified = MathTex(
            "3.6 \\times 10^5", "+", "0.08 \\times 10^5",
        ).scale(1.2).move_to(problem)
        self.play(TransformMatchingTex(problem, unified), FadeOut(adjust))
        self.wait(1)

        step3 = Text("Step 2: Factor out the shared 10^5.", font_size=22).next_to(unified, DOWN, buff=0.5)
        self.play(Write(step3))
        self.wait(0.8)

        factored = MathTex("(3.6 + 0.08)", "\\times 10^5").scale(1.2).move_to(unified)
        self.play(TransformMatchingTex(unified, factored))
        self.wait(1)

        # Step 4: 算出數字部分
        step4 = Text("Step 3: Compute the coefficient sum.", font_size=22).next_to(factored, DOWN, buff=0.5)
        self.play(Transform(step3, step4))

        coeff_calc = MathTex("3.6 + 0.08 = 3.68", color="#FFBE0B").next_to(step4, DOWN, buff=0.3)
        self.play(Write(coeff_calc))
        self.wait(1)

        result = MathTex("3.68", "\\times 10^5").scale(1.2).move_to(factored)
        self.play(TransformMatchingTex(factored, result), FadeOut(coeff_calc))
        self.wait(1)

        # 標準化檢查：3.68 已在 [1, 10) 內，無需再調整
        check = Text("Step 4: Coefficient already in [1, 10) → standard form.", font_size=22, color="#06D6A0").next_to(result, DOWN, buff=0.6)
        self.play(Transform(step3, check))
        self.wait(1)

        # 最終答案
        final_a = MathTex("a = 3.68", color="#3A86FF").next_to(result, DOWN, buff=1.5).align_to(result, LEFT)
        final_n = MathTex("n = 5", color="#06D6A0").next_to(final_a, RIGHT, buff=1.0)
        self.play(Write(final_a), Write(final_n))
        self.wait(1.5)

        final_group = VGroup(result, final_a, final_n)
        final_box = self.get_glow_rect(final_group, color="#F8FAFC", buff=0.3)
        self.play(Create(final_box))
        self.wait(1.5)

        hint = Text("If coefficient ≥ 10, normalize again (shift right, increase exponent).",
                    font_size=20, color=GRAY).to_edge(DOWN, buff=0.4)
        self.play(Write(hint))
        self.wait(2)
        self.play(FadeOut(VGroup(title, step3, result, final_a, final_n, final_box, hint)))
