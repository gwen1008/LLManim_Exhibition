# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個用維恩圖說明散度和旋度在流體流動等領域應用的動畫場景。



from manim import *
class IllustrationUseVennDiagram(Scene):
    def construct(self):
        title = Title("Divergence \\& Curl")
        title.to_edge(UP, buff=MED_SMALL_BUFF)

        useful_for = TexText("Useful for")
        useful_for.next_to(title, DOWN)
        useful_for.set_color(BLUE)

        fluid_flow = TexText("Fluid \\\\ flow")
        fluid_flow.next_to(ORIGIN, UL)
        ff_circle = Circle(color=YELLOW)
        ff_circle.surround(fluid_flow, stretch=True)
        fluid_flow.set_color(ff_circle.get_color())

        big_circle = Circle(
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_color=BLUE,
        )
        big_circle.stretch_to_fit_width(9)
        big_circle.stretch_to_fit_height(6)
        big_circle.next_to(useful_for, DOWN, SMALL_BUFF)

        illustrated_by = TexText("Illustrated by")
        illustrated_by.next_to(
            big_circle.point_from_proportion(3. / 8), UL
        )
        illustrated_by.set_color(ff_circle.get_color())
        illustrated_by_arrow = Arrow(
            illustrated_by.get_bottom(),
            ff_circle.get_left(),
            path_arc=90 * DEGREES,
            color=YELLOW,
        )
        # 在 ManimCE 中，Arrow 沒有 pointwise_become_partial 方法
        # 我們可以用 set_stroke 模擬部分箭頭效果，但這裡為了保持簡單，先省略
        # 或者使用 VMobject 的 become_partial 方法
        illustrated_by_arrow.become_partial(illustrated_by_arrow, 0, 0.95)

        examples = VGroup(
            TexText("Electricity"),
            TexText("Magnetism"),
            TexText("Phase flow"),
            TexText("Stokes' theorem"),
        )
        points = [
            2 * RIGHT + 0.5 * UP,
            2 * RIGHT + 0.5 * DOWN,
            2 * DOWN,
            2 * LEFT + DOWN,
        ]
        for example, point in zip(examples, points):
            example.move_to(point)

        self.play(Write(title), run_time=1)
        self.play(
            Write(illustrated_by),
            Create(illustrated_by_arrow),
            run_time=1,
        )
        self.play(
            Create(ff_circle),
            FadeIn(fluid_flow),
        )
        self.wait()
        self.play(
            Write(useful_for),
            DrawBorderThenFill(big_circle),
            Animation(fluid_flow),
            Animation(ff_circle),
        )
        self.play(LaggedStartMap(
            FadeIn, examples,
            run_time=3,
        ))
        self.wait()
