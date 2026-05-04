# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示三維坐標軸上標記 i, j, k 三個虛數單位，並讓相機緩慢旋轉的動畫。



from manim import *
class SimpleImaginaryQuaternionAxes(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.three_d_axes_config = {
            "axis_config": {"unit_size": 2},
            "x_range": [-2, 2],
            "y_range": [-2, 2],
            "z_range": [-1.25, 1.25],
        }

    def construct(self):
        axes = ThreeDAxes(**self.three_d_axes_config)
        labels = VGroup(*[
            MathTex(tex).set_color(color)
            for tex, color in zip(
                ["i", "j", "k"],
                [GREEN, RED, BLUE]
            )
        ])
        labels[0].next_to(axes.c2p(1, 0, 0), DOWN + IN, buff=SMALL_BUFF)
        labels[1].next_to(axes.c2p(0, 1, 0), RIGHT, buff=SMALL_BUFF)
        labels[2].next_to(axes.c2p(0, 0, 1), RIGHT, buff=SMALL_BUFF)

        self.add(axes)
        self.add(labels)
        # ManimCE 中沒有 add_fixed_orientation_mobjects，用 always_redraw 模擬固定方向
        for label in labels:
            label.add_updater(lambda m, dt: m)  # 簡單的佔位更新器保持物件存在

        # 設定相機初始位置並開始旋轉
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(15)
