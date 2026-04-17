# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個 PiCreature 角色介紹兩個主題（主要主題和元主題），並分別用數學方程式和文字說明來闡述它們。



from manim import *
class IntroSceneWrapper(PiCreatureScene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": YELLOW_E,
            "flip_at_start": False,
            "height": 2,
        },
        default_pi_creature_start_corner=DOWN + LEFT,
        **kwargs
    ):
        super().__init__(
            default_pi_creature_kwargs=default_pi_creature_kwargs,
            default_pi_creature_start_corner=default_pi_creature_start_corner,
            **kwargs
        )

    def construct(self):
        self.introduce_two_words()
        self.describe_main_topic()
        self.describe_meta_topic()

    def introduce_two_words(self):
        morty = self.pi_creature
        rect = ScreenRectangle(height=5)
        rect.to_corner(UP + RIGHT)
        self.add(rect)

        h_line = Line(LEFT, RIGHT).scale(2)
        h_line.to_corner(UP + LEFT)
        h_line.shift(0.5 * DOWN)

        main_topic, meta_topic = topics = VGroup(
            Text("Main topic"),
            Text("Meta topic"),
        )
        topics.next_to(morty, UP)
        topics.shift_onto_screen()

        self.play(
            morty.change, "raise_left_hand",
            FadeIn(main_topic, shift=DOWN)
        )
        self.wait()
        self.play(
            morty.change, "raise_right_hand",
            main_topic.next_to, meta_topic.get_top(), UP, MED_SMALL_BUFF,
            FadeIn(meta_topic, shift=DOWN)
        )
        self.wait()
        self.play(
            morty.change, "happy",
            main_topic.next_to, h_line, UP,
            meta_topic.set_fill, {"opacity": 0.2},
        )
        self.play(Create(h_line))
        self.wait()

        self.h_line = h_line
        self.main_topic = main_topic
        self.meta_topic = meta_topic

    def describe_main_topic(self):
        h_line = self.h_line
        morty = self.pi_creature
        main_topic = self.main_topic
        meta_topic = self.meta_topic

        solver = Text("2d equation solver")
        solver.match_width(h_line)
        solver.next_to(h_line, DOWN)
        rainbow_solver1 = solver.copy()
        rainbow_solver2 = solver.copy()
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        rainbow_solver1.set_color_by_gradient(*colors)
        rainbow_solver2.set_color_by_gradient(*reversed(colors))

        xy_equation = MathTex(r"""
            \left[\begin{array}{c}
                ye^x \\
                \sin(|xy|)
            \end{array}\right] = 
            \left[\begin{array}{c}
                y^2 \\
                3y
            \end{array}\right]
        """)
        xy_equation.scale(0.8)
        xy_equation.next_to(solver, DOWN, MED_LARGE_BUFF)

        z_equation = MathTex("z", "^5", "+", "z", "+", "1", "=", "0")
        z_equation.set_color_by_tex("z", GREEN)
        z_equation.move_to(xy_equation, UP)

        zeta = MathTex(r"\zeta(s) = 0")
        zeta[2].set_color(GREEN)
        zeta.next_to(z_equation, DOWN, MED_LARGE_BUFF)

        self.play(Write(solver))
        self.play(
            LaggedStartMap(FadeIn, xy_equation, run_time=1),
            morty.change, "pondering"
        )
        self.wait(2)
        self.play(
            FadeOut(xy_equation),
            FadeIn(z_equation)
        )
        self.wait()
        self.play(Write(zeta))
        self.wait()
        solver.save_state()
        for rainbow_solver in rainbow_solver1, rainbow_solver2:
            self.play(Transform(
                solver, rainbow_solver,
                run_time=2,
                lag_ratio=0.5
            ))
        self.play(solver.restore)
        self.wait()

        self.play(LaggedStartMap(
            FadeOut, VGroup(solver, z_equation, zeta)
        ))
        self.play(
            main_topic.move_to, meta_topic,
            main_topic.set_fill, {"opacity": 0.2},
            meta_topic.move_to, main_topic,
            meta_topic.set_fill, {"opacity": 1},
            morty.change, "hesitant",
            path_arc=TAU / 8,
        )

    def describe_meta_topic(self):
        h_line = self.h_line
        morty = self.pi_creature

        words = Text("Seek constructs which\ncompose nicely")
        words.scale(0.7)
        words.next_to(h_line, DOWN)

        self.play(Write(words))
        self.play(morty.change, "happy")
        self.wait(3)
