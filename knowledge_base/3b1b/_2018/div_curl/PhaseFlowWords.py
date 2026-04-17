# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示 "Phase flow" 文字以書寫動畫出現的過程。



from manim import *
class PhaseFlowWords(Scene):
    def construct(self):
        words = Text("``Phase flow''")
        words.scale(2)
        self.play(Write(words))
        self.wait()
