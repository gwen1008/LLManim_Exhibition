from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define Anchors based on layout_plan
        title_anchor = 3.5 * UP
        circle_zone_center = 3.5 * LEFT
        graph_zone_center = 3.5 * RIGHT
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Sine Function: From Unit Circle to Graph", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Circle Axes
        circle_axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=3,
            y_length=3,
            axis_config={"color": GRAY},
            tips=False
        )
        circle_axes.move_to(circle_zone_center)
        self.objects["circle_axes"] = circle_axes
        
        # Unit Circle
        unit_circle = Circle(radius=1, color=BLUE, stroke_width=3)
        unit_circle.move_to(circle_zone_center)
        self.objects["unit_circle"] = unit_circle
        
        # Circle Point (Initial position at theta=0, i.e., (1,0) relative to circle center)
        circle_point = Dot(radius=0.08, color=YELLOW)
        circle_point.move_to(circle_zone_center + RIGHT * 1)  # Start at (1,0)
        self.objects["circle_point"] = circle_point
        
        # Angle Arc (Will be updated, start at 0 angle)
        angle_arc = Arc(radius=0.4, start_angle=0, angle=0, color=GREEN)
        angle_arc.move_to(circle_zone_center)
        self.objects["angle_arc"] = angle_arc
        
        # Angle Label
        angle_label = MathTex(r"\theta = 0", color=GREEN, font_size=24)
        angle_label.next_to(angle_arc, UP, buff=0.1)
        self.objects["angle_label"] = angle_label
        
        # Graph Axes
        graph_axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": GRAY},
            tips=False
        )
        graph_axes.move_to(graph_zone_center)
        self.objects["graph_axes"] = graph_axes
        
        # Sine Graph (Initially empty, will be drawn progressively)
        sine_graph = ParametricFunction(
            lambda t: graph_axes.c2p(t, np.sin(t)),
            t_range=[0, 0],
            color=RED,
            stroke_width=3
        )
        self.objects["sine_graph"] = sine_graph
        
        # Graph Point
        graph_point = Dot(radius=0.06, color=YELLOW)
        graph_point.move_to(graph_axes.c2p(0, 0))
        self.objects["graph_point"] = graph_point
        
        # Projection Line (Initial line from start point to graph start)
        projection_line = DashedLine(
            start=circle_point.get_center(),
            end=graph_point.get_center(),
            color=WHITE,
            stroke_width=2,
            dash_length=0.05
        )
        self.objects["projection_line"] = projection_line
        
        # Theta Display (Footer)
        theta_display = MathTex(r"\theta = 0", color=GREEN, font_size=28)
        theta_display.move_to(footer_anchor)
        self.objects["theta_display"] = theta_display
        
        # ValueTracker for angle theta (will drive all animations)
        theta_tracker = ValueTracker(0)
        self.theta_tracker = theta_tracker
        
        # Updater functions for dynamic objects (defined here, added later)
        def update_circle_point(mob):
            angle = theta_tracker.get_value()
            mob.move_to(circle_zone_center + np.array([np.cos(angle), np.sin(angle), 0]))
        
        def update_angle_arc(mob):
            angle = theta_tracker.get_value()
            mob.become(Arc(radius=0.4, start_angle=0, angle=angle, color=GREEN))
            mob.move_to(circle_zone_center)
        
        def update_angle_label(mob):
            angle = theta_tracker.get_value()
            mob.become(MathTex(r"\theta = {:.2f}".format(angle), color=GREEN, font_size=24))
            mob.next_to(self.objects["angle_arc"], UP, buff=0.1)
        
        def update_graph_point(mob):
            angle = theta_tracker.get_value()
            mob.move_to(graph_axes.c2p(angle, np.sin(angle)))
        
        def update_projection_line(mob):
            angle = theta_tracker.get_value()
            circle_pos = circle_zone_center + np.array([np.cos(angle), np.sin(angle), 0])
            graph_pos = graph_axes.c2p(angle, np.sin(angle))
            mob.put_start_and_end_on(circle_pos, graph_pos)
        
        def update_theta_display(mob):
            angle = theta_tracker.get_value()
            mob.become(MathTex(r"\theta = {:.2f}".format(angle), color=GREEN, font_size=28))
            mob.move_to(footer_anchor)
        
        def update_sine_graph(mob):
            angle = theta_tracker.get_value()
            mob.become(ParametricFunction(
                lambda t: graph_axes.c2p(t, np.sin(t)),
                t_range=[0, angle],
                color=RED,
                stroke_width=3
            ))
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1 Audio + Animation
        audio_step1 = "media/audio/sine_function_unit_circle_to_graph/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["circle_axes"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2 Audio + Animation
        audio_step2 = "media/audio/sine_function_unit_circle_to_graph/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["unit_circle"], color=BLUE, run_time=1))
        self.play(Create(self.objects["unit_circle"]), run_time=2.0)
        remaining_2 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3 Audio + Animation
        audio_step3 = "media/audio/sine_function_unit_circle_to_graph/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["graph_axes"]), run_time=2.0)
        remaining_3 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4 Audio + Animation
        audio_step4 = "media/audio/sine_function_unit_circle_to_graph/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["circle_point"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["circle_point"]), Create(self.objects["angle_arc"]), Write(self.objects["angle_label"]), run_time=3.0)
        remaining_4 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5 Audio + Animation
        audio_step5 = "media/audio/sine_function_unit_circle_to_graph/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["graph_point"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["graph_point"]), run_time=3.0)
        remaining_5 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Step 6 Audio + Animation
        audio_step6 = "media/audio/sine_function_unit_circle_to_graph/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["projection_line"]), run_time=2.5)
        remaining_6 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Step 7 Audio + Animation
        audio_step7 = "media/audio/sine_function_unit_circle_to_graph/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Add updaters to dynamic objects
        self.objects["circle_point"].add_updater(update_circle_point)
        self.objects["angle_arc"].add_updater(update_angle_arc)
        self.objects["angle_label"].add_updater(update_angle_label)
        self.objects["graph_point"].add_updater(update_graph_point)
        self.objects["projection_line"].add_updater(update_projection_line)
        self.objects["theta_display"].add_updater(update_theta_display)
        self.objects["sine_graph"].add_updater(update_sine_graph)
        
        # Also add the theta_display to the scene now (it was created but not shown)
        self.add(self.objects["theta_display"])
        
        # Animate the ValueTracker from 0 to 2*PI
        self.play(self.theta_tracker.animate.set_value(2 * PI), run_time=10.0, rate_func=linear)
        remaining_7 = max(0.1, 10.0 - 10.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Remove updaters to freeze the final state
        self.objects["circle_point"].clear_updaters()
        self.objects["angle_arc"].clear_updaters()
        self.objects["angle_label"].clear_updaters()
        self.objects["graph_point"].clear_updaters()
        self.objects["projection_line"].clear_updaters()
        self.objects["theta_display"].clear_updaters()
        self.objects["sine_graph"].clear_updaters()
        
        # Step 8 Audio + Animation
        audio_step8 = "media/audio/sine_function_unit_circle_to_graph/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["sine_graph"], color=RED, run_time=1))
        remaining_8 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))