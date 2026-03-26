'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize a jump on a number line from -2 to +3, calculating the distance (5 units).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for number line, points, arrow, and temporary equation
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for number line elements. Position temporary equation above number line, then fade out. Keep step label below title.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/number_line_jump/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line.
#    - Step 2: Indicate and create start point (-2).
#    - Step 3: Indicate and create end point (+3).
#    - Step 4: Circumscribe start label, update step label, show and fade distance equation.
#    - Step 5: Indicate and grow arrow from start to end.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/On_a_number_line_ran_94e437fc1a/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Number Line Jump: From -2 to +3", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        # Note: GRAY_C is not a standard Manim color. Use GRAY_B or LIGHT_GREY.
        number_line = NumberLine(
            x_range=[-5.5, 5.5, 1],
            length=12,
            include_numbers=True,
            include_ticks=True,
            color=GRAY_B
        )
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # start_point (position depends on number_line.n2p, which requires number_line to exist)
        # We'll create it but position later in the sequence.
        start_point = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        self.objects["start_point"] = start_point

        # start_label
        start_label = MathTex("-2", color=BLUE, font_size=24)
        self.objects["start_label"] = start_label

        # end_point
        end_point = Dot(radius=0.08, color=GREEN, fill_opacity=1.0)
        self.objects["end_point"] = end_point

        # end_label
        end_label = MathTex("+3", color=GREEN, font_size=24)
        self.objects["end_label"] = end_label

        # jump_arrow (initialized as zero-length at start_point)
        # We'll create it with start and end at the same point initially.
        jump_arrow = Arrow(
            start=ORIGIN,
            end=ORIGIN,
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["jump_arrow"] = jump_arrow

        # step_label
        step_label = Text("Step 1: The Number Line", color=GRAY, font_size=24)
        step_label.next_to(title, DOWN, buff=0.5)
        self.objects["step_label"] = step_label

        # explanation_text
        explanation_text = Text(
            "We begin with a number line ranging from -5 to 5.",
            color=GRAY_B,
            font_size=20
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/number_line_jump/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # signal_action: null
        # visual_action: Create number_line
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/number_line_jump/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Position start_point and start_label relative to number_line
        start_point.move_to(self.objects["number_line"].n2p(-2))
        start_label.next_to(start_point, UP, buff=0.2)

        # signal_action: Indicate start_point
        self.play(Indicate(self.objects["start_point"], color=BLUE, run_time=1))
        # visual_action: Create start_point and start_label
        self.play(
            Create(self.objects["start_point"]),
            Write(self.objects["start_label"]),
            run_time=1.5
        )
        remaining_2 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/number_line_jump/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Position end_point and end_label
        end_point.move_to(self.objects["number_line"].n2p(3))
        end_label.next_to(end_point, UP, buff=0.2)

        # signal_action: Indicate end_point
        self.play(Indicate(self.objects["end_point"], color=GREEN, run_time=1))
        # visual_action: Create end_point and end_label
        self.play(
            Create(self.objects["end_point"]),
            Write(self.objects["end_label"]),
            run_time=1.5
        )
        remaining_3 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/number_line_jump/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # signal_action: Circumscribe start_label
        self.play(Circumscribe(self.objects["start_label"], color=YELLOW, run_time=1))

        # visual_action: Update step_label and show temporary equation
        # Create new step label
        new_step_label = Text("Step 4: Distance = 5 units", color=GRAY, font_size=24)
        new_step_label.next_to(self.objects["title"], DOWN, buff=0.5)

        # Create temporary equation
        dist_eq = MathTex("3 - (-2) = 5", color=YELLOW, font_size=32)
        dist_eq.move_to(content_center + UP)
        self.objects["dist_eq"] = dist_eq  # store for potential reference, though we'll fade it out

        # Animate step label update and show equation
        self.play(
            ReplacementTransform(self.objects["step_label"], new_step_label),
            Write(dist_eq),
            run_time=2.0
        )
        self.objects["step_label"] = new_step_label  # update registry

        # Wait a bit, then fade out the equation
        self.wait(max(0.1, 1.0))
        self.play(FadeOut(dist_eq), run_time=0.5)

        remaining_4 = max(0.1, 4.0 - (2.0 + 1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/number_line_jump/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Position jump_arrow correctly before growing
        jump_arrow.put_start_and_end_on(
            self.objects["start_point"].get_center(),
            self.objects["end_point"].get_center()
        )

        # signal_action: Indicate jump_arrow
        self.play(Indicate(self.objects["jump_arrow"], color=YELLOW, run_time=1))

        # visual_action: GrowArrow
        self.play(GrowArrow(self.objects["jump_arrow"]), run_time=2.0)

        remaining_5 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2.0))