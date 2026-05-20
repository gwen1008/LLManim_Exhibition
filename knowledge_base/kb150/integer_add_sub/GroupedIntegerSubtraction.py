from manim import *

class GroupedIntegerSubtraction(Scene):
    """
    Integer addition subtraction 整數加減: Visualizes the "group-and-pair" simplification technique for alternating integer sums.

    動畫手法範本：分組配對化簡
    ----------
    適用場景：
    - 偶數項加減交錯的長算式，可兩兩分組
    - 等差遞增/遞減的交替項，分組後每組差值相等
    - 任何「相鄰兩項用括號圈起來可化簡」的整數運算

    視覺要點：
    1. 用 self.get_glow_rect 把每組「圈起來」（不同顏色區分組別）
    2. 在每組下方算出小計，再回填到主算式
    3. 最後把所有小計加總成最終答案

    注意：本範本用 30 - 42 + 50 - 62 作為示意例（每組差均為 -12），
    使用者套用時須先**自行判斷**題目是否適合「分組配對」策略，並按題目具體數字計算。
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

        # 標題：只描述「手法」，不洩漏具體題目數字
        problem_title = Text("Technique: Group-and-Pair Simplification", font_size=36).to_edge(UP)
        self.play(Write(problem_title))
        self.wait(1)

        # 示意算式（用不同的數字，避開實驗 30 題中的任何題目）
        expr_0 = MathTex("30 - 42 + 50 - 62")
        expr_0.next_to(problem_title, DOWN, buff=1)
        self.play(Write(expr_0))
        self.wait(1.5)

        # 手法提示
        strategy_hint = Text("Strategy: pair adjacent terms with brackets", font_size=26, color="#FFBE0B")
        strategy_hint.next_to(expr_0, DOWN, buff=1.0).to_edge(LEFT)
        self.play(Write(strategy_hint))
        self.wait(1.5)

        # 加入括號分組
        expr_1 = MathTex("(30 - 42)", "+", "(50 - 62)")
        expr_1.move_to(expr_0.get_center())
        self.play(FadeOut(expr_0), FadeIn(expr_1))
        self.wait(1.5)

        # 第一組：圈起來 → 算出小計
        first_box = self.get_glow_rect(expr_1[0], color="#3A86FF")
        self.play(Create(first_box))
        calc1 = MathTex("30 - 42 = -12", color="#3A86FF").next_to(expr_1, DOWN, buff=0.8).to_edge(LEFT)
        self.play(Write(calc1))
        self.wait(1.5)

        expr_2 = MathTex("(-12)", "+", "(50 - 62)")
        expr_2.move_to(expr_1.get_center())
        self.play(FadeOut(first_box), TransformMatchingTex(expr_1, expr_2))
        self.wait(0.8)

        # 第二組：同樣手法
        second_box = self.get_glow_rect(expr_2[2], color="#FF006E")
        self.play(Create(second_box))
        calc2 = MathTex("50 - 62 = -12", color="#FF006E").next_to(calc1, DOWN, buff=0.4).align_to(calc1, LEFT)
        self.play(Write(calc2))
        self.wait(1.5)

        expr_3 = MathTex("(-12)", "+", "(-12)")
        expr_3.move_to(expr_2.get_center())
        self.play(FadeOut(second_box), TransformMatchingTex(expr_2, expr_3))
        self.wait(0.8)

        # 收尾：加總成最終結果
        self.play(FadeOut(calc1, calc2, strategy_hint),
                  expr_3.animate.move_to(ORIGIN).shift(UP*0.5))
        self.wait(0.5)

        final_result = MathTex("= -24")
        final_result.next_to(expr_3, RIGHT, buff=0.3)
        self.play(Write(final_result))
        self.wait(1.5)

        final_box = self.get_glow_rect(VGroup(expr_3, final_result), color="#06D6A0", buff=0.2)
        self.play(Create(final_box))
        self.wait(2)

        # 提示：套用此手法時的注意事項
        hint = Text("To apply: identify if pairs share a common pattern (e.g., equal difference).",
                    font_size=20, color=GRAY).to_edge(DOWN, buff=0.4)
        self.play(Write(hint))
        self.wait(2)

        self.play(FadeOut(VGroup(final_box, expr_3, final_result, problem_title, hint)))
        self.wait(0.5)
