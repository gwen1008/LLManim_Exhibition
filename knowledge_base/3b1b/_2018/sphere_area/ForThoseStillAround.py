# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 將文字 "Still here?" 轉變為網址 "3blue1brown.com/store" 的動畫場景。



from manim import *
class ForThoseStillAround(Scene):
    def construct(self):
        words = Text("Still here?")
        words.scale(1.5)
        url = Text("3blue1brown.com/store")
        # url.scale(1.5)
        url.to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(Write(words))
        self.wait()
        self.play(ReplacementTransform(words, url))
        self.wait()
