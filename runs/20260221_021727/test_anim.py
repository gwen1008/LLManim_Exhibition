from manim import *
class TestAnim(Scene):
    def construct(self):
        c = Circle(fill_opacity=0.0)
        # self.add(c) # intentionally not added
        self.play(c.animate.set_fill(opacity=1.0))
        self.wait()
