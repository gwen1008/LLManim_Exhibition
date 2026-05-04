# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 在場景中央顯示一條垂直線和一個黃色箭頭，上方有帶背景框的標題文字 "Quaternions visualized"。



from manim import *
class ThumbnailOverlay(Scene):
    def construct(self):
        title = MathTex(r"\text{Quaternions} \\", r"\text{visualized}")
        title.set_width(7)
        # title[1].scale(0.7, about_edge=UP)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        v_line = Line(DOWN, UP)
        v_line.set_height(config.frame_height)

        title.set_background_stroke(color=BLACK, width=1)

        for part in (title[0][4:6], title[1][4:5]):
            rect = BackgroundRectangle(part)
            rect.set_fill(opacity=1)
            rect.stretch(0.9, 0)
            rect.stretch(1.1, 1)
            title.add_to_back(rect)
        # title.add_to_back(BackgroundRectangle(title[0]))

        arrow = Arrow(LEFT, RIGHT)
        arrow.scale(1.5)
        arrow.tip.scale(2)
        arrow.set_stroke(width=10)
        arrow.set_color(YELLOW)

        self.add(v_line)
        self.add(arrow)
        self.add(title)
