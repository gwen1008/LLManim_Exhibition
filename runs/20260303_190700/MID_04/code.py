'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof of the Corresponding Angles Theorem: corresponding angles formed by a transversal of two parallel lines are congruent.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for parallel lines, transversal, and angle arcs
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for angle arcs and labels for easier management. Position angle labels near arc centers.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/corresponding_angles/step_XX.mp3"
# 5. Animation Flow:
#    - Draw parallel lines → Draw transversal → Mark corresponding angles → Label them → Highlight angles → Show congruence.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create title
        title = Text("Corresponding Angles Theorem", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create parallel lines
        line_l1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=6)
        line_l1.move_to(diagram_center + UP)
        self.objects["line_l1"] = line_l1
        
        line_l2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=6)
        line_l2.move_to(diagram_center + DOWN)
        self.objects["line_l2"] = line_l2
        
        # Create transversal
        line_t = Line(start=[-4, -2, 0], end=[4, 2, 0], color=RED, stroke_width=6)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t
        
        # Create angle arcs (will be positioned at intersections)
        # Intersection points: line_t with line_l1 at (2,1,0), with line_l2 at (-2,-1,0)
        # We'll create them but not add to scene yet
        angle_a = Angle(line_t, line_l1, radius=0.5, other_angle=False, color=WHITE, stroke_width=4)
        self.objects["angle_a"] = angle_a
        
        angle_b = Angle(line_t, line_l2, radius=0.5, other_angle=False, color=WHITE, stroke_width=4)
        self.objects["angle_b"] = angle_b
        
        # Create angle labels
        label_angle_a = MathTex(r"\angle 1", color=WHITE).scale(0.8)
        # Position near angle_a center
        label_angle_a.next_to(angle_a.get_center(), UR, buff=0.15)
        self.objects["label_angle_a"] = label_angle_a
        
        label_angle_b = MathTex(r"\angle 2", color=WHITE).scale(0.8)
        label_angle_b.next_to(angle_b.get_center(), UR, buff=0.15)
        self.objects["label_angle_b"] = label_angle_b
        
        # Create explanation text
        explanation_text = Text(
            "Corresponding angles are on the same side of the transversal and in corresponding positions relative to the parallel lines.",
            color=YELLOW, font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Create congruence statement for step 11
        congruence_statement = MathTex(r"\angle 1 \cong \angle 2", color=GREEN, font_size=36)
        congruence_statement.move_to(diagram_center + 2 * RIGHT)
        self.objects["congruence_statement"] = congruence_statement
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_00.mp3")  # [auto-injected]
        # Step 1: Draw first parallel line
        audio_step1 = "media/audio/corresponding_angles/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_l1"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_01.mp3")  # [auto-injected]
        # Step 2: Draw second parallel line
        audio_step2 = "media/audio/corresponding_angles/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_l2"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_02.mp3")  # [auto-injected]
        # Step 3: Introduce transversal with signal
        audio_step3 = "media/audio/corresponding_angles/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate line_t
        self.play(Indicate(self.objects["line_t"], color=RED, run_time=1))
        # Visual action: Create transversal
        self.play(Create(self.objects["line_t"]), run_time=2.0)
        remaining_3 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_03.mp3")  # [auto-injected]
        # Step 4: Mark first corresponding angle
        audio_step4 = "media/audio/corresponding_angles/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["angle_a"]), run_time=1.5)
        remaining_4 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_04.mp3")  # [auto-injected]
        # Step 5: Mark second corresponding angle
        audio_step5 = "media/audio/corresponding_angles/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["angle_b"]), run_time=1.5)
        remaining_5 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_05.mp3")  # [auto-injected]
        # Step 6: Label first angle
        audio_step6 = "media/audio/corresponding_angles/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_angle_a"]), run_time=1.0)
        remaining_6 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_07.mp3")  # [auto-injected]
        # Step 7: Label second angle
        audio_step7 = "media/audio/corresponding_angles/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_angle_b"]), run_time=1.0)
        remaining_7 = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_09.mp3")  # [auto-injected]
        # Step 8: Highlight pair with signal and change angle_a color
        audio_step8 = "media/audio/corresponding_angles/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe explanation_text
        self.play(Circumscribe(self.objects["explanation_text"], color=YELLOW, run_time=1))
        # Visual action: Transform angle_a to green
        angle_a_green = self.objects["angle_a"].copy().set_color(GREEN)
        self.play(Transform(self.objects["angle_a"], angle_a_green), run_time=1.5)
        remaining_8 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        self.add_sound("media/audio/Draw_two_parallel_li_a27e93db69/step_10.mp3")  # [auto-injected]
        # Step 9: Change angle_b color
        audio_step9 = "media/audio/corresponding_angles/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        angle_b_green = self.objects["angle_b"].copy().set_color(GREEN)
        self.play(Transform(self.objects["angle_b"], angle_b_green), run_time=1.5)
        remaining_9 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Step 10: Show congruence (transform label)
        audio_step10 = "media/audio/corresponding_angles/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # Create new label showing equality
        congruence_label = MathTex(r"\angle 1 = \angle 2", color=GREEN, font_size=36)
        congruence_label.move_to(self.objects["label_angle_a"].get_center())
        self.play(TransformMatchingTex(self.objects["label_angle_a"].copy(), congruence_label), run_time=3.0)
        remaining_10 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # Step 11: Final indication and statement
        audio_step11 = "media/audio/corresponding_angles/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        # Signal action: Indicate angle_a
        self.play(Indicate(self.objects["angle_a"], color=GREEN, run_time=1))
        # Visual action: Fade in congruence statement
        self.play(FadeIn(self.objects["congruence_statement"]), run_time=3.0)
        remaining_11 = max(0.1, 3.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # Final hold
        self.wait(max(0.1, 2))