from manim import *

class AbsoluteValueFractionSubtraction(Scene):
    """
    Fraction addition subtraction 分數加減: Visualizes the four-step workflow for "absolute value of fraction expressions".

    動畫手法範本：分數絕對值運算四步驟
    ----------
    適用場景：
    - 形如 |a| ± |b| 的表達式（a, b 為帶分數或假分數）
    - 涉及絕對值轉換 → 帶分數轉假分數 → 通分 → 加減 的綜合題型

    視覺要點（四步驟，分別用獨立 step_title 呈現）：
    1. 計算絕對值（去除負號）
    2. 帶分數化為假分數（展示 a*c + b 公式）
    3. 通分（標明 LCM 與擴分過程）
    4. 分子相減（保留共同分母）

    每步驟用 TransformMatchingTex 維持「主算式」一條線，輔助計算放側邊。

    注意：本範本用 a = -2 1/3, b = 1 1/6 作為示意例（避開 30 題中的任何具體數字），
    使用者套用時須**自行替換**真實題目的 a 與 b 並重新計算 LCM 與分子值。
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
        title = Text("Technique: Four-Step Absolute Value Fraction Workflow", font_size=32).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 示意變數宣告（用 a = -2 1/3, b = 1 1/6，避開 Q124 的具體值）
        a_val = MathTex(r"a = -2 \frac{1}{3}")
        b_val = MathTex(r"b = 1 \frac{1}{6}")
        problem_vars = VGroup(a_val, b_val).arrange(RIGHT, buff=1).next_to(title, DOWN, buff=0.4)
        self.play(Write(problem_vars))
        self.wait(0.5)

        initial_question = MathTex(r"\text{Find } |a| - |b|")
        initial_question.next_to(problem_vars, DOWN, buff=0.4)
        self.play(Write(initial_question))
        self.wait(1)

        current = MathTex(r"|a| - |b|")
        current.move_to(initial_question.get_center())
        self.add(current)
        self.play(FadeOut(initial_question, problem_vars))
        self.wait(0.3)

        # Step 1: 絕對值
        step1_title = Text("Step 1: Strip the signs (absolute value)", font_size=24).to_edge(UL).shift(RIGHT*0.3)
        abs_a = MathTex(r"|a| = \left|-2 \frac{1}{3}\right| = 2 \frac{1}{3}")
        abs_b = MathTex(r"|b| = \left|1 \frac{1}{6}\right| = 1 \frac{1}{6}")
        abs_group = VGroup(abs_a, abs_b).arrange(DOWN, buff=0.3).next_to(step1_title, DOWN, buff=0.4).align_to(step1_title, LEFT)
        self.play(Write(step1_title), Write(abs_group))
        self.wait(1)

        nxt = MathTex(r"|a| - |b| = 2 \frac{1}{3} - 1 \frac{1}{6}").move_to(current)
        self.play(TransformMatchingTex(current, nxt))
        current = nxt
        self.wait(1)
        self.play(FadeOut(step1_title, abs_group))

        # Step 2: 帶分數 → 假分數
        step2_title = Text("Step 2: Convert mixed → improper fractions", font_size=24).to_edge(UL).shift(RIGHT*0.3)
        conv1 = MathTex(r"2 \frac{1}{3} = \frac{2 \times 3 + 1}{3} = \frac{7}{3}")
        conv2 = MathTex(r"1 \frac{1}{6} = \frac{1 \times 6 + 1}{6} = \frac{7}{6}")
        conv_group = VGroup(conv1, conv2).arrange(DOWN, buff=0.3).next_to(step2_title, DOWN, buff=0.4).align_to(step2_title, LEFT)
        self.play(Write(step2_title), Write(conv_group))
        self.wait(1)

        nxt = MathTex(r"2 \frac{1}{3} - 1 \frac{1}{6} = \frac{7}{3} - \frac{7}{6}").move_to(current)
        self.play(TransformMatchingTex(current, nxt))
        current = nxt
        self.wait(1)
        self.play(FadeOut(step2_title, conv_group))

        # Step 3: 通分
        step3_title = Text("Step 3: Common denominator (LCM)", font_size=24).to_edge(UL).shift(RIGHT*0.3)
        lcm_hint = MathTex(r"\text{LCM}(3, 6) = 6").next_to(step3_title, DOWN, buff=0.3).align_to(step3_title, LEFT)
        cd1 = MathTex(r"\frac{7}{3} = \frac{7 \times 2}{3 \times 2} = \frac{14}{6}")
        cd_group = VGroup(cd1).arrange(DOWN, buff=0.3).next_to(lcm_hint, DOWN, buff=0.3).align_to(step3_title, LEFT)
        self.play(Write(step3_title), Write(lcm_hint), Write(cd_group))
        self.wait(1)

        nxt = MathTex(r"\frac{7}{3} - \frac{7}{6} = \frac{14}{6} - \frac{7}{6}").move_to(current)
        self.play(TransformMatchingTex(current, nxt))
        current = nxt
        self.wait(1)
        self.play(FadeOut(step3_title, lcm_hint, cd_group))

        # Step 4: 分子相減
        step4_title = Text("Step 4: Subtract numerators (keep denominator)", font_size=24).to_edge(UL).shift(RIGHT*0.3)
        sub_expr = MathTex(r"\frac{14}{6} - \frac{7}{6} = \frac{14 - 7}{6} = \frac{7}{6}").move_to(current)
        self.play(Write(step4_title))
        self.play(TransformMatchingTex(current, sub_expr))
        current = sub_expr
        self.wait(2)

        # 最終答案
        final_text = Text("Result:", font_size=30).next_to(current, DOWN, buff=0.8).align_to(current, LEFT)
        final_val = MathTex(r"\frac{7}{6}", font_size=44, color="#FFBE0B").next_to(final_text, RIGHT, buff=0.5)
        self.play(FadeOut(step4_title))
        self.play(Write(final_text), Write(final_val))
        final_box = self.get_glow_rect(final_val, color="#06D6A0", buff=0.2)
        self.play(Create(final_box))
        self.wait(2)

        hint = Text("To apply: only the four-step skeleton matters — your numbers will differ.",
                    font_size=20, color=GRAY).to_edge(DOWN, buff=0.3)
        self.play(Write(hint))
        self.wait(2)
        self.play(FadeOut(VGroup(title, current, final_text, final_val, final_box, hint)))
