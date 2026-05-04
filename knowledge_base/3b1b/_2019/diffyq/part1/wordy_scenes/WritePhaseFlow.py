# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示 "Phase flow" 文字從左到右書寫出現的過程，文字帶有背景矩形。



from manim import *
class WritePhaseFlow(Scene):
    def construct(self):
        words = Text("Phase flow")
        words.scale(2)
        words.shift(config.frame_width * LEFT / 4)
        words.to_edge(UP)
        words.add_background_rectangle()
        self.play(Write(words))
        self.wait()
