from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("藥物殘留量：指數衰退", font="Noto Sans CJK TC", weight=BOLD)
        title.scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Setup: exponential model
        model = MathTex(r"A(t) = A_0 \cdot k^{t}").scale(1.0)
        model.next_to(title, DOWN, buff=0.6)
        self.play(Write(model))
        self.wait(0.5)

        cond = Text("2 小時後剩一半", font="Noto Sans CJK TC").scale(0.6)
        cond.next_to(model, DOWN, buff=0.5)
        self.play(FadeIn(cond, shift=UP))
        self.wait(0.5)

        # Derive k
        eq1 = MathTex(r"A(2) = A_0 \cdot k^{2} = \tfrac{1}{2} A_0").scale(0.9)
        eq1.next_to(cond, DOWN, buff=0.5)
        self.play(Write(eq1))
        self.wait(0.5)

        eq2 = MathTex(r"k^{2} = \tfrac{1}{2}").scale(0.9)
        eq2.next_to(eq1, DOWN, buff=0.4)
        self.play(Write(eq2))
        self.wait(0.5)

        # 4 hours
        ask = MathTex(r"A(4) = A_0 \cdot k^{4}").scale(0.9)
        ask.next_to(eq2, DOWN, buff=0.5)
        self.play(Write(ask))
        self.wait(0.5)

        step = MathTex(r"k^{4} = (k^{2})^{2} = \left(\tfrac{1}{2}\right)^{2} = \tfrac{1}{4}").scale(0.9)
        step.next_to(ask, DOWN, buff=0.4)
        self.play(Write(step))
        self.wait(0.8)

        # Clear lower part for final answer
        self.play(
            FadeOut(model), FadeOut(cond), FadeOut(eq1),
            FadeOut(eq2), FadeOut(ask), FadeOut(step),
        )

        result = MathTex(r"A(4) = \frac{1}{4} A_0").scale(1.4)
        result.set_color(YELLOW)
        box = SurroundingRectangle(result, color=YELLOW, buff=0.4)
        self.play(Write(result))
        self.play(Create(box))
        self.wait(1.0)

        ans = Text("答案：剩 1/4 劑量", font="Noto Sans CJK TC", weight=BOLD).scale(0.7)
        ans.next_to(box, DOWN, buff=0.6)
        self.play(FadeIn(ans, shift=UP))
        self.wait(2)