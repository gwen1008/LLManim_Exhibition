# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個教師與學生討論湍流定義的場景，先提出問題，再將解釋分為定性特徵與嚴格定義兩部分，最後列舉三個定性描述並以角色表情動畫結束。



from manim import *
class AskAboutTurbulence(TeacherStudentsScene):
    def construct(self):
        self.pi_creatures_ask()
        self.divide_by_qualitative_quantitative()
        self.three_qualitative_descriptors()
        self.rigorous_definition()

    def pi_creatures_ask(self):
        morty = self.teacher
        randy = self.students[1]
        morty.change("surprised")

        words = TexText("Wait,", "what", "exactly \\\\", "is turbulence?")
        question = TexText("What", "is turbulence?")
        question.to_edge(UP, buff=MED_SMALL_BUFF)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH - 1)
        h_line.next_to(question, DOWN, buff=MED_LARGE_BUFF)

        self.student_says(
            words,
            target_mode='raise_left_hand',
            added_anims=[morty.change, 'pondering']
        )
        self.play_student_changes(
            "erm", "raise_left_hand", "confused",
        )
        self.wait(3)
        self.play(
            morty.change, "raise_right_hand",
            FadeOut(randy.bubble),
            ReplacementTransform(VGroup(words[1], words[3]), question),
            FadeOut(VGroup(words[0], words[2])),
            self.change_students(
                *3 * ["pondering"],
                look_at=question
            )
        )
        self.play(
            Create(h_line),
            LaggedStartMap(
                FadeOutAndShiftDown, self.pi_creatures,
                run_time=1,
                lag_ratio=0.8
            )
        )
        self.wait()

        self.question = question
        self.h_line = h_line

    def divide_by_qualitative_quantitative(self):
        v_line = Line(
            self.h_line.get_center(),
            FRAME_HEIGHT * DOWN / 2,
        )
        words = VGroup(
            TexText("Features", color=YELLOW),
            TexText("Rigorous definition", color=BLUE),
        )
        words.next_to(self.h_line, DOWN)
        words[0].shift(FRAME_WIDTH * LEFT / 4)
        words[1].shift(FRAME_WIDTH * RIGHT / 4)
        self.play(
            Create(v_line),
            LaggedStartMap(FadeInFromDown, words)
        )
        self.wait()

        self.words = words

    def three_qualitative_descriptors(self):
        words = VGroup(
            TexText("- Eddies"),
            TexText("- Chaos"),
            TexText("- Diffusion"),
        )
        words.arrange(
            DOWN, buff=1.25,
            aligned_edge=LEFT
        )
        words.to_edge(LEFT)
        words.shift(MED_LARGE_BUFF * DOWN)

        for word in words:
            self.play(
                FadeInFromDown(word),
            )
        self.wait(3)

    def rigorous_definition(self):
        randy = Randolph()
        randy.move_to(FRAME_WIDTH * RIGHT / 4)
        randy.change("pondering", self.words[1])

        self.play(FadeIn(randy))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change, "shruggie")
        for x in range(2):
            self.play(Blink(randy))
            self.wait()
        self.play(randy.look, LEFT)
        self.wait(2)
        self.play(randy.look, UP)
        self.play(Blink(randy))
        self.wait()
