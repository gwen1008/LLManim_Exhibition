from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation & Initial Positioning ==========
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.5)
        
        # Scale components
        scale_beam = Line(start=LEFT*3.5, end=RIGHT*3.5, color=GRAY_B, stroke_width=8)
        scale_beam.move_to(ORIGIN)
        
        scale_pivot = Circle(radius=0.15, color=GRAY, fill_opacity=1.0)
        scale_pivot.move_to(scale_beam.get_center())
        
        left_pan = Rectangle(width=2.5, height=0.3, color=GOLD, fill_opacity=0.3, stroke_color=GOLD)
        left_pan.move_to(scale_beam.get_start() + DOWN*1.5)
        
        right_pan = Rectangle(width=2.5, height=0.3, color=GOLD, fill_opacity=0.3, stroke_color=GOLD)
        right_pan.move_to(scale_beam.get_end() + DOWN*1.5)
        
        # Boxes representing x
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
        box1.move_to(left_pan.get_center() + LEFT*0.5)
        
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
        box2.move_to(left_pan.get_center() + RIGHT*0.5)
        
        label_box1 = MathTex("x", color=WHITE, font_size=30)
        label_box1.move_to(box1.get_center())
        
        label_box2 = MathTex("x", color=WHITE, font_size=30)
        label_box2.move_to(box2.get_center())
        
        # Circle group (initially empty, will be populated)
        circle_group = VGroup()
        
        # Step explanation text
        step_explanation = Text("We start with the equation 2x = 6.", color=YELLOW, font_size=28)
        step_explanation.to_edge(DOWN, buff=0.5)
        
        # Store objects in a dictionary for easy access
        self.objects = {
            "title": title,
            "scale_beam": scale_beam,
            "scale_pivot": scale_pivot,
            "left_pan": left_pan,
            "right_pan": right_pan,
            "box1": box1,
            "box2": box2,
            "label_box1": label_box1,
            "label_box2": label_box2,
            "circle_group": circle_group,
            "step_explanation": step_explanation,
        }
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We can model the equation two x equals six using a balance scale. On the left, we have two identical boxes, each labeled x, representing two times x.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 11.28,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "On the right, we have six unit circles, each representing a value of one, for a total of six.",
                "signal_action": {"type": "Indicate", "target": "left_pan", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "scale_beam", "details": "Draw the scale beam, pivot, pans, boxes, and labels. Then create six circles (radius=0.3) arranged in a 3x2 grid within the right_pan, adding them to circle_group."},
                "duration": 6.792,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "The scale is balanced, meaning the two sides are equal. To solve for x, we need to divide both sides by two.",
                "signal_action": {"type": "Circumscribe", "target": "circle_group", "color": "YELLOW"},
                "visual_action": {"type": "UpdateText", "target_id": "step_explanation", "details": "Change text to: 'The scale is balanced: 2x = 6. To find x, divide both sides by 2.'"},
                "duration": 8.28,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Visually, we divide the six circles into two equal groups of three.",
                "signal_action": {"type": "Indicate", "target": "circle_group", "color": "RED"},
                "visual_action": {"type": "AnimateGrouping", "target_id": "circle_group", "details": "Animate the six circles separating into two distinct VGroups (group_of_3_a, group_of_3_b), each containing three circles. Position one group above the left pan and one above the right pan."},
                "duration": 4.704,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Now, we apply this division to the entire scale. Each side is split in half, resulting in two smaller, identical balanced scales. On each, one box x equals three circles.",
                "signal_action": None,
                "visual_action": {"type": "Transform", "target_id": "scale_beam", "details": "Transform the entire scale assembly (beam, pans, boxes, circle groups) into two identical, smaller side-by-side scales. Each small scale has one box (x) on the left and three circles on the right. Use VGroup scaling and positioning."},
                "duration": 13.248,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Since both small scales show the same relationship, we can focus on one. This gives us the solution: x equals three.",
                "signal_action": {"type": "Circumscribe", "target": "The left small scale", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "The two small scales", "details": "Fade out one small scale. Transform the remaining small scale into a final, clean representation centered on screen: a single box labeled 'x' on the left, three circles on the right, with an equals sign and the label 'x = 3' appearing between them."},
                "duration": 8.448,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Therefore, the solution to the equation two x equals six is x equals three.",
                "signal_action": None,
                "visual_action": {"type": "UpdateText", "target_id": "step_explanation", "details": "Change text to: 'Solution: x = 3. Dividing both sides of 2x = 6 by 2 gives x = 3.'"},
                "duration": 5.448,
                "audio_path": "media/audio/用天平模型視覺化_2x___6_一邊放兩_985d84b2a1/step_06.mp3"
            }
        ]

        # Helper to create six circles in a grid
        def create_circle_grid(center, radius=0.3):
            circles = VGroup()
            for i in range(2):  # rows
                for j in range(3):  # columns
                    circle = Circle(radius=radius, color=RED, fill_opacity=0.7)
                    circle.move_to(center + RIGHT * (j - 1) * 0.7 + UP * (0.5 - i) * 0.7)
                    circles.add(circle)
            return circles

        # Process each step
        for step in sequence:
            # Audio
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects.get(signal["target"])
                if target_obj:
                    color = eval(signal["color"]) if signal["color"] in ["YELLOW", "RED", "GREEN", "BLUE"] else YELLOW
                    if signal["type"] == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=color, run_time=1))
                    elif signal["type"] == "Indicate":
                        self.play(Indicate(target_obj, color=color))

            # Visual Action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            details = visual.get("details", "")

            if step["step"] == 1:
                # Create title
                self.play(Write(self.objects["title"]))
                anim_time = 1.0
            elif step["step"] == 2:
                # Create scale components and circles
                self.play(Create(self.objects["scale_beam"]))
                self.play(Create(self.objects["scale_pivot"]))
                self.play(Create(self.objects["left_pan"]), Create(self.objects["right_pan"]))
                self.play(Create(self.objects["box1"]), Create(self.objects["box2"]))
                self.play(Write(self.objects["label_box1"]), Write(self.objects["label_box2"]))
                # Create six circles
                circles = create_circle_grid(self.objects["right_pan"].get_center())
                self.objects["circle_group"] = circles
                self.play(LaggedStartMap(Create, circles, lag_ratio=0.1))
                anim_time = 5.0
            elif step["step"] == 3:
                # Update explanation text
                new_text = Text("The scale is balanced: 2x = 6. To find x, divide both sides by 2.", color=YELLOW, font_size=28)
                new_text.move_to(self.objects["step_explanation"].get_center())
                self.play(ReplacementTransform(self.objects["step_explanation"], new_text))
                self.objects["step_explanation"] = new_text
                anim_time = 1.5
            elif step["step"] == 4:
                # Group circles into two VGroups
                circles = self.objects["circle_group"]
                group_a = VGroup(*circles[:3])
                group_b = VGroup(*circles[3:])
                target_pos_a = self.objects["left_pan"].get_center() + UP * 1.5
                target_pos_b = self.objects["right_pan"].get_center() + UP * 1.5
                self.play(
                    group_a.animate.move_to(target_pos_a),
                    group_b.animate.move_to(target_pos_b)
                )
                self.objects["group_a"] = group_a
                self.objects["group_b"] = group_b
                anim_time = 2.0
            elif step["step"] == 5:
                # Transform into two small scales
                # Create a VGroup of the entire original scale
                original_scale = VGroup(
                    self.objects["scale_beam"],
                    self.objects["scale_pivot"],
                    self.objects["left_pan"],
                    self.objects["right_pan"],
                    self.objects["box1"],
                    self.objects["box2"],
                    self.objects["label_box1"],
                    self.objects["label_box2"],
                    self.objects["group_a"],
                    self.objects["group_b"]
                )
                # Create two small scales
                small_scale_left = original_scale.copy().scale(0.6).shift(LEFT * 3)
                small_scale_right = original_scale.copy().scale(0.6).shift(RIGHT * 3)
                # Modify each small scale: keep only one box and three circles
                # For simplicity, we'll transform the original into the two small scales
                self.play(
                    ReplacementTransform(original_scale, small_scale_left),
                    FadeIn(small_scale_right)
                )
                self.objects["small_scale_left"] = small_scale_left
                self.objects["small_scale_right"] = small_scale_right
                anim_time = 3.0
            elif step["step"] == 6:
                # Focus on left scale, transform to final representation
                left_scale = self.objects["small_scale_left"]
                right_scale = self.objects["small_scale_right"]
                # Fade out right scale
                self.play(FadeOut(right_scale))
                # Create final representation: box, three circles, equals sign, label
                final_box = Square(side_length=0.6, color=BLUE, fill_opacity=0.7, stroke_color=WHITE)
                final_box.shift(LEFT * 2)
                final_label = MathTex("x", color=WHITE, font_size=24).move_to(final_box.get_center())
                final_circles = create_circle_grid(ORIGIN + RIGHT * 2, radius=0.25).scale(0.8)
                equals = MathTex("=", font_size=36).move_to(ORIGIN)
                solution_text = MathTex("x = 3", font_size=36, color=GREEN).move_to(DOWN * 2)
                final_group = VGroup(final_box, final_label, final_circles, equals, solution_text)
                self.play(
                    ReplacementTransform(left_scale, final_group),
                    Write(solution_text)
                )
                self.objects["final_group"] = final_group
                anim_time = 3.0
            elif step["step"] == 7:
                # Update explanation text to final solution
                new_text = Text("Solution: x = 3. Dividing both sides of 2x = 6 by 2 gives x = 3.", color=YELLOW, font_size=28)
                new_text.move_to(self.objects["step_explanation"].get_center())
                self.play(ReplacementTransform(self.objects["step_explanation"], new_text))
                self.objects["step_explanation"] = new_text
                anim_time = 1.5
            else:
                anim_time = 0

            # Wait for remaining audio duration
            remaining = step["duration"] - anim_time + 0.5
            if remaining > 0:
                self.wait(max(0.1, remaining))