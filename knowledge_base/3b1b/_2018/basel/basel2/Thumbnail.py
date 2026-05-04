# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示巴塞爾問題的視覺化縮圖，包含圓形湖泊上的光源和數學公式。



from manim import *
class Thumbnail(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.light_source_config = {
            "num_levels": 250,
            "radius": 10.0,
            "max_opacity_ambient": 1.0,
            "opacity_function": lambda x: 1 / (1 + 0.25 * x + x**2)  # inverse_quadratic(1,0.25,1) 的近似
        }

    def construct(self):
        equation = MathTex(
            "1", "+", "{1\\over 4}", "+",
            "{1\\over 9}", "+", "{1\\over 16}", "+",
            "{1\\over 25}", "+", "\\cdots"
        )
        equation.scale(1.8)
        equation.move_to(2 * UP)
        equation.set_color(RED)
        equation.set_stroke(width=1)

        answer = MathTex("= \\frac{\\pi^2}{6}", color=LIGHT_COLOR)
        answer.scale(3)
        answer.set_color(RED)
        answer.set_stroke(width=1)
        answer.move_to(1.25 * DOWN)

        lake_radius = 6
        lake_center = ORIGIN

        lake = Circle(
            fill_color=BLUE,
            fill_opacity=0.15,
            radius=lake_radius,
            stroke_color=BLUE_D,
            stroke_width=3,
        )
        lake.move_to(lake_center)

        # 簡化光源效果：用 Dot 替代
        for i in range(16):
            theta = -TAU / 4 + (i + 0.5) * TAU / 16
            pos = lake_center + lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            light = Dot(point=pos, color=YELLOW, radius=0.2)
            lake.add(light)

        self.add(lake)
        self.add(equation, answer)
        self.wait()
