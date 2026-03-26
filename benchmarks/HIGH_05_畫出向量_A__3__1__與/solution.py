from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        # Create a dictionary to store all objects for easy reference
        self.objects = {}
        
        # 1. Title
        title = Text("Vector Addition: The Triangle Method", color=WHITE, font_size=40)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title
        
        # 2. Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-1, 5.5, 1],
            y_range=[-1, 4.5, 1],
            x_length=10,
            y_length=7,
            background_line_style={
                "stroke_color": "#333333",
                "stroke_opacity": 0.5
            },
            axis_config={
                "stroke_color": "#333333",
                "stroke_width": 2,
            }
        )
        axes.center()
        self.objects["axes"] = axes
        
        # 3. Vector A
        vector_a = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            buff=0,
            color=BLUE,
            stroke_width=6
        )
        vector_a.move_to(axes.get_center())
        self.objects["vector_a"] = vector_a
        
        # 4. Label A
        label_a = MathTex(r"\vec{A}", color=BLUE)
        label_a.next_to(vector_a.get_center(), UP+LEFT, buff=0.15)
        self.objects["label_a"] = label_a
        
        # 5. Components A
        components_a = MathTex(r"(3,1)", color=BLUE, font_size=30)
        components_a.next_to(vector_a.get_end(), RIGHT, buff=0.2)
        self.objects["components_a"] = components_a
        
        # 6. Vector B
        vector_b = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            buff=0,
            color=GREEN,
            stroke_width=6
        )
        vector_b.move_to(axes.get_center())
        self.objects["vector_b"] = vector_b
        
        # 7. Label B
        label_b = MathTex(r"\vec{B}", color=GREEN)
        label_b.next_to(vector_b.get_center(), UP+RIGHT, buff=0.15)
        self.objects["label_b"] = label_b
        
        # 8. Components B
        components_b = MathTex(r"(1,2)", color=GREEN, font_size=30)
        components_b.next_to(vector_b.get_end(), UP, buff=0.2)
        self.objects["components_b"] = components_b
        
        # 9. Vector B Translated (invisible initially)
        vector_b_translated = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            buff=0,
            color=GREEN,
            stroke_width=6
        )
        vector_b_translated.set_opacity(0.0)
        vector_b_translated.move_to(axes.get_center())
        self.objects["vector_b_translated"] = vector_b_translated
        
        # 10. Vector C (invisible initially)
        vector_c = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            buff=0,
            color=RED,
            stroke_width=8
        )
        vector_c.set_opacity(0.0)
        vector_c.move_to(axes.get_center())
        self.objects["vector_c"] = vector_c
        
        # 11. Label C (invisible initially)
        label_c = MathTex(r"\vec{C}", color=RED)
        label_c.set_opacity(0.0)
        label_c.next_to(vector_c.get_center(), DOWN+RIGHT, buff=0.2)
        self.objects["label_c"] = label_c
        
        # 12. Components C (invisible initially)
        components_c = MathTex(r"(4,3)", color=RED, font_size=30)
        components_c.set_opacity(0.0)
        components_c.next_to(vector_c.get_end(), UP+RIGHT, buff=0.2)
        self.objects["components_c"] = components_c
        
        # 13. Dashed Line C (invisible initially)
        dashed_line_c = DashedLine(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=RED,
            dash_length=0.1,
            stroke_width=4
        )
        dashed_line_c.set_opacity(0.0)
        dashed_line_c.move_to(axes.get_center())
        self.objects["dashed_line_c"] = dashed_line_c
        
        # 14. Footer Text
        footer_text = Text("Step 1: Draw vector A from the origin to (3,1).", color=WHITE, font_size=28)
        footer_text.to_edge(DOWN, buff=0.5)
        self.objects["footer_text"] = footer_text
        
        # 15. Footer Equation (invisible initially)
        footer_equation = MathTex(r"\vec{C} = \vec{A} + \vec{B}", color=YELLOW, font_size=36)
        footer_equation.set_opacity(0.0)
        footer_equation.next_to(footer_text, DOWN, buff=0.5)
        self.objects["footer_equation"] = footer_equation
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's set up a 2D coordinate system and draw our first vector, A.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Fade in the coordinate grid."},
                "duration": 4.944,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Vector A starts at the origin and goes to the point (3, 1).",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "vector_a", "details": "Draw the blue arrow for vector A."},
                "duration": 4.752,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "We label it A, and note its components are (3, 1).",
                "signal_action": {"type": "Write", "target": "components_a", "color": "BLUE"},
                "visual_action": {"type": "Write", "target_id": "label_a", "details": "Write the label and components for vector A."},
                "duration": 4.536,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now, from the tip of vector A, we draw vector B to the point (4, 3). This represents the vector (1, 2).",
                "signal_action": {"type": "Indicate", "target": "vector_a", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "vector_b", "details": "Draw the green arrow for vector B, starting from the tip of A."},
                "duration": 9.048,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Label vector B and its components (1, 2). We now have a two-step path from the origin to (4,3).",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "label_b", "details": "Write the label and components for vector B."},
                "duration": 8.424,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The Triangle Method says the sum of vectors A and B is the vector from the start of the first to the end of the second. Let's draw that connection.",
                "signal_action": {"type": "Indicate", "target": "vector_a", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "dashed_line_c", "details": "Draw a red dashed line from the origin to the tip of vector B."},
                "duration": 8.52,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "This direct path is our resultant vector, C. Now, watch the key step: we can visualize the sum by translating vector B so its tail aligns with the origin, preserving its direction and length.",
                "signal_action": {"type": "Circumscribe", "target": "vector_b", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "vector_b", "details": "Animate vector B moving so its start point goes to the origin. Use the pre-defined `vector_b_translated` as the target. Simultaneously, fade out the original dashed line."},
                "duration": 12.096,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "With B translated, we see it forms a parallelogram with A. The diagonal of this parallelogram is our resultant vector C, which is exactly A plus B.",
                "signal_action": {"type": "Indicate", "target": "vector_b_translated", "color": "RED"},
                "visual_action": {"type": "FadeIn", "target_id": "vector_c", "details": "Fade in the solid red arrow for vector C, overlapping the dashed line's path and the tip of the translated B."},
                "duration": 9.432,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "Let's label the resultant vector C with its components, (4, 3). And finally, we see the component-wise addition: (3,1) plus (1,2) equals (4,3).",
                "signal_action": None,
                "visual_action": [
                    {"type": "FadeIn", "target_id": "label_c", "details": "Fade in label C."},
                    {"type": "FadeIn", "target_id": "components_c", "details": "Fade in components (4,3)."},
                    {"type": "ReplacementTransform", "target_id": "footer_equation", "details": "Update the footer equation step-by-step: First show 'C = A + B', then morph to 'C = A + B = (3,1) + (1,2)', and finally to 'C = A + B = (3,1) + (1,2) = (4,3)'."}
                ],
                "duration": 13.392,
                "audio_path": "media/audio/畫出向量_A=(3,_1)_與_B=(1,_2)。使用三角形法（首尾相接）來呈現合成向量_C=(4,/step_08.mp3"
            }
        ]
        
        # Process each step in sequence
        for step in sequence:
            step_num = step["step"]
            
            # === AUDIO (MANDATORY) ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Track animation runtime for this step
            animation_time = 0
            
            # 1. Handle signal_action if present
            if step.get("signal_action") is not None:
                signal = step["signal_action"]
                signal_type = signal["type"]
                target_ref = signal["target"]
                color_name = signal.get("color", "YELLOW")
                color = eval(color_name) if color_name in globals() else YELLOW
                
                # Find target object
                target_obj = self.objects.get(target_ref)
                
                # CRITICAL FIX: Check if target_obj exists and is not None
                if target_obj is not None:
                    if signal_type == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=color, run_time=1))
                        animation_time += 1
                    elif signal_type == "Indicate":
                        self.play(Indicate(target_obj, color=color, run_time=1))
                        animation_time += 1
                    elif signal_type == "Write":
                        self.play(Write(target_obj, run_time=1))
                        animation_time += 1
            
            # 2. Handle visual_action
            visual_action = step["visual_action"]
            
            # Check if visual_action is a list or single dict
            if isinstance(visual_action, list):
                # Multiple visual actions in this step
                for action in visual_action:
                    self._execute_visual_action(action, step_num)
                    animation_time += 1  # Approximate 1 second per action
            else:
                # Single visual action
                self._execute_visual_action(visual_action, step_num)
                animation_time += 2  # Approximate 2 seconds for single action
            
            # 3. Wait for remaining audio duration
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)
    
    def _execute_visual_action(self, action, step_num):
        """Helper method to execute a single visual action."""
        action_type = action["type"]
        target_id = action["target_id"]
        target_obj = self.objects.get(target_id)
        
        # CRITICAL FIX: Check if target_obj exists and is not None
        if target_obj is None:
            return
        
        if action_type == "Create":
            self.play(Create(target_obj))
        elif action_type == "Write":
            self.play(Write(target_obj))
        elif action_type == "FadeIn":
            self.play(FadeIn(target_obj))
        elif action_type == "FadeOut":
            self.play(FadeOut(target_obj))
        elif action_type == "Transform":
            # Special case for transforming vector_b to vector_b_translated
            if target_id == "vector_b":
                # Make vector_b_translated visible for the transform
                vector_b_translated = self.objects["vector_b_translated"]
                vector_b_translated.set_opacity(1.0)
                
                # Also fade out dashed_line_c simultaneously
                dashed_line_c = self.objects["dashed_line_c"]
                
                self.play(
                    Transform(self.objects["vector_b"], vector_b_translated),
                    FadeOut(dashed_line_c),
                    run_time=2
                )
        elif action_type == "ReplacementTransform":
            # Update footer equation step-by-step
            footer_eq = self.objects["footer_equation"]
            
            # Make it visible first if needed
            if footer_eq.get_opacity() == 0:
                self.play(FadeIn(footer_eq))
            
            # Create the sequence of equations
            eq1 = MathTex(r"\vec{C} = \vec{A} + \vec{B}", color=YELLOW, font_size=36)
            eq2 = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (3,1) + (1,2)", color=YELLOW, font_size=36)
            eq3 = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (3,1) + (1,2) = (4,3)", color=YELLOW, font_size=36)
            
            # Position them at the same location
            eq1.move_to(footer_eq.get_center())
            eq2.move_to(footer_eq.get_center())
            eq3.move_to(footer_eq.get_center())
            
            # Animate the transformations
            self.play(ReplacementTransform(footer_eq, eq1))
            self.wait(1)
            self.play(ReplacementTransform(eq1, eq2))
            self.wait(1)
            self.play(ReplacementTransform(eq2, eq3))
            
            # Update the stored object
            self.objects["footer_equation"] = eq3