# Source: 3b1b/_2018/pi_day.py
# Description: [3b1b translated] 展示歐拉簽名的SVG圖像以書寫動畫方式呈現。



from manim import *
class EulerSignature(Scene):
    def construct(self):
        sig = SVGMobject(file_name="euler-signature")
        self.play(Write(sig, run_time=5))
