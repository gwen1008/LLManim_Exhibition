# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示標題 "Three body problem" 置於畫面上方的場景。



from manim import *
class ThreeBodyTitle(Scene):
    def construct(self):
        title = Text("Three body problem")
        title.scale(1.5)
        title.to_edge(UP)
        self.add(title)
