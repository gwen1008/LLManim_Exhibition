# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 將 "Diameter" 文字放大、旋轉並顯示在畫面上。



from manim import *
class DiameterWordOverlay(Scene):
    def construct(self):
        word = Text("Diameter")
        word.set_width(config.frame_width / 2)  # FRAME_X_RADIUS 替換為 frame_width/2
        word.rotate(-45 * DEGREES)
        self.play(Write(word))
        self.wait()
