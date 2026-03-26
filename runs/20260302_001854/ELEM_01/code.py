'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate fraction equivalence (1/2 = 2/4) using a side-by-side pizza analogy.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Visualizing Fraction Equivalence"
#    - Main Content: [Center y=0] for two pizzas placed left and right of origin.
#    - Footer Region: [Bottom y=-3.5] for dynamic step explanations.
# 3. Anti-Overlap Check:
#    - Strategy: Place pizzas at LEFT*3.5 and RIGHT*3.5 from origin, ensuring they don't touch. Labels go below each pizza. Equivalence label goes above center.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_two_identical_ef36b15d3f/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1-2: Create two whole pizza circles.
#    - Step 3-5: Cut and color left pizza (1/2), add label.
#    - Step 6-8: Cut and color right pizza (2/4), add label.
#    - Step 9-10: Highlight colored areas, update footer text.
#    - Step 11-12: Show equivalence equation, final explanation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Visualizing Fraction Equivalence", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # pizza_left_circle
        pizza_left_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza_left_circle.move_to(content_center + 3.5 * LEFT)
        self.objects["pizza_left_circle"] = pizza_left_circle

        # pizza_right_circle
        pizza_right_circle = Circle(radius=2, color=WHITE, stroke_width=3)
        pizza_right_circle.move_to(content_center + 3.5 * RIGHT)
        self.objects["pizza_right_circle"] = pizza_right_circle

        # cut_line_left
        cut_line_left = Line(start=2*UP, end=2*DOWN, color=WHITE, stroke_width=2)
        cut_line_left.move_to(pizza_left_circle.get_center())
        self.objects["cut_line_left"] = cut_line_left

        # cut_line_right_vert
        cut_line_right_vert = Line(start=2*UP, end=2*DOWN, color=WHITE, stroke_width=2)
        cut_line_right_vert.move_to(pizza_right_circle.get_center())
        self.objects["cut_line_right_vert"] = cut_line_right_vert

        # cut_line_right_horz
        cut_line_right_horz = Line(start=2*LEFT, end=2*RIGHT, color=WHITE, stroke_width=2)
        cut_line_right_horz.move_to(pizza_right_circle.get_center())
        self.objects["cut_line_right_horz"] = cut_line_right_horz

        # sector_left
        # CRITICAL: Sector first arg is radius, NOT outer_radius
        sector_left = Sector(radius=2, start_angle=-PI/2, angle=PI, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        sector_left.move_to(pizza_left_circle.get_center())
        self.objects["sector_left"] = sector_left

        # sector_right_1
        sector_right_1 = Sector(radius=2, start_angle=0, angle=PI/2, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        sector_right_1.move_to(pizza_right_circle.get_center())
        self.objects["sector_right_1"] = sector_right_1

        # sector_right_2
        sector_right_2 = Sector(radius=2, start_angle=-PI, angle=PI/2, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        sector_right_2.move_to(pizza_right_circle.get_center())
        self.objects["sector_right_2"] = sector_right_2

        # label_left
        label_left = MathTex(r"\frac{1}{2}", color="#1E90FF", font_size=48)
        label_left.next_to(pizza_left_circle, DOWN, buff=0.8)
        self.objects["label_left"] = label_left

        # label_right
        label_right = MathTex(r"\frac{2}{4}", color="#FF6B6B", font_size=48)
        label_right.next_to(pizza_right_circle, DOWN, buff=0.8)
        self.objects["label_right"] = label_right

        # equiv_label
        equiv_label = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=WHITE, font_size=56)
        equiv_label.move_to(content_center + 1.5 * UP)
        self.objects["equiv_label"] = equiv_label

        # explanation_text
        explanation_text = Text("We start with two identical whole pizzas.", color=GRAY, font_size=28)
        explanation_text.move_to(footer_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_two_identical_ef36b15d3f/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Create(self.objects["pizza_left_circle"]), run_time=1.5)
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # No audio path provided for step 2, skip audio
        # signal_action: null
        self.play(Create(self.objects["pizza_right_circle"]), run_time=1.5)
        remaining_2 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_two_identical_ef36b15d3f/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: Indicate pizza_left_circle
        self.play(Indicate(self.objects["pizza_left_circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_left"]), run_time=1.5)
        remaining_3 = max(0.1, 4.2 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_two_identical_ef36b15d3f/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(FadeIn(self.objects["sector_left"]), run_time=1.5)
        remaining_4 = max(0.1, 3.936 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_two_identical_ef36b15d3f/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: Indicate sector_left
        self.play(Indicate(self.objects["sector_left"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_left"]), run_time=1.0)
        remaining_5 = max(0.1, 2.112 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/Create_two_identical_ef36b15d3f/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: Indicate pizza_right_circle
        self.play(Indicate(self.objects["pizza_right_circle"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["cut_line_right_vert"]),
            Create(self.objects["cut_line_right_horz"]),
            run_time=2.0
        )
        remaining_6 = max(0.1, 5.016 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/Create_two_identical_ef36b15d3f/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(
            FadeIn(self.objects["sector_right_1"]),
            FadeIn(self.objects["sector_right_2"]),
            run_time=1.5
        )
        remaining_7 = max(0.1, 4.392 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/Create_two_identical_ef36b15d3f/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # signal_action: Indicate sector_right_1
        self.play(Indicate(self.objects["sector_right_1"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_right"]), run_time=1.0)
        remaining_8 = max(0.1, 2.52 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        audio_step9 = "media/audio/Create_two_identical_ef36b15d3f/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # signal_action: Circumscribe sector_left
        self.play(Circumscribe(self.objects["sector_left"], color=YELLOW, run_time=1))
        # UpdateText for explanation_text
        new_explanation_9 = Text("The blue half on the left...", color=GRAY, font_size=28)
        new_explanation_9.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_9))
        self.objects["explanation_text"] = new_explanation_9
        remaining_9 = max(0.1, 4.464 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # ========== Step 10 ==========
        audio_step10 = "media/audio/Create_two_identical_ef36b15d3f/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # signal_action: Circumscribe sector_right_1 and sector_right_2
        target_group = VGroup(self.objects["sector_right_1"], self.objects["sector_right_2"])
        self.play(Circumscribe(target_group, color=YELLOW, run_time=1))
        # UpdateText for explanation_text
        new_explanation_10 = Text("...covers the same area as the two red quarters.", color=GRAY, font_size=28)
        new_explanation_10.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_10))
        self.objects["explanation_text"] = new_explanation_10
        remaining_10 = max(0.1, 4.776 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # ========== Step 11 ==========
        audio_step11 = "media/audio/Create_two_identical_ef36b15d3f/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Write(self.objects["equiv_label"]), run_time=1.5)
        remaining_11 = max(0.1, 3.96 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_11))

        # ========== Step 12 ==========
        audio_step12 = "media/audio/Create_two_identical_ef36b15d3f/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        # signal_action: Indicate equiv_label
        self.play(Indicate(self.objects["equiv_label"], color=YELLOW, run_time=1))
        # UpdateText for explanation_text
        new_explanation_12 = Text("The colored areas are equal, so 1/2 = 2/4.", color=GRAY, font_size=28)
        new_explanation_12.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_12))
        self.objects["explanation_text"] = new_explanation_12
        remaining_12 = max(0.1, 5.016 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_12))

        # Final hold
        self.wait(max(0.1, 2))