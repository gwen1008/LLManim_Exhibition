from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("向量正射影問題", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        given = VGroup(
            MathTex(r"\vec{a}=(2,-3),\quad \vec{b}=(3,2)"),
            MathTex(r"\vec{a}\cdot\vec{b}=6-6=0 \;\Rightarrow\; \vec{a}\perp\vec{b}"),
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.4)
        self.play(Write(given[0]))
        self.play(Write(given[1]))
        self.wait(0.6)

        cond = VGroup(
            MathTex(r"\text{proj}_{\vec a}=r-1,\qquad \text{proj}_{\vec b}=r-2"),
            MathTex(r"r=|\vec v|,\quad \text{(夾角皆銳角)}"),
        ).arrange(DOWN, buff=0.3).next_to(given, DOWN, buff=0.4)
        self.play(Write(cond[0]))
        self.play(Write(cond[1]))
        self.wait(0.6)

        self.play(
            FadeOut(given), FadeOut(cond),
        )

        step1 = MathTex(r"r^2=(r-1)^2+(r-2)^2").next_to(title, DOWN, buff=0.5)
        step2 = MathTex(r"r^2-6r+5=0 \;\Rightarrow\; r=1 \text{ 或 } r=5").next_to(step1, DOWN, buff=0.4)
        step3 = MathTex(r"r>2 \;\Rightarrow\; r=5").next_to(step2, DOWN, buff=0.4)
        self.play(Write(step1))
        self.wait(0.4)
        self.play(Write(step2))
        self.wait(0.4)
        self.play(Write(step3))
        self.wait(0.6)

        proj = MathTex(r"\text{proj}_{\vec a}=4,\quad \text{proj}_{\vec b}=3").next_to(step3, DOWN, buff=0.4)
        self.play(Write(proj))
        self.wait(0.6)

        self.play(FadeOut(step1), FadeOut(step2), FadeOut(step3), FadeOut(proj))

        vexpr = VGroup(
            MathTex(r"\vec v = 4\cdot\frac{(2,-3)}{\sqrt{13}} + 3\cdot\frac{(3,2)}{\sqrt{13}}"),
            MathTex(r"\vec v = \frac{(17,-6)}{\sqrt{13}}"),
        ).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.6)
        self.play(Write(vexpr[0]))
        self.play(Write(vexpr[1]))
        self.wait(0.6)

        self.play(FadeOut(vexpr))

        final = VGroup(
            MathTex(r"\vec w=(4,7),\quad |\vec w|=\sqrt{65}"),
            MathTex(r"\vec v\cdot\vec w=\frac{17\cdot4+(-6)\cdot7}{\sqrt{13}}=\frac{26}{\sqrt{13}}"),
            MathTex(r"\text{proj}_{\vec w}=\frac{26/\sqrt{13}}{\sqrt{65}}=\frac{26}{13\sqrt5}=\frac{2\sqrt5}{5}"),
        ).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.6)
        for m in final:
            self.play(Write(m))
            self.wait(0.4)
        self.wait(0.4)

        box = SurroundingRectangle(final[2][0][-5:], color=YELLOW)
        ans = MathTex(r"\boxed{\dfrac{2\sqrt5}{5}}", color=YELLOW, font_size=54).to_edge(DOWN)
        self.play(Create(box))
        self.play(Write(ans))
        self.wait(2)