'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between a point moving on the unit circle and the sine wave graph, showing how the y-coordinate (sinθ) is plotted against the angle θ.
# 2. Layout Strategy: Split-screen with clear zones.
#    - Header Region: [y=3.5] for Title and Step Title.
#    - Main Content: Left side (x=-3.5) for unit circle, right side (x=3.5) for sine graph axes.
#    - Footer Region: [Bottom y=-3.5] for explanation text.
# 3. Anti-Overlap Check: Left and right content are separated by x-axis. Use ValueTracker to synchronize all dynamic elements (dot, line, wave) to prevent misalignment.
#    - Strategy: Use always_redraw for all elements dependent on theta.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/To_create_the_desire_b0c4210cfb/step_XX.mp3"
# 5. Animation Flow: Create static elements (circle, axes, graph axes) step by step. Then introduce dynamic elements (moving dot, projection line, sine wave trace) synchronized by a single ValueTracker (theta).
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors from layout_plan
        title_anchor = 3.5 * UP
        circle_anchor = LEFT * 3.5
        graph_anchor = RIGHT * 3.5
        explanation_anchor = 3.5 * DOWN
        
        # Object registry
        self.objects = {}
        
        # Create objects from layout_plan.objects
        # title_text
        title_text = Text("Sine Wave from the Unit Circle", color=WHITE, font_size=40)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text
        
        # step_title
        step_title = Text("Step 1: The Unit Circle", color=YELLOW, font_size=30)
        step_title.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_title"] = step_title
        
        # unit_circle
        unit_circle = Circle(radius=2, color=BLUE, stroke_width=3)
        unit_circle.move_to(circle_anchor)
        self.objects["unit_circle"] = unit_circle
        
        # circle_axes
        circle_axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            axis_config={"color": GRAY, "stroke_width": 2},
            x_length=5,
            y_length=5
        )
        circle_axes.move_to(circle_anchor)
        self.objects["circle_axes"] = circle_axes
        
        # angle_label (will be updated via ValueTracker)
        angle_label = MathTex(r"\theta = 0", color=YELLOW, font_size=30)
        angle_label.next_to(circle_anchor, UP+RIGHT, buff=0.2)
        self.objects["angle_label"] = angle_label
        
        # sine_axes
        sine_axes = Axes(
            x_range=[-0.5, 6.8, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        sine_axes.move_to(graph_anchor)
        self.objects["sine_axes"] = sine_axes
        
        # sine_axes_labels
        theta_label = MathTex(r"\theta").next_to(sine_axes.x_axis, RIGHT)
        sin_label = MathTex(r"\sin(\theta)").next_to(sine_axes.y_axis, UP)
        sine_axes_labels = VGroup(theta_label, sin_label)
        sine_axes_labels.move_to(graph_anchor)
        self.objects["sine_axes_labels"] = sine_axes_labels
        
        # explanation_text
        explanation_text = Text(
            "The height of the point on the circle becomes the y-value on the graph.",
            color=GRAY_B, font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/To_create_the_desire_b0c4210cfb/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        # signal_action: null (skip)
        # visual_action: Create unit_circle
        self.play(Create(self.objects["unit_circle"]), run_time=2.0)
        remaining_1 = max(0.1, 7.248 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/To_create_the_desire_b0c4210cfb/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # signal_action: Create circle_axes
        self.play(Create(self.objects["circle_axes"]), run_time=2.0)
        # visual_action: Already executed with signal_action (same target)
        remaining_2 = max(0.1, 10.464 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/To_create_the_desire_b0c4210cfb/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # signal_action: ReplacementTransform for step_title
        step_title_new = Text("Step 2: Introducing the Sine Graph", color=YELLOW, font_size=30)
        step_title_new.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_title"], step_title_new))
        self.objects["step_title"] = step_title_new
        
        # visual_action: Create sine_axes
        self.play(Create(self.objects["sine_axes"]), run_time=2.0)
        self.play(Write(self.objects["sine_axes_labels"]), run_time=1.5)
        remaining_3 = max(0.1, 10.632 - (2.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/To_create_the_desire_b0c4210cfb/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # signal_action: ReplacementTransform for step_title
        step_title_new2 = Text("Step 3: Making the Connection", color=YELLOW, font_size=30)
        step_title_new2.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_title"], step_title_new2))
        self.objects["step_title"] = step_title_new2
        
        # Create ValueTracker for theta (shared by all dynamic elements)
        theta_tracker = ValueTracker(0)
        self.objects["theta_tracker"] = theta_tracker
        
        # Update angle_label to track theta
        angle_label_updater = always_redraw(
            lambda: MathTex(
                r"\theta = " + f"{theta_tracker.get_value():.2f}",
                color=YELLOW, font_size=30
            ).next_to(circle_anchor, UP+RIGHT, buff=0.2)
        )
        self.play(ReplacementTransform(self.objects["angle_label"], angle_label_updater))
        self.objects["angle_label"] = angle_label_updater
        self.add(angle_label_updater)
        
        # Define functions for dynamic points
        def get_circle_point():
            angle = theta_tracker.get_value()
            return circle_anchor + 2 * np.array([np.cos(angle), np.sin(angle), 0])
        
        def get_graph_point():
            angle = theta_tracker.get_value()
            return self.objects["sine_axes"].c2p(angle, np.sin(angle))
        
        # Create moving dot on circle (dot_p)
        dot_p = always_redraw(lambda: Dot(point=get_circle_point(), color=RED, radius=0.08))
        self.objects["dot_p"] = dot_p
        
        # Create corresponding dot on graph (dot_q)
        dot_q = always_redraw(lambda: Dot(point=get_graph_point(), color=RED, radius=0.08))
        self.objects["dot_q"] = dot_q
        
        # Create dashed projection line
        projection_line = always_redraw(
            lambda: DashedLine(
                start=get_circle_point(),
                end=get_graph_point(),
                color=BLUE_A,
                stroke_width=2,
                dash_length=0.1
            )
        )
        self.objects["projection_line"] = projection_line
        
        # Add dynamic elements
        self.play(
            AnimationGroup(
                FadeIn(dot_p),
                FadeIn(dot_q),
                Create(projection_line),
                lag_ratio=0.3
            ),
            run_time=2.5
        )
        
        # Start incrementing theta from 0 to 2*PI over 8 seconds
        # This will happen while audio plays
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=8.0,
            rate_func=linear
        )
        
        # Wait for remaining audio
        remaining_4 = max(0.1, 11.136 - (2.5 + 8.0) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/To_create_the_desire_b0c4210cfb/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # signal_action: ReplacementTransform for step_title
        step_title_new3 = Text("Step 4: Tracing the Sine Wave", color=YELLOW, font_size=30)
        step_title_new3.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_title"], step_title_new3))
        self.objects["step_title"] = step_title_new3
        
        # Create the sine wave trace using ParametricFunction
        sine_wave = always_redraw(
            lambda: self.objects["sine_axes"].plot(
                lambda x: np.sin(x),
                x_range=[0, theta_tracker.get_value()],
                color=PINK,
                stroke_width=4
            )
        )
        self.objects["sine_wave_trace"] = sine_wave
        
        # Add the sine wave
        self.play(Create(sine_wave), run_time=2.0)
        
        # Reset theta to 0 and animate again to show the trace
        self.play(theta_tracker.animate.set_value(0), run_time=0.5)
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=6.0,
            rate_func=linear
        )
        
        # Wait for remaining audio
        remaining_5 = max(0.1, 12.984 - (2.0 + 0.5 + 6.0) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))