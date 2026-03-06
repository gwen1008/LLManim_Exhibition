from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}

        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        circle_center = 3 * LEFT
        graph_origin = 3 * RIGHT
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Sine Function from the Unit Circle", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color=BLUE, stroke_width=3)
        circle.move_to(circle_center)
        self.objects["circle"] = circle

        # circle_axes (VGroup of two lines)
        circle_axes = VGroup(
            Line(circle_center + 2.5*LEFT, circle_center + 2.5*RIGHT),
            Line(circle_center + 2.5*DOWN, circle_center + 2.5*UP)
        )
        circle_axes.set_stroke(color=WHITE, width=2, opacity=0.7)
        self.objects["circle_axes"] = circle_axes

        # graph_axes (Axes)
        graph_axes = Axes(
            x_range=[0, 6.283, 1.571],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=4,
            axis_config={"include_numbers": True, "color": WHITE},
            tips=False
        )
        graph_axes.move_to(graph_origin)
        self.objects["graph_axes"] = graph_axes

        # sine_curve - Use plot method instead of get_graph
        sine_curve = graph_axes.plot(
            lambda x: np.sin(x),
            x_range=[0, 2*PI],
            color=GREEN,
            stroke_width=3
        )
        self.objects["sine_curve"] = sine_curve

        # circle_point (Dot) - initial at angle 0
        circle_point = Dot(radius=0.08, color=RED)
        circle_point.move_to(circle_center + np.array([2, 0, 0]))
        self.objects["circle_point"] = circle_point

        # radius_line (Line) - from center to point
        radius_line = Line(circle_center, circle_point.get_center(), color=YELLOW, stroke_width=2)
        self.objects["radius_line"] = radius_line

        # vertical_proj_line (Line) - from point to x-axis
        vertical_proj_line = Line(circle_point.get_center(), circle_point.get_center(), color=PINK, stroke_width=2, stroke_opacity=0.8)
        self.objects["vertical_proj_line"] = vertical_proj_line

        # graph_point (Dot) - initial at (0,0) on graph
        graph_point = Dot(radius=0.08, color=RED)
        graph_point.move_to(graph_axes.c2p(0, 0))
        self.objects["graph_point"] = graph_point

        # graph_vertical_line (Line) - from x-axis to point on graph
        graph_vertical_line = Line(graph_axes.c2p(0,0), graph_point.get_center(), color=PINK, stroke_width=2, stroke_opacity=0.8)
        self.objects["graph_vertical_line"] = graph_vertical_line

        # angle_label (Arc) - initial angle 0
        angle_label = Arc(radius=0.7, start_angle=0, angle=0, color=ORANGE, stroke_width=3)
        angle_label.move_to(circle_center)
        self.objects["angle_label"] = angle_label

        # explanation_text (Text)
        explanation_text = Text("The unit circle defines sin(θ) as the y-coordinate of a point at angle θ.", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ValueTracker for theta (angle)
        theta_tracker = ValueTracker(0)
        self.theta_tracker = theta_tracker

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeIn(self.objects["title"]))
        self.wait(max(0.1, 8.184 - 1))

        # Step 2
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["circle"], color=BLUE))
        self.play(
            Create(self.objects["circle"]),
            Create(self.objects["circle_axes"]),
            Create(self.objects["graph_axes"]),
            Create(self.objects["sine_curve"]),
            run_time=2
        )
        self.wait(max(0.1, 7.632 - 2 - 1))

        # Step 3
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Create(self.objects["circle_point"]),
            Create(self.objects["radius_line"]),
            Create(self.objects["angle_label"]),
            run_time=2
        )
        self.wait(max(0.1, 8.088 - 2))

        # Step 4
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["vertical_proj_line"]), run_time=1)
        self.wait(max(0.1, 8.592 - 1))

        # Step 5
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Create(self.objects["graph_point"]),
            Create(self.objects["graph_vertical_line"]),
            run_time=2
        )
        self.wait(max(0.1, 12.576 - 2))

        # Step 6 - Create updater functions for animation
        def update_circle_point():
            angle = theta_tracker.get_value()
            return circle_center + np.array([2*np.cos(angle), 2*np.sin(angle), 0])
        
        def update_radius_line():
            return Line(circle_center, update_circle_point(), color=YELLOW, stroke_width=2)
        
        def update_vertical_proj_line():
            angle = theta_tracker.get_value()
            start = update_circle_point()
            end = circle_center + np.array([2*np.cos(angle), 0, 0])
            return Line(start, end, color=PINK, stroke_width=2, stroke_opacity=0.8)
        
        def update_angle_label():
            angle = theta_tracker.get_value()
            return Arc(radius=0.7, start_angle=0, angle=angle, color=ORANGE, stroke_width=3).move_to(circle_center)
        
        def update_graph_point():
            angle = theta_tracker.get_value()
            return graph_axes.c2p(angle, np.sin(angle))
        
        def update_graph_vertical_line():
            angle = theta_tracker.get_value()
            start = graph_axes.c2p(angle, 0)
            end = graph_axes.c2p(angle, np.sin(angle))
            return Line(start, end, color=PINK, stroke_width=2, stroke_opacity=0.8)
        
        # Create always_redraw objects for smooth animation
        circle_point_anim = always_redraw(lambda: Dot(radius=0.08, color=RED).move_to(update_circle_point()))
        radius_line_anim = always_redraw(lambda: update_radius_line())
        vertical_proj_line_anim = always_redraw(lambda: update_vertical_proj_line())
        angle_label_anim = always_redraw(lambda: update_angle_label())
        graph_point_anim = always_redraw(lambda: Dot(radius=0.08, color=RED).move_to(update_graph_point()))
        graph_vertical_line_anim = always_redraw(lambda: update_graph_vertical_line())
        
        # Add the animated versions to the scene
        self.add(
            circle_point_anim,
            radius_line_anim,
            vertical_proj_line_anim,
            angle_label_anim,
            graph_point_anim,
            graph_vertical_line_anim
        )
        
        # Remove the static versions
        self.remove(
            self.objects["circle_point"],
            self.objects["radius_line"],
            self.objects["vertical_proj_line"],
            self.objects["angle_label"],
            self.objects["graph_point"],
            self.objects["graph_vertical_line"]
        )
        
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Animate theta from 0 to 2π
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=10,
            rate_func=linear
        )
        self.wait(max(0.1, 9.816 - 10))

        # Step 7
        audio_file = "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["sine_curve"], color=GREEN))
        self.wait(max(0.1, 8.688 - 1))
        
        # Final wait
        self.wait(2)