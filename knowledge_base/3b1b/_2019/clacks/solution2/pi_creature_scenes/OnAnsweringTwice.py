# Source: 3b1b/_2019/clacks/solution2/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師與學生討論問題的場景，包含對話泡泡、文字移動和學生表情變化。



from manim import *
class OnAnsweringTwice(TeacherStudentsScene):
    def construct(self):
        question = MathTex(r"\text{Why }\pi?")
        question.move_to(self.screen)
        question.to_edge(UP)
        other_questions = VGroup(
            MathTex(r"\text{Frequency of collisions?}"),
            MathTex(r"\text{Efficient simulation?}"),
            MathTex(r"\text{Time until last collision?}"),
        )
        for mob in other_questions:
            mob.move_to(self.hold_up_spot, DOWN)

        self.add(question)

        self.student_says(
            "But we already \\\\ solved it",
            bubble_config={"direction": LEFT},
            target_mode="raise_left_hand",
            added_anims=[self.teacher.change, "thinking"]
        )
        self.play_student_changes("sassy", "angry")
        self.wait()
        self.play(
            RemovePiCreatureBubble(self.students[2]),
            self.change_students("erm", "erm"),
            question.animate.move_to(self.hold_up_spot, DOWN).rotate(-90 * DEGREES),
            self.teacher.change("raise_right_hand"),
        )
        shown_questions = VGroup(question)
        for oq in other_questions:
            self.play(
                shown_questions.animate.shift(0.85 * UP),
                FadeIn(oq, shift=DOWN),
                self.change_students(
                    *["pondering"] * 3,
                    look_at=oq
                )
            )
            shown_questions.add(oq)
        self.wait(3)
