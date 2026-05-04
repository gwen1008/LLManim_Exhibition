# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示老師和學生場景中，一個學生手持雷射筆晃動，老師警告要小心雷射的動畫。



from manim import *
class CarefulWithLasers(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        randy = self.students[1]
        randy2 = self.students[2]
        # randy.change('hooray')
        laser = VGroup(
            Rectangle(
                height=0.1,
                width=0.3,
                fill_color=GREY_B,
                fill_opacity=1,
                stroke_color=GREY_D,
                stroke_width=1,
            ),
            Line(ORIGIN, 10 * RIGHT, color=GREEN_SCREEN)
        )
        laser.arrange(RIGHT, buff=0)
        laser.rotate(45 * DEGREES)
        laser.shift(randy.get_corner(UR) - laser[0].get_center() + 0.1 * DR)

        laser.time = 0

        def update_laser(laser, dt):
            laser.time += dt
            laser.rotate(
                0.5 * dt * np.sin(laser.time),
                about_point=laser[0].get_center()
            )
        laser.add_updater(update_laser)

        self.play(LaggedStartMap(
            lambda m: FadeIn(m, shift=DOWN),
            self.pi_creatures,
            run_time=1
        ))
        self.add(self.pi_creatures, laser)
        for pi in self.pi_creatures:
            pi.add_updater(lambda p: p.look_at(laser[1]))
        self.play(
            Create(laser),
            self.change_students(
                "surprised", "hooray", "horrified",
                look_at=laser
            )
        )
        self.teacher_says(
            "Careful with \\\\ the laser!",
            target_mode="angry"
        )
        self.wait(2.2)
        morty.save_state()
        randy2.save_state()
        self.play(
            morty.blink, randy2.blink,
            run_time=0.3
        )
        self.wait(2)
        self.play(
            morty.restore, randy2.restore,
            run_time=0.3
        )
        self.wait(2)
