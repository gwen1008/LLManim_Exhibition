'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing displacement on a number line, moving from -2 to +3, and representing the distance as a vector arrow.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, dots, arrow, and distance label
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use relative positioning (next_to, move_to) to keep elements spaced. Arrow is placed above the line, labels below dots.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/jump_on_number_line/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line.
#    - Step 2: Indicate and create start dot.
#    - Step 3: Animate dot jump to +3.
#    - Step 4: Circumscribe start label, update explanation text.
#    - Step 5: Grow displacement arrow.
#    - Step 6: Indicate and write distance label.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_Manim_anima_297db7ebc5/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Jump on the Number Line: -2 to +3", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create number line
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=10,
            include_numbers=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Create start dot
        start_dot = Dot(radius=0.1, color=BLUE, fill_opacity=1)
        start_dot.move_to(content_center + 2 * LEFT)
        self.objects["start_dot"] = start_dot

        # Create start label
        start_label = MathTex("-2", color=BLUE, font_size=30)
        start_label.next_to(start_dot, DOWN, buff=0.2)
        self.objects["start_label"] = start_label

        # Create end dot ghost (faint)
        end_dot_ghost = Dot(radius=0.1, color=BLUE, fill_opacity=0.3)
        end_dot_ghost.move_to(content_center + 3 * RIGHT)
        self.objects["end_dot_ghost"] = end_dot_ghost

        # Create end label
        end_label = MathTex("+3", color=BLUE, font_size=30)
        end_label.next_to(end_dot_ghost, DOWN, buff=0.2)
        self.objects["end_label"] = end_label

        # Create displacement arrow (initially zero length at start point)
        arrow_start = content_center + 2 * LEFT + 0.5 * UP
        arrow_end = content_center + 3 * RIGHT + 0.5 * UP
        displacement_arrow = Arrow(
            start=arrow_start,
            end=arrow_start,  # Zero length initially
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["displacement_arrow"] = displacement_arrow

        # Create distance label
        distance_label = MathTex("5\\ \\mathrm{units}", color=YELLOW, font_size=30)
        distance_label.move_to(content_center + 0.5 * RIGHT + 1.2 * UP)
        self.objects["distance_label"] = distance_label

        # Create initial explanation text
        explanation_text = Text(
            "We begin with a number line and an object at -2.",
            color=GRAY_B,
            font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/jump_on_number_line/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Create(self.objects["number_line"]), run_time=2.5)
        remaining_1 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/jump_on_number_line/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["start_dot"], color=BLUE, run_time=1))
        self.play(Create(self.objects["start_dot"]), run_time=1.0)
        remaining_2 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/jump_on_number_line/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(
            self.objects["start_dot"].animate.move_to(self.objects["end_dot_ghost"].get_center()),
            run_time=3.0
        )
        remaining_3 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/jump_on_number_line/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["start_label"], color=YELLOW, run_time=1))

        new_explanation = Text(
            "The displacement is a vector from start to end.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation), run_time=2.0)
        self.objects["explanation_text"] = new_explanation
        remaining_4 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/jump_on_number_line/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Update arrow to have full length for GrowArrow
        full_arrow = Arrow(
            start=arrow_start,
            end=arrow_end,
            buff=0,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.play(GrowArrow(full_arrow), run_time=2.5)
        self.objects["displacement_arrow"] = full_arrow
        remaining_5 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/jump_on_number_line/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["distance_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["distance_label"]), run_time=2.0)
        remaining_6 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))