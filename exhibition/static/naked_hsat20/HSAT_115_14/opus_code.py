from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title(r"向量 $(a,b)$ 垂直於 $y=bx-1$", include_underline=True)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: direction vector of line
        s1 = MathTex(r"y = bx - 1 \;\Rightarrow\; \text{方向向量}\ (1,\,b)")
        s1.next_to(title, DOWN, buff=0.7)
        self.play(Write(s1))
        self.wait(0.8)

        # Step 2: perpendicular condition -> dot product = 0
        s2 = MathTex(r"(a,b)\cdot(1,b)=0")
        s2.next_to(s1, DOWN, buff=0.6)
        self.play(Write(s2))
        self.wait(0.6)

        s3 = MathTex(r"a + b^{2} = 0 \;\Rightarrow\; a = -b^{2}")
        s3.next_to(s2, DOWN, buff=0.5)
        self.play(Write(s3))
        self.wait(0.8)

        # Step 3: express a+b
        s4 = MathTex(r"a + b = -b^{2} + b")
        s4.next_to(s3, DOWN, buff=0.6)
        self.play(Write(s4))
        self.wait(0.6)

        # Step 4: complete the square
        s5 = MathTex(
            r"= -\left(b-\tfrac{1}{2}\right)^{2} + \tfrac{1}{4}"
        )
        s5.next_to(s4, DOWN, buff=0.5)
        self.play(Write(s5))
        self.wait(0.8)

        # Conclusion
        box = SurroundingRectangle(
            VGroup(), color=YELLOW
        )
        ans = MathTex(
            r"(a+b)_{\max} = \dfrac{1}{4}", color=YELLOW
        ).scale(1.2)
        ans.next_to(s5, DOWN, buff=0.7)
        box = SurroundingRectangle(ans, color=YELLOW, buff=0.2)
        self.play(Write(ans))
        self.play(Create(box))
        self.wait(0.5)

        cond = MathTex(
            r"\text{當 } b=\tfrac{1}{2},\; a=-\tfrac{1}{4}",
            color=BLUE,
        ).scale(0.8)
        cond.next_to(ans, DOWN, buff=0.4)
        self.play(FadeIn(cond, shift=UP))
        self.wait(2)