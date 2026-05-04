# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 老師評估學生獨立答題時全錯的機率，並對此表示懷疑，學生則提出質疑。



from manim import *
class TeacherAssessingLiklihoodOfZero(TeacherStudentsScene):
    def construct(self):
        self.add_title()
        self.fade_other_students()
        self.show_independence_probability()
        self.teacher_reacts()

    def add_title(self):
        title = MathTex("P(", "\\text{Correct}", ")", "=", "0.65")
        title.to_edge(UP)
        title.set_color_by_tex("Correct", GREEN)
        q_mark = MathTex("?")
        q_mark.next_to(title[-2], UP, buff=SMALL_BUFF)
        title.add(q_mark)

        self.add(title)
        self.title = title

    def fade_other_students(self):
        for student in self.students[0::2]:
            student.set_opacity(0.3)
            self.pi_creatures.remove(student)

    def show_independence_probability(self):
        prob = get_probability_of_slot_group(3*[False])
        rhs = MathTex("=", "(0.35)", "^3", "\\approx 4.3\\%")
        rhs.set_color_by_tex("0.35", RED)
        rhs.next_to(prob, RIGHT)
        prob.add(rhs)
        prob.next_to(self.teacher, UP+LEFT)
        words = Text("Assuming independence")
        words.next_to(prob, UP)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(words),
            Write(prob)
        )
        self.wait()

        self.ind_group = VGroup(prob, words)

    def teacher_reacts(self):
        ind_group = self.ind_group
        box = SurroundingRectangle(ind_group)
        box.set_stroke(WHITE, 0)
        ind_group.add(box)
        ind_group.generate_target()
        ind_group.target.scale(0.7)
        ind_group.target.to_corner(UP+RIGHT, buff=MED_SMALL_BUFF)
        ind_group.target[-1].set_stroke(WHITE, 2)

        randy = self.students[1]

        self.teacher_says(
            "Highly unlikely",
            target_mode = "sassy",
            added_anims = [MoveToTarget(ind_group)],
            run_time = 2,
        )
        self.play(randy.change, "sad")
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(
                self.teacher, target_mode = "guilty",
            ),
            PiCreatureSays(randy, "Wait!", target_mode = "surprised"),
            run_time = 1
        )
        self.wait(1)
