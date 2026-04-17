# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示在一個高旋度向量場中，多層彩色點線沿著流場動態移動並逐漸扭曲的過程。


from manim import *
import itertools as it

class HighCurlFieldBreakingLayers(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flow_anim = move_submobjects_along_vector_field

    def construct(self):
        lines = VGroup(*[
            self.get_line()
            for x in range(20)
        ])
        lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        lines[0::2].set_color(BLUE)
        lines[1::2].set_color(RED)
        all_dots = VGroup(*it.chain(*lines))

        def func(p):
            vect = four_swirls_function(p)
            norm = get_norm(vect)
            if norm > 2:
                vect *= 4.0 / get_norm(vect)**2
            return vect

        self.add(lines)
        self.add(self.flow_anim(all_dots, func))
        self.wait(16)

    def get_line(self):
        line = VGroup(*[Dot() for x in range(100)])
        line.set_height(0.1)
        line.arrange(RIGHT, buff=0)
        line.set_width(10)
        return line
