'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the connection between the geometric definition of sine on the unit circle and its graph.
# 2. Layout Strategy: Left-right split screen.
#    - Header Region: [y=3.5] for Title
#    - Main Content: Left zone centered at (-3.5,0) for circle, right zone centered at (3.0,0) for graph.
#    - Footer Region: [Bottom y=-3.5] for step explanations.
# 3. Anti-Overlap Check: Use VGroups to manage left and right zones. Ensure divider line is faint.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/sine_circle_graph/step_XX.mp3"
# 5. Animation Flow: Setup anchors and objects, then unroll sequence: create circle axes, circle, projection, graph axes, connection, then continuous sweep with ValueTracker, final hold.
'''

from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Animate_a_unit_circl_a66eaf186e/final_narrative.mp3")  # [auto-injected: full narration]
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        circle_center_anchor = np.array([-3.5, 0, 0])
        graph_origin_anchor = np.array([3.0, 0, 0])
        footer_anchor = 3.5 * DOWN
        
        # Object registry
        self.objects = {}
        
        # Create objects from layout_plan
        # title
        title = Text("Sine Function: From the Unit Circle to the Graph", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # divider_line
        divider_line = Line(start=3.5*UP, end=3.5*DOWN, color="#333333", stroke_width=1)
        divider_line.move_to(ORIGIN)
        self.objects["divider_line"] = divider_line
        
        # circle_axes
        circle_axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": False, "color": GREY},
            tips=False
        )
        circle_axes.move_to(circle_center_anchor)
        self.objects["circle_axes"] = circle_axes
        
        # unit_circle
        unit_circle = Circle(radius=2, color=BLUE, stroke_width=3)
        unit_circle.move_to(circle_center_anchor)
        self.objects["unit_circle"] = unit_circle
        
        # circle_radius_line (initial at angle 0)
        circle_radius_line = Line(
            start=circle_center_anchor,
            end=circle_center_anchor + np.array([2, 0, 0]),
            color=YELLOW,
            stroke_width=4
        )
        self.objects["circle_radius_line"] = circle_radius_line
        
        # dot_circle (initial at (1,0) in circle coords)
        dot_circle = Dot(radius=0.08, color=RED)
        dot_circle.move_to(circle_center_anchor + np.array([2, 0, 0]))
        self.objects["dot_circle"] = dot_circle
        
        # theta_label
        theta_label = MathTex(r"\theta = 0", color=WHITE, font_size=24)
        theta_label.next_to(circle_center_anchor, UP+RIGHT, buff=0.2)
        self.objects["theta_label"] = theta_label
        
        # projection_line (initial zero length)
        projection_line = Line(
            start=circle_center_anchor + np.array([2, 0, 0]),
            end=circle_center_anchor + np.array([2, 0, 0]),
            color=GREEN,
            stroke_width=3
        )
        self.objects["projection_line"] = projection_line
        
        # sin_label
        sin_label = MathTex(r"\sin(\theta)", color=GREEN, font_size=24)
        sin_label.next_to(projection_line, LEFT, buff=0.1)
        self.objects["sin_label"] = sin_label
        
        # graph_axes
        graph_axes = Axes(
            x_range=[0, 6.5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "color": GREY},
            tips=False
        )
        graph_axes.move_to(graph_origin_anchor)
        self.objects["graph_axes"] = graph_axes
        
        # graph_axes_labels
        graph_axes_labels = MathTex(r"x\\y=\sin(x)", color=WHITE, font_size=24)
        graph_axes_labels.next_to(graph_axes, DOWN, buff=0.2)
        self.objects["graph_axes_labels"] = graph_axes_labels
        
        # sine_curve (full curve, will be revealed)
        sine_curve = ParametricFunction(
            lambda t: np.array([t, np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=PURPLE,
            stroke_width=3
        )
        sine_curve.move_to(graph_origin_anchor)
        self.objects["sine_curve"] = sine_curve
        
        # vertical_sweep_line (initial zero length)
        vertical_sweep_line = Line(
            start=graph_origin_anchor,
            end=graph_origin_anchor,
            color="#FFAAAA",
            stroke_width=2
        )
        self.objects["vertical_sweep_line"] = vertical_sweep_line
        
        # dot_graph (initial at (0,0))
        dot_graph = Dot(radius=0.08, color=RED)
        dot_graph.move_to(graph_origin_anchor)
        self.objects["dot_graph"] = dot_graph
        
        # connection_line (initial horizontal line from (1,0) to (0,0) in respective coords)
        connection_line = DashedLine(
            start=circle_center_anchor + np.array([2, 0, 0]),
            end=graph_origin_anchor,
            color=WHITE,
            stroke_width=2,
            dash_length=0.1
        )
        self.objects["connection_line"] = connection_line
        
        # step_explanation
        step_explanation = Text(
            "Step 1: The unit circle. Sine of an angle is the y-coordinate of the corresponding point.",
            color=WHITE,
            font_size=24
        )
        step_explanation.move_to(footer_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ValueTracker for theta (will be used in step 5/6)
        theta_tracker = ValueTracker(0)
        self.theta_tracker = theta_tracker
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/sine_circle_graph/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["divider_line"]), run_time=0.5)
        self.play(Create(self.objects["circle_axes"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - (1.0+0.5+1.5) + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/sine_circle_graph/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # signal_action: Create unit_circle (already defined as Indicate? JSON says Create)
        # We'll Create it as per visual_action.
        self.play(Create(self.objects["unit_circle"]), run_time=2.0)
        remaining_2 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/sine_circle_graph/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # signal_action: Indicate projection_line
        self.play(Indicate(self.objects["projection_line"], color=GREEN, run_time=1))
        # visual_action: Create projection_line, radius line, dot
        self.play(
            Create(self.objects["circle_radius_line"]),
            Create(self.objects["dot_circle"]),
            Create(self.objects["projection_line"]),
            Write(self.objects["theta_label"]),
            Write(self.objects["sin_label"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 3.0 - (1.0+2.0) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/sine_circle_graph/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # signal_action: Create graph_axes
        self.play(Create(self.objects["graph_axes"]), run_time=1.5)
        self.play(Write(self.objects["graph_axes_labels"]), run_time=0.5)
        remaining_4 = max(0.1, 2.5 - (1.5+0.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/sine_circle_graph/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # signal_action: Create connection_line
        self.play(Create(self.objects["connection_line"]), run_time=1.0)
        # Update step explanation
        new_explanation = Text(
            "Step 5: Connecting the two views. The dashed line bridges the same sine value.",
            color=WHITE,
            font_size=24
        )
        new_explanation.move_to(footer_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation), run_time=0.5)
        self.objects["step_explanation"] = new_explanation
        remaining_5 = max(0.1, 3.5 - (1.0+0.5) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/sine_circle_graph/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Update step explanation
        new_explanation2 = Text(
            "Step 6: Continuous sweep. The red dot traces the sine wave as theta increases.",
            color=WHITE,
            font_size=24
        )
        new_explanation2.move_to(footer_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation2), run_time=0.5)
        self.objects["step_explanation"] = new_explanation2
        
        # Define updaters using always_redraw
        # dot_circle
        dot_circle_updater = always_redraw(lambda: self.objects["dot_circle"].move_to(
            circle_center_anchor + 2 * np.array([np.cos(self.theta_tracker.get_value()), np.sin(self.theta_tracker.get_value()), 0])
        ))
        # radius_line
        radius_line_updater = always_redraw(lambda: self.objects["circle_radius_line"].become(Line(
            start=circle_center_anchor,
            end=circle_center_anchor + 2 * np.array([np.cos(self.theta_tracker.get_value()), np.sin(self.theta_tracker.get_value()), 0]),
            color=YELLOW,
            stroke_width=4
        )))
        # projection_line
        projection_line_updater = always_redraw(lambda: self.objects["projection_line"].become(Line(
            start=circle_center_anchor + 2 * np.array([np.cos(self.theta_tracker.get_value()), np.sin(self.theta_tracker.get_value()), 0]),
            end=circle_center_anchor + np.array([2*np.cos(self.theta_tracker.get_value()), 0, 0]),
            color=GREEN,
            stroke_width=3
        )))
        # sin_label (position next to projection line)
        sin_label_updater = always_redraw(lambda: self.objects["sin_label"].next_to(
            self.objects["projection_line"], LEFT, buff=0.1
        ))
        # theta_label
        theta_label_updater = always_redraw(lambda: self.objects["theta_label"].become(MathTex(
            f"\\theta = {self.theta_tracker.get_value():.2f}", color=WHITE, font_size=24
        ).next_to(circle_center_anchor, UP+RIGHT, buff=0.2)))
        # vertical_sweep_line
        vertical_sweep_line_updater = always_redraw(lambda: self.objects["vertical_sweep_line"].become(Line(
            start=graph_origin_anchor + np.array([self.theta_tracker.get_value(), -1.5, 0]),
            end=graph_origin_anchor + np.array([self.theta_tracker.get_value(), 1.5, 0]),
            color="#FFAAAA",
            stroke_width=2
        )))
        # dot_graph
        dot_graph_updater = always_redraw(lambda: self.objects["dot_graph"].move_to(
            graph_origin_anchor + np.array([self.theta_tracker.get_value(), np.sin(self.theta_tracker.get_value()), 0])
        ))
        # connection_line
        connection_line_updater = always_redraw(lambda: self.objects["connection_line"].become(DashedLine(
            start=circle_center_anchor + np.array([2*np.cos(self.theta_tracker.get_value()), np.sin(self.theta_tracker.get_value()), 0]),
            end=graph_origin_anchor + np.array([self.theta_tracker.get_value(), np.sin(self.theta_tracker.get_value()), 0]),
            color=WHITE,
            stroke_width=2,
            dash_length=0.1
        )))
        
        # Add updater objects to scene (they are already added via always_redraw)
        self.add(
            dot_circle_updater,
            radius_line_updater,
            projection_line_updater,
            sin_label_updater,
            theta_label_updater,
            vertical_sweep_line_updater,
            dot_graph_updater,
            connection_line_updater
        )
        
        # Also create the sine curve gradually using DrawBorderThenFill
        self.play(DrawBorderThenFill(self.objects["sine_curve"], run_time=0.1))  # quick appear
        # Now animate theta from 0 to 2*PI
        sweep_time = 10.0  # allocate most of the 12s duration to the sweep
        self.play(self.theta_tracker.animate.set_value(2 * PI), run_time=sweep_time, rate_func=linear)
        remaining_6 = max(0.1, 12.0 - (0.5 + sweep_time) + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/sine_circle_graph/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Update step explanation
        final_explanation = Text(
            "Step 7: One complete period. The circle generates the sine wave.",
            color=WHITE,
            font_size=24
        )
        final_explanation.move_to(footer_anchor)
        self.play(Transform(self.objects["step_explanation"], final_explanation), run_time=0.5)
        self.objects["step_explanation"] = final_explanation
        
        # signal_action: Circumscribe sine_curve
        self.play(Circumscribe(self.objects["sine_curve"], color=PURPLE, run_time=1.5))
        remaining_7 = max(0.1, 4.0 - (0.5+1.5) + 0.5)
        self.wait(max(0.1, remaining_7))