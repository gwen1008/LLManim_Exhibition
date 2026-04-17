# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示「混沌理論」標題從上方向下出現，並伴隨一條水平線在標題下方繪製的動畫。



from manim import *
class ChaosTitle(Scene):
    def construct(self):
        title = Text("Chaos theory")
        title.scale(1.5)
        title.to_edge(UP)
        line = Line(LEFT, RIGHT)
        line.set_width(config.frame_width - 1)
        line.next_to(title, DOWN)

        self.play(
            Write(title),
            Create(line),
        )
        self.wait()
