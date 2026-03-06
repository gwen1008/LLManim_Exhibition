'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing movement on a number line, specifically the jump from -2 to +3, to understand displacement as a vector.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and objects
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for dot+label pairs. Keep number line centered. Use ReplacementTransform for explanation text to avoid stacking.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/jump_on_the_number_line_from_2_to_3/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Create number line.
#    Step 2: Indicate start position, create start dot.
#    Step 3: Write start label.
#    Step 4: Animate dot moving and changing color.
#    Step 5: Circumscribe and create jump arrow.
#    Step 6: Indicate arrow, write end label, show and hide distance calculation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_Manim_anima_525afdf3db/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Jump on the Number Line: From -2 to +3", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=12,
            include_numbers=True,
            color=GRAY_B  # GRAY_C -> GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # start_dot (position depends on number_line.n2p, so create after number_line)
        start_dot = Dot(radius=0.1, color=BLUE, fill_opacity=1.0)
        start_dot.move_to(number_line.n2p(-2))
        self.objects["start_dot"] = start_dot

        # start_label
        start_label = MathTex("-2", color=BLUE, font_size=24)
        start_label.next_to(start_dot, DOWN, buff=0.2)
        self.objects["start_label"] = start_label

        # end_dot
        end_dot = Dot(radius=0.1, color=GREEN, fill_opacity=0.0)  # initially invisible
        end_dot.move_to(number_line.n2p(3))
        self.objects["end_dot"] = end_dot

        # end_label
        end_label = MathTex("+3", color=GREEN, font_size=24)
        end_label.next_to(number_line.n2p(3), DOWN, buff=0.2)
        end_label.set_opacity(0.0)
        self.objects["end_label"] = end_label

        # jump_arrow (geometry depends on dots, create after them)
        jump_arrow = Arrow(
            start=start_dot.get_center(),
            end=end_dot.get_center(),
            buff=0,
            color=YELLOW,
            stroke_width=6
        )
        jump_arrow.set_opacity(0.0)
        self.objects["jump_arrow"] = jump_arrow

        # step_explanation
        step_explanation = Text(
            "Step 1: The number line from -5 to 5.",
            color=GRAY_B,  # GRAY_C -> GRAY_B
            font_size=28
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # distance_label (temporary, from step 6 visual_action)
        distance_label = MathTex("3 - (-2) = 5", color=YELLOW, font_size=32)
        distance_label.next_to(jump_arrow, UP, buff=0.5)
        distance_label.set_opacity(0.0)
        self.objects["distance_label"] = distance_label

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/jump_on_the_number_line_from_2_to_3/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # visual_action: Create number_line
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/jump_on_the_number_line_from_2_to_3/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # signal_action: Indicate number_line.n2p(-2)
        temp_dot = Dot(self.objects["number_line"].n2p(-2), color=BLUE, radius=0.15)
        self.play(Indicate(temp_dot, color=BLUE, run_time=1))
        # visual_action: Create start_dot
        self.play(FadeIn(self.objects["start_dot"]), run_time=1.0)
        remaining_2 = max(0.1, 2.5 - 1.0 - 1.0 + 0.5)  # total 2.5, signal 1.0, anim 1.0
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/jump_on_the_number_line_from_2_to_3/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # visual_action: Write start_label
        self.play(Write(self.objects["start_label"]), run_time=1.0)
        remaining_3 = max(0.1, 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/jump_on_the_number_line_from_2_to_3/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # visual_action: Animate start_dot moving and changing color
        # We'll animate the dot moving to end position and interpolating color
        start_dot_anim = self.objects["start_dot"].animate.move_to(self.objects["number_line"].n2p(3)).set_color(GREEN)
        self.play(start_dot_anim, run_time=2.5)
        remaining_4 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/jump_on_the_number_line_from_2_to_3/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # signal_action: Circumscribe jump_arrow
        self.play(Circumscribe(self.objects["jump_arrow"], color=YELLOW, run_time=1))
        # visual_action: Create jump_arrow (fade in)
        self.play(self.objects["jump_arrow"].animate.set_opacity(1), run_time=1.5)
        remaining_5 = max(0.1, 3.0 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/jump_on_the_number_line_from_2_to_3/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # signal_action: Indicate jump_arrow
        self.play(Indicate(self.objects["jump_arrow"], color=YELLOW, run_time=1))
        # visual_action: Write end_label and FadeIn distance_label (temporary)
        self.play(Write(self.objects["end_label"]), run_time=1.0)
        self.play(self.objects["distance_label"].animate.set_opacity(1), run_time=0.5)
        self.wait(max(0.1, 1.0))
        self.play(self.objects["distance_label"].animate.set_opacity(0), run_time=0.5)
        remaining_6 = max(0.1, 4.0 - 1.0 - 0.5 - 1.0 - 0.5 - 1.0 + 0.5)  # total 4.0, signal 1.0, write 1.0, fadein 0.5, wait 1.0, fadeout 0.5
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))