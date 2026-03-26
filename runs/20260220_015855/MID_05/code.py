from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define constants
        R = 2.0
        CIRCUMFERENCE_LENGTH = 2 * PI * R  # Approximately 12.566
        
        # Create objects as per layout_plan
        title = Text("Unrolling a Circle to Find Pi", color=WHITE, font_size=40)
        title.to_edge(UP)
        
        circle = Circle(radius=R, color=BLUE, stroke_width=3)
        circle.shift(LEFT * 3.5)
        
        diameter_line = Line(start=LEFT*R, end=RIGHT*R, color=YELLOW, stroke_width=3)
        diameter_line.move_to(circle.get_center())
        
        label_D = MathTex("D", color=YELLOW)
        label_D.next_to(diameter_line, UP, buff=0.2)
        
        # Unrolled line: start at circle's rightmost point, extend rightwards
        unrolled_line_start = np.array([-3.5 + R, 0, 0])
        unrolled_line_end = np.array([-3.5 + R + CIRCUMFERENCE_LENGTH, 0, 0])
        unrolled_line = Line(
            start=unrolled_line_start, 
            end=unrolled_line_start,  # Start with zero length
            color=GREEN, 
            stroke_width=3
        )
        unrolled_line.set_opacity(0)  # Initially invisible
        
        # Diameter copy for comparison (initially invisible)
        diameter_copy = Line(start=LEFT*R, end=RIGHT*R, color=YELLOW, stroke_width=3)
        diameter_copy.move_to(np.array([3.5, -1.5, 0]))
        diameter_copy.set_opacity(0)
        
        label_D_copy = MathTex("D", color=YELLOW)
        label_D_copy.next_to(diameter_copy, UP, buff=0.2)
        label_D_copy.set_opacity(0)
        
        explanation_text = Text(
            "The unrolled circumference is the line's length.", 
            color=LIGHT_GRAY, 
            font_size=24
        )
        explanation_text.to_edge(DOWN)
        explanation_text.set_opacity(0)
        
        formula_CeqPiD = MathTex("C = \\pi D", color=GREEN, font_size=36)
        formula_CeqPiD.next_to(explanation_text, DOWN, buff=0.3)
        formula_CeqPiD.set_opacity(0)
        
        # Group diameter line and its label for transformation
        diameter_group = VGroup(diameter_line, label_D)
        diameter_copy_group = VGroup(diameter_copy, label_D_copy)
        
        # Store objects in a dictionary for easy access
        self.objects = {
            "title": title,
            "circle": circle,
            "diameter_line": diameter_line,
            "label_D": label_D,
            "unrolled_line": unrolled_line,
            "diameter_copy": diameter_copy,
            "label_D_copy": label_D_copy,
            "explanation_text": explanation_text,
            "formula_CeqPiD": formula_CeqPiD,
        }
        
        # Add all objects to scene (initially invisible except title)
        self.add(title)
        self.add(circle, diameter_line, label_D, unrolled_line, 
                diameter_copy, label_D_copy, explanation_text, formula_CeqPiD)
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        step = {
            "step": 1,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3",
            "duration": 6.768,
            "signal_action": None,
            "visual_action": {"type": "Create", "target_id": "circle"}
        }
        self.add_sound(step["audio_path"])
        self.play(Create(circle), run_time=2)
        self.wait(step["duration"] - 2)
        
        # Step 2
        step = {
            "step": 2,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3",
            "duration": 6.216,
            "signal_action": {"type": "Indicate", "target": "circle", "color": "WHITE"},
            "visual_action": {"type": "Create", "target_id": "diameter_line"}
        }
        self.add_sound(step["audio_path"])
        if step["signal_action"] is not None:
            self.play(Indicate(circle, color=WHITE), run_time=1)
        self.play(Create(diameter_line), run_time=1.5)
        self.wait(step["duration"] - 1 - 1.5)
        
        # Step 3
        step = {
            "step": 3,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3",
            "duration": 2.304,
            "signal_action": None,
            "visual_action": {"type": "Write", "target_id": "label_D"}
        }
        self.add_sound(step["audio_path"])
        self.play(Write(label_D), run_time=1)
        self.wait(step["duration"] - 1)
        
        # Step 4
        step = {
            "step": 4,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3",
            "duration": 6.36,
            "signal_action": {"type": "Circumscribe", "target": "circle", "color": "GREEN"},
            "visual_action": {"type": "Custom", "target_id": "unrolled_line"}
        }
        self.add_sound(step["audio_path"])
        if step["signal_action"] is not None:
            self.play(Circumscribe(circle, color=GREEN, run_time=1))
        
        # Animate the unrolling: grow the line from the circle's rightmost point
        unrolled_line.set_opacity(1)
        self.play(
            unrolled_line.animate.put_start_and_end_on(unrolled_line_start, unrolled_line_end),
            run_time=3
        )
        self.wait(step["duration"] - 1 - 3)
        
        # Step 5
        step = {
            "step": 5,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3",
            "duration": 6.72,
            "signal_action": {"type": "Indicate", "target": "unrolled_line", "color": "WHITE"},
            "visual_action": {"type": "FadeIn", "target_id": "explanation_text"}
        }
        self.add_sound(step["audio_path"])
        if step["signal_action"] is not None:
            self.play(Indicate(unrolled_line, color=WHITE), run_time=1)
        self.play(FadeIn(explanation_text), run_time=1)
        self.wait(step["duration"] - 1 - 1)
        
        # Step 6
        step = {
            "step": 6,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3",
            "duration": 6.648,
            "signal_action": {"type": "Indicate", "target": "diameter_line", "color": "YELLOW"},
            "visual_action": {"type": "ReplacementTransform", "target_id": "diameter_line"}
        }
        self.add_sound(step["audio_path"])
        if step["signal_action"] is not None:
            self.play(Indicate(diameter_line, color=YELLOW), run_time=1)
        
        # Make the copy visible for transformation
        diameter_copy.set_opacity(1)
        label_D_copy.set_opacity(1)
        self.play(
            ReplacementTransform(diameter_group, diameter_copy_group),
            run_time=2
        )
        self.wait(step["duration"] - 1 - 2)
        
        # Step 7
        step = {
            "step": 7,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3",
            "duration": 8.04,
            "signal_action": {"type": "Indicate", "target": "unrolled_line", "color": "GREEN"},
            "visual_action": {"type": "FadeIn", "target_id": "formula_CeqPiD"}
        }
        self.add_sound(step["audio_path"])
        if step["signal_action"] is not None:
            self.play(Indicate(unrolled_line, color=GREEN), run_time=1)
        self.play(FadeIn(formula_CeqPiD), run_time=1.5)
        self.wait(step["duration"] - 1 - 1.5)
        
        # Step 8
        step = {
            "step": 8,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_07.mp3",
            "duration": 7.032,
            "signal_action": {"type": "Circumscribe", "target": "formula_CeqPiD", "color": "YELLOW"},
            "visual_action": {"type": "Wait", "target_id": None}
        }
        self.add_sound(step["audio_path"])
        if step["signal_action"] is not None:
            self.play(Circumscribe(formula_CeqPiD, color=YELLOW, run_time=1))
        self.wait(step["duration"] - 1)