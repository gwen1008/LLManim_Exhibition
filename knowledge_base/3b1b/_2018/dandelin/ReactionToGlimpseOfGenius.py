# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 老師展示燈泡圖示，學生們從困惑到領悟，最後每個學生頭上都出現小燈泡，象徵靈感閃現。



from manim import *
class ReactionToGlimpseOfGenius(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher

        lightbulb = Lightbulb()
        lightbulb.set_stroke(width=4)
        lightbulb.scale(1.5)
        lightbulb.move_to(self.hold_up_spot, DOWN)

        # 註: ManimCE 沒有 get_rings 方法，用替代方案
        # rings = self.get_rings(
        #     lightbulb.get_center(),
        #     max_radius=15,
        #     delta_r=0.1,
        # )

        arrow = Arrow(start=LEFT, end=RIGHT, color=WHITE)
        arrow.next_to(lightbulb, LEFT)

        clock = Clock()
        clock.next_to(arrow, LEFT)

        pi_lights = VGroup()
        for pi in self.students:
            light = Lightbulb()
            light.scale(0.75)
            light.next_to(pi, UP)
            pi.light = light
            pi_lights.add(light)

        q_marks = VGroup()
        for submob in lightbulb:
            q_mark = MathTex("?")
            q_mark.move_to(submob)
            q_marks.add(q_mark)
        q_marks.space_out_submobjects(2)

        self.student_says(
            "I think Lockhart was \\\\"
            "speaking more generally.",
            target_mode="sassy",
            added_anims=[morty.change, "guilty"]
        )
        self.wait(2)
        self.play(
            morty.change("raise_right_hand"),
            FadeIn(lightbulb, shift=DOWN),
            FadeOut(self.students[1].bubble),
            self.change_students(*3 * ["confused"]),
            run_time=1
        )
        self.play(Transform(
            lightbulb, q_marks,
            run_time=3,
            rate_func=there_and_back_with_pause,
            lag_ratio=0.5
        ))
        # 註: ManimCE 沒有 ClockPassesTime 動畫，用替代方案
        self.play(
            clock.animate.set_value(4/12),  # 模擬4小時
            FadeIn(clock),
            GrowArrow(arrow),
            self.change_students(
                *3 * ["pondering"],
                look_at=clock
            ),
            run_time=4
        )
        self.play(
            clock.animate.set_value(5/12),  # 再過1小時
            FadeOut(clock),
            FadeOut(arrow),
            lightbulb.animate.scale(1.5).move_to(2 * UP),
            self.change_students(
                *3 * ["awe"],
                look_at=2 * UP
            ),
            run_time=1
        )
        # 註: ManimCE 沒有 get_light_shine 方法，用閃爍效果替代
        self.play(
            lightbulb.animate.set_fill(YELLOW, opacity=1),
            Flash(lightbulb, color=YELLOW, line_length=0.3, num_lines=12),
            run_time=1
        )
        self.play(
            ReplacementTransform(
                VGroup(lightbulb),
                pi_lights
            ),
            morty.change("happy"),
            *[
                pi.animate.change(mode, pi.get_top())
                for pi, mode in zip(self.students, [
                    "hooray", "tease", "surprised"
                ])
            ]
        )
        self.wait(3)
