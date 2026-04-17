# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示從考試分數分析轉向問題類型討論，並聚焦於特定題目的動畫過程。



from manim import *
class AskWhatsOnTest(ShowTest, MovingCameraScene):
    def construct(self):
        self.force_skipping()
        self.introduce_test()
        self.revert_to_original_skipping_status()

        self.ask_about_questions()

    def ask_about_questions(self):
        scores = self.scores
        arrows = self.proof_arrows
        proof_words = self.proof_words

        question = Text("What kind\nof problems?")  # OldTexText -> Text
        question.scale(1.5)
        question.move_to(proof_words, LEFT)

        research = Text("Research-lite")  # OldTexText -> Text
        research.scale(1.5)
        research.move_to(question, LEFT)
        research.shift(MED_SMALL_BUFF * RIGHT)
        research.set_color(BLUE)

        arrows.generate_target()
        for arrow in arrows.target:
            end = arrow.get_end()
            start = arrow.get_start()
            arrow.put_start_and_end_on(
                interpolate(question.get_left(), start, 0.1),
                end
            )

        self.play(
            FadeOut(scores),
            FadeOut(proof_words),
            MoveToTarget(arrows),
            Write(question),
        )
        self.wait()
        self.play(
            FadeIn(research, shift=DOWN),  # FadeIn(research, DOWN) -> FadeIn(research, shift=DOWN)
            question.animate.shift(2 * UP),  # .shift -> .animate.shift
        )
        self.wait()

        # Experience
        randy = Randolph(height=2)
        randy.move_to(research.get_corner(UL), DL)
        randy.shift(SMALL_BUFF * RIGHT)
        clock = Clock()
        clock.set_height(1)
        clock.next_to(randy, UR)

        self.play(
            FadeOut(question),
            FadeIn(randy),
            FadeIn(clock, shift=DOWN),  # FadeInFromDown -> FadeIn with shift
        )
        self.play(
            randy.animate.change("pondering"),  # .change -> .animate.change
            ClockPassesTime(clock, run_time=5, hours_passed=5),
        )
        self.play(
            ClockPassesTime(clock, run_time=2, hours_passed=2),
            VFadeOut(clock),
            Blink(randy),
            VFadeOut(randy),
            LaggedStartMap(
                FadeOut,
                VGroup(
                    research,
                    *arrows,
                    *self.problem_rects,
                    self.time_labels[0]
                )
            ),
        )

        # Second part
        big_rect = FullScreenFadeRectangle()
        lil_rect = self.problem_rects[1].copy()
        lil_rect.reverse_points()
        big_rect.append_vectorized_mobject(lil_rect)
        frame = self.camera.frame  # self.camera_frame -> self.camera.frame
        frame.generate_target()
        frame.target.scale(0.35)
        frame.target.move_to(lil_rect)

        self.play(
            FadeIn(self.test[1], shift=DOWN),  # FadeInFromDown -> FadeIn with shift
        )
        self.wait()
        self.play(
            FadeIn(big_rect),
            MoveToTarget(frame, run_time=6),
        )
        self.wait()
