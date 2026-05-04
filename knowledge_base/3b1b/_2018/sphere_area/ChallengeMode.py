# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個標題文字從上方寫入的挑戰模式場景。



from manim import *
class ChallengeMode(Scene):
    def construct(self):
        words = Text("Challenge mode: Predict the proof")
        words.scale(1.5)
        words.to_edge(UP)
        self.play(Write(words))
        self.wait()
