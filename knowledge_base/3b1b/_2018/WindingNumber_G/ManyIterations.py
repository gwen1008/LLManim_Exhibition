# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一系列文字版本迭代，每次用叉號標記舊版本並淡入新版本。



from manim import *
class ManyIterations(Scene):
    def construct(self):
        words = VGroup(*[
            Text(word, alignment="left")
            for word in [
                "Winding numbers, v1",
                "Winding numbers, v2\n(center on domain coloring)",
                "Winding numbers, v3\n(clarify visuals of 2d functions)",
                "Winding numbers, v4\n(postpone topology examples for part 2)",
                "Winding numbers, v5\n(start down wrong path)",
            ]
        ])
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        words.scale(0.75)
        words.to_edge(RIGHT)

        self.add(words[0])
        for last_word, word in zip(words, words[1:]):
            cross = Cross(last_word)
            self.play(Create(cross))
            self.play(FadeIn(word))
        self.wait()
