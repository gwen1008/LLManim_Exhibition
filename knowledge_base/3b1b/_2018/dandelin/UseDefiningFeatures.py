# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示一個問題解決技巧的文字提示，標題在上方，黃色提示文字從下方寫入。



from manim import *
class UseDefiningFeatures(Scene):
    def construct(self):
        title = Text("Problem-solving tip:", font_size=48)
        title.to_edge(UP)
        
        tip = Text(
            """- Make sure you're using all the
            defining features of the objects
            involved.""",
            color=YELLOW,
            font_size=36,
            line_spacing=1.2
        )
        tip.next_to(title, DOWN, buff=MED_LARGE_BUFF)
        tip.shift(MED_SMALL_BUFF * RIGHT)

        self.add(title)
        self.play(Write(tip, run_time=4))
        self.wait()
