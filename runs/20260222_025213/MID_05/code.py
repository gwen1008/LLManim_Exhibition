'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the relationship between a circle's circumference and its diameter, leading to the definition of π.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle and unrolled line (left-right split)
#    - Footer Region: [Bottom y=-3.5] for formula and explanation
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use explicit anchors for left (circle) and right (line) staging. Measurement segments are placed in a row below. Footer text is stacked vertically.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/{topic_safe_name}/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Show circle and diameter.
#    - Highlight circumference, then unroll it into a straight line.
#    - Move the line to a measurement area.
#    - Compare it against three diameter copies and a small remainder.
#    - Derive the approximate and exact formulas (C ≈ 3D + 0.14D → C = πD).
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        circle_anchor = 3 * LEFT  # Left of center
        line_start_anchor = 3 * RIGHT  # Right of center
        measurement_center = 0.5 * DOWN  # Below main action
        explanation_anchor = 3.2 * DOWN  # Footer

        # Object registry
        self.objects = {}

        # Helper to parse position strings (simplified for this blueprint)
        def parse_pos(pos_str, ref_obj=None):
            if pos_str == "move_to(title_anchor)":
                return title_anchor
            elif pos_str == "move_to(circle_anchor)":
                return circle_anchor
            elif pos_str == "move_to(line_start_anchor)":
                return line_start_anchor
            elif pos_str == "move_to(measurement_center)":
                return measurement_center
            elif pos_str == "move_to(explanation_anchor)":
                return explanation_anchor
            elif pos_str.startswith("move_to("):
                # Generic move_to with offset
                if "measurement_center + UP*1.0 + LEFT*" in pos_str:
                    # Special case for scaled line: compute length
                    scale_factor = 0.7
                    line_length = 2 * PI * 2.0 * scale_factor
                    return measurement_center + UP * 1.0 + LEFT * (line_length / 2)
                elif "measurement_center + LEFT*6.0" in pos_str:
                    return measurement_center + LEFT * 6.0
            elif pos_str.startswith("next_to("):
                parts = pos_str.replace("next_to(", "").replace(")", "").split(",")
                target_id = parts[0].strip()
                direction = parts[1].strip()
                buff = 0.2
                if "buff=" in pos_str:
                    buff_str = pos_str.split("buff=")[1].split(")")[0]
                    buff = float(buff_str)
                target_obj = self.objects.get(target_id)
                if target_obj:
                    if direction == "UP":
                        return target_obj.get_top() + buff * UP
                    elif direction == "DOWN":
                        return target_obj.get_bottom() + buff * DOWN
                    elif direction == "RIGHT":
                        return target_obj.get_right() + buff * RIGHT
                    elif direction == "LEFT":
                        return target_obj.get_left() + buff * LEFT
            return ORIGIN

        # Create objects from layout_plan.objects
        # title
        title = Text("Unrolling a Circle's Circumference", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        circle.move_to(circle_anchor)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(start=LEFT*2, end=RIGHT*2, color=YELLOW, stroke_width=6)
        diameter_line.move_to(circle_anchor)
        self.objects["diameter_line"] = diameter_line

        # diameter_label
        diameter_label = MathTex("D", color=YELLOW)
        diameter_label.next_to(diameter_line, UP, buff=0.2)
        self.objects["diameter_label"] = diameter_label

        # circle_perimeter (Arc)
        circle_perimeter = Arc(radius=2.0, angle=2*PI, color=GREEN, stroke_width=6)
        circle_perimeter.move_to(circle_anchor)
        self.objects["circle_perimeter"] = circle_perimeter

        # unrolled_line
        line_length = 2 * PI * 2.0
        unrolled_line = Line(start=ORIGIN, end=RIGHT * line_length, color=GREEN, stroke_width=6)
        unrolled_line.move_to(line_start_anchor)
        self.objects["unrolled_line"] = unrolled_line

        # line_label
        line_label = MathTex("C", color=GREEN)
        line_label.next_to(unrolled_line, UP, buff=0.2)
        self.objects["line_label"] = line_label

        # diameter_segment_1
        diameter_segment_1 = Line(start=ORIGIN, end=RIGHT*4.0, color=YELLOW, stroke_width=4)
        diameter_segment_1.move_to(measurement_center + LEFT*6.0)
        self.objects["diameter_segment_1"] = diameter_segment_1

        # diameter_segment_2
        diameter_segment_2 = Line(start=ORIGIN, end=RIGHT*4.0, color=YELLOW, stroke_width=4)
        diameter_segment_2.next_to(diameter_segment_1, RIGHT, buff=0)
        self.objects["diameter_segment_2"] = diameter_segment_2

        # diameter_segment_3
        diameter_segment_3 = Line(start=ORIGIN, end=RIGHT*4.0, color=YELLOW, stroke_width=4)
        diameter_segment_3.next_to(diameter_segment_2, RIGHT, buff=0)
        self.objects["diameter_segment_3"] = diameter_segment_3

        # remainder_segment
        remainder_length = line_length - 12.0  # 3 * diameter length (4.0 each)
        remainder_segment = Line(start=ORIGIN, end=RIGHT * remainder_length, color=RED, stroke_width=4)
        remainder_segment.next_to(diameter_segment_3, RIGHT, buff=0)
        self.objects["remainder_segment"] = remainder_segment

        # measurement_line_scaled
        scale_factor = 0.7
        scaled_length = line_length * scale_factor
        measurement_line_scaled = Line(start=ORIGIN, end=RIGHT * scaled_length, color=GREEN, stroke_width=6)
        measurement_line_scaled.set_opacity(0.7)
        measurement_line_scaled.move_to(measurement_center + UP*1.0 + LEFT*(scaled_length / 2))
        self.objects["measurement_line_scaled"] = measurement_line_scaled

        # formula_line_1
        formula_line_1 = MathTex(r"C \approx 3D + 0.14D", color=WHITE, font_size=30)
        formula_line_1.move_to(explanation_anchor)
        self.objects["formula_line_1"] = formula_line_1

        # formula_line_2
        formula_line_2 = MathTex(r"C = \pi D", color=BLUE, font_size=36)
        formula_line_2.next_to(formula_line_1, DOWN, buff=0.5)
        self.objects["formula_line_2"] = formula_line_2

        # formula_line_3
        formula_line_3 = MathTex(r"\pi \approx 3.14 > 3", color=YELLOW, font_size=30)
        formula_line_3.next_to(formula_line_2, DOWN, buff=0.5)
        self.objects["formula_line_3"] = formula_line_3

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["circle"]))
        self.wait(max(0.1, max(0.1, 6.432 - 1)))  # Approx animation time 1s

        # Step 2
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW))
        self.play(Create(self.objects["diameter_line"]), Write(self.objects["diameter_label"]))
        self.wait(max(0.1, max(0.1, 2.448 - 2)))  # Indicate + Create

        # Step 3
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["circle"], color=GREEN, run_time=1))
        self.play(Create(self.objects["circle_perimeter"]))
        self.wait(max(0.1, max(0.1, 8.28 - 2)))

        # Step 4
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Transform(self.objects["circle_perimeter"], self.objects["unrolled_line"]),
                  Write(self.objects["line_label"]))
        self.wait(max(0.1, max(0.1, 1.776 - 1)))

        # Step 5
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["unrolled_line"], color=GREEN))
        self.play(FadeOut(self.objects["circle"]),
                  self.objects["unrolled_line"].animate.move_to(self.objects["measurement_line_scaled"].get_center()).scale(0.7).set_opacity(0.7),
                  self.objects["line_label"].animate.next_to(self.objects["measurement_line_scaled"], UP, buff=0.2))
        self.wait(max(0.1, max(0.1, 5.496 - 3)))

        # Step 6
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["diameter_segment_1"], color=YELLOW))
        self.play(Create(self.objects["diameter_segment_1"]))
        self.play(Create(self.objects["diameter_segment_2"]))
        self.play(Create(self.objects["diameter_segment_3"]))
        self.wait(max(0.1, max(0.1, 4.2 - 3)))

        # Step 7
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["remainder_segment"], color=RED))
        self.play(Create(self.objects["remainder_segment"]))
        self.wait(max(0.1, max(0.1, 4.92 - 1)))

        # Step 8
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["formula_line_1"]))
        self.wait(max(0.1, max(0.1, 8.736 - 1)))

        # Step 9
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["formula_line_2"], color=BLUE, run_time=1))
        self.play(TransformMatchingTex(self.objects["formula_line_1"], self.objects["formula_line_2"]))
        self.wait(max(0.1, max(0.1, 7.752 - 2)))

        # Step 10
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_09.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["formula_line_3"]))
        self.wait(max(0.1, max(0.1, 6.504 - 1)))