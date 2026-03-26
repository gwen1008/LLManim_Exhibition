'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the relationship between a circle's circumference and its diameter to discover Pi (π). The animation shows unrolling the circumference into a straight line and measuring it with the diameter.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle (left) and unrolled line (right)
#    - Footer Region: [Bottom y=-3.5] for explanation text and final formula.
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct left/right zones for circle and line. Keep footer text concise. Use VGroups for diameter and its label.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show circle and diameter.
#    - Step 2: Indicate circle, then unroll circumference into a line (custom animation).
#    - Step 3: Circumscribe line, update and show explanation.
#    - Step 4: Measure line with diameter copies.
#    - Step 5: Indicate line, update explanation, reveal formula C = πD.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors (based on layout_plan.anchors)
        title_anchor = 3.5 * UP
        content_left = 3 * LEFT
        content_right = 3 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Unrolling a Circle to Find Pi", font_size=48, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        circle.move_to(content_left)
        self.objects["circle"] = circle

        # diameter (vertical line through circle center)
        # geometry_def: "start=[-1.5, 2, 0], end=[-1.5, -2, 0]" relative to content_left? We'll create it at circle center.
        diameter = Line(start=UP*2, end=DOWN*2, color=RED, stroke_width=6)
        diameter.move_to(circle.get_center())
        self.objects["diameter"] = diameter

        # label_d
        label_d = MathTex("D", color=RED)
        label_d.next_to(diameter, RIGHT, buff=0.2)
        self.objects["label_d"] = label_d

        # unrolled_line (length = 2*π*radius ≈ 12.566)
        line_length = 2 * PI * 2.0  # ~12.566
        unrolled_line = Line(start=ORIGIN, end=RIGHT * line_length, color=GREEN, stroke_width=4)
        unrolled_line.move_to(content_right).align_to(content_right, LEFT)
        unrolled_line.set_opacity(0.0)
        self.objects["unrolled_line"] = unrolled_line

        # diameter_copy (movable for measurement)
        diameter_copy = Line(start=ORIGIN, end=UP*4, color=RED, stroke_width=4)
        # Initial position per JSON: content_right + UP*2.5 + LEFT*2
        diameter_copy.move_to(content_right + UP*2.5 + LEFT*2)
        diameter_copy.set_opacity(0.0)
        self.objects["diameter_copy"] = diameter_copy

        # label_d_copy
        label_d_copy = MathTex("D", color=RED)
        label_d_copy.next_to(diameter_copy, RIGHT, buff=0.2)
        label_d_copy.set_opacity(0.0)
        self.objects["label_d_copy"] = label_d_copy

        # explanation_text
        explanation_text = Text("The unrolled circumference is a straight line.", font_size=36, color=YELLOW)
        explanation_text.move_to(footer_anchor)
        explanation_text.set_opacity(0.0)
        self.objects["explanation_text"] = explanation_text

        # formula
        formula = MathTex("C = \\pi D", font_size=48, color=GREEN)
        formula.move_to(footer_anchor + DOWN*0.8)
        formula.set_opacity(0.0)
        self.objects["formula"] = formula

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 6.912,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual Action: Create circle (and diameter/label? JSON says only circle, but diameter is part of setup. We'll create them all but only animate circle.)
        self.play(Create(circle))
        # Also create diameter and label but without animation? They should be visible. Let's Write them.
        self.play(Write(diameter), Write(label_d))
        animation_time = 1.0 + 1.0  # Create circle ~1s, Write diameter+label ~1s
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "circle", "color": "YELLOW"},
            "duration": 6.336,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action: Custom unroll animation
        # We'll approximate: a dot traces circle perimeter while line draws.
        # Create a dot
        dot = Dot(color=GREEN).move_to(circle.get_start())
        # Animate dot moving around circle
        line_animation = Create(unrolled_line)  # This will draw the line from start to end
        # We'll run them concurrently
        self.play(MoveAlongPath(dot, circle), line_animation, run_time=3)
        # Fade out circle stroke? Let's just fade the circle itself to emphasize line.
        self.play(circle.animate.set_opacity(0.3), FadeOut(dot))
        # Set unrolled_line opacity to 1 (it already is after Create)
        unrolled_line.set_opacity(1.0)
        animation_time = 1.0 + 3.0 + 1.0  # Indicate ~1s, MoveAlongPath+Create ~3s, Fade ~1s
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Circumscribe", "target": "unrolled_line", "color": "GREEN"},
            "duration": 6.384,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = GREEN if signal.get("color") == "GREEN" else eval(signal.get("color"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Visual Action: Update explanation text and fade in
        new_text = Text("The unrolled circumference is length C.", font_size=36, color=YELLOW)
        new_text.move_to(footer_anchor)
        new_text.set_opacity(0.0)
        self.play(ReplacementTransform(explanation_text, new_text))
        explanation_text = new_text
        self.objects["explanation_text"] = explanation_text
        self.play(explanation_text.animate.set_opacity(1.0))
        animation_time = 1.0 + 1.0 + 1.0  # Circumscribe ~1s, ReplacementTransform ~1s, FadeIn ~1s
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 4
        step = {
            "step": 4,
            "duration": 6.648,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual Action: Animate measurement with diameter_copy
        # Fade in diameter_copy and label at left end of unrolled_line
        diameter_copy.move_to(unrolled_line.get_start() + UP*2)  # Position above line start
        label_d_copy.next_to(diameter_copy, RIGHT, buff=0.2)
        self.play(FadeIn(diameter_copy), FadeIn(label_d_copy))
        # Animate sliding along line, leaving marks
        marks = VGroup()
        for i in range(3):  # positions 0, D, 2D
            mark = Line(start=unrolled_line.get_start() + RIGHT * (i * 4), 
                        end=unrolled_line.get_start() + RIGHT * (i * 4) + UP*0.3, 
                        color=RED, stroke_width=2)
            marks.add(mark)
        # Slide diameter_copy along line
        self.play(diameter_copy.animate.shift(RIGHT * 4), run_time=1.5)
        self.add(marks[0])
        self.play(diameter_copy.animate.shift(RIGHT * 4), run_time=1.5)
        self.add(marks[1])
        # Stop at 3D, showing remaining segment
        self.play(diameter_copy.animate.shift(RIGHT * 4), run_time=1.5)
        self.add(marks[2])
        # Show remaining segment (from 3D to end of line)
        remaining_seg = Line(start=unrolled_line.get_start() + RIGHT * 12, 
                             end=unrolled_line.get_end(), 
                             color=YELLOW, stroke_width=6)
        self.play(Create(remaining_seg))
        animation_time = 1.0 + 4.5 + 1.0  # FadeIn ~1s, three shifts ~4.5s, Create remaining ~1s
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "unrolled_line", "color": "GREEN"},
            "duration": 12.384,
            "audio_path": "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = GREEN if signal.get("color") == "GREEN" else eval(signal.get("color"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action: Update explanation text and fade in formula
        new_text2 = Text("C is about 3.14 times longer than D.", font_size=36, color=YELLOW)
        new_text2.move_to(footer_anchor)
        self.play(ReplacementTransform(explanation_text, new_text2))
        explanation_text = new_text2
        self.objects["explanation_text"] = explanation_text
        # Fade in formula
        self.play(FadeIn(formula))
        animation_time = 1.0 + 1.0 + 1.0  # Indicate ~1s, ReplacementTransform ~1s, FadeIn ~1s
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, max(0.1, remaining)))

        # Final wait
        self.wait(max(0.1, 2))