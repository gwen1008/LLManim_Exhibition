# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示在極坐標系中繪製質數序列的視覺化螺旋圖形，包括點狀螺旋和線狀螺旋，並支持縮放動畫。


from manim import *
import numpy as np

class SpiralScene(Scene):
    def __init__(
        self,
        axes_config={
            "axis_config": {
                "stroke_width": 1.5,
            }
        },
        default_dot_color=TEAL,
        p_spiral_width=6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.axes_config = axes_config
        self.default_dot_color = default_dot_color
        self.p_spiral_width = p_spiral_width

    def setup(self):
        super().setup()
        self.axes = Axes(**self.axes_config)
        self.add(self.axes)

    def get_v_spiral(self, sequence, axes=None, box_width=None):
        if axes is None:
            axes = self.axes
        if box_width is None:
            unit = np.linalg.norm(axes.c2p(1, 0) - axes.c2p(0, 0))
            box_width = max(
                0.2 / (-np.log10(unit) + 1),
                0.02,
            )

        return VGroup(*[
            Square(
                side_length=box_width,
                fill_color=self.default_dot_color,
                fill_opacity=1,
                stroke_width=0,
            ).move_to(self.get_polar_point(n, n, axes))
            for n in sequence
        ])

    def get_p_spiral(self, sequence, axes=None):
        if axes is None:
            axes = self.axes
        result = VMobject(
            color=self.default_dot_color,
            stroke_width=self.p_spiral_width,
        )
        result.set_points_as_corners([
            self.get_polar_point(n, n, axes)
            for n in sequence
        ])
        return result

    def get_prime_v_spiral(self, max_N, **kwargs):
        primes = self.read_in_primes(max_N)
        return self.get_v_spiral(primes, **kwargs)

    def get_prime_p_spiral(self, max_N, **kwargs):
        primes = self.read_in_primes(max_N)
        return self.get_p_spiral(primes, **kwargs)

    def get_polar_point(self, r, theta, axes=None):
        if axes is None:
            axes = self.axes
        return axes.c2p(r * np.cos(theta), r * np.sin(theta))

    def set_scale(self, scale,
                  axes=None,
                  spiral=None,
                  to_shrink=None,
                  min_box_width=0.05,
                  target_p_spiral_width=None,
                  added_anims=[],
                  run_time=3):
        if axes is None:
            axes = self.axes
        if added_anims is None:
            added_anims = []
        sf = self.get_scale_factor(scale, axes)

        anims = []
        for mob in [axes, spiral, to_shrink]:
            if mob is None:
                continue
            mob.generate_target()
            mob.target.scale(sf, about_point=ORIGIN)
            if mob is spiral:
                if isinstance(mob, VMobject) and hasattr(mob, '__len__') and len(mob) > 0:
                    old_width = mob[0].get_width()
                    for submob in mob.target:
                        submob.set_width(max(
                            old_width * sf,
                            min_box_width,
                        ))
                elif isinstance(mob, VMobject):
                    if target_p_spiral_width is not None:
                        mob.target.set_stroke(width=target_p_spiral_width)
            anims.append(MoveToTarget(mob))
        anims += added_anims

        if run_time == 0:
            for anim in anims:
                anim.begin()
                anim.update(1)
                anim.finish()
        else:
            self.play(
                *anims,
                run_time=run_time,
                rate_func=lambda t: interpolate(
                    smooth(t),
                    smooth(t)**(sf**(0.5)),
                    t,
                )
            )

    def get_scale_factor(self, target_scale, axes=None):
        if axes is None:
            axes = self.axes
        unit = np.linalg.norm(axes.c2p(1, 0) - axes.c2p(0, 0))
        return 1 / (target_scale * unit)

    def get_labels(self, sequence, scale_func=np.sqrt):
        labels = VGroup()
        for n in sequence:
            label = Integer(n)
            label.set_stroke(width=0, background=True)
            label.scale(scale_func(n))
            label.next_to(
                self.get_polar_point(n, n), UP,
                buff=0.5 * label.get_height(),
            )
            labels.add(label)
        return labels

    def get_prime_labels(self, max_N):
        primes = self.read_in_primes(max_N)
        return self.get_labels(primes)

    def read_in_primes(self, max_N):
        # 這是一個占位函數，實際使用時需要實現讀取質數的邏輯
        # 返回前 max_N 個質數
        primes = []
        num = 2
        while len(primes) < max_N:
            is_prime = True
            for p in primes:
                if p * p > num:
                    break
                if num % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
            num += 1
        return primes
