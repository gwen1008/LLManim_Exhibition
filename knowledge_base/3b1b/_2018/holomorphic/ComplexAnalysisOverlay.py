# Source: 3b1b/_2018/holomorphic.py
# Description: [3b1b translated] 在場景頂部顯示帶有背景矩形的「Complex analysis」文字標題。



from manim import *
class ComplexAnalysisOverlay(Scene):
    def construct(self):
        words = Text("Complex analysis")
        words.scale(1.25)
        words.to_edge(UP)
        words.add_background_rectangle()
        self.add(words)
        self.wait()
