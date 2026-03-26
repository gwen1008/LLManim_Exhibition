'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually prove the equivalence of fractions 1/2 and 2/4 by transforming a colored half into two quarters and comparing to a pre-divided pizza.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0.5] for two pizzas side-by-side (left at x=-3.5, right at x=3.5)
#    - Footer Region: [Bottom y=-3.5] for final equivalence equation
# 3. Anti-Overlap Check:
#    - Strategy: Keep pizzas separated by 7 units horizontally. Use VGroups for composite objects (right_quarter_slices, divider_lines_quarters).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/fraction_equivalence_1_2_equals_2_4/step_XX.mp3"
# 5. Animation Flow:
#    - Show two whole pizzas.
#    - Divide left pizza into halves, color one half.
#    - Subdivide the colored half with a diagonal line.
#    - Transform label 1/2 to 2/4.
#    - Show right pizza divided into quarters, color two quarters.
#    - Compare colored areas.
#    - Morph labels into central equivalence equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # pizza_left_outline
        pizza_left_outline = Circle(radius=2.0, color=WHITE, stroke_width=3, fill_opacity=0)
        pizza_left_outline.move_to(content_center + LEFT*3.5 + UP*0.5)
        self.objects["pizza_left_outline"] = pizza_left_outline
        
        # pizza_right_outline
        pizza_right_outline = Circle(radius=2.0, color=WHITE, stroke_width=3, fill_opacity=0)
        pizza_right_outline.move_to(content_center + RIGHT*3.5 + UP*0.5)
        self.objects["pizza_right_outline"] = pizza_right_outline
        
        # label_left_initial
        label_left_initial = MathTex(r"\frac{1}{2}", color=BLUE)
        label_left_initial.next_to(pizza_left_outline, DOWN, buff=0.8)
        self.objects["label_left_initial"] = label_left_initial
        
        # label_right_initial
        label_right_initial = MathTex(r"\frac{2}{4}", color=BLUE)
        label_right_initial.next_to(pizza_right_outline, DOWN, buff=0.8)
        self.objects["label_right_initial"] = label_right_initial
        
        # left_half_slice
        left_half_slice = Sector(
            radius=2.0,
            angle=180 * DEGREES,
            start_angle=90 * DEGREES,
            color=BLUE,
            fill_opacity=0.7,
            stroke_width=0
        )
        left_half_slice.move_to(pizza_left_outline.get_center())
        self.objects["left_half_slice"] = left_half_slice
        
        # divider_line_half
        divider_line_half = Line(start=[0,0,0], end=[2,0,0], color=WHITE, stroke_width=3)
        divider_line_half.move_to(pizza_left_outline.get_center())
        self.objects["divider_line_half"] = divider_line_half
        
        # right_quarter_slices (VGroup of two Sectors)
        # We'll create the two sectors: one from 45 to 135 deg, another from 135 to 225 deg.
        sector1 = Sector(
            radius=2.0,
            angle=90 * DEGREES,
            start_angle=45 * DEGREES,
            color=BLUE,
            fill_opacity=0.7,
            stroke_width=0
        )
        sector2 = Sector(
            radius=2.0,
            angle=90 * DEGREES,
            start_angle=135 * DEGREES,
            color=BLUE,
            fill_opacity=0.7,
            stroke_width=0
        )
        right_quarter_slices = VGroup(sector1, sector2)
        right_quarter_slices.move_to(pizza_right_outline.get_center())
        self.objects["right_quarter_slices"] = right_quarter_slices
        
        # divider_lines_quarters (VGroup of four Lines)
        lines = []
        for angle in [45, 135, 225, 315]:
            end_x = 2 * np.cos(angle * DEGREES)
            end_y = 2 * np.sin(angle * DEGREES)
            line = Line(start=[0,0,0], end=[end_x, end_y, 0], color=WHITE, stroke_width=3)
            lines.append(line)
        divider_lines_quarters = VGroup(*lines)
        divider_lines_quarters.move_to(pizza_right_outline.get_center())
        self.objects["divider_lines_quarters"] = divider_lines_quarters
        
        # subdivision_line
        sub_x = 2 * 0.7071  # cos45
        sub_y = 2 * 0.7071  # sin45
        subdivision_line = Line(start=[0,0,0], end=[sub_x, sub_y, 0], color=YELLOW, stroke_width=4)
        subdivision_line.move_to(pizza_left_outline.get_center())
        self.objects["subdivision_line"] = subdivision_line
        
        # equation_footer
        equation_footer = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=GREEN, font_size=56)
        equation_footer.move_to(footer_anchor)
        self.objects["equation_footer"] = equation_footer
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["pizza_left_outline"]), run_time=1.0)
        remaining_1 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_02.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["pizza_right_outline"]), run_time=1.0)
        remaining_2 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_03.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        self.play(Create(self.objects["divider_line_half"]), run_time=1.5)
        remaining_3 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_04.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # signal_action: Indicate left_half_slice
        self.play(Indicate(self.objects["left_half_slice"], color=YELLOW, run_time=1))
        # visual_action: DrawBorderThenFill for left_half_slice
        self.play(DrawBorderThenFill(self.objects["left_half_slice"]), run_time=2.0)
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_05.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_left_initial"]), run_time=1.5)
        remaining_5 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_06.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: Circumscribe left_half_slice
        self.play(Circumscribe(self.objects["left_half_slice"], color=YELLOW, run_time=1))
        # visual_action: Create subdivision_line
        self.play(Create(self.objects["subdivision_line"]), run_time=3.0)
        remaining_6 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_07.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # signal_action: Indicate subdivision_line
        self.play(Indicate(self.objects["subdivision_line"], color=YELLOW, run_time=1))
        # visual_action: ReplacementTransform label_left_initial into a new 2/4 label
        # Create target label for transformation
        label_left_transformed = MathTex(r"\frac{2}{4}", color=BLUE)
        label_left_transformed.move_to(self.objects["label_left_initial"].get_center())
        self.play(ReplacementTransform(self.objects["label_left_initial"], label_left_transformed), run_time=3.0)
        self.objects["label_left_initial"] = label_left_transformed  # update registry
        remaining_7 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_08.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        self.play(Create(self.objects["divider_lines_quarters"]), run_time=2.0)
        remaining_8 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_09.mp3")  # [auto-injected]
        # Step 9
        audio_step9 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        self.play(DrawBorderThenFill(self.objects["right_quarter_slices"]), run_time=2.0)
        remaining_9 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_10.mp3")  # [auto-injected]
        # Step 10
        audio_step10 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_right_initial"]), run_time=1.5)
        remaining_10 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_11.mp3")  # [auto-injected]
        # Step 11
        audio_step11 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        # signal_action: Indicate left_half_slice
        self.play(Indicate(self.objects["left_half_slice"], color=YELLOW, run_time=1))
        # visual_action: Indicate right_quarter_slices
        self.play(Indicate(self.objects["right_quarter_slices"], color=YELLOW, run_time=3.0))
        remaining_11 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # Step 12
        audio_step12 = "media/audio/fraction_equivalence_1_2_equals_2_4/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        # visual_action: TransformMatchingTex to morph the two separate fraction labels into the central equivalence equation.
        # We'll create a source VGroup containing both labels, and transform into equation_footer.
        source_labels = VGroup(self.objects["label_left_initial"], self.objects["label_right_initial"])
        # Position equation_footer at the center of the two labels for smooth morph
        self.objects["equation_footer"].move_to(source_labels.get_center())
        self.play(TransformMatchingTex(source_labels, self.objects["equation_footer"]), run_time=3.0)
        # Move equation to footer after transformation
        self.play(self.objects["equation_footer"].animate.move_to(footer_anchor), run_time=0.5)
        remaining_12 = max(0.1, 3.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_12))