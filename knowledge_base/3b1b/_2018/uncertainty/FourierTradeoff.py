# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示高斯波包在時間域和頻率域之間的傅立葉變換關係，並通過調整波包寬度來演示不確定性原理。


from manim import *
import numpy as np

class FourierTradeoff(Scene):
    def __init__(self, show_text=True, complex_to_real_func=lambda z: z.real, widths=[6, 0.02, 1], **kwargs):
        super().__init__(**kwargs)
        self.show_text = show_text
        self.complex_to_real_func = complex_to_real_func
        self.widths = widths

    def construct(self):
        # Setup axes
        time_mean = 4
        time_axes = Axes(
            x_range=[0, 2*time_mean],
            y_range=[-2, 2],
            x_length=1.5*(2*time_mean),
            y_length=0.5*4,
            axis_config={"include_numbers": False},
        )
        time_label = Text("Time", font_size=36)
        time_label.next_to(
            time_axes.x_axis.get_right(), UP+LEFT,
            buff=MED_SMALL_BUFF,
        )
        time_axes.add(time_label)
        time_axes.center().to_edge(UP)
        # Add numbers to x-axis
        time_axes.x_axis.add_numbers(
            *list(range(1, 2*time_mean)),
            font_size=24
        )

        frequency_axes = Axes(
            x_range=[0, 8],
            y_range=[-0.025, 0.075],
            x_length=1.5*8,
            y_length=30*0.1,  # unit_size * range
            axis_config={
                "include_numbers": False,
                "color": TEAL,
            },
        )
        frequency_label = Text("Frequency", font_size=36)
        frequency_label.next_to(
            frequency_axes.x_axis.get_right(), UP+LEFT,
            buff=MED_SMALL_BUFF,
        )
        frequency_label.set_color(TEAL)
        frequency_axes.add(frequency_label)
        frequency_axes.move_to(time_axes, LEFT)
        frequency_axes.to_edge(DOWN, buff=LARGE_BUFF)
        frequency_axes.x_axis.add_numbers(font_size=24)

        # Graph information
        # x-coordinate of this point determines width of wave_packet graph
        width_tracker = ValueTracker(0.5)
        get_width = width_tracker.get_value

        def get_wave_packet_function():
            factor = 1./get_width()
            return lambda t: (factor**0.25)*np.cos(4*TAU*t)*np.exp(-factor*(t-time_mean)**2)

        def get_wave_packet():
            graph = time_axes.plot(
                get_wave_packet_function(),
                x_range=[0, 2*time_mean],
                color=YELLOW,
                use_smoothing=True
            )
            return graph

        time_radius = 10
        def get_wave_packet_fourier_transform():
            # Simplified Fourier transform visualization
            # In practice, you might want to implement a proper Fourier transform
            # For now, we'll create a placeholder graph
            def freq_func(f):
                # Approximate Gaussian in frequency domain
                width = get_width()
                return 0.05*np.exp(-(f-4)**2/(2*width))
            
            graph = frequency_axes.plot(
                freq_func,
                x_range=[0, 8],
                color=TEAL,
                use_smoothing=True
            )
            return graph

        wave_packet = get_wave_packet()
        fourier_graph = get_wave_packet_fourier_transform()

        arrow = Arrow(
            wave_packet.get_center(),
            frequency_axes.c2p(4, frequency_axes.y_range[1]/2),
            color=TEAL,
            buff=0.1
        )
        fourier_words = Text("Fourier Transform", font_size=30)
        fourier_words.next_to(arrow, LEFT, buff=MED_LARGE_BUFF)
        sub_words = Text("(To be explained shortly)", font_size=18)
        sub_words.set_color(BLUE)
        sub_words.next_to(fourier_words, DOWN)

        # Draw items
        self.add(time_axes, frequency_axes)
        self.play(Create(wave_packet, rate_func=double_smooth))
        
        anims = [TransformFromCopy(wave_packet, fourier_graph)]
        if self.show_text:
            anims += [
                GrowArrow(arrow),
                Write(fourier_words, run_time=1)
            ]
        self.play(*anims)
        self.wait()
        
        for width in self.widths:
            self.play(
                width_tracker.animate.set_value(width),
                wave_packet.animate.become(get_wave_packet()),
                fourier_graph.animate.become(get_wave_packet_fourier_transform()),
                run_time=3
            )
            if self.show_text and sub_words not in self.mobjects:
                self.play(FadeIn(sub_words, shift=DOWN))
            else:
                self.wait()
        self.wait()
