# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示三個不同顏色的問題文字在場景中兩兩交換位置，並帶有圓弧路徑動畫。


from manim import *
import itertools as it

class PermuteQuizQuestions(Scene):
    def construct(self):
        quiz = get_quiz(
            "Define ``Brachistochrone''",
            "Define ``Tautochrone''",
            "Define ``Cycloid''",
        )
        questions = [
            VGroup(*q[2:])
            for q in quiz.questions
        ]
        colors = [BLUE, GREEN, RED]
        for color, question in zip(colors, questions):
            question.set_color(color)
        quiz.scale(2)

        self.add(quiz)
        self.wait()
        for m1, m2 in it.combinations(questions, 2):
            self.play(
                m1.animate.move_to(m2.get_left()),
                m2.animate.move_to(m1.get_left()),
                path_arc=PI
            )
            self.wait()
