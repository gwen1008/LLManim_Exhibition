'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing fraction equivalence 1/2 = 2/4 using concrete pizza analogy.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two pizzas side-by-side
#    - Footer Region: [Bottom y=-3.0] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Position pizzas at x=-3.5 and x=3.5, leaving center for equals sign.
#    - Use VGroups for each pizza's components for easier management.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_two_identical_51d8f386ff/step_XX.mp3"
# 5. Animation Flow:
#    - Show title and two whole pizzas.
#    - Cut and color left pizza (1/2).
#    - Cut and color right pizza (2/4).
#    - Compare colored areas.
#    - Show equals sign and final equivalence.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.0 * DOWN
        pizza_left_pos = 3.5 * LEFT
        pizza_right_pos = 3.5 * RIGHT
        
        # Object registry
        self.objects = {}
        
        # Create title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create pizza outlines
        pizza_left = Circle(radius=1.5, color=GRAY_B, stroke_width=3, fill_opacity=0.2)
        pizza_left.move_to(pizza_left_pos)
        self.objects["pizza_left"] = pizza_left
        
        pizza_right = Circle(radius=1.5, color=GRAY_B, stroke_width=3, fill_opacity=0.2)
        pizza_right.move_to(pizza_right_pos)
        self.objects["pizza_right"] = pizza_right
        
        # Create cutting line for half (vertical line through center)
        cut_line_half = Line(
            start=pizza_left_pos + 1.5 * UP,
            end=pizza_left_pos + 1.5 * DOWN,
            color=WHITE,
            stroke_width=2
        )
        self.objects["cut_line_half"] = cut_line_half
        
        # Create sector for half (right half, starting from left)
        sector_half = Sector(
            radius=1.5,
            angle=PI,
            start_angle=0,
            color="#FF6B6B",
            fill_opacity=0.7,
            stroke_width=0
        )
        sector_half.move_to(pizza_left_pos)
        self.objects["sector_half"] = sector_half
        
        # Create label for half
        label_half = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_half.next_to(pizza_left, DOWN, buff=0.5)
        self.objects["label_half"] = label_half
        
        # Create cutting lines for quarters (vertical and horizontal cross)
        line_v = Line(
            start=pizza_right_pos + 1.5 * UP,
            end=pizza_right_pos + 1.5 * DOWN,
            color=WHITE,
            stroke_width=2
        )
        line_h = Line(
            start=pizza_right_pos + 1.5 * LEFT,
            end=pizza_right_pos + 1.5 * RIGHT,
            color=WHITE,
            stroke_width=2
        )
        cut_lines_quarters = VGroup(line_v, line_h)
        self.objects["cut_lines_quarters"] = cut_lines_quarters
        
        # Create sectors for quarters (top-right and bottom-right quadrants)
        sector_quarter_1 = Sector(
            radius=1.5,
            angle=PI/2,
            start_angle=0,
            color="#4ECDC4",
            fill_opacity=0.7,
            stroke_width=0
        )
        sector_quarter_1.move_to(pizza_right_pos)
        self.objects["sector_quarter_1"] = sector_quarter_1
        
        sector_quarter_2 = Sector(
            radius=1.5,
            angle=PI/2,
            start_angle=PI,
            color="#4ECDC4",
            fill_opacity=0.7,
            stroke_width=0
        )
        sector_quarter_2.move_to(pizza_right_pos)
        self.objects["sector_quarter_2"] = sector_quarter_2
        
        # Create label for fourths
        label_fourths = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_fourths.next_to(pizza_right, DOWN, buff=0.5)
        self.objects["label_fourths"] = label_fourths
        
        # Create equals sign
        equals_sign = MathTex("=", color=YELLOW, font_size=72)
        equals_sign.move_to(content_center)
        self.objects["equals_sign"] = equals_sign
        
        # Create step explanation text
        step_explanation = Text(
            "We start with two identical whole pizzas.",
            color=GRAY_B,
            font_size=28
        )
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_two_identical_51d8f386ff/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.5)
        self.play(
            Create(self.objects["pizza_left"]),
            Create(self.objects["pizza_right"]),
            Write(self.objects["step_explanation"]),
            run_time=1.5
        )
        remaining_1 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_two_identical_51d8f386ff/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza_left"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_half"]), run_time=1.5)
        
        # Update explanation
        new_explanation_2 = Text(
            "Let's look at the first pizza. We cut it into two equal halves.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_2.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        
        remaining_2 = max(0.1, 4.296 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_two_identical_51d8f386ff/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["cut_line_half"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["sector_half"]), run_time=1.5)
        
        # Update explanation
        new_explanation_3 = Text(
            "We color one of these halves red. This represents the fraction one-half.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_3.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        
        remaining_3 = max(0.1, 4.656 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_two_identical_51d8f386ff/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["sector_half"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_half"]), run_time=1.0)
        
        # Update explanation
        new_explanation_4 = Text(
            "Now, we label this pizza with the fraction one-half.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_4.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        
        remaining_4 = max(0.1, 3.696 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_two_identical_51d8f386ff/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza_right"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_lines_quarters"]), run_time=1.5)
        
        # Update explanation
        new_explanation_5 = Text(
            "Now, let's look at the second pizza. We cut it into four equal quarters.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_5.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        
        remaining_5 = max(0.1, 4.992 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/Create_two_identical_51d8f386ff/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["cut_lines_quarters"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["sector_quarter_1"]), run_time=1.5)
        
        # Update explanation
        new_explanation_6 = Text(
            "We color two of these quarters teal. This represents the fraction two-fourths.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_6.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_6))
        self.objects["step_explanation"] = new_explanation_6
        
        remaining_6 = max(0.1, 5.184 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        # No audio for step 7 (narrative is empty)
        self.play(Create(self.objects["sector_quarter_2"]), run_time=1.0)
        remaining_7 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/Create_two_identical_51d8f386ff/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Create VGroup for the two quarter sectors for circumscribing
        quarters_group = VGroup(self.objects["sector_quarter_1"], self.objects["sector_quarter_2"])
        self.play(Circumscribe(quarters_group, color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_fourths"]), run_time=1.0)
        
        # Update explanation
        new_explanation_8 = Text(
            "We label this pizza with the fraction two-fourths.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_8.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_8))
        self.objects["step_explanation"] = new_explanation_8
        
        remaining_8 = max(0.1, 3.312 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = "media/audio/Create_two_identical_51d8f386ff/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["sector_half"], color=YELLOW, run_time=1))
        self.play(Indicate(quarters_group, color=YELLOW, run_time=1))
        
        # Update explanation
        new_explanation_9 = Text(
            "Now, let's compare the colored areas. The red half on the left takes up the same amount of pizza as the two teal quarters on the right.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_9.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_9))
        self.objects["step_explanation"] = new_explanation_9
        
        remaining_9 = max(0.1, 8.112 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # ========== Step 10 ==========
        audio_step10 = "media/audio/Create_two_identical_51d8f386ff/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # Create VGroup for the two fraction labels for circumscribing
        labels_group = VGroup(self.objects["label_half"], self.objects["label_fourths"])
        self.play(Circumscribe(labels_group, color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["equals_sign"]), run_time=1.0)
        
        # Update explanation
        new_explanation_10 = Text(
            "This visual equivalence shows that one-half is equal to two-fourths.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_10.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_10))
        self.objects["step_explanation"] = new_explanation_10
        
        remaining_10 = max(0.1, 4.776 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # ========== Step 11 ==========
        audio_step11 = "media/audio/Create_two_identical_51d8f386ff/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["equals_sign"], color=YELLOW, run_time=1))
        self.play(
            self.objects["title"].animate.scale(1.2).set_color(YELLOW),
            run_time=1.0
        )
        self.play(
            self.objects["title"].animate.scale(1/1.2).set_color(WHITE),
            run_time=0.5
        )
        
        # Update explanation
        new_explanation_11 = Text(
            "Therefore, we can write the mathematical statement: one-half equals two-fourths.",
            color=GRAY_B,
            font_size=28
        )
        new_explanation_11.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_11))
        self.objects["step_explanation"] = new_explanation_11
        
        remaining_11 = max(0.1, 5.88 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # Final hold
        self.wait(max(0.1, 2))