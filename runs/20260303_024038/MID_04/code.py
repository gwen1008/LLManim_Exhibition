'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof of the Corresponding Angles Theorem (∠1 ≅ ∠2 when lines are parallel).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Corresponding Angles Theorem"
#    - Main Content: [Center y=0] for parallel lines, transversal, and angle arcs.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Strategy: Keep diagram centered, use relative positioning for labels. Explanation text is scaled to 0.8 and placed at bottom.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/corresponding_angles_theorem/step_XX.mp3"
# 5. Animation Flow:
#    - Setup parallel lines and labels.
#    - Add transversal.
#    - Identify and draw corresponding angles (∠1 and ∠2).
#    - Visual proof: copy ∠1, rotate/translate it to overlap ∠2.
#    - Conclusion.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Draw_two_parallel_li_d84c06f773/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Corresponding Angles Theorem", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # line_l1
        line_l1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center + UP)
        self.objects["line_l1"] = line_l1

        # line_l2
        line_l2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN)
        self.objects["line_l2"] = line_l2

        # line_t
        line_t = Line(start=[-3, 1, 0], end=[3, -1, 0], color=YELLOW, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t

        # label_l1
        label_l1 = MathTex("l_1", color=BLUE)
        label_l1.next_to(self.objects["line_l1"], RIGHT, buff=0.2)
        self.objects["label_l1"] = label_l1

        # label_l2
        label_l2 = MathTex("l_2", color=BLUE)
        label_l2.next_to(self.objects["line_l2"], RIGHT, buff=0.2)
        self.objects["label_l2"] = label_l2

        # label_t
        label_t = MathTex("t", color=YELLOW)
        label_t.next_to(self.objects["line_t"].get_end(), RIGHT+UP, buff=0.1)
        self.objects["label_t"] = label_t

        # angle1_arc (will be created after lines exist)
        # We'll create it later when needed (step 8)
        # angle1_label
        # angle2_arc
        # angle2_label
        # angle_copy_group (created during sequence)

        # explanation_text
        explanation_text = Text("Step 1: Two parallel lines and a transversal.", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        explanation_text.scale(0.8)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/corresponding_angles_theorem/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title"]), run_time=1.0)
        remaining_1 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/corresponding_angles_theorem/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Create(self.objects["line_l1"]), run_time=1.0)
        remaining_2 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/corresponding_angles_theorem/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Create(self.objects["line_l2"]), run_time=1.0)
        remaining_3 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/corresponding_angles_theorem/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Write(self.objects["label_l1"]), run_time=0.5)
        remaining_4 = max(0.1, 0.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/corresponding_angles_theorem/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Write(self.objects["label_l2"]), run_time=0.5)
        remaining_5 = max(0.1, 0.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/corresponding_angles_theorem/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Create(self.objects["line_t"]), run_time=1.5)
        remaining_6 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/corresponding_angles_theorem/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Write(self.objects["label_t"]), run_time=0.5)
        remaining_7 = max(0.1, 0.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/corresponding_angles_theorem/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        # Signal action: Circumscribe VGroup(line_l1, line_t)
        self.play(Circumscribe(VGroup(self.objects["line_l1"], self.objects["line_t"]), color=WHITE, run_time=1))
        # Update explanation text
        new_explanation1 = Text("Step 2: Identify corresponding angles.", color=GRAY_B, font_size=24)
        new_explanation1.move_to(explanation_anchor)
        new_explanation1.scale(0.8)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation1))
        self.objects["explanation_text"] = new_explanation1
        remaining_8 = max(0.1, 3.0 - 1.0 - 0.5 + 0.5)  # signal 1s + transform ~0.5s
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        audio_step9 = "media/audio/corresponding_angles_theorem/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))

        # Create angle1_arc
        angle1_arc = Angle(line1=self.objects["line_t"], line2=self.objects["line_l1"], radius=0.4, other_angle=False, color=GREEN, stroke_width=6)
        self.objects["angle1_arc"] = angle1_arc
        self.play(Create(angle1_arc), run_time=1.5)
        remaining_9 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # ========== Step 10 ==========
        audio_step10 = "media/audio/corresponding_angles_theorem/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))

        # Create angle1_label
        angle1_label = MathTex(r"\angle 1", color=GREEN)
        angle1_label.next_to(angle1_arc.get_center(), UP+LEFT, buff=0.1)
        self.objects["angle1_label"] = angle1_label
        self.play(Write(angle1_label), run_time=1.0)
        remaining_10 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # ========== Step 11 ==========
        audio_step11 = "media/audio/corresponding_angles_theorem/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))

        # Signal action: Indicate angle1_arc
        self.play(Indicate(self.objects["angle1_arc"], color=GREEN, run_time=1))
        # Create angle2_arc
        angle2_arc = Angle(line1=self.objects["line_l2"], line2=self.objects["line_t"], radius=0.4, other_angle=False, color=GREEN, stroke_width=6)
        self.objects["angle2_arc"] = angle2_arc
        self.play(Create(angle2_arc), run_time=2.0)
        remaining_11 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_11))

        # ========== Step 12 ==========
        audio_step12 = "media/audio/corresponding_angles_theorem/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))

        # Create angle2_label
        angle2_label = MathTex(r"\angle 2", color=GREEN)
        angle2_label.next_to(angle2_arc.get_center(), DOWN+RIGHT, buff=0.1)
        self.objects["angle2_label"] = angle2_label
        self.play(Write(angle2_label), run_time=1.0)
        remaining_12 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_12))

        # ========== Step 13 ==========
        audio_step13 = "media/audio/corresponding_angles_theorem/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))

        # Signal action: Indicate angle1_arc
        self.play(Indicate(self.objects["angle1_arc"], color=YELLOW, run_time=1))
        # Update explanation text
        new_explanation2 = Text("Step 3: Visual proof by rotation.", color=GRAY_B, font_size=24)
        new_explanation2.move_to(explanation_anchor)
        new_explanation2.scale(0.8)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation2))
        self.objects["explanation_text"] = new_explanation2
        remaining_13 = max(0.1, 2.5 - 1.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_13))

        # ========== Step 14 ==========
        audio_step14 = "media/audio/corresponding_angles_theorem/step_13.mp3"
        if os.path.exists(audio_step14):
            self.add_sound(audio_step14)
        elif os.path.exists(audio_step14.replace(".mp3", ".wav")):
            self.add_sound(audio_step14.replace(".mp3", ".wav"))

        # Create angle_copy_group (copy of angle1_arc and angle1_label)
        angle_copy_group = VGroup(self.objects["angle1_arc"].copy(), self.objects["angle1_label"].copy())
        self.objects["angle_copy_group"] = angle_copy_group
        self.add(angle_copy_group)  # Add it for the transformation
        # Animate the copy to overlap angle2
        target_group = VGroup(self.objects["angle2_arc"], self.objects["angle2_label"])
        # We'll transform the copy group to match the target group's position and orientation
        # Use Transform for simplicity (the copy will morph to overlap the existing angle2)
        self.play(Transform(angle_copy_group, target_group.copy().set_opacity(0.7)), run_time=4.0)
        remaining_14 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_14))

        # ========== Step 15 ==========
        audio_step15 = "media/audio/corresponding_angles_theorem/step_14.mp3"
        if os.path.exists(audio_step15):
            self.add_sound(audio_step15)
        elif os.path.exists(audio_step15.replace(".mp3", ".wav")):
            self.add_sound(audio_step15.replace(".mp3", ".wav"))

        # Signal action: Circumscribe VGroup(angle2_arc, angle_copy_group)
        self.play(Circumscribe(VGroup(self.objects["angle2_arc"], angle_copy_group), color=WHITE, run_time=1))
        # Update explanation text
        new_explanation3 = Text("Conclusion: ∠1 ≅ ∠2. Corresponding angles are congruent.", color=GRAY_B, font_size=24)
        new_explanation3.move_to(explanation_anchor)
        new_explanation3.scale(0.8)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation3))
        self.objects["explanation_text"] = new_explanation3
        remaining_15 = max(0.1, 3.5 - 1.0 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_15))

        # Final hold
        self.wait(max(0.1, 2))