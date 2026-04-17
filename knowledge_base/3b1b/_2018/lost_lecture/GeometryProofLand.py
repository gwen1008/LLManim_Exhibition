# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示「Geometry proof land」文字經過複數指數函數變換後，彩色圓圈收縮到文字位置的動畫過程。


from manim import *
import random
import numpy as np

class GeometryProofLand(Scene):
    def __init__(self, colors=None, text="Geometry proof land", **kwargs):
        super().__init__(**kwargs)
        if colors is None:
            colors = [
                PINK, RED, YELLOW, GREEN, GREEN_A, BLUE,
                MAROON_E, MAROON_B, YELLOW, BLUE,
            ]
        self.colors = colors
        self.text = text

    def construct(self):
        word = self.get_geometry_proof_land_word()
        word_outlines = word.copy()
        word_outlines.set_fill(opacity=0)
        word_outlines.set_stroke(WHITE, 1)
        colors = list(self.colors)
        random.shuffle(colors)
        word_outlines.set_color_by_gradient(*colors)
        word_outlines.set_stroke(width=5)

        circles = VGroup()
        for letter in word:
            circle = Circle()
            circle.replace(letter, dim_to_match=1)
            circle.scale(3)
            circle.set_stroke(WHITE, 0)
            circle.set_fill(letter.get_color(), 0)
            circles.add(circle)
            circle.target = letter

        self.play(
            LaggedStartMap(MoveToTarget, circles),
            run_time=2
        )
        self.add(word_outlines, circles)
        self.play(LaggedStartMap(
            FadeIn, word_outlines,
            run_time=3,
            rate_func=there_and_back,
        ), Animation(circles))
        self.wait()

    def get_geometry_proof_land_word(self):
        word = Text(self.text, font_size=48)
        word.rotate(-90 * DEGREES)
        word.scale(0.25)
        word.shift(3 * RIGHT)
        # 應用複數指數函數變換
        for i, letter in enumerate(word):
            pos = letter.get_center()
            z = complex(pos[0], pos[1])
            w = np.exp(z)
            new_pos = np.array([w.real, w.imag, 0])
            letter.move_to(new_pos)
        word.rotate(90 * DEGREES)
        word.set_width(9)
        word.center()
        word.to_edge(UP)
        word.set_color_by_gradient(*self.colors)
        word.set_stroke(width=0, background=True)
        return word
