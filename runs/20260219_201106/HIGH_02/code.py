from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan
        # Title
        title = Text("Graphing a Parabola: Transformational Approach", color=WHITE, font_size=36)
        self.objects["title"] = title
        title.to_edge(UP, buff=0.5)
        
        # Axes
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": True},
            color=LIGHT_GRAY
        )
        self.objects["axes"] = axes
        axes.center()
        
        # Parent Equation
        parent_eq = MathTex("y = x^2", color=YELLOW)
        self.objects["parent_eq"] = parent_eq
        parent_eq.next_to(axes, UP, buff=1.0)
        
        # Transformed Equation (initially hidden)
        transformed_eq = MathTex("y = (x-2)^2 - 3", color=BLUE)
        self.objects["transformed_eq"] = transformed_eq
        transformed_eq.move_to(parent_eq.get_center())
        
        # Parent Graph (function plot)
        parent_graph = axes.plot(lambda x: x**2, color=YELLOW, stroke_width=3)
        self.objects["parent_graph"] = parent_graph
        
        # Final Graph (function plot, initially at transformed position)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, color=BLUE, stroke_width=3)
        self.objects["final_graph"] = final_graph
        
        # Vertex Dot
        vertex_dot = Dot(axes.c2p(2, -3), color=RED, radius=0.08, fill_opacity=1.0)
        self.objects["vertex_dot"] = vertex_dot
        
        # Vertex Label
        vertex_label = MathTex("(2,-3)", color=RED, font_size=24)
        self.objects["vertex_label"] = vertex_label
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.1)
        
        # Axis Line
        axis_line = Line(axes.c2p(2, -5), axes.c2p(2, 5), color=GREEN, stroke_width=2, stroke_opacity=0.7)
        self.objects["axis_line"] = axis_line
        
        # Axis Label
        axis_label = MathTex("x = 2", color=GREEN, font_size=24)
        self.objects["axis_label"] = axis_label
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        
        # Step Explanation
        step_explanation = Text("Step 1: Start with the parent function y = x²", color=WHITE, font_size=24)
        self.objects["step_explanation"] = step_explanation
        step_explanation.to_edge(DOWN, buff=0.5)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.get_sequence_data()
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")
            
            # --- AUDIO ---
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            
            # --- Signal Action ---
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects[target_id]
                color_name = signal.get("color", "YELLOW")
                color = eval(color_name) if hasattr(self, color_name) else YELLOW
                
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
            
            # --- Visual Action & Narrative Update ---
            visual = step["visual_action"]
            
            # Update explanation text based on narrative
            if step_num == 1:
                new_explanation = Text("Step 1: Start with the parent function y = x²", color=WHITE, font_size=24)
            elif step_num == 2:
                new_explanation = Text("Step 2: Graph the parent parabola y = x²", color=WHITE, font_size=24)
            elif step_num == 3:
                new_explanation = Text("Step 3: Shift right 2 units (x → x-2)", color=WHITE, font_size=24)
            elif step_num == 4:
                new_explanation = Text("Step 4: Shift down 3 units to get y = (x-2)² - 3", color=WHITE, font_size=24)
            elif step_num == 5:
                new_explanation = Text("Step 5: Vertex is at (2, -3)", color=WHITE, font_size=24)
            elif step_num == 6:
                new_explanation = Text("Step 6: Axis of symmetry is x = 2", color=WHITE, font_size=24)
            elif step_num == 7:
                new_explanation = Text("Step 7: Label the vertex", color=WHITE, font_size=24)
            elif step_num == 8:
                new_explanation = Text("Step 8: Label the axis of symmetry", color=WHITE, font_size=24)
            else:
                new_explanation = step_explanation
            
            new_explanation.move_to(step_explanation.get_center())
            if step_num > 1:
                self.play(ReplacementTransform(step_explanation, new_explanation))
                step_explanation = new_explanation
                self.objects["step_explanation"] = step_explanation
            else:
                # First step, just create it
                step_explanation = new_explanation
                self.objects["step_explanation"] = step_explanation
            
            # Execute visual action
            if step_num == 1:
                # Create title, axes, and parent equation
                self.play(Write(title))
                self.play(Create(axes))
                self.play(Write(parent_eq))
                self.wait(0.5)
            elif step_num == 2:
                # Create parent graph
                self.play(Create(parent_graph))
                self.wait(0.5)
            elif step_num == 3:
                # Shift right 2 units
                temp_graph = axes.plot(lambda x: (x-2)**2, color=YELLOW, stroke_width=3)
                self.play(Transform(parent_graph, temp_graph))
                self.wait(0.5)
            elif step_num == 4:
                # Shift down 3 units to final position and change color to blue
                self.play(Transform(parent_graph, final_graph))
                self.play(ReplacementTransform(parent_eq, transformed_eq))
                self.wait(0.5)
            elif step_num == 5:
                # Show vertex dot
                self.play(FadeIn(vertex_dot, scale=0.5))
                self.wait(0.5)
            elif step_num == 6:
                # Draw axis line
                self.play(Create(axis_line))
                self.wait(0.5)
            elif step_num == 7:
                # Write vertex label
                self.play(Write(vertex_label))
                self.wait(0.5)
            elif step_num == 8:
                # Write axis label
                self.play(Write(axis_label))
                self.wait(0.5)
            
            # --- Wait for remaining duration ---
            estimated_animation_time = 1.5  # base
            if signal is not None:
                estimated_animation_time += 1
            if step_num > 1:
                estimated_animation_time += 0.5  # explanation transform
            
            remaining = duration - estimated_animation_time
            if remaining > 0:
                self.wait(remaining)
        
        # Final hold
        self.wait(2)
    
    def get_sequence_data(self):
        """Returns the sequence data from the JSON."""
        return [
            {
                "step": 1,
                "duration": 9.0,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3",
                "signal_action": {"type": "Circumscribe", "target": "parent_eq", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw coordinate grid"}
            },
            {
                "step": 2,
                "duration": 5.184,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3",
                "signal_action": {"type": "Indicate", "target": "parent_graph", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "parent_graph", "details": "Draw the parent parabola"}
            },
            {
                "step": 3,
                "duration": 7.488,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3",
                "signal_action": {"type": "Indicate", "target": "parent_graph", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "parent_graph", "details": "Shift right 2 units"}
            },
            {
                "step": 4,
                "duration": 9.0,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3",
                "signal_action": {"type": "Indicate", "target": "final_graph", "color": "BLUE"},
                "visual_action": {"type": "Transform", "target_id": "parent_graph", "details": "Shift down 3 units"}
            },
            {
                "step": 5,
                "duration": 10.2,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3",
                "signal_action": {"type": "Circumscribe", "target": "vertex_dot", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "vertex_dot", "details": "Show vertex point"}
            },
            {
                "step": 6,
                "duration": 4.32,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_05.mp3",
                "signal_action": {"type": "Indicate", "target": "axis_line", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "axis_line", "details": "Draw vertical line at x=2"}
            },
            {
                "step": 7,
                "duration": 5.592,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_06.mp3",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "vertex_label", "details": "Write vertex label"}
            },
            {
                "step": 8,
                "duration": 9.168,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_07.mp3",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "axis_label", "details": "Write axis label"}
            }
        ]