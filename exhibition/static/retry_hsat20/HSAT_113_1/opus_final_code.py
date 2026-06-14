from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("藥物指數衰退問題", font="Noto Sans CJK TC", color=BLUE).scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        problem = VGroup(
            Text("服用 2 小時後，剩下一半劑量", font="Noto Sans CJK TC").scale(0.5),
            Text("問：4 小時後剩下多少？", font="Noto Sans CJK TC").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        problem.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(problem, shift=UP))
        self.wait(1)

        # Model
        model = MathTex(r"A(t) = A_0 \cdot r^{\,t}").scale(0.9)
        model.next_to(problem, DOWN, buff=0.6)
        self.play(Write(model))
        self.wait(1)

        # Half-life condition
        cond = MathTex(r"A(2) = \frac{1}{2} A_0").scale(0.8)
        cond.next_to(model, DOWN, buff=0.5)
        self.play(Write(cond))
        self.wait(0.5)

        solve = MathTex(r"r^{2} = \frac{1}{2}").scale(0.8)
        solve.next_to(cond, DOWN, buff=0.4)
        self.play(Write(solve))
        self.wait(1)

        # Step at t=4
        step = MathTex(
            r"A(4) = A_0 \cdot r^{4}",
            r"= A_0 \cdot (r^{2})^{2}",
            r"= A_0 \cdot \left(\frac{1}{2}\right)^{2}",
        ).scale(0.7).arrange(RIGHT, buff=0.25)
        step.next_to(solve, DOWN, buff=0.6)
        self.play(Write(step), run_time=2)
        self.wait(1)

        result = MathTex(r"A(4) = \frac{1}{4} A_0", color=YELLOW).scale(1.0)
        result.next_to(step, DOWN, buff=0.6)
        box = SurroundingRectangle(result, color=YELLOW, buff=0.2)
        self.play(Write(result))
        self.play(Create(box))
        self.wait(2)

        # Highlight half each 2 hours visual
        self.play(
            FadeOut(model), FadeOut(cond), FadeOut(solve),
            FadeOut(step), FadeOut(problem),
        )
        self.play(
            VGroup(result, box).animate.next_to(title, DOWN, buff=0.8)
        )

        bars = VGroup()
        labels = VGroup()
        amounts = ["1", r"\frac{1}{2}", r"\frac{1}{4}"]
        times = ["0 hr", "2 hr", "4 hr"]
        heights = [3.0, 1.5, 0.75]
        for i, (a, t, h) in enumerate(zip(amounts, times, heights)):
            bar = Rectangle(width=1.0, height=h, fill_color=BLUE,
                            fill_opacity=0.8, stroke_color=WHITE)
            bar.move_to(np.array([-3 + i * 3, -1.5 + h / 2, 0]))
            amt = MathTex(a).scale(0.6).next_to(bar, UP, buff=0.15)
            tl = Text(t, font="Noto Sans CJK TC").scale(0.4).next_to(bar, DOWN, buff=0.15)
            bars.add(bar)
            labels.add(VGroup(amt, tl))

        for bar, lab in zip(bars, labels):
            self.play(GrowFromEdge(bar, DOWN), FadeIn(lab), run_time=0.7)
        self.wait(2)

        ans = Text("答案：剩下 1/4 劑量", font="Noto Sans CJK TC",
                   color=YELLOW).scale(0.6)
        ans.to_edge(DOWN, buff=0.3)
        self.play(Write(ans))
        self.wait(2)