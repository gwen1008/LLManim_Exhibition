# Source: 3b1b/_2019/diffyq/part2/staging.py
# Description: [3b1b translated] 展示熱傳導方程作為縮圖，包含方程、圖像、問句和箭頭。



from manim import *
class Thumbnail(Scene):
    def construct(self):
        image = ImageMobject("HeatSurfaceExampleFlipped")
        image.set_height(6.5)
        image.to_edge(DOWN, buff=-SMALL_BUFF)
        self.add(image)

        equation = MathTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            tex_to_color_map={
                "{t}": YELLOW,
                "{T}": RED,
            }
        )
        equation.scale(2)
        equation.to_edge(UP)

        self.add(equation)

        Group(equation, image).shift(1.5 * RIGHT)

        question = Text("What is\nthis?", font_size=72)
        question.scale(2.5)
        question.to_edge(LEFT)
        arrow = Arrow(
            question.get_top(),
            equation.get_left(),
            buff=0.5,
            path_arc=-90 * DEGREES,
        )
        arrow.set_stroke(width=5)

        self.add(question, arrow)
