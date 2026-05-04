# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示從數線到複數平面的轉換，並用箭頭和點標示輸入與輸出的對應關係。



from manim import *
class HasItsLimitations(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.use_z_coordinate_for_display_order = True

    def construct(self):
        num_line = NumberLine()
        num_line.add_numbers()
        self.add(num_line)

        self.wait()

        # We arrange to go from 2 to 4, a la the squaring in FirstSqrtScene
        base_point = num_line.number_to_point(2) + OUT

        dot_color = ORANGE

        DOT_Z = OUT
        # Note: This z-buffer value is needed for our static scenes, but is
        # not sufficient for everything, in that we still need to use 
        # the foreground_mobjects trick during animations.
        # At some point, we should figure out how to have animations
        # play well with z coordinates.
        
        input_dot = Dot(base_point + DOT_Z, color = dot_color)
        input_label = Text("Input", color = dot_color)
        input_label.next_to(input_dot, UP + LEFT)
        input_label.add_background_rectangle()
        self.add(input_dot)
        self.add(input_label)

        curved_arrow = Arc(0, color = MAROON_E)
        curved_arrow.set_bound_angles(PI, 0)
        curved_arrow.init_points()
        curved_arrow.add_tip()
        curved_arrow.move_arc_center_to(base_point + RIGHT)
        # Could do something smoother, with arrowhead moving along partial arc?
        self.play(Create(curved_arrow))

        output_dot = Dot(base_point + 2 * RIGHT + DOT_Z, color = dot_color)
        output_label = Text("Output", color = dot_color)
        output_label.next_to(output_dot, UP + RIGHT)
        output_label.add_background_rectangle()

        self.add(output_dot)
        self.add(output_label)
        self.wait()

        num_plane = NumberPlane()
        num_plane.add_coordinates()

        new_base_point = base_point + 2 * UP
        new_input_dot = input_dot.copy().move_to(new_base_point)
        new_input_label = input_label.copy().next_to(new_input_dot, UP + LEFT)
        
        new_curved_arrow = Arc(0).set_style(curved_arrow.get_style())
        new_curved_arrow.set_bound_angles(PI * 3/4, 0)
        new_curved_arrow.init_points()
        new_curved_arrow.add_tip()

        input_diff = input_dot.get_center() - curved_arrow.get_points()[0]
        output_diff = output_dot.get_center() - curved_arrow.get_points()[-1]

        new_curved_arrow.shift((new_input_dot.get_center() - new_curved_arrow.get_points()[0]) - input_diff)

        new_output_dot = output_dot.copy().move_to(new_curved_arrow.get_points()[-1] + output_diff)
        new_output_label = output_label.copy().next_to(new_output_dot, UP + RIGHT)

        dot_objects = Group(input_dot, input_label, output_dot, output_label, curved_arrow)
        new_dot_objects = Group(new_input_dot, new_input_label, new_output_dot, new_output_label, new_curved_arrow)

        self.play(
            FadeOut(num_line), FadeIn(num_plane), 
            ReplacementTransform(dot_objects, new_dot_objects),
        )

        self.wait()

        self.add(new_dot_objects)

        complex_plane = ComplexPlane()
        complex_plane.add_coordinates()
        
        # This looks a little wonky and we may wish to do a crossfade in Premiere instead
        self.play(FadeOut(num_plane), FadeIn(complex_plane))

        self.wait()
