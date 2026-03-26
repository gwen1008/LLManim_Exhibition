'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the equivalence 1/2 = 2/4 by progressively constructing a whole, then a half, then subdividing the half into two quarters, showing the area remains constant.
# 2. Layout Strategy: Use High-Low Split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for construction animation, then left/right comparison at y=0.
#    - Footer Region: [Bottom y=-3.5] for explanatory text and fraction labels.
# 3. Anti-Overlap Check:
#    - The central animation uses ORIGIN. The final comparison moves left/right by 3 units.
#    - Footer text is centered at y=-3.5, leaving the main area clear.
#    - Use VGroups for final comparison circles for easy alignment.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/fraction_equivalence_1_2_equals_2_4/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show whole circle.
#    - Step 2: Indicate whole, fill top half, update footer to 1/2.
#    - Step 3: Circumscribe half, transform it into two quarters, update footer to 2/4.
#    - Step 4: Indicate quarters, fade out central circle, fade in side-by-side comparison (left half, right two quarters), update footer to equivalence statement.
#    - Step 5: Indicate blue areas in both circles, hold.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_two_identical_752693b444/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        animation_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN
        left_comparison_anchor = 3 * LEFT
        right_comparison_anchor = 3 * RIGHT

        # Object registry
        self.objects = {}

        # Helper to parse geometry_def string (simplified parsing for this specific case)
        def create_sector_from_def(def_str, default_radius=2.0):
            # Expects format like "outer_radius=2.0, inner_radius=0.0, angle=PI, start_angle=0"
            params = {}
            for part in def_str.split(','):
                part = part.strip()
                if '=' in part:
                    key, value = part.split('=')
                    key = key.strip()
                    value = value.strip()
                    try:
                        # Evaluate PI, TAU, etc.
                        params[key] = eval(value, {"__builtins__": {}}, {"PI": PI, "TAU": TAU})
                    except:
                        # Fallback to float
                        params[key] = float(value)
            # Sector signature: radius, angle, start_angle=0, **kwargs
            # In Manim v0.19, first arg is 'radius', not 'outer_radius'.
            # 'inner_radius' is not a valid kwarg for Sector (that's for AnnularSector).
            # According to JSON, inner_radius=0.0, so we just use radius.
            radius = params.get('outer_radius', default_radius)
            angle = params.get('angle', PI)
            start_angle = params.get('start_angle', 0)
            return Sector(radius=radius, angle=angle, start_angle=start_angle)

        # Create objects from layout_plan.objects
        # title
        title = Text("Fraction Equivalence: 1/2 = 2/4", font_size=48, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # whole_circle
        whole_circle = Circle(radius=2.0, color=WHITE, stroke_width=4, fill_opacity=0.0)
        whole_circle.move_to(animation_anchor)
        self.objects["whole_circle"] = whole_circle

        # half_sector
        half_sector = create_sector_from_def("outer_radius=2.0, inner_radius=0.0, angle=PI, start_angle=0")
        half_sector.move_to(animation_anchor)
        half_sector.set_color(BLUE).set_fill(opacity=0.8).set_stroke(width=0)
        self.objects["half_sector"] = half_sector

        # quarter_sector_1
        quarter_sector_1 = create_sector_from_def("outer_radius=2.0, inner_radius=0.0, angle=PI/2, start_angle=0")
        quarter_sector_1.move_to(animation_anchor)
        quarter_sector_1.set_color(BLUE).set_fill(opacity=0.8).set_stroke(width=0)
        self.objects["quarter_sector_1"] = quarter_sector_1

        # quarter_sector_2
        quarter_sector_2 = create_sector_from_def("outer_radius=2.0, inner_radius=0.0, angle=PI/2, start_angle=PI/2")
        quarter_sector_2.move_to(animation_anchor)
        quarter_sector_2.set_color(BLUE).set_fill(opacity=0.8).set_stroke(width=0)
        self.objects["quarter_sector_2"] = quarter_sector_2

        # left_circle_whole
        left_circle_whole = Circle(radius=2.0, color=WHITE, stroke_width=4, fill_opacity=0.0)
        left_circle_whole.move_to(left_comparison_anchor)
        self.objects["left_circle_whole"] = left_circle_whole

        # left_half_sector
        left_half_sector = create_sector_from_def("outer_radius=2.0, inner_radius=0.0, angle=PI, start_angle=0")
        left_half_sector.move_to(left_comparison_anchor)
        left_half_sector.set_color(BLUE).set_fill(opacity=0.8).set_stroke(width=0)
        self.objects["left_half_sector"] = left_half_sector

        # right_circle_whole
        right_circle_whole = Circle(radius=2.0, color=WHITE, stroke_width=4, fill_opacity=0.0)
        right_circle_whole.move_to(right_comparison_anchor)
        self.objects["right_circle_whole"] = right_circle_whole

        # right_quarter_sector_1
        right_quarter_sector_1 = create_sector_from_def("outer_radius=2.0, inner_radius=0.0, angle=PI/2, start_angle=0")
        right_quarter_sector_1.move_to(right_comparison_anchor)
        right_quarter_sector_1.set_color(BLUE).set_fill(opacity=0.8).set_stroke(width=0)
        self.objects["right_quarter_sector_1"] = right_quarter_sector_1

        # right_quarter_sector_2
        right_quarter_sector_2 = create_sector_from_def("outer_radius=2.0, inner_radius=0.0, angle=PI/2, start_angle=PI/2")
        right_quarter_sector_2.move_to(right_comparison_anchor)
        right_quarter_sector_2.set_color(BLUE).set_fill(opacity=0.8).set_stroke(width=0)
        self.objects["right_quarter_sector_2"] = right_quarter_sector_2

        # footer_label_initial
        footer_label_initial = Text("Start with one whole.", font_size=36, color=GRAY_B)
        footer_label_initial.move_to(footer_anchor)
        self.objects["footer_label_initial"] = footer_label_initial

        # footer_label_half
        footer_label_half = MathTex(r"\frac{1}{2}", color=BLUE, font_size=48)
        footer_label_half.move_to(footer_anchor)
        self.objects["footer_label_half"] = footer_label_half

        # footer_label_quarter
        footer_label_quarter = MathTex(r"\frac{2}{4}", color=BLUE, font_size=48)
        footer_label_quarter.move_to(footer_anchor)
        self.objects["footer_label_quarter"] = footer_label_quarter

        # footer_label_equals
        footer_label_equals = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=YELLOW, font_size=48)
        footer_label_equals.move_to(footer_anchor)
        self.objects["footer_label_equals"] = footer_label_equals

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Visual action: Create whole_circle
        self.play(Create(self.objects["whole_circle"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Indicate whole_circle
        self.play(Indicate(self.objects["whole_circle"], color=YELLOW, run_time=1))

        # Visual actions: DrawBorderThenFill half_sector and ReplacementTransform footer
        # DrawBorderThenFill is not a standard Manim animation. We'll simulate with Create (for stroke) then set_fill.
        half_sector = self.objects["half_sector"]
        # Start with zero fill opacity
        half_sector.set_fill(opacity=0.0)
        self.play(Create(half_sector), run_time=1.0)
        self.play(half_sector.animate.set_fill(opacity=0.8), run_time=1.0)
        # ReplacementTransform footer_label_initial to footer_label_half
        self.play(ReplacementTransform(self.objects["footer_label_initial"], self.objects["footer_label_half"]), run_time=1.0)
        total_anim_time_step2 = 1 + 1.0 + 1.0 + 1.0  # Indicate + Create + set_fill + ReplacementTransform
        remaining_2 = max(0.1, 4.0 - total_anim_time_step2 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Circumscribe half_sector
        self.play(Circumscribe(self.objects["half_sector"], color=YELLOW, run_time=1))

        # Visual actions: Transform half_sector into quarter_sector_1, Create quarter_sector_2, ReplacementTransform footer
        # We need to transform the existing half_sector into quarter_sector_1.
        # Since both are Sector objects with different angles/start_angles, Transform should work.
        # quarter_sector_2 is created simultaneously.
        quarter_sector_1 = self.objects["quarter_sector_1"]
        quarter_sector_2 = self.objects["quarter_sector_2"]
        # Ensure quarter_sector_2 starts invisible
        quarter_sector_2.set_fill(opacity=0.0)
        self.play(
            Transform(self.objects["half_sector"], quarter_sector_1),
            Create(quarter_sector_2),
            run_time=2.0
        )
        # Now set fill opacity for quarter_sector_2
        self.play(quarter_sector_2.animate.set_fill(opacity=0.8), run_time=1.0)
        # ReplacementTransform footer_label_half to footer_label_quarter
        self.play(ReplacementTransform(self.objects["footer_label_half"], self.objects["footer_label_quarter"]), run_time=1.0)
        total_anim_time_step3 = 1 + 2.0 + 1.0 + 1.0
        remaining_3 = max(0.1, 5.0 - total_anim_time_step3 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate quarter_sector_1 and quarter_sector_2
        self.play(
            Indicate(self.objects["quarter_sector_1"], color=YELLOW, run_time=1),
            Indicate(self.objects["quarter_sector_2"], color=YELLOW, run_time=1)
        )

        # Visual actions: FadeOut whole_circle, FadeIn left_circle_whole, left_half_sector, right_circle_whole, right_quarter_sector_1, right_quarter_sector_2, ReplacementTransform footer
        self.play(FadeOut(self.objects["whole_circle"]), run_time=0.5)
        self.play(
            FadeIn(self.objects["left_circle_whole"]),
            FadeIn(self.objects["left_half_sector"]),
            FadeIn(self.objects["right_circle_whole"]),
            FadeIn(self.objects["right_quarter_sector_1"]),
            FadeIn(self.objects["right_quarter_sector_2"]),
            run_time=2.0
        )
        # ReplacementTransform footer_label_quarter to footer_label_equals
        self.play(ReplacementTransform(self.objects["footer_label_quarter"], self.objects["footer_label_equals"]), run_time=1.0)
        total_anim_time_step4 = 1 + 0.5 + 2.0 + 1.0
        remaining_4 = max(0.1, 6.0 - total_anim_time_step4 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate left_half_sector, right_quarter_sector_1, right_quarter_sector_2 simultaneously
        self.play(
            Indicate(self.objects["left_half_sector"], color=YELLOW, run_time=1),
            Indicate(self.objects["right_quarter_sector_1"], color=YELLOW, run_time=1),
            Indicate(self.objects["right_quarter_sector_2"], color=YELLOW, run_time=1)
        )

        # Visual action: Wait (hold final frame)
        remaining_5 = max(0.1, 4.0 - 1.0 + 0.5)  # signal action took 1.0
        self.wait(max(0.1, remaining_5))