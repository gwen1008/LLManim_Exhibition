from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole Number", color=WHITE, font_size=36)
        self.objects["title"] = title
        
        # Number Line
        number_line = NumberLine(
            x_range=[3, 4, 0.1],
            length=4,
            include_numbers=True,
            color=LIGHT_GRAY
        )
        self.objects["number_line"] = number_line
        
        # Points and Labels
        # Point and label for 3
        point_3 = Dot(radius=0.08, color=BLUE)
        label_3 = MathTex("3", color=BLUE)
        self.objects["point_3"] = point_3
        self.objects["label_3"] = label_3
        
        # Point and label for 4
        point_4 = Dot(radius=0.08, color=BLUE)
        label_4 = MathTex("4", color=BLUE)
        self.objects["point_4"] = point_4
        self.objects["label_4"] = label_4
        
        # Point and label for 3.5 (midpoint)
        point_35 = Dot(radius=0.08, color=YELLOW)
        label_35 = MathTex("3.5", color=YELLOW)
        self.objects["point_35"] = point_35
        self.objects["label_35"] = label_35
        
        # Point and label for 3.7
        point_37 = Dot(radius=0.08, color=GREEN)
        label_37 = MathTex("3.7", color=GREEN)
        self.objects["point_37"] = point_37
        self.objects["label_37"] = label_37
        
        # Vertical line at 3.7
        vertical_line = Line(color=GREEN, stroke_width=3)
        self.objects["vertical_line"] = vertical_line
        
        # Step label (footer text)
        step_label = Text("Step 1: Draw the number line and mark 3 and 4.", color=LIGHT_GRAY, font_size=24)
        self.objects["step_label"] = step_label
        
        # Rule text
        rule_text = MathTex(r"\text{Rule: If digit after decimal } \geq 5, \text{ round up.}", color=WHITE, font_size=28)
        self.objects["rule_text"] = rule_text
        
        # Digit highlight for '7'
        digit_highlight = MathTex("7", color=RED, font_size=36)
        self.objects["digit_highlight"] = digit_highlight
        
        # Initialize Layout Engine
        from utils.layout_engine import LayoutEngine, LayoutObject
        
        layout = LayoutEngine()
        
        # Register objects with layout
        obj_title = LayoutObject(title, "title")
        obj_number_line = LayoutObject(number_line, "number_line")
        obj_point_3 = LayoutObject(point_3, "point_3")
        obj_label_3 = LayoutObject(label_3, "label_3")
        obj_point_4 = LayoutObject(point_4, "point_4")
        obj_label_4 = LayoutObject(label_4, "label_4")
        obj_point_35 = LayoutObject(point_35, "point_35")
        obj_label_35 = LayoutObject(label_35, "label_35")
        obj_point_37 = LayoutObject(point_37, "point_37")
        obj_label_37 = LayoutObject(label_37, "label_37")
        obj_vertical_line = LayoutObject(vertical_line, "vertical_line")
        obj_step_label = LayoutObject(step_label, "step_label")
        obj_rule_text = LayoutObject(rule_text, "rule_text")
        obj_digit_highlight = LayoutObject(digit_highlight, "digit_highlight")
        
        layout.add(obj_title)
        layout.add(obj_number_line)
        layout.add(obj_point_3)
        layout.add(obj_label_3)
        layout.add(obj_point_4)
        layout.add(obj_label_4)
        layout.add(obj_point_35)
        layout.add(obj_label_35)
        layout.add(obj_point_37)
        layout.add(obj_label_37)
        layout.add(obj_vertical_line)
        layout.add(obj_step_label)
        layout.add(obj_rule_text)
        layout.add(obj_digit_highlight)
        
        # Assign to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_number_line, "CONTENT")
        layout.add_to_zone(obj_point_3, "CONTENT")
        layout.add_to_zone(obj_label_3, "CONTENT")
        layout.add_to_zone(obj_point_4, "CONTENT")
        layout.add_to_zone(obj_label_4, "CONTENT")
        layout.add_to_zone(obj_point_35, "CONTENT")
        layout.add_to_zone(obj_label_35, "CONTENT")
        layout.add_to_zone(obj_point_37, "CONTENT")
        layout.add_to_zone(obj_label_37, "CONTENT")
        layout.add_to_zone(obj_vertical_line, "CONTENT")
        layout.add_to_zone(obj_step_label, "FOOTER")
        layout.add_to_zone(obj_rule_text, "FOOTER")
        layout.add_to_zone(obj_digit_highlight, "CONTENT")
        
        # Center title and step label horizontally
        layout.add_constraint(obj_title.center_x == 0)
        layout.add_constraint(obj_step_label.center_x == 0)
        layout.add_constraint(obj_rule_text.center_x == 0)
        
        # Align rule text below step label
        layout.align_to(obj_rule_text, obj_step_label, 'TOP', buff=-0.5)
        
        # Solve layout
        layout.solve()
        
        # Now position objects relative to number line coordinates (post-solve)
        # Get number line center after layout
        nl_center = obj_number_line.get_center()
        nl = number_line
        
        # Position points at correct coordinates on number line
        point_3.move_to(nl.n2p(3))
        label_3.next_to(point_3, DOWN, buff=0.2)
        
        point_4.move_to(nl.n2p(4))
        label_4.next_to(point_4, DOWN, buff=0.2)
        
        point_35.move_to(nl.n2p(3.5))
        label_35.next_to(point_35, UP, buff=0.2)
        
        point_37.move_to(nl.n2p(3.7))
        label_37.next_to(point_37, UP, buff=0.2)
        
        # Set vertical line position
        vertical_line.put_start_and_end_on(
            nl.n2p(3.7),
            nl.n2p(3.7) + UP
        )
        
        # Position digit highlight near label_37
        digit_highlight.move_to(label_37.get_center() + UP * 0.5)
        
        # Initially hide some objects
        point_35.set_opacity(0)
        label_35.set_opacity(0)
        point_37.set_opacity(0)
        label_37.set_opacity(0)
        vertical_line.set_opacity(0)
        rule_text.set_opacity(0)
        digit_highlight.set_opacity(0)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start with a number line from 3 to 4.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "number_line",
                    "details": "Draw the number line with ticks and labels for 3 and 4."
                },
                "duration": 3.168,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Now, let's plot the number 3.7 on this line. We draw a point at 3.7 and a vertical line to emphasize its exact position.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "label_37",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "AnimationGroup",
                    "target_id": "group_step2",
                    "details": "Create point_37, label_37, and vertical_line simultaneously."
                },
                "duration": 9.312,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "The key to rounding is the midpoint between 3 and 4, which is 3.5. Let's plot that.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "label_35",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "point_35",
                    "details": "Draw the yellow dot at 3.5 and write its label."
                },
                "duration": 6.768,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "We see 3.7 is to the right of 3.5, meaning it's closer to 4. The rounding rule says: if the digit immediately after the decimal point is 5 or greater, we round up. In 3.7, that digit is 7.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "digit_highlight",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "AnimationGroup",
                    "target_id": "group_step4",
                    "details": "FadeIn rule_text. Create and highlight the digit '7' from 3.7. FadeOut vertical_line to reduce clutter."
                },
                "duration": 14.616,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Since 7 is greater than 5, we round 3.7 up to 4. Watch as the point transforms to its rounded value.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "point_4",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Transform",
                    "target_id": "point_37",
                    "details": "Animate the green dot (point_37) moving along the number line to the position of the blue dot at 4. Simultaneously, transform label_37 into a label showing '4' at that location."
                },
                "duration": 7.896,
                "audio_path": "media/audio/在_3_到_4_之間的數線上標示出_3__7eab4021cf/step_04.mp3"
            }
        ]
        
        # Step 1
        step = sequence[0]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Write(title))
        self.play(Create(number_line))
        self.play(FadeIn(point_3), FadeIn(label_3), FadeIn(point_4), FadeIn(label_4))
        self.play(Write(step_label))
        
        animation_time = 1 + 1 + 1 + 1 + 0.5  # Estimate: Write title, Create number_line, FadeIn points, Write step_label
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 2
        step = sequence[1]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Update step label
        new_step_label = Text("Step 2: Plot 3.7 on the number line.", color=LIGHT_GRAY, font_size=24)
        new_step_label.move_to(step_label.get_center())
        self.play(ReplacementTransform(step_label, new_step_label))
        step_label = new_step_label
        
        # Show point_37, label_37, and vertical_line
        self.play(
            FadeIn(point_37),
            Write(label_37),
            Create(vertical_line)
        )
        
        # Signal action: Indicate label_37
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_id = signal["target"]
            color = signal.get("color", "YELLOW")
            target_obj = self.objects[target_id]
            color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
            self.play(Indicate(target_obj, color=color_map.get(color, YELLOW)))
        
        animation_time = 1 + 1 + 1 + 1  # Estimate: Transform label, FadeIn/Write/Create, Indicate
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 3
        step = sequence[2]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Update step label
        new_step_label = Text("Step 3: Mark the midpoint 3.5.", color=LIGHT_GRAY, font_size=24)
        new_step_label.move_to(step_label.get_center())
        self.play(ReplacementTransform(step_label, new_step_label))
        step_label = new_step_label
        
        # Show point_35 and label_35
        self.play(
            FadeIn(point_35),
            Write(label_35)
        )
        
        # Signal action: Circumscribe label_35
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_id = signal["target"]
            color = signal.get("color", "YELLOW")
            target_obj = self.objects[target_id]
            color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
            self.play(Circumscribe(target_obj, color=color_map.get(color, YELLOW), run_time=1))
        
        animation_time = 1 + 1 + 1  # Estimate: Transform label, FadeIn/Write, Circumscribe
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 4
        step = sequence[3]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Update step label
        new_step_label = Text("Step 4: Apply the rounding rule.", color=LIGHT_GRAY, font_size=24)
        new_step_label.move_to(step_label.get_center())
        self.play(ReplacementTransform(step_label, new_step_label))
        step_label = new_step_label
        
        # Show rule text
        self.play(FadeIn(rule_text))
        
        # Show and highlight digit '7'
        self.play(FadeIn(digit_highlight))
        
        # Signal action: Indicate digit_highlight
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_id = signal["target"]
            color = signal.get("color", "YELLOW")
            target_obj = self.objects[target_id]
            color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
            self.play(Indicate(target_obj, color=color_map.get(color, YELLOW)))
        
        # Fade out vertical line
        self.play(FadeOut(vertical_line))
        
        animation_time = 1 + 1 + 1 + 1 + 1  # Estimate: Transform label, FadeIn rule, FadeIn digit, Indicate, FadeOut
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 5
        step = sequence[4]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Update step label
        new_step_label = Text("Step 5: Round 3.7 up to 4.", color=LIGHT_GRAY, font_size=24)
        new_step_label.move_to(step_label.get_center())
        self.play(ReplacementTransform(step_label, new_step_label))
        step_label = new_step_label
        
        # Signal action: Indicate point_4
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_id = signal["target"]
            color = signal.get("color", "YELLOW")
            target_obj = self.objects[target_id]
            color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
            self.play(Indicate(target_obj, color=color_map.get(color, YELLOW)))
        
        # Create a copy of point_4 for transformation target
        point_4_target = Dot(radius=0.08, color=GREEN)
        point_4_target.move_to(point_4.get_center())
        
        # Create transformed label
        label_4_transformed = MathTex("4", color=GREEN)
        label_4_transformed.move_to(label_37.get_center())
        
        # Animate point moving and label transforming
        self.play(
            Transform(point_37, point_4_target),
            Transform(label_37, label_4_transformed)
        )
        
        # Also fade out digit highlight
        self.play(FadeOut(digit_highlight))
        
        animation_time = 1 + 1 + 2 + 1  # Estimate: Transform label, Indicate, Transform point/label, FadeOut
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Final hold
        self.wait(2)