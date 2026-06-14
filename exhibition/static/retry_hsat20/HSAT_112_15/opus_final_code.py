from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("向量垂直與內積問題", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            MathTex(r"\vec{OA} \perp \vec{OB},\quad O=(0,0)"),
            MathTex(r"A=(a,0),\quad B=(0,b)"),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8).next_to(title, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(setup))
        self.wait(0.5)

        oc = MathTex(
            r"\vec{OC}=\tfrac{3}{5}\vec{OA}+\tfrac{2}{5}\vec{OB}"
            r"=\left(\tfrac{3a}{5},\tfrac{2b}{5}\right)"
        ).scale(0.75).next_to(setup, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(oc))
        self.wait(0.5)

        d1 = MathTex(r"3\vec{AD}=8\vec{BD}").scale(0.75)
        d2 = MathTex(r"3(D-A)=8(D-B)").scale(0.75)
        d3 = MathTex(r"5D=8B-3A").scale(0.75)
        d4 = MathTex(r"\vec{OD}=\left(-\tfrac{3a}{5},\tfrac{8b}{5}\right)").scale(0.75)
        dgroup = VGroup(d1, d2, d3, d4).arrange(DOWN, aligned_edge=LEFT).next_to(oc, DOWN, buff=0.35).to_edge(LEFT)
        for d in dgroup:
            self.play(Write(d))
            self.wait(0.3)
        self.wait(0.5)

        self.play(
            FadeOut(setup), FadeOut(oc),
            FadeOut(d1), FadeOut(d2), FadeOut(d3),
            d4.animate.scale(1.0).next_to(title, DOWN, buff=0.4).to_edge(LEFT),
        )

        perp = VGroup(
            MathTex(r"\vec{OC}\perp\vec{OD}\ \Rightarrow\ \vec{OC}\cdot\vec{OD}=0").scale(0.75),
            MathTex(r"\frac{3a}{5}\cdot\left(-\frac{3a}{5}\right)"
                    r"+\frac{2b}{5}\cdot\frac{8b}{5}=0").scale(0.75),
            MathTex(r"-\frac{9a^2}{25}+\frac{16b^2}{25}=0").scale(0.75),
            MathTex(r"16b^2=9a^2").scale(0.75),
            MathTex(r"\frac{b^2}{a^2}=\frac{9}{16}").scale(0.8),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(d4, DOWN, buff=0.35).to_edge(LEFT)
        for p in perp:
            self.play(Write(p))
            self.wait(0.3)
        self.wait(0.5)

        answer = MathTex(
            r"\frac{\lvert \vec{OB} \rvert}{\lvert \vec{OA} \rvert}=\frac{b}{a}=\frac{3}{4}",
            color=YELLOW,
        ).scale(1.0).to_edge(DOWN, buff=0.6)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        self.play(Write(answer), Create(box))
        self.wait(2)