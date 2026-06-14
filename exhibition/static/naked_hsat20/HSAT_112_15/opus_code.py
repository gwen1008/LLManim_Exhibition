from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title(r"向量垂直問題", font_size=40)
        self.play(Write(title))
        self.wait(0.5)

        setup = VGroup(
            MathTex(r"\overrightarrow{OA} \perp \overrightarrow{OB}"),
            MathTex(r"O=(0,0),\ A=(a,0),\ B=(0,b)"),
        ).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.5)

        self.play(Write(setup[0]))
        self.wait(0.3)
        self.play(Write(setup[1]))
        self.wait(0.6)
        self.play(FadeOut(setup), FadeOut(title))

        # Step 1: C
        s1 = MathTex(
            r"\overrightarrow{OC}=\tfrac{3}{5}\overrightarrow{OA}+\tfrac{2}{5}\overrightarrow{OB}",
        ).to_edge(UP)
        c_val = MathTex(r"C=\left(\tfrac{3a}{5},\ \tfrac{2b}{5}\right)").next_to(s1, DOWN, buff=0.5)
        self.play(Write(s1))
        self.wait(0.3)
        self.play(Write(c_val))
        self.wait(0.6)

        # Step 2: D from 3AD = 8BD
        s2 = MathTex(r"3\overrightarrow{AD}=8\overrightarrow{BD}").next_to(c_val, DOWN, buff=0.6)
        d1 = MathTex(r"3(D-A)=8(D-B)").next_to(s2, DOWN, buff=0.4)
        d2 = MathTex(r"-5D=3A-8B").next_to(d1, DOWN, buff=0.4)
        d3 = MathTex(r"D=\left(-\tfrac{3a}{5},\ \tfrac{8b}{5}\right)").next_to(d2, DOWN, buff=0.4)
        self.play(Write(s2))
        self.wait(0.3)
        self.play(Write(d1))
        self.play(TransformMatchingShapes(d1.copy(), d2))
        self.wait(0.3)
        self.play(Write(d3))
        self.wait(0.6)

        self.play(
            FadeOut(VGroup(s1, c_val, s2, d1, d2)),
            d3.animate.to_edge(UP),
        )
        c_keep = MathTex(r"C=\left(\tfrac{3a}{5},\ \tfrac{2b}{5}\right)").next_to(d3, DOWN, buff=0.4)
        self.play(Write(c_keep))
        self.wait(0.4)

        # Step 3: OC ⊥ OD  => C·D = 0
        perp = MathTex(r"\overrightarrow{OC}\perp\overrightarrow{OD}\ \Rightarrow\ C\cdot D=0").next_to(c_keep, DOWN, buff=0.5)
        eq1 = MathTex(r"\left(\tfrac{3a}{5}\right)\left(-\tfrac{3a}{5}\right)+\left(\tfrac{2b}{5}\right)\left(\tfrac{8b}{5}\right)=0").next_to(perp, DOWN, buff=0.4)
        eq2 = MathTex(r"-\tfrac{9a^2}{25}+\tfrac{16b^2}{25}=0").next_to(eq1, DOWN, buff=0.4)
        eq3 = MathTex(r"16b^2=9a^2").next_to(eq2, DOWN, buff=0.4)
        eq4 = MathTex(r"\frac{b^2}{a^2}=\frac{9}{16}").next_to(eq3, DOWN, buff=0.4)

        self.play(Write(perp))
        self.wait(0.3)
        self.play(Write(eq1))
        self.wait(0.3)
        self.play(Write(eq2))
        self.play(Write(eq3))
        self.play(Write(eq4))
        self.wait(0.5)

        self.play(
            FadeOut(VGroup(d3, c_keep, perp, eq1, eq2, eq3)),
            eq4.animate.move_to(UP * 1.5),
        )

        result = MathTex(
            r"\frac{\overline{OB}}{\overline{OA}}=\frac{b}{a}=\frac{3}{4}",
            font_size=56,
        ).set_color(YELLOW)
        box = SurroundingRectangle(result, color=YELLOW, buff=0.3)
        self.play(Write(result))
        self.play(Create(box))
        self.wait(2)