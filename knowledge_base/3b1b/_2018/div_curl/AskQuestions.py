# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 老師與學生討論流體流動與電學的關聯，並引入散度和旋度概念，最後連結到複變分析。



from manim import *
class AskQuestions(TeacherStudentsScene):
    def construct(self):
        div_tex = MathTex("\\nabla \\cdot", vec_tex("v"))
        curl_tex = MathTex("\\nabla \\times", vec_tex("v"))
        div_name = Text("Divergence")
        curl_name = Text("Curl")
        div = VGroup(div_name, div_tex)
        curl = VGroup(curl_name, curl_tex)
        for group in div, curl:
            # 在 ManimCE 中，set_color_by_tex 已移除，改用 set_color 並手動指定
            # 假設 vec_tex("v") 返回 "\\vec{\\textbf{v}}"
            group[1].set_color(YELLOW, substring="\\vec{\\textbf{v}}")
            group.arrange(DOWN)
        topics = VGroup(div, curl)
        topics.arrange(DOWN, buff=LARGE_BUFF)
        topics.move_to(self.hold_up_spot, DOWN)
        div.save_state()
        div.move_to(self.hold_up_spot, DOWN)
        screen = self.screen

        self.student_says(
            "What does fluid flow have \\\\ to do with electricity?",
            added_anims=[self.teacher.change, "happy"]
        )
        self.wait()
        self.student_says(
            "And you mentioned \\\\ complex numbers?",
            index=0,
        )
        self.wait(3)
        self.play(
            FadeIn(div, shift=DOWN),
            self.teacher.change, "raise_right_hand",
            FadeOut(self.students[0].bubble),
            FadeOut(self.students[0].bubble.content),
            self.change_students(*["pondering"] * 3)
        )
        self.play(
            FadeIn(curl, shift=DOWN),
            div.restore
        )
        self.wait()
        self.look_at(self.screen)
        self.wait()
        self.play_all_student_changes("hooray", look_at=screen)
        self.wait(3)

        topics.generate_target()
        topics.target.to_edge(LEFT, buff=LARGE_BUFF)
        arrow = MathTex("\\leftrightarrow")
        arrow.scale(2)
        arrow.next_to(topics.target, RIGHT, buff=LARGE_BUFF)
        screen.next_to(arrow, RIGHT, LARGE_BUFF)
        complex_analysis = Text("Complex analysis")
        complex_analysis.next_to(screen, UP)

        self.play(
            MoveToTarget(topics),
            self.change_students(
                "confused", "sassy", "erm",
                look_at=topics.target
            ),
            self.teacher.change, "pondering", screen
        )
        self.play(
            Write(arrow),
            FadeIn(complex_analysis, shift=DOWN)
        )
        self.look_at(screen)
        self.wait(6)
