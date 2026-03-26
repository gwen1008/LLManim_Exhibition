from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        # Create a registry for objects
        self.objects = {}
        
        # Title
        title = Text("Graphing a Parabola: Transformations", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title
        
        # Axes
        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": LIGHT_GRAY}
        )
        axes.move_to(ORIGIN)
        self.objects["axes"] = axes
        
        # Parent Equation
        parent_eq = MathTex("y = x^2", color=BLUE)
        parent_eq.next_to(title, DOWN, buff=1.0)
        self.objects["parent_eq"] = parent_eq
        
        # Transformed Equation (initially invisible)
        transformed_eq = MathTex("y = (x-2)^2 - 3", color=YELLOW)
        transformed_eq.move_to(parent_eq.get_center())
        transformed_eq.set_opacity(0)
        self.objects["transformed_eq"] = transformed_eq
        
        # Parent Graph
        parent_graph = axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE, stroke_width=3)
        parent_graph.set_stroke(opacity=0.7)
        self.objects["parent_graph"] = parent_graph
        
        # Final Graph (initially invisible)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-1, 5], color=YELLOW, stroke_width=4)
        final_graph.set_opacity(0)
        self.objects["final_graph"] = final_graph
        
        # Vertex Dot
        vertex_dot = Dot(axes.coords_to_point(2, -3), color=RED, radius=0.08, fill_opacity=1.0)
        self.objects["vertex_dot"] = vertex_dot
        
        # Vertex Label
        vertex_label = MathTex(r"\text{Vertex: }(2, -3)", color=RED, font_size=28)
        vertex_label.to_edge(DOWN, buff=0.5)
        vertex_label.set_opacity(0)
        self.objects["vertex_label"] = vertex_label
        
        # Axis of Symmetry Line
        axis_line = DashedLine(
            start=axes.coords_to_point(2, -4),
            end=axes.coords_to_point(2, 4),
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.8
        )
        axis_line.set_opacity(0)
        self.objects["axis_line"] = axis_line
        
        # Add objects that should be visible from the start
        self.add(title, axes, parent_eq, parent_graph)
        # Add invisible objects to the scene so they can be animated later
        self.add(transformed_eq, final_graph, vertex_dot, vertex_label, axis_line)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with the basic parabola, the parent function y equals x squared.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw coordinate axes"},
                "duration": 5.304,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We plot the graph of y = x², which is a symmetric U-shaped curve with vertex at the origin.",
                "signal_action": {"type": "Indicate", "target": "parent_eq", "color": "BLUE"},
                "visual_action": {"type": "Create", "target_id": "parent_graph", "details": "Draw parent parabola"},
                "duration": 6.672,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now we transform this graph to get y = (x-2)² - 3. The (x-2) shifts the graph 2 units right, and the -3 shifts it 3 units down.",
                "signal_action": {"type": "Circumscribe", "target": "transformed_eq", "color": "YELLOW"},
                "visual_action": {"type": "ReplacementTransform", "target_id": "parent_eq", "new_target_id": "transformed_eq", "details": "Transform equation display"},
                "duration": 12.6,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The transformed parabola has its vertex at (2, -3), which is the minimum point of the curve.",
                "signal_action": {"type": "Indicate", "target": "vertex_dot", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "final_graph", "details": "Draw transformed parabola, fading out parent"},
                "duration": 6.792,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Finally, we draw the axis of symmetry at x = 2, which is the vertical line through the vertex that divides the parabola into mirror images.",
                "signal_action": {"type": "Indicate", "target": "axis_line", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "axis_line", "details": "Draw dashed vertical line"},
                "duration": 8.976,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The complete graph shows the parabola y = (x-2)² - 3 with vertex at (2, -3) and axis of symmetry x = 2.",
                "signal_action": {"type": "Circumscribe", "target": "vertex_label", "color": "RED"},
                "visual_action": {"type": "Write", "target_id": "vertex_label", "details": "Write vertex label at bottom"},
                "duration": 10.632,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_05.mp3"
            }
        ]
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_file = step.get("audio_path")
            
            # === AUDIO (MANDATORY) ===
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            else:
                # Fallback path construction (legacy support)
                file_index = step_num - 1
                mp3_path = f"media/audio/step_{file_index:02d}.mp3"
                wav_path = f"media/audio/step_{file_index:02d}.wav"
                if os.path.exists(mp3_path):
                    self.add_sound(mp3_path)
                elif os.path.exists(wav_path):
                    self.add_sound(wav_path)
            
            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects[target_id]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)
                
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
            
            # Visual Action
            visual = step["visual_action"]
            action_type = visual["type"]
            
            if action_type == "Create":
                target_id = visual["target_id"]
                target_obj = self.objects[target_id]
                if target_id == "axes":
                    # Axes are already added, just animate their creation
                    self.play(Create(axes), run_time=2)
                elif target_id == "parent_graph":
                    self.play(Create(parent_graph), run_time=3)
                elif target_id == "final_graph":
                    # Fade out parent graph while creating final graph
                    self.play(
                        FadeOut(parent_graph, run_time=1),
                        Create(final_graph, run_time=3),
                        FadeIn(vertex_dot, run_time=1)
                    )
                    final_graph.set_opacity(1)
                elif target_id == "axis_line":
                    self.play(Create(axis_line), run_time=2)
                    axis_line.set_opacity(1)
                elif target_id == "vertex_label":
                    self.play(Write(vertex_label), run_time=2)
                    vertex_label.set_opacity(1)
            
            elif action_type == "ReplacementTransform":
                source_id = visual["target_id"]
                target_id = visual["new_target_id"]
                source_obj = self.objects[source_id]
                target_obj = self.objects[target_id]
                # Make target visible and transform
                target_obj.set_opacity(1)
                self.play(ReplacementTransform(source_obj, target_obj), run_time=2)
            
            elif action_type == "Write":
                target_id = visual["target_id"]
                target_obj = self.objects[target_id]
                self.play(Write(target_obj), run_time=2)
                target_obj.set_opacity(1)
            
            # Calculate remaining wait time
            # Estimate animation run_time for this step
            if action_type == "Create":
                if visual["target_id"] == "axes":
                    anim_time = 2
                elif visual["target_id"] == "parent_graph":
                    anim_time = 3
                elif visual["target_id"] == "final_graph":
                    anim_time = 3  # Longest animation in this step
                elif visual["target_id"] == "axis_line":
                    anim_time = 2
                elif visual["target_id"] == "vertex_label":
                    anim_time = 2
                else:
                    anim_time = 2
            elif action_type == "ReplacementTransform":
                anim_time = 2
            elif action_type == "Write":
                anim_time = 2
            else:
                anim_time = 0
            
            # Add signal action time if present
            if signal is not None:
                anim_time += 1  # Signal actions typically run for 1 second
            
            remaining = duration - anim_time + 0.5  # 0.5s safety buffer
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait to show complete graph
        self.wait(2)