from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        self.objects = {}
        
        # Title
        title = Text("Unrolling a Circle to Discover Pi (π)", color=WHITE, font_size=40)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title
        
        # Circle
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(ORIGIN)
        self.objects["circle"] = circle
        
        # Diameter Line
        diameter_line = Line(start=[-2, 0, 0], end=[2, 0, 0], color=YELLOW, stroke_width=6)
        diameter_line.move_to(circle.get_center())
        self.objects["diameter_line"] = diameter_line
        
        # Diameter Label
        diameter_label = MathTex("D", color=YELLOW)
        diameter_label.next_to(diameter_line, UP, buff=0.2)
        diameter_label.shift(LEFT * 0.1)
        self.objects["diameter_label"] = diameter_label
        
        # Unrolled Line (initially invisible)
        unrolled_line = Line(start=[-6.28, -0.5, 0], end=[6.28, -0.5, 0], color=GREEN, stroke_width=4)
        unrolled_line.set_opacity(0.0)
        unrolled_line.move_to([0, -0.5, 0])
        self.objects["unrolled_line"] = unrolled_line
        
        # Unrolled Line Start Label (initially invisible)
        line_label_start = MathTex("C", color=GREEN)
        line_label_start.set_opacity(0.0)
        line_label_start.next_to(unrolled_line, UP, buff=0.2)
        line_label_start.align_to(unrolled_line.get_start(), LEFT)
        self.objects["line_label_start"] = line_label_start
        
        # Diameter Segments for measurement (initially invisible)
        diameter_segment_1 = Line(start=[0, 0, 0], end=[4, 0, 0], color=YELLOW, stroke_width=4)
        diameter_segment_1.set_opacity(0.0)
        self.objects["diameter_segment_1"] = diameter_segment_1
        
        diameter_segment_2 = Line(start=[0, 0, 0], end=[4, 0, 0], color=YELLOW, stroke_width=4)
        diameter_segment_2.set_opacity(0.0)
        self.objects["diameter_segment_2"] = diameter_segment_2
        
        diameter_segment_3 = Line(start=[0, 0, 0], end=[4, 0, 0], color=YELLOW, stroke_width=4)
        diameter_segment_3.set_opacity(0.0)
        self.objects["diameter_segment_3"] = diameter_segment_3
        
        diameter_segment_4_partial = Line(start=[0, 0, 0], end=[0.56, 0, 0], color=RED, stroke_width=4)
        diameter_segment_4_partial.set_opacity(0.0)
        self.objects["diameter_segment_4_partial"] = diameter_segment_4_partial
        
        # Group and position diameter segments
        diameter_segments = VGroup(diameter_segment_1, diameter_segment_2, diameter_segment_3, diameter_segment_4_partial)
        diameter_segments.arrange(RIGHT, buff=0)
        diameter_segments.move_to([0, 1, 0])
        self.objects["diameter_segments"] = diameter_segments
        
        # Measurement Label (initially invisible)
        measurement_label = MathTex("D + D + D + 0.14D = 3.14D", color=WHITE)
        measurement_label.set_opacity(0.0)
        measurement_label.next_to(diameter_segments, UP, buff=0.8)
        self.objects["measurement_label"] = measurement_label
        
        # Pi Equation (initially invisible)
        pi_equation = MathTex(r"\pi = \frac{C}{D} \approx 3.14", color=PINK, font_size=36)
        pi_equation.set_opacity(0.0)
        pi_equation.to_edge(DOWN, buff=0.5)
        self.objects["pi_equation"] = pi_equation
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start with a circle. Its diameter, labeled D, is the distance across through the center.",
                "signal_action": {"type": "Indicate", "target": "diameter_line", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "circle", "details": "Draw the blue circle"},
                "duration": 6.768,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Now, let's unroll the circumference of the circle, transforming it into a straight line.",
                "signal_action": {"type": "Indicate", "target": "circle", "color": "BLUE"},
                "visual_action": {"type": "Transform", "target_id": "circle", "details": "Morph the circle mobject into the unrolled_line mobject. This gives the visual effect of the perimeter straightening out. Simultaneously, set opacity of unrolled_line to 1.0 and write the label C."},
                "duration": 5.736,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "How does the length of this line, the circumference C, compare to the diameter D? Let's measure C using copies of D.",
                "signal_action": {"type": "Circumscribe", "target": "unrolled_line", "color": "GREEN"},
                "visual_action": {"type": "Create", "target_id": "diameter_segment_1", "details": "Fade in the first yellow diameter segment above the left end of the unrolled line."},
                "duration": 8.28,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "One diameter fits. A second diameter fits end-to-end... and a third.",
                "signal_action": {"type": "Indicate", "target": "diameter_segment_1", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "diameter_segment_2", "details": "Fade in the second diameter segment, aligned to the end of the first."},
                "duration": 5.736,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Three diameters are placed, but the line is still not fully covered. There's a small gap remaining.",
                "signal_action": {"type": "Create", "target_id": "diameter_segment_3", "details": "Fade in the third diameter segment, aligned to the end of the second."},
                "visual_action": {"type": "Indicate", "target": "unrolled_line_end", "color": "GREEN"},
                "duration": 6.888,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The remaining gap is about 0.14 times the diameter. So the total circumference is approximately three diameters plus a little bit more.",
                "signal_action": {"type": "Indicate", "target": "diameter_segment_4_partial", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "diameter_segment_4_partial", "details": "Fade in the small red segment to fill the gap. Then write the measurement label above."},
                "duration": 9.312,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Therefore, the circumference C is about 3.14 times the diameter D. This ratio is the famous constant Pi.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "pi_equation", "details": "Write the final Pi equation in the footer zone."},
                "duration": 7.68,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
            }
        ]
        
        # Add title at the beginning
        self.play(Write(title))
        self.wait(0.5)
        
        for step in sequence:
            # === AUDIO (MANDATORY) ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                # Handle special case for step 5 where signal action is Create
                if signal.get("type") == "Create" and signal.get("target_id") == "diameter_segment_3":
                    target_obj = self.objects[signal["target_id"]]
                    self.play(FadeIn(target_obj))
                else:
                    # Normal signal action handling
                    target_key = signal.get("target")
                    if target_key in self.objects:
                        target_obj = self.objects[target_key]
                        color = eval(signal["color"]) if signal.get("color") else YELLOW
                        if signal["type"] == "Circumscribe":
                            self.play(Circumscribe(target_obj, color=color, run_time=1))
                        elif signal["type"] == "Indicate":
                            self.play(Indicate(target_obj, color=color))
            
            # Visual Action
            visual = step["visual_action"]
            target_id = visual.get("target_id")
            
            # Handle special case for step 5 visual action
            if target_id == "unrolled_line_end":
                # Create a dot at the end of the unrolled line to indicate it
                end_point = self.objects["unrolled_line"].get_end()
                dot = Dot(end_point, color=GREEN)
                self.play(FadeIn(dot, scale=0.5), run_time=0.5)
                self.play(FadeOut(dot), run_time=0.5)
            elif target_id in self.objects:
                target_obj = self.objects[target_id]
                
                if visual["type"] == "Create":
                    if target_id == "circle":
                        self.play(Create(target_obj), Create(self.objects["diameter_line"]), Write(self.objects["diameter_label"]))
                    elif target_id == "diameter_segment_1":
                        self.play(FadeIn(target_obj))
                    elif target_id == "diameter_segment_2":
                        self.play(FadeIn(target_obj))
                    elif target_id == "diameter_segment_3":
                        # Already handled in signal action for step 5
                        pass
                    elif target_id == "diameter_segment_4_partial":
                        self.play(FadeIn(target_obj), Write(self.objects["measurement_label"]))
                elif visual["type"] == "Transform":
                    # Transform circle into unrolled line
                    unrolled_line_copy = self.objects["unrolled_line"].copy()
                    unrolled_line_copy.set_opacity(1.0)
                    line_label = self.objects["line_label_start"].copy()
                    line_label.set_opacity(1.0)
                    
                    # Create the transform animation
                    self.play(
                        Transform(self.objects["circle"], unrolled_line_copy),
                        self.objects["diameter_line"].animate.set_opacity(0.0),
                        self.objects["diameter_label"].animate.set_opacity(0.0),
                        Write(line_label)
                    )
                    # Update the actual objects
                    self.objects["unrolled_line"].set_opacity(1.0)
                    self.objects["line_label_start"].set_opacity(1.0)
                elif visual["type"] == "Write":
                    self.play(Write(target_obj))
            
            # Wait for remaining audio duration
            animation_time = 1.0 if signal and signal.get("type") in ["Circumscribe", "Indicate"] else 0.0
            animation_time += 1.0  # Approximate time for visual action
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)
        
        # Final wait
        self.wait(2)