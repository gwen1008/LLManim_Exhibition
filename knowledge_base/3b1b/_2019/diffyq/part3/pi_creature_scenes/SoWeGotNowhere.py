# Source: 3b1b/_2019/diffyq/part3/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師和學生在課堂上的互動，學生表達不滿，老師回應並展示數學公式。



from manim import *
class SoWeGotNowhere(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "So we've gotten\\\\nowhere!",
            target_mode="angry",
            added_anims=[
                self.teacher.change, "guilty"
            ]
        )
        self.play_all_student_changes("angry")
        self.wait()
        text = MathTex(
            "&\\text{Actually,}\\\\",
            "&\\sin\\left({x}\\right)"
            "e^{-\\alpha {t}}\\\\",
            "&\\text{isn't far off.}",
            tex_to_color_map={
                "{x}": GREEN,
                "{t}": YELLOW,
            }
        )
        text.scale(0.8)
        self.teacher_says(
            text,
            content_introduction_class=FadeIn,
            bubble_config={
                "width": 4,
                "height": 3.5,
            }
        )
        self.play_all_student_changes(
            "pondering",
            look_at=self.screen
        )
        self.wait(3)
