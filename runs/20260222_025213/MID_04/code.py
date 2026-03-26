'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof that alternate interior angles (∠3 and ∠6) formed by a transversal cutting two parallel lines are congruent.
# 2. Layout Strategy:
#    - Header Region: [y=3.2] for Title
#    - Main Content: [Center y=0] for parallel lines and transversal diagram
#    - Footer Region: [Bottom y=-3.2] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each angle (arc + label) to keep them together during transformation.
#    - The main diagram is centered, labels are placed relative to line ends/arc centers.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step where audio_path is provided?
#    - [x] Files: "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_XX.mp3"
# 5. Animation Flow:
#    - Draw title, parallel lines (l, m), transversal (t), and labels.
#    - Create and label angle arcs for ∠3 and ∠6, color them green.
#    - Transform angle 3 group onto angle 6 group to demonstrate congruence.
#    - Display final congruence statement.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for all objects
        self.objects = {}

        # Create anchors from layout_plan
        title_anchor = 3.2 * UP
        explanation_anchor = 3.2 * DOWN
        global_center = ORIGIN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Parallel Lines and a Transversal", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Parallel lines l and m
        line_l = Line(start=[-5, 2, 0], end=[5, 2, 0], color=BLUE, stroke_width=4)
        self.objects["line_l"] = line_l

        line_m = Line(start=[-5, -2, 0], end=[5, -2, 0], color=BLUE, stroke_width=4)
        self.objects["line_m"] = line_m

        # Transversal line t
        line_t = Line(start=[-3.5, 2, 0], end=[3.5, -2, 0], color=RED, stroke_width=4)
        self.objects["line_t"] = line_t

        # Labels for lines
        label_l = MathTex("l", color=BLUE)
        label_l.next_to(line_l.get_end(), RIGHT, buff=0.2)
        self.objects["label_l"] = label_l

        label_m = MathTex("m", color=BLUE)
        label_m.next_to(line_m.get_end(), RIGHT, buff=0.2)
        self.objects["label_m"] = label_m

        label_t = MathTex("t", color=RED)
        label_t.next_to(line_t.get_end(), RIGHT + UP, buff=0.2)
        self.objects["label_t"] = label_t

        # Angle arcs and labels
        # Angle 3: intersection of t and l (at start of line_t)
        angle_3_arc = Angle(line_t, line_l, radius=0.6, color=WHITE, stroke_width=6, other_angle=False)
        self.objects["angle_3_arc"] = angle_3_arc

        label_angle_3 = MathTex("3", color=WHITE, font_size=24)
        # Position relative to arc center
        label_angle_3.next_to(angle_3_arc.get_center(), RIGHT + UP, buff=0.1)
        self.objects["label_angle_3"] = label_angle_3

        # Angle 6: intersection of m and t (at end of line_t)
        angle_6_arc = Angle(line_m, line_t, radius=0.6, color=WHITE, stroke_width=6, other_angle=False)
        self.objects["angle_6_arc"] = angle_6_arc

        label_angle_6 = MathTex("6", color=WHITE, font_size=24)
        label_angle_6.next_to(angle_6_arc.get_center(), LEFT + DOWN * 0.3, buff=0.1)
        self.objects["label_angle_6"] = label_angle_6

        # VGroups for angles (arc + label)
        angle_group_3 = VGroup(angle_3_arc, label_angle_3)
        self.objects["angle_group_3"] = angle_group_3

        angle_group_6 = VGroup(angle_6_arc, label_angle_6)
        self.objects["angle_group_6"] = angle_group_6

        # Step explanation text
        step_text = Text("Step 1: Draw two parallel lines and a transversal.", color=WHITE, font_size=24)
        step_text.move_to(explanation_anchor)
        self.objects["step_text"] = step_text

        # Final congruence statement
        congruence_statement = MathTex(r"\angle 3 \cong \angle 6", color=GREEN, font_size=40)
        congruence_statement.move_to(global_center + 2 * DOWN)
        self.objects["congruence_statement"] = congruence_statement

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeIn(self.objects["title"]))
        self.wait(max(0.1, max(0.1, 5.712 - 1.0)))

        # Step 2
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["line_l"]))
        self.wait(max(0.1, max(0.1, 2.928 - 1.0)))

        # Step 3
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["line_m"]))
        self.wait(max(0.1, max(0.1, 2.832 - 1.0)))

        # Step 4
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["line_t"]))
        self.wait(max(0.1, max(0.1, 5.352 - 1.0)))

        # Step 5
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["label_l"]))
        self.wait(max(0.1, max(0.1, 2.808 - 1.0)))

        # Step 6
        self.play(Write(self.objects["label_m"]))
        self.wait(max(0.1, 2.0 - 1.0))

        # Step 7
        self.play(Write(self.objects["label_t"]))
        self.wait(max(0.1, 2.0 - 1.0))

        # Step 8
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate label_angle_3
        self.play(Indicate(self.objects["label_angle_3"], color=YELLOW))
        self.play(Create(self.objects["angle_3_arc"]))
        self.wait(max(0.1, max(0.1, 9.744 - 2.0)))

        # Step 9
        self.play(Write(self.objects["label_angle_3"]))
        self.wait(max(0.1, 2.0 - 1.0))

        # Step 10
        # Signal action: Indicate label_angle_6
        self.play(Indicate(self.objects["label_angle_6"], color=YELLOW))
        self.play(Create(self.objects["angle_6_arc"]))
        self.wait(max(0.1, 2.0 - 2.0))

        # Step 11
        self.play(Write(self.objects["label_angle_6"]))
        self.wait(max(0.1, 2.0 - 1.0))

        # Step 12
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_11.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(self.objects["angle_3_arc"].animate.set_color(GREEN))
        self.wait(max(0.1, max(0.1, 11.976 - 1.0)))

        # Step 13
        self.play(self.objects["angle_6_arc"].animate.set_color(GREEN))
        self.wait(max(0.1, 2.0 - 1.0))

        # Step 14
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_13.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        new_step_text = Text("Demonstrating Congruence: ∠3 ≅ ∠6", color=WHITE, font_size=24)
        new_step_text.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_text"], new_step_text))
        self.objects["step_text"] = new_step_text
        self.wait(max(0.1, max(0.1, 7.752 - 1.0)))

        # Step 15
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_14.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe angle_group_3
        self.play(Circumscribe(self.objects["angle_group_3"], color=YELLOW, run_time=1))
        # Visual action: Indicate (pulsate) angle_group_3
        self.play(Indicate(self.objects["angle_group_3"], color=YELLOW))
        self.wait(max(0.1, max(0.1, 5.472 - 2.0)))

        # Step 16
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_15.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Create a copy of angle_group_6 to transform onto
        target_group = self.objects["angle_group_6"].copy()
        # Transform angle_group_3 to match target_group's position and orientation
        self.play(Transform(self.objects["angle_group_3"], target_group))
        self.wait(max(0.1, max(0.1, 4.392 - 1.0)))

        # Step 17
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_16.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate angle_group_6
        self.play(Indicate(self.objects["angle_group_6"], color=GREEN))
        self.play(Write(self.objects["congruence_statement"]))
        self.wait(max(0.1, max(0.1, 6.096 - 2.0)))

        # Final pause
        self.wait(max(0.1, 2))