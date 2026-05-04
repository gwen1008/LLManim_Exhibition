# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示教師與學生場景中，球體、圓柱體、公式和圓形等幾何圖形從上到下排列，並帶有箭頭和問號標記的動畫過程。



from manim import *
class AskAboutDirectConnection(TeacherStudentsScene, ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(
            camera_config={
                "light_source_start_point": [-4, 5, 7],
            },
            **kwargs
        )

    def construct(self):
        sphere = Sphere()
        cylinder = Cylinder()
        for mob in sphere, cylinder:
            mob.rotate(70 * DEGREES, LEFT)
        formula = MathTex("4\\pi R^2")
        formula.set_color(BLUE)
        circle = Circle()
        circle.set_stroke(width=0)
        circle.set_fill(GREY_BROWN, 1)
        area_label = MathTex("\\pi R^2")
        area_label.scale(1.5)
        circle.add(area_label)
        group = VGroup(
            sphere, cylinder, formula, circle
        )
        for mob in group:
            mob.set_height(1.5)
        formula.scale(0.5)
        group.arrange(RIGHT, buff=1.5)
        group.to_edge(UP, buff=2)
        group[1:3].to_edge(UP)

        arrows = VGroup()
        for m1, m2 in zip(group, group[1:]):
            arrow = Arrow(
                m1.get_center(), m2.get_center(),
                buff=1,
                color=WHITE
            )
            arrows.add(arrow)
        direct_arrow = Arrow(
            sphere.get_center(), circle.get_center(), color=WHITE
        )
        q_marks = MathTex(*"???")
        q_marks.arrange(RIGHT, buff=0.5)
        q_marks.scale(1.5)
        q_marks.next_to(direct_arrow, DOWN)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            self.change_students(
                *3 * ["pondering"],
                look_at=group,
            ),
            LaggedStartMap(FadeIn, group, shift=DOWN),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.wait()
        self.play(
            self.teacher.animate.change("pondering"),
            self.students[2].animate.change("raise_right_hand"),
            GrowArrow(direct_arrow),
            LaggedStartMap(
                FadeIn, q_marks,
                shift=UP,
                lag_ratio=0.8,
                run_time=1.5,
            )
        )
        self.play_student_changes(
            "erm", "sassy", "raise_right_hand",
        )
        self.wait(2)
        self.look_at(group)
        self.wait(2)
