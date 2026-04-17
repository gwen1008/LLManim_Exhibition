# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示一個圓的半徑旋轉時，對應的圓弧長度變化，並用動態數值顯示圓周率近似值。


from manim import *
import numpy as np

class CircleConstants(Scene):
    def radial_label_func(self, a, b, theta):
        theta2 = theta % TAU
        slope = (a - b) / (TAU / 4)

        if theta2 < TAU / 4:
            x = a - slope * theta2
        elif theta < TAU / 2:
            x = b + slope * (theta2 - TAU / 4)
        elif theta < 3 * TAU / 4:
            x = a - slope * (theta2 - TAU / 2)
        else:
            x = b + slope * (theta2 - 3 * TAU / 4)
        return x

    def construct(self):
        self.setup_circle()
        self.change_arc_length(0.004)
        self.pi_equals.next_to(self.decimal, LEFT)
        self.wait()
        self.change_arc_length(TAU / 2)
        self.wait()
        self.change_arc_length(TAU)
        self.wait()
        self.change_arc_length(TAU / 4)
        self.wait()
        self.change_arc_length(TAU / 2)
        self.wait()

    def setup_circle(self):
        RADIUS = 2.0
        RADIUS_COLOR = YELLOW
        CIRCUM_COLOR = BLUE
        RADIUS_BUFF_HOR = 0.5
        RADIUS_BUFF_VER = 0.5

        self.circle_arc = Arc(angle=0.004, radius=RADIUS)
        self.radius = Line(ORIGIN, RADIUS * RIGHT)
        self.radius.set_color(RADIUS_COLOR)
        self.circle_arc.set_color(CIRCUM_COLOR)

        self.pi_equals = MathTex(r"\pi\approx", color=CIRCUM_COLOR)
        self.decimal = DecimalNumber(0, color=CIRCUM_COLOR)
        self.decimal.next_to(self.pi_equals, RIGHT, buff=0.25)
        self.circum_label = VGroup(self.pi_equals, self.decimal)
        self.circum_label.next_to(self.radius, RIGHT, buff=RADIUS_BUFF_HOR)

        self.one = MathTex("1", color=RADIUS_COLOR)
        self.one.next_to(self.radius, UP)

        self.play(Create(self.radius), FadeIn(self.one))
        self.play(
            Create(self.circle_arc),
            Write(self.pi_equals),
            Write(self.decimal)
        )

    def change_arc_length(self, new_angle):
        RADIUS = 2.0
        RADIUS_BUFF_HOR = 0.5
        RADIUS_BUFF_VER = 0.5

        def decimal_position_update_func(decimal):
            angle = decimal.number
            max_radius = RADIUS + RADIUS_BUFF_HOR
            min_radius = RADIUS + RADIUS_BUFF_VER
            label_radius = self.radial_label_func(max_radius, min_radius, angle)
            label_center = label_radius * np.array([np.cos(angle), np.sin(angle), 0])
            label_center += 0.5 * RIGHT
            decimal.move_to(label_center)

        # 自定義動畫：更新圓弧角度
        def update_arc(arc):
            arc.become(Arc(angle=new_angle, radius=arc.radius, color=arc.get_color()))

        # 自定義動畫：保持標籤相對位置
        def update_one_label(one):
            one.next_to(self.radius.get_end(), UP, buff=0.5)

        # 自定義動畫：保持 pi_equals 相對位置
        def update_pi_equals(pi_eq):
            pi_eq.next_to(self.decimal, LEFT)

        self.play(
            self.radius.animate.rotate(new_angle - self.circle_arc.angle, about_point=ORIGIN),
            UpdateFromFunc(self.circle_arc, update_arc),
            ChangeDecimalToValue(
                self.decimal, new_angle,
                position_update_func=decimal_position_update_func
            ),
            UpdateFromFunc(self.pi_equals, update_pi_equals),
            UpdateFromFunc(self.one, update_one_label),
            run_time=3,
        )
        self.wait(2)
