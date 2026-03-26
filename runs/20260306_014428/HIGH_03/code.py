from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        circle_anchor = LEFT * 3
        sine_anchor = RIGHT * 3
        footer_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title
        title = Text("Sine Wave from the Unit Circle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle_axes
        circle_axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_numbers": True, "color": GRAY_C}
        ).move_to(circle_anchor)
        self.objects["circle_axes"] = circle_axes

        # unit_circle
        unit_circle = Circle(radius=1.5, color=BLUE, stroke_width=3).move_to(circle_anchor)
        self.objects["unit_circle"] = unit_circle

        # sine_axes
        sine_axes = Axes(
            x_range=[0, 6.283, 1.571],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "numbers_to_exclude": [], "color": GRAY_C}
        ).move_to(sine_anchor)
        self.objects["sine_axes"] = sine_axes

        # sine_graph_label
        sine_graph_label = MathTex(r"y = \sin(x)", color=GREEN).next_to(sine_axes, UP, buff=0.2)
        self.objects["sine_graph_label"] = sine_graph_label

        # point_P - initial position at (radius, 0) relative to circle_anchor
        point_P = Dot(radius=0.08, color=YELLOW, fill_opacity=1.0)
        point_P.move_to(circle_anchor + np.array([1.5, 0, 0]))
        self.objects["point_P"] = point_P

        # angle_arc - initial angle 0
        angle_arc = Arc(radius=0.5, start_angle=0, angle=0, color=YELLOW, stroke_width=2).move_to(circle_anchor)
        self.objects["angle_arc"] = angle_arc

        # angle_label
        angle_label = MathTex(r"\theta = 0", color=YELLOW).scale(0.7).next_to(angle_arc, RIGHT, buff=0.1)
        self.objects["angle_label"] = angle_label

        # projection_line - initial line from (radius,0) to sine_anchor origin
        projection_line = DashedLine(
            start=circle_anchor + np.array([1.5, 0, 0]),
            end=sine_anchor,
            color=GRAY_C,
            stroke_width=2,
            dash_length=0.05
        )
        self.objects["projection_line"] = projection_line

        # point_Q - initial at sine_anchor origin
        point_Q = Dot(radius=0.06, color=YELLOW, fill_opacity=1.0).move_to(sine_anchor)
        self.objects["point_Q"] = point_Q

        # sine_trace - empty VMobject to be updated
        sine_trace = VMobject(color=GREEN, stroke_width=4)
        sine_trace.move_to(sine_anchor)
        self.objects["sine_trace"] = sine_trace

        # footer_text
        footer_text = Text(
            "The y-coordinate of the point on the circle is plotted against its angle, tracing the sine wave.",
            color=GRAY_C,
            font_size=24
        ).move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # Core driver: ValueTracker for angle theta
        theta_tracker = ValueTracker(0)
        self.theta_tracker = theta_tracker

        # Define updater functions for dynamic objects
        def update_point_P(mob):
            angle = theta_tracker.get_value()
            mob.move_to(circle_anchor + 1.5 * np.array([np.cos(angle), np.sin(angle), 0]))

        # Create redrawn objects instead of updaters with become
        angle_arc_redraw = always_redraw(lambda: Arc(
            radius=0.5,
            start_angle=0,
            angle=theta_tracker.get_value(),
            color=YELLOW,
            stroke_width=2
        ).move_to(circle_anchor))
        
        angle_label_redraw = always_redraw(lambda: MathTex(
            r"\theta = {:.2f}".format(theta_tracker.get_value()),
            color=YELLOW
        ).scale(0.7).next_to(angle_arc_redraw, RIGHT, buff=0.1))
        
        projection_line_redraw = always_redraw(lambda: DashedLine(
            start=circle_anchor + 1.5 * np.array([
                np.cos(theta_tracker.get_value()),
                np.sin(theta_tracker.get_value()),
                0
            ]),
            end=sine_axes.c2p(
                theta_tracker.get_value(),
                np.sin(theta_tracker.get_value())
            ),
            color=GRAY_C,
            stroke_width=2,
            dash_length=0.05
        ))

        def update_point_Q(mob):
            angle = theta_tracker.get_value()
            mob.move_to(sine_axes.c2p(angle, np.sin(angle)))

        # We will update sine_trace via an updater that appends points
        trace_points = []
        def update_sine_trace(mob):
            angle = theta_tracker.get_value()
            new_point = sine_axes.c2p(angle, np.sin(angle))
            trace_points.append(new_point)
            mob.set_points_as_corners(trace_points)

        # Attach updaters (but objects are not added to scene yet)
        point_P.add_updater(update_point_P)
        # Replace the original objects with redrawn versions
        self.objects["angle_arc"] = angle_arc_redraw
        self.objects["angle_label"] = angle_label_redraw
        self.objects["projection_line"] = projection_line_redraw
        point_Q.add_updater(update_point_Q)
        sine_trace.add_updater(update_sine_trace)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        # [missing audio] self.add_sound("media/audio/The_animation_will_s_d8f576ac66/step_00.mp3")
        self.play(Create(self.objects["circle_axes"]), run_time=1.5)
        remaining_1 = 2.0 - 1.5
        self.wait(max(0.1, remaining_1))

        # Step 2
        # [missing audio] self.add_sound("media/audio/The_animation_will_s_d8f576ac66/step_01.mp3")
        self.play(Create(self.objects["unit_circle"].set_color(BLUE)), run_time=2.0)
        remaining_2 = 2.0 - 2.0
        self.wait(max(0.1, remaining_2))

        # Step 3
        # [missing audio] self.add_sound("media/audio/The_animation_will_s_d8f576ac66/step_02.mp3")
        self.play(Create(self.objects["sine_axes"].set_color(WHITE)), run_time=1.5)
        self.play(Write(self.objects["sine_graph_label"]), run_time=1.0)
        total_anim_3 = 1.5 + 1.0
        remaining_3 = 2.0 - total_anim_3
        self.wait(max(0.1, remaining_3))

        # Step 4
        # [missing audio] self.add_sound("media/audio/The_animation_will_s_d8f576ac66/step_03.mp3")
        self.play(Create(self.objects["projection_line"].set_color(YELLOW)), run_time=1.5)
        self.play(Create(self.objects["point_Q"]), run_time=1.0)
        total_anim_4 = 1.5 + 1.0
        remaining_4 = 2.0 - total_anim_4
        self.wait(max(0.1, remaining_4))

        # Step 5
        # [missing audio] self.add_sound("media/audio/The_animation_will_s_d8f576ac66/step_04.mp3")
        self.play(
            Write(self.objects["title"]),
            Write(self.objects["footer_text"]),
            Create(self.objects["point_P"]),
            Create(self.objects["angle_arc"]),
            Write(self.objects["angle_label"]),
            run_time=2.0
        )
        # Now add the sine_trace to the scene (it will be updated)
        self.add(self.objects["sine_trace"])

        self.play(Indicate(self.objects["point_P"], color=YELLOW, run_time=1))
        self.play(self.theta_tracker.animate.set_value(2 * PI), run_time=10, rate_func=linear)
        total_anim_5 = 2.0 + 1 + 10
        remaining_5 = 2.0 - total_anim_5
        self.wait(max(0.1, remaining_5))

        # Step 6
        # [missing audio] self.add_sound("media/audio/The_animation_will_s_d8f576ac66/step_05.mp3")
        self.play(Circumscribe(self.objects["sine_trace"], color=GREEN, run_time=1))
        remaining_6 = 2.0 - 1.0
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))