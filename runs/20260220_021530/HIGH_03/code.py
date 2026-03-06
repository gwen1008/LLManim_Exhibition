from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}  # Registry for objects by ID
        
        # Define layout positions manually (simpler approach)
        title_pos = UP * 3.2
        circle_pos = LEFT * 3.5 + UP * 0.5
        graph_pos = RIGHT * 3.5 + UP * 0.5
        explanation_pos = DOWN * 2.5
        
        # 1. Title
        title = Text("Sine Function from the Unit Circle", color=WHITE, font_size=40)
        title.move_to(title_pos)
        self.objects["title"] = title
        
        # 2. Circle Axes
        circle_axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_numbers": True, "color": LIGHT_GRAY},
            tips=False
        )
        circle_axes.move_to(circle_pos)
        self.objects["circle_axes"] = circle_axes
        
        # 3. Unit Circle
        unit_circle = Circle(radius=1.5, color=BLUE, stroke_width=3)
        unit_circle.move_to(circle_pos)
        self.objects["unit_circle"] = unit_circle
        
        # 4. Point P (Dot on circle) - Initial position at angle 0
        point_P = Dot(color=YELLOW, radius=0.08)
        point_P.move_to(circle_pos + RIGHT * 1.5)
        self.objects["point_P"] = point_P
        
        # 5. Label P
        label_P = MathTex(r"P(\cos t, \sin t)", color=YELLOW, font_size=24)
        label_P.next_to(point_P, UP+RIGHT, buff=0.1)
        self.objects["label_P"] = label_P
        
        # 6. Angle Line (Radius line)
        angle_line = Line(
            start=circle_pos, 
            end=point_P.get_center(), 
            color=GREEN, 
            stroke_width=2
        )
        self.objects["angle_line"] = angle_line
        
        # 7. Graph Axes
        graph_axes = Axes(
            x_range=[0, 6.283, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "color": LIGHT_GRAY},
            tips=False
        )
        graph_axes.move_to(graph_pos)
        self.objects["graph_axes"] = graph_axes
        
        # 8. Sine Graph
        sine_graph = graph_axes.plot(
            lambda x: 1.5 * np.sin(x), 
            x_range=[0, 2*PI], 
            color=RED, 
            stroke_width=3
        )
        self.objects["sine_graph"] = sine_graph
        
        # 9. Point Q (Dot on graph) - Initial position at (0,0)
        point_Q = Dot(color=YELLOW, radius=0.08)
        point_Q.move_to(graph_axes.c2p(0, 0))
        self.objects["point_Q"] = point_Q
        
        # 10. Label Q
        label_Q = MathTex(r"Q(t, \sin t)", color=YELLOW, font_size=24)
        label_Q.next_to(point_Q, UP, buff=0.1)
        self.objects["label_Q"] = label_Q
        
        # 11. Explanation Text
        explanation_text = Text(
            "The vertical coordinate of P is sin(t). This becomes the y-coordinate of Q. The angle t becomes the x-coordinate of Q.",
            color=LIGHT_GRAY,
            font_size=28
        )
        explanation_text.move_to(explanation_pos)
        self.objects["explanation_text"] = explanation_text
        
        # ValueTracker for angle t
        t_tracker = ValueTracker(0)
        
        # Updater for point P on circle
        def update_point_P(mob):
            t = t_tracker.get_value()
            mob.move_to(circle_pos + np.array([1.5 * np.cos(t), 1.5 * np.sin(t), 0]))
        point_P.add_updater(update_point_P)
        
        # Updater for label P (follows point P)
        def update_label_P(mob):
            mob.next_to(point_P, UP+RIGHT, buff=0.1)
        label_P.add_updater(update_label_P)
        
        # Updater for angle line (radius)
        def update_angle_line(mob):
            mob.put_start_and_end_on(circle_pos, point_P.get_center())
        angle_line.add_updater(update_angle_line)
        
        # Updater for point Q on graph
        def update_point_Q(mob):
            t = t_tracker.get_value()
            mob.move_to(graph_axes.c2p(t, 1.5 * np.sin(t)))
        point_Q.add_updater(update_point_Q)
        
        # Updater for label Q (follows point Q)
        def update_label_Q(mob):
            mob.next_to(point_Q, UP, buff=0.1)
        label_Q.add_updater(update_label_Q)
        
        # Apply initial updater positions
        update_point_P(point_P)
        update_label_P(label_P)
        update_angle_line(angle_line)
        update_point_Q(point_Q)
        update_label_Q(label_Q)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with the unit circle, defined parametrically as x equals cosine t and y equals sine t.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "circle_axes", "details": "Draw the axes for the left plot."},
                "duration": 7.104,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Here is the circle itself, with radius one. We'll scale it up slightly for clarity.",
                "signal_action": {"type": "Circumscribe", "target": "unit_circle", "color": "BLUE"},
                "visual_action": {"type": "Create", "target_id": "unit_circle", "details": "Draw the unit circle on the left axes."},
                "duration": 6.264,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "On the right, we have the graph of the sine function, y equals sine of x.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "graph_axes", "details": "Draw the axes for the right plot, with x from 0 to 2 pi."},
                "duration": 5.352,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "And here is its plot. Notice the x-axis represents the angle in radians.",
                "signal_action": {"type": "Indicate", "target": "sine_graph", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "sine_graph", "details": "Draw the sine curve on the right axes."},
                "duration": 5.952,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Now, consider a point P moving around the circle. Its coordinates are cosine t and sine t.",
                "signal_action": {"type": "Indicate", "target": "point_P", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "point_P", "details": "Create the yellow dot on the circle at angle t=0."},
                "duration": 7.2,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Simultaneously, on the sine graph, there is a corresponding point Q. Its x-coordinate is the angle t, and its y-coordinate is sine t.",
                "signal_action": {"type": "Indicate", "target": "point_Q", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "point_Q", "details": "Create the yellow dot on the graph at (0, 0)."},
                "duration": 9.576,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "As the point moves around the circle, watch how its vertical position, sine t, traces out the sine wave on the right. The angle t becomes the horizontal coordinate.",
                "signal_action": None,
                "visual_action": {"type": "Animation", "target_id": "point_P", "details": "Animate point_P moving around the unit circle (e.g., using MoveAlongPath over 10 seconds). Simultaneously, update point_Q's position via an updater linked to the same angle parameter t."},
                "duration": 10.92,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "To see the connection clearly, let's project the vertical coordinate from the circle to the graph at a specific angle.",
                "signal_action": {"type": "Indicate", "target": "point_P", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "projection_line_h", "details": "Create a temporary horizontal dashed line from point P to the vertical line x = (graph_anchor.x + t) on the right. Then create a vertical dashed line from that intersection down/up to point Q. Fade out after 3 seconds."},
                "duration": 6.816,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "This demonstrates the fundamental relationship: the sine function's graph is generated by plotting the vertical component of circular motion against the angle.",
                "signal_action": None,
                "visual_action": {"type": "Update", "target_id": "explanation_text", "details": "Change explanation text to: 'Graph of y = sin(x) is the vertical projection of circular motion.'"},
                "duration": 9.288,
                "audio_path": "media/audio/演示單位圓運動同步正弦波_左邊有一個點在_e90b3e33c7/step_08.mp3"
            }
        ]
        
        # Add title at the beginning
        self.play(Write(title))
        self.wait(0.5)
        
        for step in sequence:
            step_num = step["step"]
            audio_file = step.get("audio_path")
            
            # Add audio if file exists
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Handle signal_action
            if step.get("signal_action") is not None:
                signal = step["signal_action"]
                target_id = signal["target"]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                target_obj = self.objects.get(target_id)
                if target_obj:
                    if signal["type"] == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=color, run_time=1))
                    elif signal["type"] == "Indicate":
                        self.play(Indicate(target_obj, color=color))
            
            # Handle visual_action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            action_type = visual["type"]
            
            if action_type == "Create":
                target_obj = self.objects.get(target_id)
                if target_obj:
                    if target_id == "circle_axes":
                        self.play(Create(circle_axes))
                    elif target_id == "unit_circle":
                        self.play(Create(unit_circle))
                    elif target_id == "graph_axes":
                        self.play(Create(graph_axes))
                    elif target_id == "sine_graph":
                        self.play(Create(sine_graph))
                    elif target_id == "point_P":
                        self.play(FadeIn(point_P), FadeIn(label_P), FadeIn(angle_line))
                    elif target_id == "point_Q":
                        self.play(FadeIn(point_Q), FadeIn(label_Q))
                    elif target_id == "projection_line_h":
                        # Create projection lines at current angle
                        t = t_tracker.get_value()
                        P_pos = point_P.get_center()
                        Q_pos = point_Q.get_center()
                        
                        # Horizontal line from P to vertical line at x = graph_axes.c2p(t, 0)[0]
                        proj_point = np.array([graph_axes.c2p(t, 0)[0], P_pos[1], 0])
                        horizontal_line = DashedLine(P_pos, proj_point, color=BLUE, stroke_width=2)
                        vertical_line = DashedLine(proj_point, Q_pos, color=BLUE, stroke_width=2)
                        
                        self.play(Create(horizontal_line), Create(vertical_line))
                        self.wait(3)
                        self.play(FadeOut(horizontal_line), FadeOut(vertical_line))
            
            elif action_type == "Animation" and target_id == "point_P":
                # Animate t from 0 to 2π
                run_time = 10
                self.play(t_tracker.animate.set_value(2 * PI), run_time=run_time, rate_func=linear)
            
            elif action_type == "Update" and target_id == "explanation_text":
                new_text = Text(
                    "Graph of y = sin(x) is the vertical projection of circular motion.",
                    color=LIGHT_GRAY,
                    font_size=28
                )
                new_text.move_to(explanation_pos)
                self.play(ReplacementTransform(explanation_text, new_text))
                self.objects["explanation_text"] = new_text
                explanation_text = new_text
            
            # Calculate remaining wait time
            animation_time = 0
            if action_type == "Create":
                animation_time = 1.0
            elif action_type == "Animation" and target_id == "point_P":
                animation_time = 10.0
            elif action_type == "Update":
                animation_time = 1.0
            
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait
        self.wait(2)