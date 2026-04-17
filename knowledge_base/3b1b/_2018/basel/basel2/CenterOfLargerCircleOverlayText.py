# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 在場景頂部顯示「較大圓的圓心」文字，並附帶指向左下角的箭頭。



from manim import *
class CenterOfLargerCircleOverlayText(Scene):
    def construct(self):
        words = Text("Center of\nlarger circle")
        arrow = Arrow(start=ORIGIN, end=DOWN+LEFT, color=WHITE)
        arrow.shift(words.get_bottom() + SMALL_BUFF*DOWN - arrow.get_start())
        group = VGroup(words, arrow)
        group.set_height(config.frame_height - 1)
        group.to_edge(UP)
        self.add(group)
