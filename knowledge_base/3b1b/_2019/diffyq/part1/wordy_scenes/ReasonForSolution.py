# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示從微分方程到解的理解與計算兩個路徑的視覺化流程，並切換到第二個例子說明直接從方程到理解與計算的可能性。



from manim import *
class ReasonForSolution(Scene):
    def construct(self):
        # Words
        eq_word = Text("Differential\nEquation")
        s_word = Text("Solution")
        u_word = Text("Understanding")
        c_word = Text("Computation")
        cu_group = VGroup(u_word, c_word)
        cu_group.arrange(DOWN, buff=2)
        group = VGroup(eq_word, s_word, cu_group)
        group.arrange(RIGHT, buff=2)

        # Arrows
        arrows = VGroup(
            Arrow(eq_word.get_right(), s_word.get_left()),
            Arrow(s_word.get_right(), u_word.get_left()),
            Arrow(s_word.get_right(), c_word.get_left()),
        )
        arrows.set_color(GREY_B)
        new_arrows = VGroup(
            Arrow(
                eq_word.get_corner(UR),
                u_word.get_left(),
                path_arc=-60 * DEGREES,
            ),
            Arrow(
                eq_word.get_corner(DR),
                c_word.get_left(),
                path_arc=60 * DEGREES,
            ),
        )
        new_arrows.set_color(BLUE)

        # Define first examples
        t2c = {
            "{x}": BLUE,
            "{\\dot x}": RED,
        }
        equation = MathTex(
            "{\\dot x}(t) = k {x}(t)",
            tex_to_color_map=t2c,
        )
        equation.next_to(eq_word, DOWN)
        solution = MathTex(
            "{x}(t) = x_0 e^{kt}",
            tex_to_color_map=t2c,
        )
        solution.next_to(s_word, DOWN, buff=MED_LARGE_BUFF)
        equation.align_to(solution, DOWN)

        axes = Axes(
            x_range=[-1, 5.5, 1],
            y_range=[-1, 4.5, 1],
            y_length=2.25,
        )
        axes.set_stroke(width=2)
        graph_line = axes.plot(
            lambda x: np.exp(0.4 * x)
        )
        graph_line.set_stroke(width=2)
        graph = VGroup(axes, graph_line)
        graph.scale(0.5)
        graph.next_to(u_word, UP)

        computation = MathTex(
            "e^x = \\sum_{n=0}^\\infty "
            "\\frac{x^n}{n!}"
        )
        computation.next_to(c_word, DOWN)

        first_examples = VGroup(
            equation, solution, graph, computation
        )

        # Second example
        ode = MathTex(
            "\\frac{d^2 x}{dt^2} + \\omega^2 x = 0"
        )
        ode.scale(0.75)
        second_examples = VGroup(
            ode,
            MathTex("???").set_color(GREY_B),
            ScreenRectangle(
                height=2,
                stroke_width=1,
            ),
        )
        for fe, se in zip(first_examples, second_examples):
            se.move_to(fe, DOWN)

        ode.shift(2 * SMALL_BUFF * DOWN)
        ode.add_to_back(BackgroundRectangle(ode[-4:]))

        self.add(eq_word)
        self.add(equation)
        self.play(
            FadeIn(s_word, shift=LEFT),
            GrowArrow(arrows[0]),
            TransformFromCopy(equation, solution)
        )
        self.wait()
        self.play(
            FadeIn(c_word, shift=UL),
            GrowArrow(arrows[2]),
            FadeIn(computation, shift=UP)
        )
        self.wait()
        self.play(
            FadeIn(u_word, shift=DL),
            GrowArrow(arrows[1]),
            FadeIn(graph, shift=DOWN)
        )
        self.wait(2)

        self.play(
            FadeOut(first_examples),
            FadeIn(second_examples[:2])
        )
        self.wait()
        self.play(
            arrows.animate.set_opacity(0.25),
            s_word.animate.set_opacity(0.25),
            second_examples[1].animate.set_opacity(0.25),
            Create(new_arrows[0]),
            FadeIn(second_examples[2])
        )
        self.play(
            Create(new_arrows[1]),
            Animation(second_examples),
        )
        self.wait()
