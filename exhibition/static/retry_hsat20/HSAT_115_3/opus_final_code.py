from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("等差 × 等比 數列問題", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        setup = MathTex(r"f(x)=a^x,\quad a>0", font_size=44)
        setup.next_to(title, DOWN, buff=0.5)
        self.play(Write(setup))
        self.wait(0.5)

        c_cond = VGroup(
            MathTex(r"c_1,\,c_2,\,c_3:", font_size=38),
            Text("公差", font_size=30),
            MathTex(r"=\tfrac{10}{3}", font_size=38),
        ).arrange(RIGHT, buff=0.2).next_to(setup, DOWN, buff=0.5)

        f_cond = VGroup(
            MathTex(r"f(c_1),\,f(c_2),\,f(c_3):", font_size=38),
            Text("公比", font_size=30),
            MathTex(r"=4", font_size=38),
        ).arrange(RIGHT, buff=0.2).next_to(c_cond, DOWN, buff=0.4)

        self.play(Write(c_cond))
        self.play(Write(f_cond))
        self.wait(0.6)

        step1 = MathTex(
            r"\frac{f(c_2)}{f(c_1)}=a^{\,c_2-c_1}=a^{\frac{10}{3}}=4",
            font_size=40,
        ).next_to(f_cond, DOWN, buff=0.6)
        self.play(Write(step1))
        self.wait(0.6)

        box1 = SurroundingRectangle(step1, color=YELLOW, buff=0.15)
        self.play(Create(box1))
        self.wait(0.5)

        self.play(
            FadeOut(c_cond), FadeOut(f_cond), FadeOut(box1),
            step1.animate.next_to(setup, DOWN, buff=0.5),
        )
        self.wait(0.3)

        target = MathTex(
            r"f(10),\,f(8),\,f(6)\ \Rightarrow\ r=\frac{f(8)}{f(10)}=a^{-2}",
            font_size=40,
        ).next_to(step1, DOWN, buff=0.6)
        self.play(Write(target))
        self.wait(0.6)

        derive = MathTex(
            r"a^{\frac{10}{3}}=4\ \Rightarrow\ a^{-2}=4^{-\frac{3}{5}}",
            font_size=40,
        ).next_to(target, DOWN, buff=0.5)
        self.play(Write(derive))
        self.wait(0.6)

        answer = MathTex(
            r"r=4^{-\frac{3}{5}}=2^{-\frac{6}{5}}\approx 0.435",
            font_size=46,
            color=YELLOW,
        ).next_to(derive, DOWN, buff=0.6)
        self.play(Write(answer))
        box2 = SurroundingRectangle(answer, color=GREEN, buff=0.2)
        self.play(Create(box2))
        self.wait(2)