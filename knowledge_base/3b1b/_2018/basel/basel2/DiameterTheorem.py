# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示直徑定理的視覺化，一個圓內接直角三角形隨著頂點在圓周上移動，並保持直角標記。



from manim import *
class DiameterTheorem(TeacherStudentsScene):
    def construct(self):
        circle = Circle(radius=2, color=WHITE)
        circle.next_to(self.students[2], UP)
        self.add(circle)

        center = Dot(circle.get_center(), color=WHITE)
        self.add_foreground_mobject(center)

        diameter_word = Text("Diameter")
        diameter_word.next_to(center, DOWN, buff=SMALL_BUFF)

        point = Dot(circle.get_top(), radius=0)  # 用不可見的 Dot 替代 VectorizedPoint
        triangle = Polygon(LEFT, RIGHT, UP)
        triangle.set_stroke(BLUE)
        triangle.set_fill(WHITE, 0.5)
        
        def update_triangle(triangle):
            triangle.set_points_as_corners([
                circle.get_left(), circle.get_right(),
                point.get_center(), circle.get_left(),
            ])
        triangle.add_updater(update_triangle)
        triangle.update()  # 初始化

        perp_mark = VMobject()
        perp_mark.set_points_as_corners([LEFT, DOWN, RIGHT])
        perp_mark.shift(DOWN)
        perp_mark.scale(0.15, about_point=ORIGIN)
        perp_mark.shift(point.get_center())
        perp_mark.add(point.copy())

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            DrawBorderThenFill(triangle),
            Write(diameter_word),
        )
        self.play(
            Create(perp_mark),
            self.change_students(*["pondering"]*3)
        )
        self.add_foreground_mobjects(perp_mark)
        for angle in [0.2*TAU, -0.4*TAU, 0.3*TAU]:
            point.generate_target()
            point.target.rotate(angle, about_point=circle.get_center())

            perp_mark.generate_target()
            perp_mark.target.rotate(angle/2)
            perp_mark.target.shift(
                point.target.get_center() - \
                perp_mark.target[1].get_center()
            )

            self.play(
                MoveToTarget(point),
                MoveToTarget(perp_mark),
                path_arc=angle,
                run_time=3,
            )
