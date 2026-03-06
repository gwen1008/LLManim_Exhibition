'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing fraction equivalence 1/2 = 2/4 using two identical circles (pizzas).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two pizzas side-by-side
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Place left pizza at x=-3.5, right pizza at x=3.5. Keep labels below each pizza.
#    - Use VGroups for each pizza to manage components together.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/fraction_equivalence_1_2_2_4/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create left pizza (2/4) with label.
#    - Step 2: Create right pizza (1/2) with label.
#    - Step 3: Subdivide right pizza: fade in lines, fade out half, fade in quarters, transform label.
#    - Step 4: Highlight all shaded sectors in green.
#    - Step 5: Show equivalence equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        pizza_left_anchor = np.array([-3.5, 0, 0])
        pizza_right_anchor = np.array([3.5, 0, 0])
        explanation_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Create left pizza (2/4)
        pizza_left_outline = Circle(radius=2.0, color=WHITE, stroke_width=3)
        pizza_left_outline.move_to(pizza_left_anchor)
        self.objects["pizza_left_outline"] = pizza_left_outline

        # Note: Sector first arg is radius, not outer_radius
        pizza_left_sector1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color="#FF9999", fill_opacity=0.8, stroke_width=0)
        pizza_left_sector1.move_to(pizza_left_anchor)
        self.objects["pizza_left_sector1"] = pizza_left_sector1

        pizza_left_sector2 = Sector(radius=2.0, angle=PI/2, start_angle=PI, color="#FF9999", fill_opacity=0.8, stroke_width=0)
        pizza_left_sector2.move_to(pizza_left_anchor)
        self.objects["pizza_left_sector2"] = pizza_left_sector2

        pizza_left_label = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        pizza_left_label.next_to(pizza_left_outline, DOWN, buff=0.8)
        self.objects["pizza_left_label"] = pizza_left_label

        # Create right pizza (1/2 initially)
        pizza_right_outline = Circle(radius=2.0, color=WHITE, stroke_width=3)
        pizza_right_outline.move_to(pizza_right_anchor)
        self.objects["pizza_right_outline"] = pizza_right_outline

        pizza_right_halves_shaded = Sector(radius=2.0, angle=PI, start_angle=0, color="#9999FF", fill_opacity=0.8, stroke_width=0)
        pizza_right_halves_shaded.move_to(pizza_right_anchor)
        self.objects["pizza_right_halves_shaded"] = pizza_right_halves_shaded

        pizza_right_label_initial = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        pizza_right_label_initial.next_to(pizza_right_outline, DOWN, buff=0.8)
        self.objects["pizza_right_label_initial"] = pizza_right_label_initial

        pizza_right_label_final = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        pizza_right_label_final.next_to(pizza_right_outline, DOWN, buff=0.8)
        pizza_right_label_final.set_opacity(0)
        self.objects["pizza_right_label_final"] = pizza_right_label_final

        # Dividing lines for right pizza (initially invisible)
        divider_line_vertical = Line(UP*2, DOWN*2, color=WHITE, stroke_width=3)
        divider_line_vertical.move_to(pizza_right_anchor)
        divider_line_vertical.set_opacity(0)
        self.objects["divider_line_vertical"] = divider_line_vertical

        divider_line_horizontal = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=3)
        divider_line_horizontal.move_to(pizza_right_anchor)
        divider_line_horizontal.set_opacity(0)
        self.objects["divider_line_horizontal"] = divider_line_horizontal

        # Create the two quarter sectors for right pizza (for subdivision animation)
        # These will be created but initially invisible
        pizza_right_sector1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color="#9999FF", fill_opacity=0.0, stroke_width=0)
        pizza_right_sector1.move_to(pizza_right_anchor)
        self.objects["pizza_right_sector1"] = pizza_right_sector1

        pizza_right_sector2 = Sector(radius=2.0, angle=PI/2, start_angle=PI, color="#9999FF", fill_opacity=0.0, stroke_width=0)
        pizza_right_sector2.move_to(pizza_right_anchor)
        self.objects["pizza_right_sector2"] = pizza_right_sector2

        # Explanation text (dynamic, will be updated per step)
        explanation_text = Text("", color=YELLOW, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # Equivalence text (initially invisible)
        equivalence_text = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=GREEN, font_size=48)
        equivalence_text.move_to(ORIGIN + DOWN*0.5)
        equivalence_text.set_opacity(0)
        self.objects["equivalence_text"] = equivalence_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/fraction_equivalence_1_2_2_4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Signal action: Indicate left label
        self.play(Indicate(self.objects["pizza_left_label"], color=YELLOW, run_time=1))

        # Visual action: Create left pizza components
        anim_time_step1 = 3.0
        self.play(
            Create(self.objects["pizza_left_outline"]),
            Create(self.objects["pizza_left_sector1"]),
            Create(self.objects["pizza_left_sector2"]),
            Write(self.objects["pizza_left_label"]),
            run_time=anim_time_step1
        )
        remaining_1 = max(0.1, 5.0 - anim_time_step1 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/fraction_equivalence_1_2_2_4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate right initial label
        self.play(Indicate(self.objects["pizza_right_label_initial"], color=YELLOW, run_time=1))

        # Visual action: Create right pizza components
        anim_time_step2 = 2.5
        self.play(
            Create(self.objects["pizza_right_outline"]),
            Create(self.objects["pizza_right_halves_shaded"]),
            Write(self.objects["pizza_right_label_initial"]),
            run_time=anim_time_step2
        )
        remaining_2 = max(0.1, 4.0 - anim_time_step2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/fraction_equivalence_1_2_2_4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate the shaded half on right pizza
        self.play(Indicate(self.objects["pizza_right_halves_shaded"], color=RED, run_time=1))

        # Visual action: Subdivision animation
        # 1. Fade in dividing lines
        # 2. Fade out half-sector while fading in quarter-sectors
        # 3. Transform label
        anim_time_step3 = 4.0
        self.play(
            self.objects["divider_line_vertical"].animate.set_opacity(1),
            self.objects["divider_line_horizontal"].animate.set_opacity(1),
            run_time=1.0
        )
        self.play(
            self.objects["pizza_right_halves_shaded"].animate.set_opacity(0),
            self.objects["pizza_right_sector1"].animate.set_fill(opacity=0.8),
            self.objects["pizza_right_sector2"].animate.set_fill(opacity=0.8),
            ReplacementTransform(self.objects["pizza_right_label_initial"], self.objects["pizza_right_label_final"]),
            run_time=anim_time_step3 - 1.0
        )
        remaining_3 = max(0.1, 6.0 - anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/fraction_equivalence_1_2_2_4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # No signal action for step 4 (signal_action is null)

        # Visual action: Highlight all shaded sectors in green, then revert
        anim_time_step4 = 2.0
        shaded_sectors = [
            self.objects["pizza_left_sector1"],
            self.objects["pizza_left_sector2"],
            self.objects["pizza_right_sector1"],
            self.objects["pizza_right_sector2"]
        ]
        original_colors = [sector.fill_color for sector in shaded_sectors]

        # Change to bright green
        for sector in shaded_sectors:
            sector.save_state()
        self.play(
            *[sector.animate.set_fill(GREEN, opacity=0.8) for sector in shaded_sectors],
            run_time=0.5
        )
        self.wait(max(0.1, 0.5))
        # Revert to original colors
        self.play(
            *[sector.animate.restore() for sector in shaded_sectors],
            run_time=0.5
        )
        remaining_4 = max(0.1, 3.0 - anim_time_step4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/fraction_equivalence_1_2_2_4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Circumscribe equivalence text
        # First fade in the text, then circumscribe
        anim_time_step5 = 2.0
        self.play(
            self.objects["equivalence_text"].animate.set_opacity(1),
            run_time=1.0
        )
        self.play(
            Circumscribe(self.objects["equivalence_text"], color=YELLOW, run_time=1)
        )
        remaining_5 = max(0.1, 4.0 - anim_time_step5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))