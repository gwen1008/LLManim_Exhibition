# Source: 3b1b/_2019/diffyq/part2/heat_equation.py
# Description: [3b1b translated] 展示牛頓冷卻定律的圖形，包含溫度隨時間變化的指數衰減曲線、初始水溫與室溫標示，以及微分方程的視覺化推導。


from manim import *
import numpy as np

class ShowNewtonsLawGraph(Scene):
    def __init__(
        self,
        k=0.2,
        initial_water_temp=80,
        room_temp=20,
        delta_T_color=YELLOW,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.k = k
        self.initial_water_temp = initial_water_temp
        self.room_temp = room_temp
        self.delta_T_color = delta_T_color

    def construct(self):
        self.setup_axes()
        self.show_temperatures()
        self.show_graph()
        self.show_equation()
        self.talk_through_examples()

    def setup_axes(self):
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 20],
            y_length=6,
            tips=False,
        )
        axes.shift(5 * LEFT + 2.5 * DOWN)
        
        # 添加坐標軸標籤
        x_label = Text("Time").scale(0.7)
        x_label.next_to(axes.x_axis, DOWN, buff=MED_SMALL_BUFF)
        
        y_label = MathTex("\\text{Temperature}")
        y_label.next_to(axes.y_axis, RIGHT, buff=SMALL_BUFF)
        y_label.align_to(axes, UP)
        
        # 添加坐標軸數字
        y_numbers = VGroup(*[
            Integer(y).scale(0.5).next_to(
                axes.c2p(0, y), LEFT, buff=SMALL_BUFF
            )
            for y in range(20, 100, 20)
        ])
        
        x_numbers = VGroup(*[
            Integer(x).scale(0.5).next_to(
                axes.c2p(x, 0), DOWN, buff=SMALL_BUFF
            )
            for x in range(1, 11)
        ])
        
        self.add(axes, x_label, y_label, x_numbers, y_numbers)
        self.axes = axes

    def show_temperatures(self):
        axes = self.axes

        water_dot = Dot(color=BLUE)
        water_dot.move_to(axes.c2p(0, self.initial_water_temp))
        
        room_line = DashedLine(
            axes.c2p(0, self.room_temp),
            axes.c2p(10, self.room_temp),
            color=BLUE,
        )

        water_arrow = Arrow(
            start=water_dot.get_right() + RIGHT * SMALL_BUFF,
            end=water_dot.get_right(),
            color=WHITE,
            buff=0
        )
        water_words = Text("Initial water\ntemperature", font_size=24)
        water_words.next_to(water_arrow, RIGHT)

        room_words = Text("Room temperature", font_size=24)
        room_words.next_to(room_line, DOWN, SMALL_BUFF)

        self.play(
            FadeIn(water_dot, shift=RIGHT),
            GrowArrow(water_arrow),
            Write(water_words),
            run_time=1,
        )
        self.play(Create(room_line))
        self.play(FadeIn(room_words, shift=DOWN))
        self.wait()

        self.water_dot = water_dot
        self.water_arrow = water_arrow
        self.water_words = water_words
        self.room_line = room_line
        self.room_words = room_words

    def show_graph(self):
        axes = self.axes
        water_dot = self.water_dot

        k = self.k
        rt = self.room_temp
        t0 = self.initial_water_temp
        
        # 定義指數衰減函數
        def temp_func(t):
            return rt + (t0 - rt) * np.exp(-k * t)
        
        graph = axes.plot(temp_func, color=BLUE)

        def get_x():
            return axes.x_axis.p2n(water_dot.get_center())

        brace_line = always_redraw(lambda: Line(
            axes.c2p(get_x(), rt),
            water_dot.get_center(),
            stroke_width=0,
        ))
        brace = always_redraw(
            lambda: Brace(
                brace_line, RIGHT, buff=SMALL_BUFF
            )
        )

        delta_T = MathTex("\\Delta T")
        delta_T.set_color(self.delta_T_color)
        delta_T.add_updater(lambda m: m.next_to(
            brace, RIGHT, SMALL_BUFF
        ))

        self.add(brace_line)
        self.play(
            GrowFromCenter(brace),
            Write(delta_T),
        )
        
        # 創建水點沿著曲線移動的動畫
        def update_dot(mob, alpha):
            t = 10 * alpha  # 時間從0到10
            y = temp_func(t)
            mob.move_to(axes.c2p(t, y))
        
        self.play(
            Create(graph),
            UpdateFromAlphaFunc(water_dot, update_dot),
            run_time=10,
            rate_func=linear,
        )
        self.wait()

        self.graph = graph
        self.brace = brace
        self.delta_T = delta_T

    def show_equation(self):
        delta_T = self.delta_T

        equation = MathTex(
            "{d ({\\Delta T}) \\over dt} = -k \\cdot {\\Delta T}",
            tex_to_color_map={
                "{\\Delta T}": self.delta_T_color,
                "-k": WHITE,
                "=": WHITE,
            }
        )
        equation.to_corner(UR)
        equation.shift(LEFT)

        # 獲取方程的各部分
        delta_T_parts = VGroup(*[
            part for part in equation
            if "\\Delta T" in part.get_tex_string()
        ])
        
        # 找到等號的位置
        eq_index = None
        for i, part in enumerate(equation):
            if "=" in part.get_tex_string():
                eq_index = i
                break
        
        if eq_index is not None:
            deriv = VGroup(*equation[:eq_index])
            prop_to = VGroup(*[
                part for part in equation
                if "-k" in part.get_tex_string()
            ])
        else:
            deriv = VGroup()
            prop_to = VGroup()
        
        parts = VGroup(deriv, prop_to, delta_T_parts[1])

        words = Text(
            "Rate of change\nis proportional to\nitself",
            font_size=24,
            line_spacing=1.2
        )
        words.next_to(equation, DOWN)
        
        colors = [BLUE, WHITE, YELLOW]
        for part, word_line, color in zip(parts, words.split("\n"), colors):
            word = Text(word_line, font_size=24, color=color)
            word.next_to(part, DOWN)
            part.word = word
            word.save_state()
        
        words_group = VGroup(*[part.word for part in parts])

        self.play(
            TransformFromCopy(
                VGroup(delta_T),
                delta_T_parts,
            ),
            Write(VGroup(*[
                part for part in equation
                if part not in delta_T_parts
            ]))
        )

        rects = VGroup()
        for part in parts:
            rect = SurroundingRectangle(
                part,
                color=part.word.get_color(),
                buff=SMALL_BUFF,
                stroke_width=2,
            )
            anims = [
                Create(rect),
                FadeIn(part.word),
            ]
            if part is parts[1] and hasattr(words_group[0], 'saved_state'):
                anims.append(Restore(words_group[0]))
            self.play(*anims)
            rects.add(rect)

        self.play(FadeOut(rects, lag_ratio=0.2))

        self.equation = equation
        self.equation_words = words_group

    def talk_through_examples(self):
        dot = self.water_dot
        graph = self.graph

        # 反向移動點沿著曲線
        self.play(
            MoveAlongPath(
                dot, graph,
                rate_func=lambda t: smooth(1 - t),
                run_time=2,
            )
        )
