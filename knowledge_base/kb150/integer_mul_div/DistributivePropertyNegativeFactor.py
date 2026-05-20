from manim import *

class DistributivePropertyNegativeFactor(Scene):
    """
    Integer multiplication division 整數乘除: Visualizes the "factor-out-common-negative" technique for distributive law with a negative shared factor.

    動畫手法範本：負號公因數提取
    ----------
    適用場景：
    - a × (-c) ± b × c 形式的算式（兩項共享絕對值相同但符號相反的因數）
    - 兩項相減後可改寫成共享同一個負號因數的「分配律逆用」
    - 任何適合「提取公因數簡化兩項相乘」的整數運算

    視覺要點：
    1. 用 Indicate + 顏色標記同符號因數，提示「可提公因數」
    2. 用 TransformMatchingTex 演出「改寫減法 → 提取共同因數 → 計算括號 → 最後乘法」四階段
    3. 每階段配說明文字，但說明文字描述「手法」而非「具體數字」

    注意：本範本用 a=20, b=30, c=15 形式的示意例（20×(-15) - 30×15），
    使用者套用時須**自行替換**真實題目的數字並逐步推導。
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
        title = Text("Technique: Factor-Out a Negative Common Factor", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: 示意算式（避開實驗 30 題的具體數字 54, 39, 46）
        expr1 = MathTex("20", "\\times", "(-15)", "-", "30", "\\times", "15")
        expr1.move_to(ORIGIN)
        self.play(Write(expr1))
        self.wait(1)

        explanation1 = Text("Step 1: Rewrite subtraction as addition with a negative factor",
                            font_size=24).next_to(expr1, DOWN, buff=0.8)
        self.play(Write(explanation1))
        self.play(
            Indicate(expr1[3], color="#FFBE0B"),  # '-'
            Indicate(expr1[6], color="#FFBE0B"),  # 後項的正因數
        )
        self.wait(1)

        # Step 2: 改寫成兩項共享 (-c)
        expr2 = MathTex("20", "\\times", "(-15)", "+", "30", "\\times", "(-15)")
        expr2.move_to(expr1)
        self.play(TransformMatchingTex(expr1, expr2), FadeOut(explanation1))
        self.wait(1)

        explanation2 = Text("Step 2: Factor out the shared negative factor",
                            font_size=24).next_to(expr2, DOWN, buff=0.8)
        self.play(Write(explanation2))
        self.play(
            Indicate(expr2[2], color="#FFBE0B"),
            Indicate(expr2[6], color="#FFBE0B"),
        )
        self.wait(1)

        # Step 3: 提公因數
        expr3 = MathTex("(-15)", "\\times", "(", "20", "+", "30", ")")
        expr3.move_to(expr2)
        self.play(TransformMatchingTex(expr2, expr3), FadeOut(explanation2))
        self.wait(1)

        explanation3 = Text("Step 3: Sum inside the parentheses",
                            font_size=24).next_to(expr3, DOWN, buff=0.8)
        self.play(Write(explanation3))
        self.play(Indicate(VGroup(expr3[3], expr3[4], expr3[5]), color="#FFBE0B"))
        self.wait(1)

        # Step 4: 計算括號
        expr4 = MathTex("(-15)", "\\times", "50")
        expr4.move_to(expr3)
        self.play(TransformMatchingTex(expr3, expr4), FadeOut(explanation3))
        self.wait(1)

        explanation4 = Text("Step 4: Final multiplication",
                            font_size=24).next_to(expr4, DOWN, buff=0.8)
        self.play(Write(explanation4))
        self.wait(1)

        # Step 5: 最終答案
        final = MathTex("-750")
        final.move_to(expr4)
        self.play(TransformMatchingTex(expr4, final), FadeOut(explanation4))
        self.wait(1)

        final_box = self.get_glow_rect(final, color="#06D6A0", buff=0.2)
        self.play(Create(final_box))
        self.wait(2)

        # 套用提示
        hint = Text("To apply: look for two terms sharing |c| with opposite signs.",
                    font_size=20, color=GRAY).to_edge(DOWN, buff=0.4)
        self.play(Write(hint))
        self.wait(2)

        self.play(FadeOut(VGroup(title, final, final_box, hint)))
        self.wait(0.5)
