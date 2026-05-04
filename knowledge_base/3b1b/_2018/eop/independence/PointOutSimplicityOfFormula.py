# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示教師指向簡化的公式，學生們從思考到歡呼，最後教師解釋公式簡化的原因在於獨立性。



from manim import *
class PointOutSimplicityOfFormula(TeacherStudentsScene, GeneralBinomialDistributionValues):
    def construct(self):
        prob = self.get_probability_expression(full=False)
        corner = self.teacher.get_corner(UP + LEFT)
        prob.next_to(corner, UP, buff=MED_LARGE_BUFF)
        prob.save_state()
        prob.move_to(corner)
        prob.set_opacity(0)

        self.play(
            prob.animate.restore(),
            self.teacher.animate.change_mode("raise_right_hand")
        )
        self.play_student_changes(
            *["pondering"] * 3,
            look_at=prob
        )
        self.wait()
        self.student_says(
            "Simpler than I feared",
            target_mode="hooray",
            index=0,
            added_anims=[prob.animate.to_corner(UP + RIGHT)]
        )
        self.wait()
        self.teacher_says("Due to \\\\ independence")
        self.wait(2)
