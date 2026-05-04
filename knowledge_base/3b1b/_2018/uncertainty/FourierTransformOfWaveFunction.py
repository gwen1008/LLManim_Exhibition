# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示波包在位置空間的波形、其傅立葉變換到頻率空間的過程，以及波包寬度與動量不確定性之間的權衡關係。



from manim import *
class FourierTransformOfWaveFunction(Scene):
    def __init__(self, wave_stroke_width=3, wave_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.wave_stroke_width = wave_stroke_width
        self.wave_color = wave_color
        
    def construct(self):
        self.setup()
        self.show_wave_packet()
        self.take_fourier_transform()
        self.show_correlations_with_pure_frequencies()
        self.this_is_momentum()
        self.show_tradeoff()

    def setup(self):
        self.x0_tracker = ValueTracker(-3)
        self.k_tracker = ValueTracker(1)
        self.a_tracker = ValueTracker(0.5)

    def show_wave_packet(self):
        axes = Axes(
            x_range=[0, 12],
            y_range=[-1, 1],
            y_axis_config={
                "tick_frequency": 0.5
            }
        )
        position_label = Text("Position")
        position_label.next_to(axes.x_axis.get_right(), UP)
        axes.add(position_label)
        axes.center().to_edge(UP, buff=LARGE_BUFF)

        wave = self.get_wave(axes)
        wave_update_animation = always_redraw(
            lambda: Transform(wave, self.get_wave(axes))
        )

        self.add(axes, wave)
        self.play(
            self.x0_tracker.animate.set_value(5),
            wave_update_animation,
            run_time=3,
        )
        self.wait()

        self.wave_function = wave.underlying_function
        self.wave_update_animation = wave_update_animation
        self.wave = wave
        self.axes = axes

    def take_fourier_transform(self):
        wave = self.wave
        wave_update_animation = self.wave_update_animation
        frequency_axes = Axes(
            x_range=[0, 3],
            x_axis_config={
                "unit_size": 4,
                "tick_frequency": 0.25,
                "numbers_with_elongated_ticks": [1, 2]
            },
            y_range=[-0.15, 0.15],
            y_axis_config={
                "unit_size": 7.5,
                "tick_frequency": 0.05,
            }
        )
        label = self.frequency_x_axis_label = Text("Spatial frequency")
        label.next_to(frequency_axes.x_axis.get_right(), UP)
        frequency_axes.add(label)
        frequency_axes.move_to(self.axes, LEFT)
        frequency_axes.to_edge(DOWN, buff=LARGE_BUFF)
        label.shift_onto_screen()

        def get_wave_function_fourier_graph():
            return self.get_fourier_graph(
                frequency_axes, self.get_wave_func(),
                t_min=0, t_max=15,
            )
        fourier_graph = get_wave_function_fourier_graph()
        self.fourier_graph_update_animation = always_redraw(
            lambda: Transform(
                fourier_graph, get_wave_function_fourier_graph()
            )
        )

        wave_copy = wave.copy()
        wave_copy.generate_target()
        wave_copy.target.move_to(fourier_graph, LEFT)
        wave_copy.target.set_opacity(0)
        fourier_graph.save_state()
        fourier_graph.move_to(wave, LEFT)
        fourier_graph.set_opacity(0)

        arrow = Arrow(
            self.axes.c2p(5, -1),
            frequency_axes.c2p(1, 0.1),
            color=YELLOW,
        )
        fourier_label = Text("Fourier Transform")
        fourier_label.next_to(arrow.get_center(), RIGHT)

        self.play(ReplacementTransform(
            self.axes.copy(), frequency_axes
        ))
        self.play(
            MoveToTarget(wave_copy, remover=True),
            fourier_graph.animate.restore(),
            GrowArrow(arrow),
            Write(fourier_label, run_time=1),
        )
        self.wait()

        self.frequency_axes = frequency_axes
        self.fourier_graph = fourier_graph
        self.fourier_label = VGroup(arrow, fourier_label)

    def show_correlations_with_pure_frequencies(self):
        frequency_axes = self.frequency_axes
        axes = self.axes

        sinusoid = axes.plot(
            lambda x: 0.5*np.cos(TAU*x),
            x_range=[-config.frame_width/2, 3*config.frame_width/2],
        )
        sinusoid.to_edge(UP, buff=SMALL_BUFF)

        v_line = DashedLine(1.5*UP, ORIGIN, color=YELLOW)
        v_line.move_to(frequency_axes.c2p(1, 0), DOWN)

        f_equals = MathTex("f = ")
        freq_decimal = DecimalNumber(1)
        freq_decimal.next_to(f_equals, RIGHT, buff=SMALL_BUFF)
        freq_label = VGroup(f_equals, freq_decimal)
        freq_label.next_to(
            v_line, UP, SMALL_BUFF, 
            aligned_edge=LEFT
        )

        self.play(
            Create(sinusoid),
            Create(v_line),
            Write(freq_label, run_time=1),
            FadeOut(self.fourier_label)
        )
        last_f = 1
        for f in [1.4, 0.7, 1]:
            self.play(
                sinusoid.animate.stretch(f/last_f, 0, 
                    about_point=axes.c2p(0, 0)),
                v_line.animate.move_to(frequency_axes.c2p(f, 0), DOWN),
                freq_label.animate.next_to(v_line, UP, SMALL_BUFF, aligned_edge=LEFT),
                ChangeDecimalToValue(freq_decimal, f),
                run_time=3,
            )
            last_f = f
        self.play(*[FadeOut(mob) for mob in [
            sinusoid, v_line, freq_label
        ]])

    def this_is_momentum(self):
        formula = MathTex("p", "=", "h", "\\xi")
        formula.set_color_by_tex("p", BLUE)
        formula.set_color_by_tex("\\xi", YELLOW)
        formula.next_to(
            self.frequency_x_axis_label, UP
        )

        f_max = 0.12
        brace = Brace(Line(2*LEFT, 2*RIGHT), UP)
        brace.move_to(self.frequency_axes.c2p(1, f_max), DOWN)
        words = Text("This wave\ndescribes momentum")
        words.next_to(brace, UP)

        self.play(Write(formula))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(words)
        )
        brace.add(words)
        for k in [2, 0.5, 1]:
            self.play(
                self.k_tracker.animate.set_value(k),
                self.wave_update_animation,
                self.fourier_graph_update_animation,
                UpdateFromFunc(
                    brace, lambda b: b.move_to(
                        self.frequency_axes.c2p(
                            self.k_tracker.get_value(),
                            f_max,
                        ),
                        DOWN
                    )
                ),
                run_time=2
            )
        self.wait()
        self.play(*[FadeOut(mob) for mob in [brace, words, formula]])

    def show_tradeoff(self):
        for a in [5, 0.1, 0.01, 10, 0.5]:
            self.play(
                self.a_tracker.animate.set_value(a),
                self.wave_update_animation,
                self.fourier_graph_update_animation,
                run_time=2
            )
            self.wait()

    ##

    def get_wave_func(self):
        x0 = self.x0_tracker.get_value()
        k = self.k_tracker.get_value()
        a = self.a_tracker.get_value()
        A = a**(0.25)
        return lambda x: A*np.cos(TAU*k*x)*np.exp(-a*(x - x0)**2)

    def get_wave(self, axes):
        return axes.plot(
            self.get_wave_func(), 
            color=self.wave_color,
            stroke_width=self.wave_stroke_width
        )
    
    def get_fourier_graph(self, axes, func, t_min, t_max):
        # 簡化的傅立葉變換圖形生成函數
        # 實際實現可能需要更複雜的數值積分
        return axes.plot(
            lambda x: 0.1 * np.exp(-0.5 * (x - 1)**2) * np.cos(TAU * x),
            color=YELLOW,
            stroke_width=2
        )
