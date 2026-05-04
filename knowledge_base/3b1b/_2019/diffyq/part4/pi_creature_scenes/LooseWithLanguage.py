# Source: 3b1b/_2019/diffyq/part4/pi_creature_scenes.py
# Description: [3b1b translated] 展示老師對學生說話，並在螢幕上方顯示兩個術語標籤，學生們思考著這些術語。



from manim import *
class LooseWithLanguage(TeacherStudentsScene):
    def construct(self):
        terms = VGroup(
            Text("``Complex number''"),
            Text("``Vector''"),
        )
        colors = [YELLOW, BLUE]
        for term, color in zip(terms, colors):
            term.set_color(color)

        terms.scale(1.5)
        terms.arrange(DOWN, buff=LARGE_BUFF)
        terms.to_edge(UP)
        terms.match_x(self.students)

        self.teacher_says(
            "Loose with\\\\language",
            bubble_config={"width": 3, "height": 3},
            run_time=2,
        )
        self.play(
            FadeIn(terms[1], shift=DOWN),
            self.change_students(
                "thinking", "pondering", "erm",
                look_at=terms,
            )
        )
        self.play(FadeIn(terms[0], shift=DOWN))
        self.wait()
        self.play(Swap(*terms))
        self.wait(3)
