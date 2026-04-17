# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 在畫面左上角顯示紅色文字，內容為 Patron 優惠資訊。



from manim import *
class PatronWords(Scene):
    def construct(self):
        words = Text("$2+ Patrons get\n50% off")
        words.to_corner(UL)
        words.set_color(RED)
        self.add(words)
