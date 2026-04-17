# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 在一個半透明的全螢幕矩形上，以紅色文字顯示「Not the most computationally efficient」並帶有白色描邊。



from manim import *
class NotTheMostComputationallyEfficient(Scene):
    def __init__(self, words="Not the most \\\\ computationally efficient", word_height=4, opacity=0.7, **kwargs):
        super().__init__(**kwargs)
        self.words = words
        self.word_height = word_height
        self.opacity = opacity

    def construct(self):
        big_rect = FullScreenFadeRectangle(opacity=self.opacity)
        self.add(big_rect)

        words = TexText(self.words)
        words.set_color(RED)
        words.set_stroke(WHITE, 1)
        words.set_width(config.frame_width - 2 * MED_LARGE_BUFF)
        self.play(Write(words))
        self.wait()
