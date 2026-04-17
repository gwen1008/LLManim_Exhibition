# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示傅立葉變換的視覺化過程，包括時間域上的餘弦波、極坐標平面上的繞線、頻率域上的中心點軌跡，以及最終繪製出頻率響應圖。


from manim import *
import numpy as np

class DrawFrequencyPlot(WrapCosineGraphAroundCircle, PiCreatureScene):
    def __init__(
        self,
        initial_winding_frequency=3.0,
        center_of_mass_color=RED,
        center_of_mass_multiple=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.initial_winding_frequency = initial_winding_frequency
        self.center_of_mass_color = center_of_mass_color
        self.center_of_mass_multiple = center_of_mass_multiple
    
    def construct(self):
        self.remove(self.pi_creature)
        self.setup_graph()
        self.indicate_weight_of_wire()
        self.show_center_of_mass_dot()
        self.change_to_various_frequencies()
        self.introduce_frequency_plot()
        self.draw_full_frequency_plot()
        self.recap_objects_on_screen()
        self.lower_graph()
        self.label_as_almost_fourier()

    def setup_graph(self):
        self.add(self.get_time_axes())
        self.add(self.get_circle_plane())
        self.graph = self.get_cosine_wave(self.signal_frequency)
        self.add(self.graph)
        self.add(self.get_polarized_mobject(
            self.graph, self.initial_winding_frequency
        ))
        self.add(self.get_winding_frequency_label())
        self.beats_per_second_label = self.get_bps_label()
        self.add(self.beats_per_second_label)        
        self.v_lines_indicating_periods = self.get_v_lines_indicating_periods(
            self.initial_winding_frequency
        )
        self.add(self.v_lines_indicating_periods)
        self.change_frequency(1.03)
        self.wait()

    def indicate_weight_of_wire(self):
        graph = self.graph
        pol_graph = graph.polarized_mobject.copy()
        pol_graph.save_state()
        morty = self.pi_creature
        morty.change("raise_right_hand")
        morty.save_state()
        morty.change("plain")
        morty.set_opacity(0)

        self.play(
            morty.restore,
            pol_graph.animate.scale(0.5),
            pol_graph.animate.next_to(morty.get_corner(UP+LEFT), UP, -SMALL_BUFF),
        )
        self.play(
            morty.change("lower_right_hand", pol_graph.get_bottom()),
            pol_graph.animate.shift(0.45*DOWN),
            rate_func = there_and_back,
            run_time = 2,
        )
        self.wait()

        metal_wire = pol_graph.copy().set_stroke(GREY_B)
        self.play(
            Create(metal_wire),
            run_time = 2,
        )
        self.play(
            FadeOut(metal_wire),
            run_time = 0.5
        )
        self.play(
            pol_graph.restore,
            morty.change("pondering")
        )
        self.remove(pol_graph)

    def show_center_of_mass_dot(self):
        color = self.center_of_mass_color
        dot = self.get_center_of_mass_dot()
        dot.save_state()
        arrow = Arrow(
            start=dot.get_center(),
            end=dot.get_center() + DOWN+2*LEFT,
            color = color,
            buff=0
        )
        arrow.next_to(dot.get_center(), UP+RIGHT, buff = SMALL_BUFF)
        dot.move_to(arrow.get_start())
        words = Text("Center of mass")
        words.next_to(arrow.get_start(), RIGHT)
        words.set_color(color)

        self.play(
            GrowArrow(arrow),
            dot.restore,
        )
        self.play(Write(words))
        self.play(FadeOut(arrow), FadeOut(self.pi_creature))
        self.wait()

        self.generate_center_of_mass_dot_update_anim()
        self.center_of_mass_label = words

    def change_to_various_frequencies(self):
        self.change_frequency(
            3.0, run_time = 30,
            rate_func = bezier([0, 0, 1, 1])
        )
        self.wait()
        self.play(
            *self.get_vector_animations(self.graph),
            run_time = 15
        )

    def introduce_frequency_plot(self):
        wps_label = self.winding_freq_label
        wps_label.add_to_back(BackgroundRectangle(wps_label))
        com_label = self.center_of_mass_label
        com_label.add_background_rectangle()
        frequency_axes = self.get_frequency_axes()
        x_coord_label = Text("$x$-coordinate for center of mass")
        x_coord_label.set_color(self.center_of_mass_color)
        x_coord_label.scale(self.text_scale_val)
        x_coord_label.next_to(
            frequency_axes.y_axis.get_top(),
            RIGHT, aligned_edge = UP, buff = LARGE_BUFF
        )
        x_coord_label.add_background_rectangle()
        flower_path = ParametricFunction(
            lambda t : self.circle_plane.coords_to_point(
                np.sin(2*t)*np.cos(t),
                np.sin(2*t)*np.sin(t),
            ),
            t_range = [0, TAU],
        )
        flower_path.move_to(self.center_of_mass_dot)

        self.play(
            wps_label.animate.move_to(self.circle_plane.get_top()),
            com_label.animate.move_to(self.circle_plane.get_bottom()),
        )
        self.play(LaggedStart(*[FadeIn(obj) for obj in frequency_axes]))
        self.wait()
        self.play(MoveAlongPath(
            self.center_of_mass_dot, flower_path,
            run_time = 4,
        ))
        self.play(Transform(
            com_label.copy(), x_coord_label
        ))
        self.wait()

        self.x_coord_label = x_coord_label

    def draw_full_frequency_plot(self):
        graph = self.graph
        fourier_graph = self.get_fourier_transform_graph(graph)
        fourier_graph.save_state()
        fourier_graph_update = self.get_fourier_graph_drawing_update_anim(
            fourier_graph
        )
        v_line = DashedLine(
            self.frequency_axes.coords_to_point(0, 0),
            self.frequency_axes.coords_to_point(0, 1),
            stroke_width = 6,
            color = fourier_graph.get_color()
        )

        self.change_frequency(0.0)
        self.generate_fourier_dot_transform(fourier_graph)
        self.wait()
        self.play(Create(v_line))
        self.play(
            GrowFromCenter(self.fourier_graph_dot),
            FadeOut(v_line)
        )
        f_max = int(self.frequency_axes.x_max)
        for freq in [0.2, 1.5, 3.0, 4.0, 5.0]:
            fourier_graph.restore()
            self.change_frequency(
                freq,
                added_anims = [fourier_graph_update],
                run_time = 8,
            )
            self.wait()
        self.fourier_graph = fourier_graph

    def recap_objects_on_screen(self):
        rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0
        )
        time_group = VGroup(
            self.graph,
            self.time_axes,
            self.beats_per_second_label,
        ).copy()
        circle_group = VGroup(
            self.graph.polarized_mobject,
            self.circle_plane,
            self.winding_freq_label,
            self.center_of_mass_label,
            self.center_of_mass_dot,
        ).copy()
        frequency_group = VGroup(
            self.fourier_graph,
            self.frequency_axes,
            self.x_coord_label,
        ).copy()
        groups = [time_group, circle_group, frequency_group]

        self.play(FadeIn(rect))
        self.wait()
        for group in groups:
            graph_copy = group[0].copy().set_color(PINK)
            self.play(FadeIn(group))
            self.play(Create(graph_copy))
            self.play(FadeOut(graph_copy))
            self.wait()
            self.play(FadeOut(group))
        self.wait()
        self.play(FadeOut(rect))

    def lower_graph(self):
        graph = self.graph
        time_axes = self.time_axes
        shift_vect = time_axes.coords_to_point(0, 1)
        shift_vect -= time_axes.coords_to_point(0, 0)
        fourier_graph = self.fourier_graph
        new_graph = self.get_cosine_wave(
            self.signal_frequency, shift_val = 0
        )
        new_fourier_graph = self.get_fourier_transform_graph(new_graph)
        for mob in graph, time_axes, fourier_graph:
            mob.save_state()

        new_freq = 0.03
        self.change_frequency(new_freq)
        self.wait()
        self.play(
            time_axes.animate.shift(shift_vect/2),
            graph.animate.shift(-shift_vect/2),
            self.get_frequency_change_animation(
                self.graph, new_freq
            ),
            self.center_of_mass_dot_anim,
            self.get_period_v_lines_update_anim(),
            Transform(fourier_graph, new_fourier_graph),
            self.fourier_graph_dot.animate.move_to(
                self.frequency_axes.coords_to_point(new_freq, 0)
            ),
            run_time = 2
        )
        self.wait()
        self.remove(self.fourier_graph_dot)
        self.generate_fourier_dot_transform(new_fourier_graph)
        self.change_frequency(3.0, run_time = 15, rate_func=linear)
        self.wait()
        self.play(
            graph.restore, 
            time_axes.restore,
            self.get_frequency_change_animation(
                self.graph, 3.0
            ),
            self.center_of_mass_dot_anim,
            self.get_period_v_lines_update_anim(),
            fourier_graph.restore,
            Animation(self.fourier_graph_dot),
            run_time = 2
        )
        self.generate_fourier_dot_transform(self.fourier_graph)
        self.wait()
        self.play(Indicate(self.fourier_graph_dot))
        self.wait()

    def label_as_almost_fourier(self):
        x_coord_label = self.x_coord_label
        almost_fourier_label = Text(
            "``Almost Fourier Transform''",
        )
        almost_fourier_label.move_to(x_coord_label, UP+LEFT)
        x_coord_label.generate_target()
        x_coord_label.target.next_to(almost_fourier_label, DOWN)

        self.play(
            MoveToTarget(x_coord_label),
            Write(almost_fourier_label)
        )
        self.wait(2)

    ##

    def get_center_of_mass_dot(self):
        dot = Dot(
            self.get_pol_graph_center_of_mass(),
            color = self.center_of_mass_color
        )
        self.center_of_mass_dot = dot
        return dot

    def get_pol_graph_center_of_mass(self):
        pg = self.graph.polarized_mobject
        result = center_of_mass(pg.get_anchors())
        if self.center_of_mass_multiple != 1:
            mult = self.center_of_mass_multiple
            origin = self.circle_plane.coords_to_point(0, 0)
            result = mult*(result - origin) + origin
        return result

    def generate_fourier_dot_transform(self, fourier_graph):
        self.fourier_graph_dot = Dot(color = WHITE, radius = 0.05)
        def update_dot(dot):
            f = self.graph.polarized_mobject.frequency
            dot.move_to(self.frequency_axes.input_to_graph_point(
                f, fourier_graph
            ))
        self.fourier_graph_dot_anim = UpdateFromFunc(
            self.fourier_graph_dot, update_dot
        )
        self.fourier_graph_dot_anim.update(0)

    def get_fourier_graph_drawing_update_anim(self, fourier_graph):
        fourier_graph_copy = fourier_graph.copy()
        max_freq = self.frequency_axes.x_max
        def update_fourier_graph(fg):
            freq = self.graph.polarized_mobject.frequency
            fg.pointwise_become_partial(
                fourier_graph_copy,
                0, freq/max_freq
            )
            return fg
        self.fourier_graph_drawing_update_anim = UpdateFromFunc(
            fourier_graph, update_fourier_graph
        )
        return self.fourier_graph_drawing_update_anim

    def generate_center_of_mass_dot_update_anim(self, multiplier = 1):
        origin = self.circle_plane.coords_to_point(0, 0)
        com = self.get_pol_graph_center_of_mass
        self.center_of_mass_dot_anim = UpdateFromFunc(
            self.center_of_mass_dot, 
            lambda d : d.move_to(
                multiplier*(com()-origin)+origin
            )
        )

    def change_frequency(self, new_freq, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 3)
        rate_func = kwargs.pop("rate_func", None)
        if rate_func is None:
            rate_func = bezier([0, 0, 1, 1])
        added_anims = kwargs.get("added_anims", [])
        anims = [self.get_frequency_change_animation(self.graph, new_freq)]
        if hasattr(self, "winding_freq_label"):
            freq_label = [
                sm for sm in self.winding_freq_label
                if isinstance(sm, DecimalNumber)
            ][0]
            self.add(freq_label)
            anims.append(
                ChangeDecimalToValue(freq_label, new_freq)
            )
        if hasattr(self, "v_lines_indicating_periods"):
            anims.append(self.get_period_v_lines_update_anim())
        if hasattr(self, "center_of_mass_dot"):
            anims.append(self.center_of_mass_dot_anim)
        if hasattr(self, "fourier_graph_dot"):
            anims.append(self.fourier_graph_dot_anim)
        if hasattr(self, "fourier_graph_drawing_update_anim"):
            anims.append(self.fourier_graph_drawing_update_anim)
        for anim in anims:
            anim.rate_func = rate_func
        anims += added_anims
        self.play(*anims, **kwargs)

    def create_pi_creature(self):
        return Mortimer().to_corner(DOWN+RIGHT)
