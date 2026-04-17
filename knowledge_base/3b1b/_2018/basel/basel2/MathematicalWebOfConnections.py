# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示數學中 π 不僅與圓相關，還出現在巴塞爾問題等公式中，並以網絡圖和光效動畫呈現數學概念間的關聯。


from manim import *
import random

class MathematicalWebOfConnections(PiCreatureScene):
    def construct(self):
        self.complain_that_pi_is_not_about_circles()
        self.show_other_pi_formulas()
        self.question_fundamental()
        self.draw_circle()
        self.remove_all_but_basel_sum()
        self.show_web_of_connections()
        self.show_light()

    def complain_that_pi_is_not_about_circles(self):
        jerk, randy = self.pi_creatures

        words = self.words = Text(
            "I am not\nfundamentally\nabout circles",
            t2c={"fundamentally": YELLOW}
        )

        self.play(PiCreatureSays(
            jerk, words,
            target_mode = "angry"
        ))
        self.play(randy.change("guilty"))
        self.wait(2)

    def show_other_pi_formulas(self):
        jerk, randy = self.pi_creatures
        words = self.words

        basel_sum = MathTex(
            "1 + {1 \\over 4} + {1 \\over 9} + {1 \\over 16} + \\cdots", 
            "=", "{\\pi^2 \\over 6}"
        )
        leibniz_sum = MathTex(
            "1-{1\\over 3}+{1\\over 5}-{1\\over 7}+{1\\over 9}-\\cdots",
            "=", "{\\pi \\over 4}")

        wallis_product = MathTex(
            "{2\\over 1} \\cdot {2\\over 3} \\cdot {4\\over 3} \\cdot {4\\over 5}" +
             "\\cdot {6\\over 5} \\cdot {6\\over 7} \\cdots",
             "=", "{\\pi \\over 2}")

        basel_sum.move_to(randy)
        basel_sum.to_edge(UP)
        basel_equals = basel_sum.get_part_by_tex("=")

        formulas = VGroup(basel_sum, leibniz_sum, wallis_product)
        formulas.scale(0.75)
        formulas.arrange(DOWN, buff = MED_LARGE_BUFF)
        for formula in formulas:
            basel_equals_x = basel_equals.get_center()[0]
            formula_equals_x = formula.get_part_by_tex("=").get_center()[0]
            formula.shift((basel_equals_x - formula_equals_x)*RIGHT)

        formulas.to_corner(UP+RIGHT)
        formulas.shift(2*LEFT)
        self.formulas = formulas

        self.play(
            jerk.change("sassy"),
            randy.change("raise_right_hand"),
            FadeOut(jerk.bubble),
            words.animate.next_to(jerk, UP),
            FadeIn(basel_sum, lag_ratio = 0.5, run_time = 3)
        )
        for formula in formulas[1:]:
            self.play(
                FadeIn(
                    formula, 
                    lag_ratio = 0.5, 
                    run_time = 3
                ),
            )
        self.wait()

    def question_fundamental(self):
        jerk, randy = self.pi_creatures
        words = self.words
        fundamentally = words.get_part_by_text("fundamentally")
        words.remove(fundamentally)

        self.play(
            fundamentally.animate.move_to(self.pi_creatures).shift(UP),
            FadeOut(words),
            jerk.change("pondering"),
            randy.change("pondering"),
        )
        self.wait()

        question = Text("Does this mean\nanything?")
        question.scale(0.8)
        question.set_stroke(WHITE, 0.5)
        question.next_to(fundamentally, DOWN, LARGE_BUFF)
        arrow = Arrow(question.get_top(), fundamentally.get_bottom())
        arrow.set_color(WHITE)

        self.play(
            FadeIn(question),
            GrowArrow(arrow)
        )
        self.wait()

        fundamentally.add(question, arrow)
        self.fundamentally = fundamentally

    def draw_circle(self):
        semi_circle = Arc(angle = PI, radius = 2)
        radius = Line(ORIGIN, semi_circle.get_points()[0])
        radius.set_color(BLUE)
        semi_circle.set_color(YELLOW)

        VGroup(radius, semi_circle).move_to(
            config.frame_width/4 * LEFT + config.frame_height/4 * UP,
        )

        decimal = DecimalNumber(0)
        def decimal_position_update_func(decimal):
            decimal.move_to(semi_circle.get_points()[-1])
            decimal.shift(0.3*radius.get_vector())

        one = MathTex("1")
        one.next_to(radius, UP)

        self.play(Create(radius), FadeIn(one))
        self.play(
            Rotate(radius, PI, about_point = radius.get_start()),
            Create(semi_circle),
            ChangeDecimalToValue(
                decimal, PI, 
                position_update_func = decimal_position_update_func
            ),
            one.animate.move_to(radius.get_end() + UP*0.5),
            run_time = 3,
        )
        self.wait(2)

        self.circle_group = VGroup(semi_circle, radius, one, decimal)

    def remove_all_but_basel_sum(self):
        to_shift_down = VGroup(
            self.circle_group, self.pi_creatures,
            self.fundamentally, self.formulas[1:],
        )
        to_shift_down.generate_target()
        for part in to_shift_down.target:
            part.move_to(config.frame_height*DOWN)

        basel_sum = self.formulas[0]

        self.play(
            MoveToTarget(to_shift_down),
            basel_sum.animate.scale(1.5).move_to(1.5*DOWN),
        )

        self.basel_sum = basel_sum

    def show_web_of_connections(self):
        self.remove(self.pi_creatures)
        title = Text("Interconnected web of mathematics")
        title.to_edge(UP)
        basel_sum = self.basel_sum

        dots = VGroup(*[
            Dot(radius = 0.1).move_to(
                (j - 0.5*(i%2))*RIGHT + \
                (np.sqrt(3)/2.0)* i*DOWN + \
                0.5*(random.random()*RIGHT + random.random()*UP),
            )
            for i in range(4)
            for j in range(7+(i%2))
        ])
        dots.set_height(3)
        dots.next_to(title, DOWN, MED_LARGE_BUFF)
        edges = VGroup()
        for x in range(100):
            d1, d2 = random.sample(dots, 2)
            edge = Line(d1.get_center(), d2.get_center())
            edge.set_stroke(YELLOW, 0.5)
            edges.add(edge)

        ## Choose special path
        path_dots = VGroup(
            dots[-7],
            dots[-14],
            dots[9],
            dots[19],
            dots[14],
        )
        path_edges = VGroup(*[
            Line(
                d1.get_center(), d2.get_center(),
                color = RED
            )
            for d1, d2 in zip(path_dots, path_dots[1:])
        ])

        circle = Circle(color = YELLOW, radius = 1)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_color(BLUE)
        VGroup(circle, radius).next_to(path_dots[-1], RIGHT)

        self.play(
            Write(title),
            LaggedStartMap(Create, edges, run_time = 3),
            LaggedStartMap(GrowFromCenter, dots, run_time = 3)
        )
        self.play(path_dots[0].animate.set_color(RED))
        for dot, edge in zip(path_dots[1:], path_edges):
            self.play(
                Create(edge),
                dot.animate.set_color(RED)
            )
        self.play(Create(radius))
        self.play(
            Create(circle),
            Rotate(radius, angle = 0.999*TAU, about_point = radius.get_start()),
            run_time = 2
        )
        self.wait()

        graph = VGroup(dots, edges, path_edges, title)
        circle.add(radius)
        basel_sum.generate_target()
        basel_sum.target.to_edge(UP)

        arrow = Arrow(
            UP, DOWN, 
            stroke_width = 10,
            tip_length = 0.45,
            color = RED,
        )
        arrow.next_to(basel_sum.target, DOWN, buff = MED_LARGE_BUFF)

        self.play(
            MoveToTarget(basel_sum),
            graph.animate.next_to(basel_sum.target, UP, LARGE_BUFF),
            circle.animate.next_to(arrow, DOWN, MED_LARGE_BUFF),
        )
        self.play(GrowArrow(arrow))
        self.wait()

        self.arrow = arrow
        self.circle = circle

    def show_light(self):
        # 在 ManimCE 中，我們用一個發光的圓來模擬光效
        light = Circle(
            radius=13,
            color=WHITE,
            fill_opacity=0.1,
            stroke_width=0
        )
        pi = self.basel_sum[-1][0]
        pi.set_stroke(BLACK, 0.5)
        light.move_to(pi)
        
        # 創建光暈效果
        glow = VGroup()
        for i in range(5):
            glow_circle = Circle(
                radius=13 - i*2,
                color=WHITE,
                fill_opacity=0.05 - i*0.01,
                stroke_width=0
            )
            glow.add(glow_circle)
        glow.move_to(pi)
        
        self.play(
            FadeIn(light),
            FadeIn(glow),
            run_time=3
        )
        self.wait()

    def create_pi_creatures(self):
        jerk = PiCreature(color = GREEN_D)
        randy = Randolph().flip()
        jerk.move_to(0.5*config.frame_width/2 * LEFT).to_edge(DOWN)
        randy.move_to(0.5*config.frame_width/2 * RIGHT).to_edge(DOWN)

        return VGroup(jerk, randy)
