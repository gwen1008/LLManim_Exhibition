'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate that a circle's circumference C = πD and that π > 3 by comparing the unfolded circumference to a line of length 3D.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for circle and transformation, [Right x=4,6] for vertical comparison lines.
#    - Footer Region: [Bottom y=-3.5] for explanation text.
# 3. Anti-Overlap Check:
#    - The circle and its diameter are centered. The vertical lines (C and 3D) are placed to the right at x=4 and x=6, anchored at y=1 to keep them on screen.
#    - Labels are placed to the right of their respective lines.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_an_animation__d795d8dee1/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show circle and its diameter.
#    - Step 2: Highlight circle boundary, then morph it into the vertical circumference line.
#    - Step 3: Label the circumference line.
#    - Step 4: Indicate diameter, then draw the 3D line.
#    - Step 5: Indicate and draw the excess line segment, showing π > 3.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan description
        title_anchor = 3.5 * UP
        stage_center = ORIGIN
        # Comparison anchor: to the right of center. We'll place lines at x=4 and x=6, top at y=1.
        comparison_top_anchor = np.array([4, 1, 0])
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Unfolding a Circle: Circumference and π", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # circle
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(stage_center)
        self.objects["circle"] = circle

        # diameter_line
        diameter_line = Line(start=np.array([-2, 0, 0]), end=np.array([2, 0, 0]), color=YELLOW, stroke_width=6)
        diameter_line.move_to(stage_center)
        self.objects["diameter_line"] = diameter_line

        # diameter_label
        diameter_label = MathTex("D", color=YELLOW)
        diameter_label.next_to(diameter_line, UP, buff=0.2)
        self.objects["diameter_label"] = diameter_label

        # circumference_line (length = π*D = π*4 ≈ 12.566, vertical, top at y=1, x=4)
        circumference_line = Line(
            start=np.array([4, 1, 0]),
            end=np.array([4, 1 - 12.566, 0]),
            color=GREEN,
            stroke_width=4
        )
        self.objects["circumference_line"] = circumference_line

        # circumference_label
        circumference_label = MathTex(r"C = \pi D", color=GREEN)
        circumference_label.next_to(circumference_line, RIGHT, buff=0.3)
        self.objects["circumference_label"] = circumference_label

        # three_d_line (length = 3*D = 12, vertical, top at y=1, x=6)
        three_d_line = Line(
            start=np.array([6, 1, 0]),
            end=np.array([6, 1 - 12, 0]),
            color=RED,
            stroke_width=4
        )
        self.objects["three_d_line"] = three_d_line

        # three_d_label
        three_d_label = MathTex("3D", color=RED)
        three_d_label.next_to(three_d_line, RIGHT, buff=0.3)
        self.objects["three_d_label"] = three_d_label

        # excess_line (segment from bottom of 3D line to bottom of circumference line)
        excess_line = Line(
            start=np.array([4, 1 - 12, 0]),
            end=np.array([4, 1 - 12.566, 0]),
            color=PINK,
            stroke_width=6
        )
        self.objects["excess_line"] = excess_line

        # explanation_text (initial content)
        explanation_text = Text("The circle's boundary is its circumference, C.", color=GRAY_C, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_an_animation__d795d8dee1/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Signal action: Create diameter_line (as per JSON, signal_action type is Create)
        self.play(Create(self.objects["diameter_line"]), run_time=1.5)
        # Visual action: Create circle
        self.play(Create(self.objects["circle"]), run_time=2.0)
        # Write title and diameter label together
        self.play(Write(self.objects["title"]), Write(self.objects["diameter_label"]), run_time=1.5)
        # Update explanation text (optional, but we can set it)
        new_explanation = Text("We begin with a circle. Its diameter, labeled D, is the distance across it through the center.",
                               color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation), run_time=1.0)
        self.objects["explanation_text"] = new_explanation

        remaining_1 = max(0.1, 7.128 - (1.5 + 2.0 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_an_animation__d795d8dee1/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Circumscribe circle
        self.play(Circumscribe(self.objects["circle"], color=YELLOW, run_time=1))
        # Visual action: ReplacementTransform circle into circumference_line
        # We'll create a copy of circumference_line at the circle's location for transformation
        circle_for_transform = self.objects["circle"].copy()
        self.play(ReplacementTransform(circle_for_transform, self.objects["circumference_line"]), run_time=2.5)
        # Update explanation
        new_explanation2 = Text("Now, imagine taking the boundary of the circle and straightening it out into a line. This line is the circumference, C.",
                                color=GRAY_C, font_size=24)
        new_explanation2.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation2), run_time=1.5)
        self.objects["explanation_text"] = new_explanation2

        remaining_2 = max(0.1, 7.752 - (1 + 2.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_an_animation__d795d8dee1/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # No signal action (null)
        # Visual action: Write circumference_label
        self.play(Write(self.objects["circumference_label"]), run_time=1.5)
        # Update explanation
        new_explanation3 = Text("Let's label this line. Its length is pi times the diameter, C equals pi D.",
                                color=GRAY_C, font_size=24)
        new_explanation3.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation3), run_time=1.5)
        self.objects["explanation_text"] = new_explanation3

        remaining_3 = max(0.1, 5.736 - (1.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_an_animation__d795d8dee1/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate diameter_line
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        # Visual action: Create three_d_line
        self.play(Create(self.objects["three_d_line"]), run_time=2.0)
        # Also write its label
        self.play(Write(self.objects["three_d_label"]), run_time=1.0)
        # Update explanation
        new_explanation4 = Text("How does this length compare to just three diameters? Let's place a line of length three D next to it.",
                                color=GRAY_C, font_size=24)
        new_explanation4.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation4), run_time=1.5)
        self.objects["explanation_text"] = new_explanation4

        remaining_4 = max(0.1, 5.856 - (1 + 2.0 + 1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_an_animation__d795d8dee1/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate excess_line
        self.play(Indicate(self.objects["excess_line"], color=PINK, run_time=1))
        # Visual action: Create excess_line
        self.play(Create(self.objects["excess_line"]), run_time=2.0)
        # Update explanation
        new_explanation5 = Text("Now, we compare. Align the 3D line with the start of the circumference line. We see that the circumference is longer. This extra piece demonstrates that pi is greater than three.",
                                color=GRAY_C, font_size=24)
        new_explanation5.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], new_explanation5), run_time=3.0)
        self.objects["explanation_text"] = new_explanation5

        remaining_5 = max(0.1, 12.192 - (1 + 2.0 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))