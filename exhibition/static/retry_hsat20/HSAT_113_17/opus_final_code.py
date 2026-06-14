from manim import *
import numpy as np


class GeneratedScene(Scene):
    def construct(self):
        scale = 3.6
        base = np.array([-6.0, -2.6, 0.0])

        def p(x, y):
            return base + np.array([x * scale, y * scale, 0.0])

        # ---------- Title ----------
        title = Text("圓全落在正方形內的圓心區域 R", font_size=34)
        title.to_edge(UP)
        underline = Line(title.get_left(), title.get_right(),
                         color=WHITE).next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(underline))
        self.wait(0.5)

        # ---------- Square ----------
        square = Polygon(
            p(0, 0), p(0, 1), p(1, 1), p(1, 0),
            color=BLUE, stroke_width=4
        )
        labels = VGroup(
            MathTex("O").next_to(p(0, 0), DL, buff=0.12),
            MathTex("A").next_to(p(0, 1), UL, buff=0.12),
            MathTex("B").next_to(p(1, 1), UR, buff=0.12),
            MathTex("C").next_to(p(1, 0), DR, buff=0.12),
        )
        self.play(Create(square), Write(labels))
        self.wait(0.4)

        # ---------- Setup text ----------
        s1 = VGroup(MathTex("P(x,y)"), Text("為圓心", font_size=26)).arrange(RIGHT, buff=0.15)
        s2 = MathTex(r"r=|x-y|").scale(0.8)
        s3 = Text("要求：圓完全落在正方形內", font_size=26)
        setup = VGroup(s1, s2, s3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        setup.to_corner(UR).shift(DOWN * 0.6)
        self.play(Write(setup))
        self.wait(0.5)

        # ---------- Failing example ----------
        Pf = (0.8, 0.2)
        rf = abs(Pf[0] - Pf[1])
        dotf = Dot(p(*Pf), color=YELLOW)
        cf = Circle(radius=rf * scale, color=RED).move_to(p(*Pf))
        labf = MathTex(r"P=(0.8,\,0.2),\ r=0.6", color=RED).scale(0.7)
        labf.next_to(setup, DOWN, buff=0.5).align_to(setup, LEFT)
        self.play(FadeIn(dotf), Create(cf), Write(labf))
        cross = Cross(scale_factor=0.4).move_to(p(*Pf))
        self.play(Create(cross))
        self.wait(0.6)
        self.play(FadeOut(dotf), FadeOut(cf), FadeOut(cross), FadeOut(labf))

        # ---------- Passing example ----------
        Pg = (0.6, 0.4)
        rg = abs(Pg[0] - Pg[1])
        dotg = Dot(p(*Pg), color=GREEN)
        cg = Circle(radius=rg * scale, color=GREEN).move_to(p(*Pg))
        labg = MathTex(r"P=(0.6,\,0.4),\ r=0.2\ \checkmark", color=GREEN).scale(0.7)
        labg.next_to(setup, DOWN, buff=0.5).align_to(setup, LEFT)
        self.play(FadeIn(dotg), Create(cg), Write(labg))
        self.wait(0.6)
        self.play(FadeOut(dotg), FadeOut(cg), FadeOut(labg), FadeOut(setup))

        # ---------- Conditions ----------
        cond_title = VGroup(
            Text("圓心到四邊距離", font_size=26),
            MathTex(r"\geq |x-y|").scale(0.8),
        ).arrange(RIGHT, buff=0.15)
        conds = VGroup(
            MathTex(r"x \ge |x-y|"),
            MathTex(r"1-x \ge |x-y|"),
            MathTex(r"y \ge |x-y|"),
            MathTex(r"1-y \ge |x-y|"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.85)
        block = VGroup(cond_title, conds).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        block.to_corner(UR).shift(DOWN * 0.4)
        self.play(Write(cond_title))
        self.play(LaggedStart(*[Write(c) for c in conds], lag_ratio=0.3))
        self.wait(0.5)

        simplify = VGroup(
            MathTex(r"\Rightarrow\ y\le x\le 2y,\ \ 2x-y\le 1").scale(0.75),
            Text("（及對稱）", font_size=22),
        ).arrange(RIGHT, buff=0.15)
        simplify.next_to(block, DOWN, buff=0.5).align_to(block, LEFT)
        self.play(Write(simplify))
        self.wait(0.6)
        self.play(FadeOut(block), FadeOut(simplify))

        # ---------- Region R (rhombus) ----------
        v0 = p(0, 0)
        v1 = p(2 / 3, 1 / 3)
        v2 = p(1, 1)
        v3 = p(1 / 3, 2 / 3)
        rhombus = Polygon(v0, v1, v2, v3, color=ORANGE,
                          fill_opacity=0.5, stroke_width=3)
        diag = DashedLine(p(0, 0), p(1, 1), color=GRAY)
        self.play(Create(diag))
        self.play(DrawBorderThenFill(rhombus))

        vdots = VGroup(
            MathTex("O").next_to(v0, DL, buff=0.1).scale(0.7),
            MathTex(r"\left(\tfrac{2}{3},\tfrac{1}{3}\right)").next_to(v1, DR, buff=0.1).scale(0.6),
            MathTex(r"\left(\tfrac{1}{3},\tfrac{2}{3}\right)").next_to(v3, UL, buff=0.1).scale(0.6),
        )
        self.play(Write(vdots))
        self.wait(0.5)

        # ---------- Area computation ----------
        comp = VGroup(
            Text("R 為菱形（風箏形）", font_size=26),
            MathTex(r"d_1 = |OB| = \sqrt 2").scale(0.78),
            MathTex(r"d_2 = \tfrac{\sqrt 2}{3}").scale(0.78),
            VGroup(
                Text("面積", font_size=24),
                MathTex(r"= \tfrac{1}{2}\,d_1 d_2 = \tfrac{1}{2}\cdot\sqrt 2\cdot\tfrac{\sqrt 2}{3}").scale(0.7),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        comp.to_corner(UR).shift(DOWN * 0.4)
        self.play(Write(comp))
        self.wait(0.5)

        answer = VGroup(
            Text("面積", font_size=30, color=YELLOW),
            MathTex(r"= \dfrac{1}{3}", color=YELLOW).scale(1.1),
        ).arrange(RIGHT, buff=0.15)
        box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        ans_group = VGroup(answer, box)
        ans_group.next_to(comp, DOWN, buff=0.6)
        self.play(Write(answer), Create(box))
        self.wait(2)