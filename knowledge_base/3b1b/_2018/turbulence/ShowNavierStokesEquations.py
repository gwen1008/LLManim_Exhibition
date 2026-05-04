# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示納維-斯托克斯方程及其相關概念，包括方程介紹、演化問題、解的存在性問題，以及百萬美元獎金的懸賞問題。



from manim import *
class ShowNavierStokesEquations(Scene):
    def construct(self):
        self.introduce_equations()
        self.ask_about_evolution()
        self.ask_about_reasonable()
        self.ask_about_blowup()
        self.show_money()

    def introduce_equations(self):
        name = Text("Navier-Stokes equations (incompressible)")
        equations = NavierStokesEquations()
        name.to_edge(UP)
        equations.next_to(name, DOWN, buff=MED_LARGE_BUFF)
        labels = equations.get_labels()
        parts = equations.get_parts()
        newtons_second = Text(
            "Newton's 2nd law\n$ma = F$"
        )
        newtons_second.next_to(parts, DOWN)
        variables = MathTex(
            "&\\textbf{v}", "\\text{ is velocity}\\\\",
            "&\\rho", "\\text{ is density}\\\\",
            "&p{}", "\\text{ is pressure}\\\\",
            "&\\mu", "\\text{ is viscosity}\\\\",
            tex_to_color_map=NavierStokesEquations.CONFIG["tex_to_color_map"]
        )
        variables.to_corner(DL)

        self.play(FadeIn(equations, shift=DOWN))
        self.play(Write(name))
        self.play(LaggedStart(*[
            FadeIn(m, shift=RIGHT) for m in variables
        ]))
        self.wait()
        self.play(Write(newtons_second))
        self.wait()
        self.play(
            FadeIn(labels[0], shift=DOWN),
            newtons_second.animate.next_to(variables, RIGHT, buff=LARGE_BUFF)
        )
        self.play(Create(parts[0]), run_time=2)
        self.play(FadeOut(parts[0]))
        self.wait()
        self.play(LaggedStart(*[FadeIn(label, shift=RIGHT) for label in labels[1:]]))
        self.wait(3)
        self.play(LaggedStart(*[
            FadeOut(m) for m in [*labels, variables, newtons_second]
        ]))

        self.equations = equations

    def ask_about_evolution(self):
        words = Text(
            "Given a start state...\n...how does it evolve?"
        )
        words.arrange(RIGHT, buff=2)

        words.next_to(self.equations, DOWN, buff=LARGE_BUFF)

        self.play(Write(words[0]))
        self.wait()
        self.play(Write(words[1]))
        self.wait(2)
        self.play(FadeOut(words))

    def ask_about_reasonable(self):
        question = Text(
            "Do ``reasonable''\n"
            "solutions always\n"
            "exist?"
        )
        self.play(FadeIn(question, shift=DOWN))
        self.wait()

        self.reasonable_question = question

    def ask_about_blowup(self):
        axes, graph = self.get_axes_and_graph()
        question = Text("Is this possible?")
        question.set_color(YELLOW)
        question.move_to(axes.get_corner(UR), LEFT)
        question.align_to(axes, UP)
        q_arrow = Arrow(
            question.get_bottom(),
            graph.point_from_proportion(0.8),
            buff=SMALL_BUFF,
            path_arc=-60 * DEGREES
        )
        q_arrow.set_stroke(WHITE, 3)
        morty = Mortimer()
        morty.to_corner(DR)
        morty.change('confused', graph)

        self.play(
            Write(axes, run_time=1),
            self.reasonable_question.animate.to_edge(LEFT).shift(DOWN),
        )
        self.play(
            Write(question),
            Create(graph),
            FadeIn(morty),
        )
        self.add(q_arrow, morty)
        self.play(Create(q_arrow), Blink(morty))
        self.wait()
        self.play(morty.animate.look_at(question))
        self.wait()
        self.play(morty.change("maybe", graph))
        self.wait(2)
        to_fade = VGroup(question, q_arrow, axes, graph)
        self.play(
            LaggedStart(*[FadeOut(m) for m in to_fade]),
            morty.change("pondering")
        )
        self.wait(2)
        self.play(Blink(morty))
        self.wait(2)

        self.morty = morty

    def show_money(self):
        # Million dollar problem
        problem = Text(
            "Navier-Stokes existence\nand smoothness problems"
        )
        money = Text("\\$1,000,000")
        money.set_color(GREEN)
        money.next_to(problem, DOWN)
        pi1 = Randolph()
        pi2 = self.morty
        pi1.to_corner(DL)
        pis = VGroup(pi1, pi2)
        for pi in pis:
            pi.change("pondering")
            pi.money_eyes = VGroup()
            for eye in pi.eyes:
                cash = MathTex("\\$")
                cash.set_color(GREEN)
                cash.replace(eye, dim_to_match=1)
                pi.money_eyes.add(cash)

        self.play(
            ReplacementTransform(
                self.reasonable_question,
                problem,
            ),
            pi2.animate.look_at(problem),
            pi1.animate.look_at(problem),
            FadeIn(pi1),
        )
        self.wait()
        self.play(FadeIn(money, scale=2))
        self.play(
            pi1.change("hooray"),
            pi2.change("hooray"),
        )
        self.play(
            ReplacementTransform(pi1.pupils, pi1.money_eyes),
            ReplacementTransform(pi2.pupils, pi2.money_eyes),
        )
        self.wait()

    # Helpers
    def get_axes_and_graph(self):
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            axis_config={"include_numbers": False}
        )
        time = Text("Time")
        time.next_to(axes.x_axis, RIGHT)
        ke = Text("Kinetic energy")
        ke.next_to(axes.y_axis, UP)
        axes.add(time, ke)
        axes.set_height(4)
        axes.center()
        axes.to_edge(DOWN)
        v_line = DashedLine(
            axes.c2p(4, 0),
            axes.c2p(4, 5),
        )
        axes.add(v_line)
        graph = axes.plot(
            lambda x: -1.0 / (x - 4),
            x_range=[0.01, 3.8],
        )
        graph.set_color(BLUE)
        return axes, graph


class NavierStokesEquations(VGroup):
    CONFIG = {
        "tex_to_color_map": {
            "\\textbf{v}": BLUE,
            "\\rho": RED,
            "p": YELLOW,
            "\\mu": GREEN,
        }
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 簡化實現：創建方程組
        equation = MathTex(
            "\\rho\\left(\\frac{\\partial \\textbf{v}}{\\partial t}"
            "+ \\textbf{v} \\cdot \\nabla \\textbf{v}\\right)"
            "= -\\nabla p + \\mu \\nabla^2 \\textbf{v}",
            tex_to_color_map=self.CONFIG["tex_to_color_map"]
        )
        self.add(equation)
    
    def get_labels(self):
        # 簡化實現：返回空列表
        return VGroup()
    
    def get_parts(self):
        # 簡化實現：返回方程的不同部分
        return VGroup(*self.submobjects)
