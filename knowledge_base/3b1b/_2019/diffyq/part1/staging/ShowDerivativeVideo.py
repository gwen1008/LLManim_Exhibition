# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示兩個標題的替換動畫，並在標題下方顯示一個帶有動態邊界的黑色矩形區域。



from manim import *
class ShowDerivativeVideo(Scene):
    def construct(self):
        title = Tex("Essence of", "Calculus")
        title.scale(1.5)
        title.to_edge(UP)

        title2 = Tex("Essence of", "Linear Algebra")
        title2.scale(1.5)
        title2.move_to(title, DOWN)

        rect = ScreenRectangle(height=6)
        rect = rect.copy()
        rect.set_style(
            fill_opacity=1,
            fill_color=BLACK,
            stroke_width=0,
        )
        rect.next_to(title, DOWN)
        animated_rect = AnimatedBoundary(rect)

        self.add(title, rect)
        self.add(animated_rect)
        self.wait(5)
        self.play(ReplacementTransform(title, title2))
        self.wait(10)
