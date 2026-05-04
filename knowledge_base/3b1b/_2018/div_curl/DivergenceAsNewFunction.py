# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示向量場的散度計算，透過移動點顯示輸入座標與輸出向量，並在點周圍繪製向量環和流線來視覺化散度。


from manim import *
import itertools as it
import random

class DivergenceAsNewFunction(Scene):
    def construct(self):
        self.add_plane()
        self.show_vector_field_function()
        self.show_divergence_function()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        self.add(plane)

    def show_vector_field_function(self):
        func = self.func
        unscaled_vector_field = VectorField(
            func,
            length_func=lambda norm: norm,
            colors=[BLUE_C, YELLOW, RED],
            delta_x=np.inf,
            delta_y=np.inf,
        )

        in_dot = Dot(color=PINK)
        in_dot.move_to(3.75 * LEFT + 1.25 * UP)

        def get_input():
            return in_dot.get_center()

        def get_out_vect():
            return unscaled_vector_field.get_vector(get_input())

        # Tex
        func_tex = MathTex(
            "\\textbf{F}(", "+0.00", ",", "+0.00", ")", "=",
        )
        dummy_in_x, dummy_in_y = func_tex.get_parts_by_tex("+0.00")
        func_tex.add_background_rectangle()
        rhs = DecimalMatrix(
            [[0], [0]],
            element_to_mobject_config={
                "num_decimal_places": 2,
                "include_sign": True,
            },
            include_background_rectangle=True
        )
        rhs.next_to(func_tex, RIGHT)
        dummy_out_x, dummy_out_y = rhs.get_mob_matrix().flatten()

        VGroup(func_tex, rhs).to_corner(UL, buff=MED_SMALL_BUFF)

        VGroup(
            dummy_in_x, dummy_in_y,
            dummy_out_x, dummy_out_y,
        ).set_fill(BLACK, opacity=0)

        # Changing decimals
        in_x, in_y, out_x, out_y = [
            DecimalNumber(0, include_sign=True)
            for x in range(4)
        ]
        VGroup(in_x, in_y).set_color(in_dot.get_color())
        VGroup(out_x, out_y).set_color(get_out_vect().get_fill_color())
        
        # 使用 always_redraw 替代 ContinualChangingDecimal
        in_x_always = always_redraw(
            lambda: DecimalNumber(get_input()[0], include_sign=True)
            .set_color(in_dot.get_color())
            .move_to(dummy_in_x)
        )
        in_y_always = always_redraw(
            lambda: DecimalNumber(get_input()[1], include_sign=True)
            .set_color(in_dot.get_color())
            .move_to(dummy_in_y)
        )
        out_x_always = always_redraw(
            lambda: DecimalNumber(func(get_input())[0], include_sign=True)
            .set_color(get_out_vect().get_fill_color())
            .move_to(dummy_out_x)
        )
        out_y_always = always_redraw(
            lambda: DecimalNumber(func(get_input())[1], include_sign=True)
            .set_color(get_out_vect().get_fill_color())
            .move_to(dummy_out_y)
        )

        self.add(func_tex, rhs)

        # 添加 always_redraw 物件
        self.add(in_x_always, in_y_always)

        in_dot.save_state()
        in_dot.move_to(ORIGIN)
        self.play(in_dot.animate.restore())
        self.wait()
        
        # 替換轉場動畫
        self.play(
            ReplacementTransform(
                in_x_always.copy().set_opacity(0),
                out_x_always,
            ),
            ReplacementTransform(
                in_y_always.copy().set_opacity(0),
                out_y_always,
            )
        )
        
        out_vect = get_out_vect()
        VGroup(out_x_always, out_y_always).match_style(out_vect)
        out_vect.save_state()
        out_vect.move_to(rhs)
        out_vect.set_fill(opacity=0)
        self.play(out_vect.animate.restore())
        
        # 使用 always_redraw 更新輸出向量
        out_vect_always = always_redraw(lambda: get_out_vect())
        self.add(out_vect_always)

        self.add(out_x_always, out_y_always)

        # 更新樣式
        def update_style(m):
            m.match_style(out_vect_always)
        self.add(always_redraw(lambda: update_style(VGroup(out_x_always, out_y_always))))
        self.wait()

        for vect in DOWN, 2 * RIGHT, UP:
            self.play(
                in_dot.animate.shift(3 * vect),
                run_time=3
            )
            self.wait()

        self.in_dot = in_dot
        self.out_vect = out_vect_always
        self.func_equation = VGroup(func_tex, rhs)
        self.out_x, self.out_y = out_x_always, out_y_always
        self.in_x, self.in_y = in_x_always, in_y_always
        self.in_x_always = in_x_always
        self.in_y_always = in_y_always
        self.out_x_always = out_x_always
        self.out_y_always = out_y_always

    def show_divergence_function(self):
        vector_field = VectorField(self.func)
        vector_field.remove(*[
            v for v in vector_field
            if v.get_start()[0] < 0 and v.get_start()[1] > 2
        ])
        vector_field.set_fill(opacity=0.5)
        in_dot = self.in_dot

        def get_neighboring_points(step_sizes=[0.3], n_angles=12):
            point = in_dot.get_center()
            return list(it.chain(*[
                [
                    point + step_size * step
                    for step in compass_directions(n_angles)
                ]
                for step_size in step_sizes
            ]))

        def get_vector_ring():
            return VGroup(*[
                vector_field.get_vector(point)
                for point in get_neighboring_points()
            ])

        def get_stream_lines():
            return StreamLines(
                self.func,
                start_points_generator=get_neighboring_points,
                start_points_generator_config={
                    "step_sizes": np.arange(0.1, 0.5, 0.1)
                },
                virtual_time=1,
                stroke_width=3,
            )

        def show_flow():
            stream_lines = get_stream_lines()
            random.shuffle(stream_lines.submobjects)
            self.play(LaggedStart(
                *[Create(line) for line in stream_lines],
                lag_ratio=0.1
            ))
            self.play(FadeOut(stream_lines))

        vector_ring = get_vector_ring()
        vector_ring_always = always_redraw(lambda: get_vector_ring())

        func_tex, rhs = self.func_equation
        out_x, out_y = self.out_x_always, self.out_y_always
        div_tex = MathTex("\\text{div}")
        div_tex.add_background_rectangle()
        div_tex.move_to(func_tex, LEFT)
        div_tex.shift(2 * SMALL_BUFF * RIGHT)

        self.remove(self.out_x_always, self.out_y_always)
        self.remove(self.out_vect)
        self.add(self.in_x_always, self.in_y_always)
        self.play(
            func_tex.animate.next_to(div_tex, RIGHT, SMALL_BUFF),
            Write(div_tex),
            FadeOut(self.out_vect),
            FadeOut(out_x),
            FadeOut(out_y),
            FadeOut(rhs),
        )
        
        # 添加虛擬更新器
        def dummy_updater(m):
            m.set_opacity(0)
        self.add(always_redraw(lambda: dummy_updater(out_x)))
        self.add(always_redraw(lambda: dummy_updater(out_y)))
        
        self.add_foreground_mobjects(div_tex)
        self.play(
            LaggedStart(*[GrowArrow(v) for v in vector_field], lag_ratio=0.1),
            LaggedStart(*[GrowArrow(v) for v in vector_ring], lag_ratio=0.1),
        )
        self.add(vector_ring_always)
        self.wait()

        div_func = divergence(self.func)
        div_rhs = DecimalNumber(
            0, include_sign=True,
        )
        div_rhs.add_background_rectangle()
        
        div_rhs_always = always_redraw(
            lambda: DecimalNumber(
                div_func(in_dot.get_center()),
                include_sign=True,
            ).add_background_rectangle()
            .next_to(func_tex, RIGHT, SMALL_BUFF)
        )

        self.play(FadeIn(div_rhs_always))
        self.add(div_rhs_always)
        show_flow()

        for vect in 2 * RIGHT, 3 * DOWN, 2 * LEFT, 2 * LEFT:
            self.play(in_dot.animate.shift(vect), run_time=3)
            show_flow()
        self.wait()

    def func(self, point):
        x, y = point[:2]
        return np.sin(x + y) * RIGHT + np.sin(y * x / 3) * UP

def divergence(func):
    def div(point):
        x, y = point[:2]
        h = 0.0001
        dx = (func([x + h/2, y, 0])[0] - func([x - h/2, y, 0])[0]) / h
        dy = (func([x, y + h/2, 0])[1] - func([x, y - h/2, 0])[1]) / h
        return dx + dy
    return div

def compass_directions(n=12, start_vect=RIGHT):
    angle = 2 * np.pi / n
    return [rotate_vector(start_vect, k * angle) for k in range(n)]
