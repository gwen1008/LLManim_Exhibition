# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示一系列技術性問題從上方標題下方逐個淡入淡出，每個問題停留一段時間。



from manim import *
class TechnicalNuances(Scene):
    def construct(self):
        title = Tex("Technical nuances not discussed")
        title.scale(1.5)
        title.set_color(YELLOW)
        line = DashedLine(title.get_left(), title.get_right())
        line.next_to(title, DOWN, SMALL_BUFF)
        line.set_stroke(GREY_B, 3)

        questions = VGroup(*map(Tex, [
            "Does the value at $0.5$ matter?",
            "What does it mean to solve a PDE with\\\\"
            "a discontinuous initial condition?",
            "Is the limit of a sequence of solutions\\\\"
            "also a solution?",
            "Do all functions have a Fourier series?",
        ]))

        self.play(
            Write(title),
            Create(line),
        )
        title.add(line)
        self.play(
            title.animate.to_edge(UP),
        )

        last_question = VMobject()
        for question in questions:
            question.next_to(line, DOWN, MED_LARGE_BUFF)
            self.play(
                FadeIn(question, shift=DOWN),
                FadeOut(last_question, shift=UP)
            )
            self.wait(2)
            last_question = question
