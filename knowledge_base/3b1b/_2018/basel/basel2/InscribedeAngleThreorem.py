# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示圓周角定理，一個圓內接四邊形隨著頂點在圓周上移動，圓心角與圓周角的關係保持不變。



from manim import *
class InscribedeAngleThreorem(TeacherStudentsScene):
    def construct(self):
        circle = Circle(radius=2, color=WHITE)
        circle.next_to(self.students[2], UP)
        self.add(circle)

        title = Text("Inscribed angle\n theorem")  # OldTexText -> Text
        title.to_corner(UL)
        self.add(title)

        center = Dot(circle.get_center(), color=WHITE)
        self.add_foreground_mobject(center)

        point = Dot(circle.get_left(), radius=0)  # VectorizedPoint -> 半徑為0的Dot
        shape = Polygon(UL, ORIGIN, DL, RIGHT)
        shape.set_stroke(BLUE)
        
        def update_shape(shape):
            shape.set_points_as_corners([
                point.get_center(),
                circle.point_from_proportion(7./8), 
                circle.get_center(),
                circle.point_from_proportion(1./8), 
                point.get_center(),
            ])
        shape.add_updater(update_shape)  # Mobject.add_updater -> add_updater
        shape.update()  # 手動更新一次

        angle_mark = Arc(start_angle=-TAU/8, angle=TAU/4)
        angle_mark.scale(0.3, about_point=ORIGIN)
        angle_mark.shift(circle.get_center())
        theta = MathTex("\\theta").set_color(RED)  # OldTex -> MathTex
        theta.next_to(angle_mark, RIGHT, buff=MED_SMALL_BUFF)
        angle_mark.set_color(theta.get_color())  # match_color -> set_color

        half_angle_mark = Arc(start_angle=-TAU/16, angle=TAU/8)
        half_angle_mark.scale(0.3, about_point=ORIGIN)
        half_angle_mark.shift(point.get_center())
        half_angle_mark.add(point.copy())
        theta_halves = MathTex("\\theta/2").set_color(GREEN)  # OldTex -> MathTex
        theta_halves.scale(0.7)
        half_angle_mark.set_color(theta_halves.get_color())  # match_color -> set_color
        
        def update_theta_halves(theta_halves):
            theta_halves.move_to(interpolate(
                point.get_center(), 
                half_angle_mark.point_from_proportion(0.5),
                2.5,
            ))
        theta_halves.add_updater(update_theta_halves)  # UpdateFromFunc -> add_updater
        theta_halves.update()  # 手動更新一次

        self.play(
            self.teacher.change("raise_right_hand"),
            Create(shape, rate_func=linear),  # ShowCreation -> Create
        )
        self.play(*[FadeIn(mob) for mob in [angle_mark, theta]])  # list(map(...)) -> 列表推導
        self.play(
            Create(half_angle_mark),  # ShowCreation -> Create
            Write(theta_halves),
            self.change_students(*["pondering"]*3)
        )
        self.add_foreground_mobjects(half_angle_mark, theta_halves)
        # shape_update_anim 已通過 add_updater 添加，無需額外添加
        
        for angle in [0.25*TAU, -0.4*TAU, 0.3*TAU, -0.35*TAU]:
            point.generate_target()
            point.target.rotate(angle, about_point=circle.get_center())

            half_angle_mark.generate_target()
            half_angle_mark.target.rotate(angle/2)
            half_angle_mark.target.shift(
                point.target.get_center() - \
                half_angle_mark.target[1].get_center()
            )

            self.play(
                MoveToTarget(point),
                MoveToTarget(half_angle_mark),
                # theta_halves_update 已通過 add_updater 自動更新
                path_arc=angle,
                run_time=3,
            )
