from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Title("正方形內的圓完全內含問題", font_size=40)
        self.play(Write(title))
        self.wait(0.5)

        # coordinate / square setup
        ax = Axes(
            x_range=[0, 1, 0.5],
            y_range=[0, 1, 0.5],
            x_length=4.5,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 22},
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)

        square = Polygon(
            ax.c2p(0, 0), ax.c2p(0, 1), ax.c2p(1, 1), ax.c2p(1, 0),
            color=WHITE, stroke_width=3,
        )
        labels = VGroup(
            MathTex("O").next_to(ax.c2p(0, 0), DL, buff=0.1),
            MathTex("A").next_to(ax.c2p(0, 1), UL, buff=0.1),
            MathTex("B").next_to(ax.c2p(1, 1), UR, buff=0.1),
            MathTex("C").next_to(ax.c2p(1, 0), DR, buff=0.1),
        ).set_color(YELLOW)

        self.play(Create(ax), Create(square), Write(labels))
        self.wait(0.5)

        # show an example point and its circle radius |x-y|
        px, py = 0.35, 0.62
        r = abs(px - py)
        P = Dot(ax.c2p(px, py), color=RED)
        Plabel = MathTex("P(x,y)", font_size=24).next_to(P, UR, buff=0.08)
        circ = Circle(radius=r * ax.x_length, color=BLUE).move_to(ax.c2p(px, py))

        info = MathTex(r"r=|x-y|", font_size=30).next_to(ax, UP, buff=0.2)
        self.play(FadeIn(P), Write(Plabel))
        self.play(Create(circ), Write(info))
        self.wait(0.6)

        # the four conditions
        cond = VGroup(
            MathTex(r"x-r\ge 0"),
            MathTex(r"x+r\le 1"),
            MathTex(r"y-r\ge 0"),
            MathTex(r"y+r\le 1"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.85)
        cond_box = VGroup(
            Text("圓內含於正方形：", font_size=24, color=GREEN),
            cond,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cond_box.to_edge(RIGHT, buff=0.7).shift(UP * 0.6)

        self.play(Write(cond_box[0]))
        self.play(LaggedStart(*[Write(c) for c in cond], lag_ratio=0.3))
        self.wait(0.8)

        # substitute r, assume y>=x  => r=y-x
        sub = VGroup(
            MathTex(r"\text{設 } y\ge x,\ r=y-x", font_size=28, color=ORANGE),
            MathTex(r"x\ge r:\ \ y\le 2x", font_size=28),
            MathTex(r"y+r\le1:\ \ y\le\tfrac{1+x}{2}", font_size=28),
            MathTex(r"\text{其餘自動成立}", font_size=26, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        sub.move_to(cond_box).align_to(cond_box, UP)

        self.play(FadeOut(cond_box), FadeOut(circ), FadeOut(P), FadeOut(Plabel), FadeOut(info))
        self.play(Write(sub))
        self.wait(1)

        # draw region R on the square: union of two symmetric pieces
        def upper_curve(x):
            # y from x up to min(2x, (1+x)/2)
            return min(2 * x, (1 + x) / 2)

        # region (y>=x part): between y=x and upper bound, for x in [0,1]
        upper_pts = [ax.c2p(x, x) for x in np.linspace(0, 1, 60)]
        top_pts = [ax.c2p(x, upper_curve(x)) for x in np.linspace(1, 0, 60)]
        region_upper = Polygon(*upper_pts, *top_pts, color=BLUE, fill_opacity=0.5, stroke_width=0)

        # lower (x>=y) by symmetry: swap roles
        lpts = [ax.c2p(x, x) for x in np.linspace(0, 1, 60)]
        bot_pts = [ax.c2p(upper_curve(y), y) for y in np.linspace(1, 0, 60)]
        region_lower = Polygon(*lpts, *bot_pts, color=BLUE, fill_opacity=0.5, stroke_width=0)

        diag = Line(ax.c2p(0, 0), ax.c2p(1, 1), color=YELLOW, stroke_width=2)
        self.play(Create(diag))
        self.play(FadeIn(region_upper), FadeIn(region_lower))
        Rlabel = MathTex("R", font_size=36, color=BLUE).move_to(ax.c2p(0.4, 0.5))
        self.play(Write(Rlabel))
        self.wait(1)

        # area computation
        self.play(FadeOut(sub))
        calc = VGroup(
            MathTex(r"\text{上半面積}=\int_0^{1/3}\! x\,dx+\int_{1/3}^1\!\tfrac{1-x}{2}\,dx", font_size=26),
            MathTex(r"=\tfrac{1}{18}+\tfrac{1}{9}=\tfrac{1}{6}", font_size=28),
            MathTex(r"\text{對稱：}\ \times 2", font_size=28, color=ORANGE),
            MathTex(r"\boxed{\,\text{面積}(R)=\tfrac{1}{3}\,}", font_size=36, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        calc.to_edge(RIGHT, buff=0.5).shift(UP * 0.2)

        for m in calc:
            self.play(Write(m))
            self.wait(0.4)
        self.wait(2)