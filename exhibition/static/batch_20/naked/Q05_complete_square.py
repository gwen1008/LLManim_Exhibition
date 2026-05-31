from manim import *

class GeneratedScene(Scene):
    def construct(self):
        title = Text("配方法：化為頂點式", font="PingFang TC").to_edge(UP)
        self.play(Write(title))

        eq1 = MathTex("y = x^2 - 6x + 5").scale(1.1)
        eq2 = MathTex("y = (x^2 - 6x + 9) - 9 + 5").scale(1.1)
        eq3 = MathTex("y = (x - 3)^2 - 4").scale(1.1)

        for e in (eq1, eq2, eq3):
            e.next_to(title, DOWN, buff=0.6)

        self.play(Write(eq1))
        self.wait(0.8)

        note = MathTex(r"\left(\tfrac{-6}{2}\right)^2 = 9", color=YELLOW).scale(0.9)
        note.next_to(eq1, DOWN, buff=0.5)
        self.play(FadeIn(note, shift=DOWN))
        self.wait(0.6)

        self.play(Transform(eq1, eq2))
        self.wait(0.8)
        self.play(Transform(eq1, eq3), FadeOut(note))
        self.wait(0.6)

        self.play(eq1.animate.scale(0.7).to_corner(UR))

        axes = Axes(
            x_range=[-1, 7, 1],
            y_range=[-5, 6, 1],
            x_length=7,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 20},
        ).to_edge(DL, buff=0.6)

        f = lambda x: x**2 - 6*x + 5
        g = lambda x: (x - 3)**2 - 4

        graph_orig = axes.plot(f, x_range=[0.2, 5.8], color=BLUE)
        graph_orig_label = MathTex("x^2-6x+5", color=BLUE).scale(0.6).next_to(axes.c2p(0.5, 5), RIGHT)

        self.play(Create(axes))
        self.play(Create(graph_orig), FadeIn(graph_orig_label))
        self.wait(0.5)

        vertex_orig = Dot(axes.c2p(3, -4), color=RED)
        vtx_label = MathTex("(3,-4)", color=RED).scale(0.6).next_to(vertex_orig, DR, buff=0.1)
        self.play(FadeIn(vertex_orig), Write(vtx_label))
        self.wait(0.4)

        axis_sym = DashedLine(axes.c2p(3, -5), axes.c2p(3, 6), color=YELLOW)
        sym_label = MathTex("x=3", color=YELLOW).scale(0.6).next_to(axis_sym, UP, buff=0.1)
        self.play(Create(axis_sym), Write(sym_label))
        self.wait(0.6)

        # show shift from parabola y=x^2 vertex (0,0) to (3,-4)
        graph_base = axes.plot(lambda x: x**2, x_range=[-1, 2.5], color=GREY)
        base_vtx = Dot(axes.c2p(0, 0), color=GREEN)
        self.play(Create(graph_base), FadeIn(base_vtx))
        self.wait(0.4)

        shift_vec = Arrow(axes.c2p(0, 0), axes.c2p(3, -4), buff=0.1, color=GREEN)
        shift_lbl = MathTex(r"\to (3,-4)", color=GREEN).scale(0.55).next_to(shift_vec.get_center(), UR, buff=0.05)
        self.play(GrowArrow(shift_vec), Write(shift_lbl))
        self.wait(1.2)

        concl = Text("頂點 (3,-4)，對稱軸 x=3", font="PingFang TC").scale(0.55).to_edge(DOWN)
        self.play(Write(concl))
        self.wait(2)