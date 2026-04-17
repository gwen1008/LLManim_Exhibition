# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示一組帶有透明背景的數學標籤，放置在場景中的特定位置。



from manim import *
class MissingLabels(Scene):
    def construct(self):
        labels = VGroup(
            MathTex("i").move_to(UR),
            MathTex("1").move_to(0.3 * DOWN),
            MathTex("-i").move_to(DOWN + 1.2 * LEFT),
            MathTex("-j").move_to(1.7 * RIGHT + 0.8 * DOWN),
        )
        labels.set_background_stroke(width=0)
        self.add(labels)
