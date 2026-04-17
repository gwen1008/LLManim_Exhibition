# Source: 3b1b/_2019/diffyq/part2/wordy_scenes.py
# Description: [3b1b translated] 展示兩個標題分別從上方淡入，一個在左側，一個在右側。



from manim import *
class TwoGraphTypeTitles(Scene):
    def construct(self):
        left_title = Text(
            "Represent time\nwith actual time"
        )
        left_title.shift(config.frame_width * LEFT / 4)
        right_title = Text(
            "Represent time\nwith an axis"
        )
        right_title.shift(config.frame_width * RIGHT / 4)

        titles = VGroup(left_title, right_title)
        for title in titles:
            title.scale(1.25)
            title.to_edge(UP)

        self.play(FadeIn(right_title, shift=DOWN))
        self.wait()
        self.play(FadeIn(left_title, shift=DOWN))
        self.wait()
