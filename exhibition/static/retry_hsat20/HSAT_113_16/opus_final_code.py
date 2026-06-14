from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("向量正射影問題", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            VGroup(
                Text("在 (2,-3) 方向正射影長 =", font_size=26),
                MathTex(r"r-1").scale(0.7),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("在 (3,2) 方向正射影長 =", font_size=26),
                MathTex(r"r-2").scale(0.7),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                MathTex(r"r=|\vec{v}|,").scale(0.7),
                Text("兩夾角皆銳角", font_size=26),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        setup.next_to(title, DOWN, buff=0.5)
        for line in setup:
            self.play(Write(line))
        self.wait(0.5)

        key = MathTex(
            r"(2,-3)\perp(3,2),\quad |(2,-3)|=|(3,2)|=\sqrt{13}"
        ).scale(0.7)
        key.next_to(setup, DOWN, buff=0.35)
        self.play(Write(key))
        self.wait(0.5)

        ortho = MathTex(r"(r-1)^2+(r-2)^2=r^2").scale(0.85)
        ortho.next_to(key, DOWN, buff=0.35)
        self.play(Write(ortho))
        self.wait(0.5)

        self.play(FadeOut(setup), FadeOut(key))

        solve = VGroup(
            MathTex(r"2r^2-6r+5=r^2"),
            MathTex(r"r^2-6r+5=0"),
            VGroup(
                MathTex(r"(r-1)(r-5)=0 \Rightarrow r=1"),
                Text("或", font_size=24),
                MathTex(r"r=5"),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                MathTex(r"r=1 \Rightarrow r-2=-1<0"),
                Text("(非銳角)", font_size=24),
            ).arrange(RIGHT, buff=0.2),
            MathTex(r"\therefore r=5,\quad p_1=4,\ p_2=3"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.75)
        solve.next_to(ortho, DOWN, buff=0.35)
        for line in solve:
            self.play(Write(line))
        self.wait(0.5)

        self.play(FadeOut(ortho), FadeOut(solve))

        vform = VGroup(
            MathTex(r"\vec{v}=4\cdot\frac{(2,-3)}{\sqrt{13} }+3\cdot\frac{(3,2)}{\sqrt{13} }"),
            MathTex(r"\vec{v}=\frac{(17,-6)}{\sqrt{13} },\quad |\vec{v}|=5"),
        ).arrange(DOWN, buff=0.4).scale(0.8)
        vform.next_to(title, DOWN, buff=0.6)
        for line in vform:
            self.play(Write(line))
        self.wait(0.5)

        proj = VGroup(
            MathTex(r"\text{proj}_{(4,7)}=\frac{\vec{v}\cdot(4,7)}{\sqrt{65} }"),
            MathTex(r"\vec{v}\cdot(4,7)=\frac{68-42}{\sqrt{13} }=\frac{26}{\sqrt{13} }"),
            MathTex(r"=\frac{26}{\sqrt{13}\cdot\sqrt{65} }=\frac{26}{13\sqrt{5} }"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.75)
        proj.next_to(vform, DOWN, buff=0.45)
        for line in proj:
            self.play(Write(line))
        self.wait(0.5)

        answer = MathTex(r"=\frac{2\sqrt{5} }{5}", color=YELLOW).scale(1.1)
        answer.next_to(proj, DOWN, buff=0.35)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        self.play(Write(answer), Create(box))
        self.wait(2)