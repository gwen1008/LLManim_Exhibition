# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示巴塞爾問題的視覺化證明，透過數線、光源和分數項的動畫，說明奇數項與偶數項的關係，最終導出 π²/6 的結果。


from manim import *
import numpy as np

class FinalSumManipulationScene(PiCreatureScene):
    def construct(self):
        LAKE_COLOR = BLUE
        LAKE_OPACITY = 0.15
        LAKE_STROKE_WIDTH = 5.0
        LAKE_STROKE_COLOR = BLUE
        TEX_SCALE = 0.8

        LIGHT_COLOR = YELLOW  # 補充定義（原代碼未定義）
        LIGHT_COLOR2 = RED
        LIGHT_COLOR3 = BLUE

        unit_length = 1.5
        vertical_spacing = 2.5 * DOWN
        switch_on_time = 0.2

        sum_vertical_spacing = 1.5

        randy = self.pi_creature  # ManimCE 中 PiCreatureScene 的屬性名
        randy.set_color(MAROON_D)
        randy.color = MAROON_D
        randy.scale(0.7).flip().to_edge(DOWN + LEFT)
        self.wait()

        # 自定義光源類（簡化實現）
        class LightSource(VGroup):
            def __init__(self, radius=1, num_levels=10, max_opacity_ambient=0.5, opacity_function=None, color=YELLOW):
                super().__init__()
                self.lighthouse = Circle(radius=radius/10, color=color, fill_opacity=1)
                self.ambient_light = VGroup()
                for i in range(num_levels):
                    r = radius * (i+1)/num_levels
                    circle = Circle(radius=r, color=color, fill_opacity=max_opacity_ambient*(num_levels-i)/num_levels)
                    self.ambient_light.add(circle)
                self.add(self.lighthouse, self.ambient_light)
                self.color = color
            
            def move_source_to(self, point):
                self.move_to(point)
                return self

        ls_template = LightSource(
            radius = 1,
            num_levels = 10,
            max_opacity_ambient = 0.5,
            opacity_function = None,  # 省略原函數
            color = LIGHT_COLOR
        )

        odd_range = np.arange(1,9,2)
        even_range = np.arange(2,16,2)
        full_range = np.arange(1,8,1)

        self.number_line1 = NumberLine(
            x_range = [0, 11, 1],  # ManimCE 使用 x_range
            length = 11 * unit_length,  # 通過長度控制
            color = LAKE_STROKE_COLOR,
            stroke_width = LAKE_STROKE_WIDTH,
            include_tip = True,
            include_ticks = True,
            tick_size = 0.1,
        )
        self.number_line1.next_to(2.5 * UP + 3 * LEFT, RIGHT, buff = 0.3)
        # 手動添加數字標籤
        for i in range(0, 12):
            num = Integer(i).scale(0.5).next_to(self.number_line1.n2p(i), UP, buff=SMALL_BUFF)
            self.number_line1.add(num)

        odd_lights = VGroup()
        for i in odd_range:
            pos = self.number_line1.n2p(i)
            ls = ls_template.copy()
            ls.move_source_to(pos)
            odd_lights.add(ls)

        self.play(
            Create(self.number_line1, run_time = 5),
        )
        self.wait()

        odd_terms = VGroup()
        for i in odd_range:
            if i == 1:
                term = MathTex(r"\phantom{+\,\,\,}{1\over " + str(i) + "^2}",
                    color = LIGHT_COLOR)
            else:
                term = MathTex(r"+\,\,\, {1\over " + str(i) + "^2}",
                    color = LIGHT_COLOR)

            term.next_to(self.number_line1.n2p(i), DOWN, buff = 1.5)
            odd_terms.add(term)

        for (ls, term) in zip(odd_lights.submobjects, odd_terms.submobjects):
            self.play(
                FadeIn(ls.lighthouse, run_time = switch_on_time),
                FadeIn(ls.ambient_light, run_time = switch_on_time),  # SwitchOn 改為 FadeIn
                Write(term, run_time = switch_on_time)
            )

        result1 = MathTex(r"{\pi^2\over 8} =", color = LIGHT_COLOR)
        result1.next_to(self.number_line1, LEFT, buff = 0.5)
        result1.shift(0.87 * vertical_spacing)
        self.play(Write(result1))

        self.number_line2 = self.number_line1.copy()
        self.number_line2.shift(2 * vertical_spacing)

        full_lights = VGroup()
        for i in full_range:
            pos = self.number_line2.n2p(i)
            ls = LightSource(color=LIGHT_COLOR3)  # 重新創建
            ls.move_source_to(pos)
            full_lights.add(ls)

        self.play(
            Create(self.number_line2, run_time = 5),
        )
        self.wait()

        full_lighthouses = VGroup()
        full_ambient_lights = VGroup()
        for ls in full_lights:
            full_lighthouses.add(ls.lighthouse)
            full_ambient_lights.add(ls.ambient_light)

        self.play(
            LaggedStartMap(FadeIn, full_lighthouses, lag_ratio = 0.2, run_time = 3),
        )
        self.play(
            LaggedStartMap(FadeIn, full_ambient_lights, lag_ratio = 0.2, run_time = 3)  # SwitchOn 改為 FadeIn
        )

        even_terms = VGroup()
        for i in even_range:
            term = MathTex(r"+\,\,\, {1\over " + str(i) + "^2}", color = LIGHT_COLOR2)
            term.next_to(self.number_line1.n2p(i), DOWN, buff = sum_vertical_spacing)
            even_terms.add(term)

        even_lights = VGroup()
        for i in even_range:
            pos = self.number_line1.n2p(i)
            ls = LightSource(color=LIGHT_COLOR2)
            ls.move_source_to(pos)
            even_lights.add(ls)

        for (ls, term) in zip(even_lights.submobjects, even_terms.submobjects):
            self.play(
                FadeIn(ls.ambient_light, run_time = switch_on_time),  # SwitchOn 改為 FadeIn
                Write(term)
            )
        self.wait()

        # now morph the even lights into the full lights
        full_lights_copy = full_lights.copy()
        even_lights_copy = even_lights.copy()

        self.play(
            Transform(even_lights, full_lights, run_time = 2)
        )
        self.wait()

        for i in range(6):
            self.play(
                Transform(even_lights[i], even_lights_copy[i])
            )
            self.wait()

        # draw arrows
        P1 = self.number_line2.n2p(1)
        P2 = even_terms.submobjects[0].get_center()
        Q1 = interpolate(P1, P2, 0.2)
        Q2 = interpolate(P1, P2, 0.8)
        quarter_arrow = Arrow(Q1, Q2, color = LIGHT_COLOR2)
        quarter_label = MathTex(r"\times {1\over 4}", color = LIGHT_COLOR2)
        quarter_label.scale(0.7)
        quarter_label.next_to(quarter_arrow.get_center(), RIGHT)

        self.play(
            Create(quarter_arrow),
            Write(quarter_label),
        )
        self.wait()

        P3 = odd_terms.submobjects[0].get_center()
        R1 = interpolate(P1, P3, 0.2)
        R2 = interpolate(P1, P3, 0.8)
        three_quarters_arrow = Arrow(R1, R2, color = LIGHT_COLOR)
        three_quarters_label = MathTex(r"\times {3\over 4}", color = LIGHT_COLOR)
        three_quarters_label.scale(0.7)
        three_quarters_label.next_to(three_quarters_arrow.get_center(), LEFT)

        self.play(
            Create(three_quarters_arrow),
            Write(three_quarters_label)
        )
        self.wait()

        four_thirds_arrow = Arrow(R2, R1, color = LIGHT_COLOR)
        four_thirds_label = MathTex(r"\times {4\over 3}", color = LIGHT_COLOR)
        four_thirds_label.scale(0.7)
        four_thirds_label.next_to(four_thirds_arrow.get_center(), LEFT)

        self.play(
            FadeOut(quarter_label),
            FadeOut(quarter_arrow),
            FadeOut(even_lights),
            FadeOut(even_terms)
        )
        self.wait()

        self.play(
            ReplacementTransform(three_quarters_arrow, four_thirds_arrow),
            ReplacementTransform(three_quarters_label, four_thirds_label)
        )
        self.wait()

        full_terms = VGroup()
        for i in range(1,8):
            if i == 1:
                term = MathTex(r"\phantom{+\,\,\,}{1\over " + str(i) + "^2}", color = LIGHT_COLOR3)
            elif i == 7:
                term = MathTex(r"+\,\,\,\dots", color = LIGHT_COLOR3)
            else:
                term = MathTex(r"+\,\,\, {1\over " + str(i) + "^2}", color = LIGHT_COLOR3)

            term.move_to(self.number_line2.n2p(i))
            full_terms.add(term)

        self.play(
            FadeOut(self.number_line1),
            FadeOut(odd_lights),
            FadeOut(self.number_line2),
            FadeOut(full_lights),
            FadeIn(full_terms)
        )
        self.wait()

        v = (sum_vertical_spacing + 0.5) * UP
        self.play(
            odd_terms.animate.shift(v),
            result1.animate.shift(v),
            four_thirds_arrow.animate.shift(v),
            four_thirds_label.animate.shift(v),
            full_terms.animate.shift(v)
        )

        arrow_copy = four_thirds_arrow.copy()
        label_copy = four_thirds_label.copy()
        arrow_copy.shift(2.5 * LEFT)
        label_copy.shift(2.5 * LEFT)

        self.play(
            FadeIn(arrow_copy),
            FadeIn(label_copy)
        )
        self.wait()

        final_result = MathTex(r"{\pi^2 \over 6}=", color = LIGHT_COLOR3)
        final_result.next_to(arrow_copy, DOWN)

        self.play(
            Write(final_result),
            randy.change("hooray")  # 模式改變語法
        )
        self.wait()

        equation = VGroup()
        equation.add(final_result)
        equation.add(full_terms)

        self.play(
            FadeOut(result1),
            FadeOut(odd_terms),
            FadeOut(arrow_copy),
            FadeOut(label_copy),
            FadeOut(four_thirds_arrow),
            FadeOut(four_thirds_label),
            full_terms.animate.shift(LEFT),
        )
        self.wait()

        self.play(equation.animate.shift(-equation.get_center()[1] * UP + UP + 1.5 * LEFT))

        result_box = Rectangle(width = 1.1 * equation.get_width(),
            height = 2 * equation.get_height(), color = LIGHT_COLOR3)
        result_box.move_to(equation)

        self.play(
            Create(result_box)
        )
        self.wait()
