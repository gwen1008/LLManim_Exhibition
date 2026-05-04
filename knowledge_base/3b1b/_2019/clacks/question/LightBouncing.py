# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示一束黃色光線在兩面鏡子之間反射的動畫，光線從右側進入並在鏡面間來回反射，最終從左側射出。


from manim import *
import numpy as np

class LightBouncing(MovingCameraScene):
    def __init__(
        self,
        theta=np.arctan(0.15),
        show_fanning=False,
        mirror_shift_vect=5 * LEFT,
        mirror_length=10,
        beam_start_x=12,
        beam_height=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.theta = theta
        self.show_fanning = show_fanning
        self.mirror_shift_vect = mirror_shift_vect
        self.mirror_length = mirror_length
        self.beam_start_x = beam_start_x
        self.beam_height = beam_height

    def construct(self):
        theta = self.theta
        h_line = Line(ORIGIN, self.mirror_length * RIGHT)
        d_line = h_line.copy().rotate(theta, about_point=ORIGIN)
        mirrors = VGroup(h_line, d_line)
        self.add(mirrors)

        beam_height = self.beam_height
        start_point = self.beam_start_x * RIGHT + beam_height * UP
        
        # 計算光線路徑點
        points = [start_point] + [
            np.array([
                (beam_height / np.tan(k * theta)),
                beam_height,
                0,
            ])
            for k in range(1, int(PI / theta))
        ] + [rotate(start_point, PI, UP)]
        
        # 計算反射後的路徑點
        reflected_points = []
        for k, point in enumerate(points):
            reflected_point = rotate_vector(point, -2 * (k // 2) * theta)
            reflected_point[1] = abs(reflected_point[1])
            reflected_points.append(reflected_point)
        
        # 創建光束
        beam = VMobject()
        beam.set_points_as_corners(reflected_points)
        beam.set_stroke(YELLOW, 2)

        anims = [self.get_beam_anim(beam)]

        # 可選：顯示扇形鏡面
        if self.show_fanning:
            for k in range(2, int(PI / theta) + 1):
                line = h_line.copy()
                line.set_stroke(WHITE, 1)
                line.rotate(k * theta, about_point=ORIGIN)
                self.add(line)
            straight_beam = VMobject()
            straight_beam.set_points_as_corners(points)
            straight_beam.set_stroke(YELLOW, 2)
            anims.append(self.get_beam_anim(straight_beam))

        # 移動相機視角
        self.camera.frame.shift(-self.mirror_shift_vect)
        self.play(*anims)
        self.wait()

    def get_beam_anim(self, beam):
        dot = Dot()
        dot.scale(0.5)
        dot.set_color(beam.get_stroke_color())
        
        return AnimationGroup(
            ShowPassingFlash(
                beam,
                run_time=5,
                rate_func=lambda t: smooth(t, 5),
                time_width=0.05,
            ),
            UpdateFromFunc(
                dot,
                lambda m: m.move_to(beam.get_points()[-1])
            ),
        )
