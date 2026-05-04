# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示一個帶有旋轉角度標示的網格圓盤，隨著旋轉動態更新角度數值。



from manim import *
class OneDegreeOfFreedomForRotation(Scene):
    def construct(self):
        circle = CheckeredCircle(radius=2, stroke_width=10)
        r_line = Line(circle.get_center(), circle.get_right())
        moving_r_line = r_line.copy()
        right_dot = Dot(color=WHITE)
        right_dot.move_to(circle.get_right())
        circle.add(moving_r_line, right_dot)
        center_dot = Dot(color=WHITE)

        def get_angle():
            return moving_r_line.get_angle() % TAU

        angle_label = Integer(0, unit="^\\circ")
        angle_label.scale(2)
        angle_label.add_updater(
            lambda m: m.set_value(get_angle() / DEGREES)
        )
        angle_label.add_updater(
            lambda m: m.next_to(circle, UP, buff=MED_LARGE_BUFF)
        )

        def get_arc():
            return Arc(
                angle=get_angle(),
                radius=0.5,
                color=GREY_B,
            )

        arc = get_arc()
        arc.add_updater(lambda m: m.become(get_arc()))

        self.add(circle, center_dot, r_line, angle_label, arc)
        # 假設 example_angles 為一組旋轉角度列表
        example_angles = [PI/2, PI, 3*PI/2, 2*PI]  # 替換為實際需要的角度
        for angle in example_angles:
            self.play(Rotate(circle, angle, run_time=4))
            self.wait()
