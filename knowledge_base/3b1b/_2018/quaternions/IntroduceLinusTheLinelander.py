# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示一個名為 Linus 的角色從登場、觀察實數軸到困惑地看向複數平面的動畫過程。


from manim import *
import random

class IntroduceLinusTheLinelander(Scene):
    def construct(self):
        self.introduce_linus()
        self.show_real_number_line()
        self.look_at_complex_plane()

    def introduce_linus(self):
        linus = Linus()
        linus.move_to(3 * LEFT)
        name = Text("Linus the Linelander")
        name.next_to(linus, DR, buff=MED_LARGE_BUFF)
        arrow = Arrow(name.get_top(), linus.get_right())

        self.play(FadeIn(linus, shift=DOWN))
        self.play(
            Write(name),
            GrowArrow(arrow),
            linus.change, "gracious", name,
        )
        self.play(
            linus.become_squiggle, {"factor": -0.1},
        )
        self.play(Blink(linus))
        self.wait()

        self.name_text = name
        self.name_arrow = arrow
        self.linus = linus

    def show_real_number_line(self):
        linus = self.linus
        number_line = NumberLine()
        number_line.add_numbers()
        number_line.to_edge(UP)

        algebra = VGroup(
            MathTex("3 \\cdot 4 = 12"),
            MathTex("3 + 4 = 7"),
            MathTex("(-2) \\cdot 3 = -6"),
        )
        algebra.arrange(DOWN)
        algebra.next_to(number_line, DOWN, LARGE_BUFF)
        algebra.shift(3 * RIGHT)

        self.play(
            Create(number_line),
            linus.look_at, number_line
        )
        self.play(
            LaggedStartMap(FadeIn, number_line.numbers, shift=DOWN),
            LaggedStartMap(Create, number_line.tick_marks),
            linus.change, "happy"
        )
        self.play(
            LaggedStartMap(FadeIn, algebra, shift=DOWN),
            linus.look_at, algebra
        )
        self.play(Blink(linus))
        self.wait()

        self.algebra = algebra

    def look_at_complex_plane(self):
        linus = self.linus
        to_fade = VGroup(
            self.name_text,
            self.name_arrow,
            self.algebra,
        )
        frame = ScreenRectangle()
        frame.set_width(8)
        frame.to_corner(DR)

        q_marks = VGroup(*[
            MathTex("?").shift(
                random.random() * RIGHT,
                random.random() * UP,
            )
            for x in range(50)
        ])
        q_marks.next_to(linus.body, UP, buff=0)
        q_marks.set_color_by_gradient(BLUE, GREEN, YELLOW)
        random.shuffle(q_marks.submobjects)
        q_marks_anim = LaggedStartMap(
            FadeIn, q_marks,
            run_time=15,
            rate_func=there_and_back,
            lag_ratio=0.1
        )
        q_marks_continual = self.turn_animation_into_updater(q_marks_anim)

        self.play(
            FadeOut(to_fade),
            Create(frame),
            linus.look_at, frame
        )
        self.add(q_marks_continual)
        self.play(linus.change_mode, "confused")
        self.wait()
        self.play(Blink(linus))
        self.play(linus.change, "confused", frame.get_bottom())
        self.wait()
        self.play(linus.change, "sad", frame.get_center())
        self.wait(10)
    
    def turn_animation_into_updater(self, animation):
        # 創建一個持續運行的動畫更新器
        mobject = animation.mobject
        animation.suspend_mobject_updating = False
        animation.begin()
        def update(mob, dt):
            animation.interpolate(dt)
        mobject.add_updater(update)
        return mobject
