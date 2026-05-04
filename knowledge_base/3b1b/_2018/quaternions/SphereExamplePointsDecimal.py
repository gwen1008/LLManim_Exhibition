# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示一個三維空間中的點在球面上旋轉時，其座標值（w, x, y）的實時更新，並驗證它們滿足球面方程 w² + x² + y² = 1。



from manim import *
class SphereExamplePointsDecimal(Scene):
    def __init__(self, point_rotation_angle_axis_pairs=None, **kwargs):
        super().__init__(**kwargs)
        if point_rotation_angle_axis_pairs is None:
            self.point_rotation_angle_axis_pairs = [
                (45 * DEGREES, DOWN),
                (120 * DEGREES, OUT),
                (35 * DEGREES, rotate_vector(RIGHT, 30 * DEGREES)),
                (90 * DEGREES, IN),
            ]
        else:
            self.point_rotation_angle_axis_pairs = point_rotation_angle_axis_pairs

    def construct(self):
        decimals = VGroup(*[
            DecimalNumber(
                0,
                num_decimal_places=3,
                color=color,
                include_sign=True,
            )
            for color in [YELLOW, GREEN, RED]
        ])
        # 使用 MathTex 替換 OldTex
        number_label = VGroup(
            decimals[0], MathTex("+"),
            decimals[1], MathTex("i"), MathTex("+"),
            decimals[2], MathTex("j"),
        )
        number_label.arrange(RIGHT, buff=SMALL_BUFF)
        number_label.to_corner(UL)

        # 使用 Dot 或 Sphere 來表示一個點，但這裡需要一個可旋轉的向量點
        # 使用一個不可見的點，其位置用於更新小數
        point = Dot3D(point=OUT, radius=0)  # 一個不可見的 3D 點

        def generate_decimal_updater(decimal, index):
            shifted_i = (index - 1) % 3
            # 更新函數：根據點的位置設置小數值
            decimal.add_updater(lambda d: d.set_value(
                point.get_center()[shifted_i]
            ))
            return decimal

        for i, decimal in enumerate(decimals):
            self.add(generate_decimal_updater(decimal, i))

        decimal_braces = VGroup()
        for decimal, char in zip(decimals, "wxy"):
            brace = Brace(decimal, DOWN, buff=SMALL_BUFF)
            # 使用 MathTex 替換 get_tex
            label = MathTex(char, color=decimal.get_color()).next_to(brace, DOWN, buff=SMALL_BUFF)
            brace.add(label)
            decimal_braces.add(brace)

        equation = MathTex(
            "w^2 + x^2 + y^2 = 1",
            tex_to_color_map={
                "w": YELLOW,
                "x": GREEN,
                "y": RED,
            }
        )
        equation.next_to(decimal_braces, DOWN, buff=MED_LARGE_BUFF)

        self.add(number_label)
        self.add(decimal_braces)
        self.add(equation)

        pairs = self.point_rotation_angle_axis_pairs
        for angle, axis in pairs:
            # 使用 Rotate 動畫旋轉點
            self.play(
                Rotate(point, angle=angle, axis=axis, about_point=ORIGIN),
                run_time=2
            )
            self.wait()
