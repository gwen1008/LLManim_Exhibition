from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("解對數方程", font_size=44, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        eq0 = MathTex(r"\log_2(x) + \log_2(x-2) = 3", font_size=48)
        eq0.next_to(title, DOWN, buff=0.7)
        self.play(Write(eq0))
        self.wait(1)

        step1_label = Text("1. 合併對數（對數運算律）", font_size=26, color=BLUE)
        eq1 = MathTex(r"\log_2\big(x(x-2)\big) = 3", font_size=44)
        step1 = VGroup(step1_label, eq1).arrange(DOWN, buff=0.3)
        step1.next_to(eq0, DOWN, buff=0.6)
        self.play(FadeIn(step1_label, shift=RIGHT))
        self.play(TransformFromCopy(eq0, eq1))
        self.wait(1)

        step2_label = Text("2. 轉為指數形式", font_size=26, color=BLUE)
        eq2 = MathTex(r"x(x-2) = 2^3 = 8", font_size=44)
        step2 = VGroup(step2_label, eq2).arrange(DOWN, buff=0.3)
        step2.next_to(step1, DOWN, buff=0.5)
        self.play(FadeIn(step2_label, shift=RIGHT))
        self.play(Write(eq2))
        self.wait(1)

        # Clear top equations to make room
        self.play(
            FadeOut(eq0),
            FadeOut(step1),
            step2.animate.next_to(title, DOWN, buff=0.6),
        )
        self.wait(0.3)

        step3_label = Text("3. 整理成二次方程", font_size=26, color=BLUE)
        eq3 = MathTex(r"x^2 - 2x - 8 = 0", font_size=46)
        step3 = VGroup(step3_label, eq3).arrange(DOWN, buff=0.3)
        step3.next_to(step2, DOWN, buff=0.6)
        self.play(FadeIn(step3_label, shift=RIGHT))
        self.play(Write(eq3))
        self.wait(1)

        step4_label = Text("4. 因式分解", font_size=26, color=BLUE)
        eq4 = MathTex(r"(x-4)(x+2) = 0", font_size=46)
        step4 = VGroup(step4_label, eq4).arrange(DOWN, buff=0.3)
        step4.next_to(step3, DOWN, buff=0.6)
        self.play(FadeIn(step4_label, shift=RIGHT))
        self.play(TransformFromCopy(eq3, eq4))
        self.wait(1)

        roots = MathTex(r"x = 4 \quad \text{或} \quad x = -2", font_size=46)
        roots.next_to(step4, DOWN, buff=0.6)
        self.play(Write(roots))
        self.wait(1)

        # Domain check
        self.play(
            FadeOut(step2),
            FadeOut(step3),
            step4.animate.to_edge(UP, buff=1.2),
            roots.animate.next_to(title, DOWN, buff=2.4),
        )
        self.wait(0.3)

        check_label = Text("5. 檢驗定義域", font_size=28, color=GREEN)
        check_cond = MathTex(r"x > 0 \;\; \text{且} \;\; x - 2 > 0 \;\Rightarrow\; x > 2", font_size=40)
        check = VGroup(check_label, check_cond).arrange(DOWN, buff=0.35)
        check.next_to(roots, DOWN, buff=0.7)
        self.play(FadeIn(check_label, shift=UP))
        self.play(Write(check_cond))
        self.wait(1)

        # Reject extraneous root
        reject = MathTex(r"x = -2", r"\;\;(\text{捨去：不符 } x>2)", font_size=40)
        reject.set_color_by_tex(r"x = -2", RED)
        reject.next_to(check, DOWN, buff=0.5)
        cross = Line(
            reject[0].get_left() + LEFT * 0.1,
            reject[0].get_right() + RIGHT * 0.1,
            color=RED,
            stroke_width=5,
        )
        self.play(Write(reject))
        self.play(Create(cross))
        self.wait(1)

        answer = MathTex(r"\boxed{x = 4}", font_size=60, color=YELLOW)
        answer.next_to(reject, DOWN, buff=0.6)
        self.play(Write(answer))
        self.play(Flash(answer, color=YELLOW, flash_radius=1.2))
        self.wait(2)