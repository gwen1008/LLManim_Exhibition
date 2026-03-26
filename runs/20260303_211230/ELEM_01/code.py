'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually prove the equivalence of fractions 1/2 and 2/4 using a pizza analogy and a progressive transformation.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for pizzas and transformation
#    - Footer Region: [Bottom y=-3.5] for final equation
# 3. Anti-Overlap Check:
#    - Initial stage: Two pizzas side-by-side (LEFT*3 and RIGHT*3) to avoid overlap.
#    - Transformation stage: Move left pizza to center, fade out right pizza.
#    - Use VGroups to manage composite objects (pizza with lines and shade).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/equivalent_fractions/step_XX.mp3"
# 5. Animation Flow:
#    - Draw two pizza circles.
#    - Divide and shade left pizza (half).
#    - Divide and shade right pizza (quarters).
#    - Move left pizza to center, fade out right.
#    - Transform the blue half into two orange quarters.
#    - Show final equivalence equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_two_identical_9513704b60/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        pizza_a_anchor = 3 * LEFT
        pizza_b_anchor = 3 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Equivalent Fractions: 1/2 = 2/4", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # pizza_a_circle
        pizza_a_circle = Circle(radius=2.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        pizza_a_circle.move_to(pizza_a_anchor)
        self.objects["pizza_a_circle"] = pizza_a_circle

        # pizza_b_circle
        pizza_b_circle = Circle(radius=2.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        pizza_b_circle.move_to(pizza_b_anchor)
        self.objects["pizza_b_circle"] = pizza_b_circle

        # half_line
        half_line = Line(UP * 2, DOWN * 2, color=WHITE, stroke_width=3)
        half_line.move_to(pizza_a_circle.get_center())
        self.objects["half_line"] = half_line

        # half_shade
        half_shade = Sector(radius=2.0, angle=PI, color="#1E90FF", fill_opacity=0.7, stroke_width=0)
        half_shade.move_to(pizza_a_circle.get_center())
        self.objects["half_shade"] = half_shade

        # quarter_lines_v
        quarter_lines_v = Line(UP * 2, DOWN * 2, color=WHITE, stroke_width=3)
        quarter_lines_v.move_to(pizza_b_circle.get_center())
        self.objects["quarter_lines_v"] = quarter_lines_v

        # quarter_lines_h
        quarter_lines_h = Line(LEFT * 2, RIGHT * 2, color=WHITE, stroke_width=3)
        quarter_lines_h.move_to(pizza_b_circle.get_center())
        self.objects["quarter_lines_h"] = quarter_lines_h

        # quarter_shade_1
        quarter_shade_1 = Sector(radius=2.0, angle=PI/2, color="#FF8C00", fill_opacity=0.7, stroke_width=0)
        quarter_shade_1.move_to(pizza_b_circle.get_center())
        self.objects["quarter_shade_1"] = quarter_shade_1

        # quarter_shade_2
        quarter_shade_2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color="#FF8C00", fill_opacity=0.7, stroke_width=0)
        quarter_shade_2.move_to(pizza_b_circle.get_center())
        self.objects["quarter_shade_2"] = quarter_shade_2

        # label_half
        label_half = MathTex(r"\frac{1}{2}", font_size=36, color="#1E90FF")
        label_half.next_to(pizza_a_circle, DOWN, buff=0.5)
        self.objects["label_half"] = label_half

        # label_quarters
        label_quarters = MathTex(r"\frac{2}{4}", font_size=36, color="#FF8C00")
        label_quarters.next_to(pizza_b_circle, DOWN, buff=0.5)
        self.objects["label_quarters"] = label_quarters

        # final_equation
        final_equation = MathTex(r"\frac{1}{2} = \frac{2}{4}", font_size=48, color=YELLOW)
        final_equation.move_to(footer_anchor)
        self.objects["final_equation"] = final_equation

        # transformed_shade (VGroup of two quarters, positioned at content_center, not added initially)
        transformed_shade_1 = Sector(radius=2.0, angle=PI/2, color="#FF8C00", fill_opacity=0.7, stroke_width=0)
        transformed_shade_2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color="#FF8C00", fill_opacity=0.7, stroke_width=0)
        transformed_shade = VGroup(transformed_shade_1, transformed_shade_2)
        transformed_shade.move_to(content_center)
        self.objects["transformed_shade"] = transformed_shade

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/equivalent_fractions/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(DrawBorderThenFill(self.objects["pizza_a_circle"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/equivalent_fractions/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["half_line"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/equivalent_fractions/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate half_shade
        self.play(Indicate(self.objects["half_shade"], color=YELLOW, run_time=1))
        # Visual action: FadeIn half_shade
        self.play(FadeIn(self.objects["half_shade"]), run_time=1.0)
        remaining_3 = max(0.1, 2.0 - 1.0 - 1.0 + 0.5)  # total 2.0, signal 1.0, visual 1.0
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/equivalent_fractions/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(DrawBorderThenFill(self.objects["pizza_b_circle"]), run_time=1.5)
        remaining_4 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/equivalent_fractions/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Create(self.objects["quarter_lines_v"]), run_time=1.0)
        remaining_5 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/equivalent_fractions/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Signal action: Indicate quarter_shade_1
        self.play(Indicate(self.objects["quarter_shade_1"], color=YELLOW, run_time=1))
        # Visual action: FadeIn quarter_shade_1
        self.play(FadeIn(self.objects["quarter_shade_1"]), run_time=0.5)
        remaining_6 = max(0.1, 1.5 - 1.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/equivalent_fractions/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # Signal action: Indicate quarter_shade_2
        self.play(Indicate(self.objects["quarter_shade_2"], color=YELLOW, run_time=1))
        # Visual action: FadeIn quarter_shade_2
        self.play(FadeIn(self.objects["quarter_shade_2"]), run_time=1.0)
        remaining_7 = max(0.1, 2.0 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/equivalent_fractions/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        # Signal action: Circumscribe final_equation
        self.play(Circumscribe(self.objects["final_equation"], color=GREEN, run_time=1))
        # Visual action: Write final_equation
        self.play(Write(self.objects["final_equation"]), run_time=2.0)
        remaining_8 = max(0.1, 3.0 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))