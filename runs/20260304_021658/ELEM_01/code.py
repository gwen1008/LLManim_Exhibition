'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing fraction equivalence 1/2 = 2/4 using side-by-side circle models.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two circles at x=-3 and x=3
#    - Footer Region: [Bottom y=-3.5] for final equivalence equation
# 3. Anti-Overlap Check:
#    - Strategy: Circles placed at x=-3 and x=3 with radius 2. Labels placed below each circle.
#    - Connector arrow placed between circles at y=1.0.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/fraction_equivalence_1_2_2_4/step_XX.mp3"
# 5. Animation Flow:
#    - Create two whole circles.
#    - Divide left circle in half, color one half, label 1/2.
#    - Divide right circle into quarters, color two quarters, label 2/4.
#    - Draw connector arrow between colored regions.
#    - Show final equivalence equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        left_pizza_center = 3.0 * LEFT
        right_pizza_center = 3.0 * RIGHT

        # Object registry
        self.objects = {}

        # Helper to parse geometry_def strings (simplified parsing)
        def parse_geometry_def(obj_def):
            # For simplicity, we'll create objects directly based on type and geometry_def
            # In a full implementation, this would parse the string
            pass

        # Create objects from layout_plan.objects
        # title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # pizza1_base
        pizza1_base = Circle(radius=2.0, color=WHITE, stroke_width=4, fill_opacity=0.0)
        pizza1_base.move_to(left_pizza_center)
        self.objects["pizza1_base"] = pizza1_base

        # pizza2_base
        pizza2_base = Circle(radius=2.0, color=WHITE, stroke_width=4, fill_opacity=0.0)
        pizza2_base.move_to(right_pizza_center)
        self.objects["pizza2_base"] = pizza2_base

        # pizza1_half_sector - NOTE: Sector first arg is radius, not outer_radius
        pizza1_half_sector = Sector(radius=2.0, angle=PI, start_angle=0, color="#1E90FF", fill_opacity=0.0, stroke_width=0)
        pizza1_half_sector.move_to(left_pizza_center)
        self.objects["pizza1_half_sector"] = pizza1_half_sector

        # pizza1_div_line
        pizza1_div_line = Line(start=2*LEFT, end=2*RIGHT, color=WHITE, stroke_width=3)
        pizza1_div_line.move_to(left_pizza_center)
        self.objects["pizza1_div_line"] = pizza1_div_line

        # pizza2_quarter_sector1
        pizza2_quarter_sector1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color="#1E90FF", fill_opacity=0.0, stroke_width=0)
        pizza2_quarter_sector1.move_to(right_pizza_center)
        self.objects["pizza2_quarter_sector1"] = pizza2_quarter_sector1

        # pizza2_quarter_sector2
        pizza2_quarter_sector2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color="#1E90FF", fill_opacity=0.0, stroke_width=0)
        pizza2_quarter_sector2.move_to(right_pizza_center)
        self.objects["pizza2_quarter_sector2"] = pizza2_quarter_sector2

        # pizza2_div_line1
        pizza2_div_line1 = Line(start=2*DOWN, end=2*UP, color=WHITE, stroke_width=3)
        pizza2_div_line1.move_to(right_pizza_center)
        self.objects["pizza2_div_line1"] = pizza2_div_line1

        # pizza2_div_line2
        pizza2_div_line2 = Line(start=2*LEFT, end=2*RIGHT, color=WHITE, stroke_width=3)
        pizza2_div_line2.move_to(right_pizza_center)
        self.objects["pizza2_div_line2"] = pizza2_div_line2

        # label_pizza1
        label_pizza1 = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_pizza1.next_to(pizza1_base, DOWN, buff=0.5)
        self.objects["label_pizza1"] = label_pizza1

        # label_pizza2
        label_pizza2 = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_pizza2.next_to(pizza2_base, DOWN, buff=0.5)
        self.objects["label_pizza2"] = label_pizza2

        # equality_equation
        equality_equation = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=YELLOW, font_size=48)
        equality_equation.move_to(explanation_anchor)
        self.objects["equality_equation"] = equality_equation

        # connector_arrow - double-headed arrow
        connector_arrow = DoubleArrow(start=1.5*RIGHT, end=1.5*LEFT, color="#FFD700", stroke_width=6, tip_length=0.2)
        connector_arrow.move_to(content_center + UP*1.0)
        self.objects["connector_arrow"] = connector_arrow

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_00.mp3")  # [auto-injected]
        # Step 1: Let's start with two identical whole pizzas.
        audio_step1 = "media/audio/fraction_equivalence_1_2_2_4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Create(self.objects["pizza1_base"]), run_time=1.0)
        remaining_1 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_02.mp3")  # [auto-injected]
        # Step 2: 
        audio_step2 = "media/audio/fraction_equivalence_1_2_2_4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Create(self.objects["pizza2_base"]), run_time=1.0)
        remaining_2 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_03.mp3")  # [auto-injected]
        # Step 3: Now, we divide the first pizza into two equal halves.
        audio_step3 = "media/audio/fraction_equivalence_1_2_2_4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # signal_action: Indicate pizza1_base
        self.play(Indicate(self.objects["pizza1_base"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["pizza1_div_line"]), run_time=2.0)
        remaining_3 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_04.mp3")  # [auto-injected]
        # Step 4: We color one of these halves to represent the fraction one-half.
        audio_step4 = "media/audio/fraction_equivalence_1_2_2_4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # signal_action: Indicate pizza1_half_sector
        self.play(Indicate(self.objects["pizza1_half_sector"], color=YELLOW, run_time=1))
        # Fill the sector by setting fill_opacity
        self.play(self.objects["pizza1_half_sector"].animate.set_fill(color="#1E90FF", opacity=0.7), run_time=2.0)
        remaining_4 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_05.mp3")  # [auto-injected]
        # Step 5: We label this model as one-half.
        audio_step5 = "media/audio/fraction_equivalence_1_2_2_4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Write(self.objects["label_pizza1"]), run_time=1.5)
        remaining_5 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_06.mp3")  # [auto-injected]
        # Step 6: Next, we take the second pizza and divide it into four equal quarters.
        audio_step6 = "media/audio/fraction_equivalence_1_2_2_4/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # signal_action: Indicate pizza2_base
        self.play(Indicate(self.objects["pizza2_base"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["pizza2_div_line1"]), Create(self.objects["pizza2_div_line2"]), run_time=2.5)
        remaining_6 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_07.mp3")  # [auto-injected]
        # Step 7: We color two of these quarters to represent the fraction two-fourths.
        audio_step7 = "media/audio/fraction_equivalence_1_2_2_4/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(
            self.objects["pizza2_quarter_sector1"].animate.set_fill(color="#1E90FF", opacity=0.7),
            self.objects["pizza2_quarter_sector2"].animate.set_fill(color="#1E90FF", opacity=0.7),
            run_time=2.5
        )
        remaining_7 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_08.mp3")  # [auto-injected]
        # Step 8: We label this model as two-fourths.
        audio_step8 = "media/audio/fraction_equivalence_1_2_2_4/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # signal_action: null
        self.play(Write(self.objects["label_pizza2"]), run_time=1.5)
        remaining_8 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_09.mp3")  # [auto-injected]
        # Step 9: Now, observe the colored regions. The blue area in the first pizza is exactly equal to the blue area in the second pizza.
        audio_step9 = "media/audio/fraction_equivalence_1_2_2_4/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        # signal_action: Circumscribe pizza1_half_sector
        self.play(Circumscribe(self.objects["pizza1_half_sector"], color="#FFD700", run_time=1))
        self.play(Create(self.objects["connector_arrow"]), run_time=3.0)
        remaining_9 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10: This visual equivalence demonstrates the mathematical truth: one-half is equal to two-fourths.
        audio_step10 = "media/audio/fraction_equivalence_1_2_2_4/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        # signal_action: Indicate connector_arrow
        self.play(Indicate(self.objects["connector_arrow"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["equality_equation"]), run_time=3.0)
        remaining_10 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))