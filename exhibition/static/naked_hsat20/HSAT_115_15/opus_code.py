from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("等差數列與共線問題", font_size=40)
        self.play(Write(title))
        self.wait(0.5)

        problem = VGroup(
            Tex(r"正數 $a,b,c$ 成等差數列，$a<b<c$", font_size=30),
            Tex(r"三點 $(a,\log 3a),\ (b,\log 4b),\ (c,\log 6c)$ 共線", font_size=30),
            Tex(r"求 $\dfrac{b}{a}=?$", font_size=30),
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.5)
        self.play(LaggedStartMap(FadeIn, problem, shift=UP*0.2, lag_ratio=0.3))
        self.wait(1)

        self.play(problem.animate.scale(0.8).to_edge(LEFT).shift(UP*1.5))

        steps = VGroup(
            Tex(r"等差：$2b=a+c \Rightarrow b-a=c-b$", font_size=30),
            Tex(r"共線 $\Rightarrow$ 斜率相等，分母相等", font_size=30),
            Tex(r"$\log 4b-\log 3a=\log 6c-\log 4b$", font_size=30),
            Tex(r"$2\log 4b=\log 3a+\log 6c$", font_size=30),
            Tex(r"$(4b)^2=3a\cdot 6c=18ac$", font_size=30),
            Tex(r"$16b^2=18ac$", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(problem, DOWN, buff=0.5).to_edge(LEFT)

        for s in steps:
            self.play(FadeIn(s, shift=RIGHT*0.2), run_time=0.7)
        self.wait(0.8)

        right = VGroup(
            Tex(r"代入 $c=2b-a$：", font_size=30),
            Tex(r"$16b^2=18a(2b-a)$", font_size=30),
            Tex(r"$8b^2-18ab+9a^2=0$", font_size=30),
            Tex(r"令 $r=\dfrac{b}{a}$：", font_size=30),
            Tex(r"$8r^2-18r+9=0$", font_size=30),
            Tex(r"$r=\dfrac{18\pm6}{16}=\dfrac32 \text{ 或 } \dfrac34$", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT).shift(UP*0.5)

        for s in right:
            self.play(FadeIn(s, shift=LEFT*0.2), run_time=0.7)
        self.wait(0.8)

        cond = Tex(r"因 $a<b \Rightarrow r>1$", font_size=30, color=YELLOW)
        cond.next_to(right, DOWN, buff=0.4).align_to(right, LEFT)
        self.play(Write(cond))
        self.wait(0.5)

        answer = Tex(r"$\dfrac{b}{a}=\dfrac32$", font_size=48, color=GREEN)
        box = SurroundingRectangle(answer, color=GREEN, buff=0.3)
        ans_group = VGroup(answer, box).next_to(cond, DOWN, buff=0.4)
        self.play(Write(answer))
        self.play(Create(box))
        self.wait(2)