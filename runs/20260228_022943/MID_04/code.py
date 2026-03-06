'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof of the Corresponding Angles Theorem (when a transversal crosses parallel lines, corresponding angles are congruent).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Corresponding Angles Theorem"
#    - Main Content: [Center y=0] for parallel lines, transversal, and angle arcs.
#    - Footer Region: [Bottom y=-3.5] for explanation text and property statement.
# 3. Anti-Overlap Check:
#    - Lines are placed at y=2 and y=-2, transversal runs diagonally. Angle arcs have small radius (0.4). Labels are placed with buff.
#    - Explanation and property statement are in footer, separated vertically.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step where audio_path is provided?
#    - [x] Files: "media/audio/Draw_two_parallel_li_865c978e39/step_XX.mp3"
# 5. Animation Flow:
#    - Draw parallel lines and transversal with labels.
#    - Show explanation text.
#    - Create and label the two green corresponding angles.
#    - Transform explanation into property statement.
#    - Animate first angle moving to overlap the second, proving congruence.
#    - Final indication.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Corresponding Angles Theorem", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Parallel lines and transversal (geometry_def parsed as start/end lists)
        line_l1 = Line(start=[-4, 2, 0], end=[4, 2, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center + UP*2)
        self.objects["line_l1"] = line_l1

        line_l2 = Line(start=[-4, -2, 0], end=[4, -2, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN*2)
        self.objects["line_l2"] = line_l2

        line_t = Line(start=[-3.5, 3, 0], end=[3.5, -3, 0], color=RED, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t

        # Labels for lines
        label_l1 = MathTex("l_1", color=BLUE)
        label_l1.next_to(line_l1, RIGHT, buff=0.2)
        self.objects["label_l1"] = label_l1

        label_l2 = MathTex("l_2", color=BLUE)
        label_l2.next_to(line_l2, RIGHT, buff=0.2)
        self.objects["label_l2"] = label_l2

        label_t = MathTex("t", color=RED)
        label_t.next_to(line_t.get_end(), RIGHT+DOWN, buff=0.1)
        self.objects["label_t"] = label_t

        # Angle arcs (will be created after lines exist, but we define placeholders)
        # We'll create them in the steps where they are first used (steps 8 and 10)
        # For now, store None; they will be created dynamically.
        self.objects["angle_arc_1"] = None
        self.objects["angle_arc_2"] = None

        # Angle labels (depend on arcs, so also placeholders)
        self.objects["angle_label_1"] = None
        self.objects["angle_label_2"] = None

        # Explanation text
        explanation_text = Text("Interior angles on the same side of the transversal.", color=WHITE, font_size=32)
        explanation_text.scale(0.8)
        explanation_text.move_to(explanation_anchor + UP*0.3)
        self.objects["explanation_text"] = explanation_text

        # Property statement
        property_statement = MathTex(r"\angle 1 \cong \angle 2", color=YELLOW, font_size=40)
        property_statement.move_to(explanation_anchor + DOWN*0.3)
        self.objects["property_statement"] = property_statement

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_step1 = "media/audio/Draw_two_parallel_li_865c978e39/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Create(self.objects["line_l1"]), run_time=1.5)
        remaining_1 = max(0.1, 9.168 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2
        self.play(Create(self.objects["line_l2"]), run_time=1.5)
        remaining_2 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3
        self.play(Create(self.objects["line_t"]), run_time=1.5)
        remaining_3 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4
        audio_step4 = "media/audio/Draw_two_parallel_li_865c978e39/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        self.play(Write(self.objects["label_l1"]), run_time=1.0)
        remaining_4 = max(0.1, 2.472 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5
        self.play(Write(self.objects["label_l2"]), run_time=1.0)
        remaining_5 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6
        self.play(Write(self.objects["label_t"]), run_time=1.0)
        remaining_6 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7
        audio_step7 = "media/audio/Draw_two_parallel_li_865c978e39/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        self.play(Write(self.objects["explanation_text"]), run_time=2.0)
        remaining_7 = max(0.1, 8.424 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Step 8: Create angle_arc_1 (first corresponding angle)
        audio_step8 = "media/audio/Draw_two_parallel_li_865c978e39/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Create the angle arc dynamically
        angle_arc_1 = Angle(line1=self.objects["line_t"], line2=self.objects["line_l1"], radius=0.4, other_angle=False, color=GREEN, stroke_width=6)
        angle_arc_1.set_fill(color=GREEN, opacity=0.3)
        self.objects["angle_arc_1"] = angle_arc_1
        # Signal action: Circumscribe the arc (target is the arc itself, but it doesn't exist yet; we'll circumscribe after creation)
        # We'll create the arc, then circumscribe it.
        self.play(Create(angle_arc_1), run_time=1.5)
        self.play(Circumscribe(angle_arc_1, color=YELLOW, run_time=1))
        remaining_8 = max(0.1, 4.896 - (1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9: Write angle_label_1
        angle_label_1 = MathTex(r"\angle 1", color=GREEN, font_size=30)
        # Position next to the arc's midpoint
        angle_label_1.next_to(angle_arc_1.point_from_proportion(0.5), UL, buff=0.1)
        self.objects["angle_label_1"] = angle_label_1
        self.play(Write(angle_label_1), run_time=1.0)
        remaining_9 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10: Create angle_arc_2 (second corresponding angle)
        audio_step10 = "media/audio/Draw_two_parallel_li_865c978e39/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        angle_arc_2 = Angle(line1=self.objects["line_t"], line2=self.objects["line_l2"], radius=0.4, other_angle=False, color=GREEN, stroke_width=6)
        angle_arc_2.set_fill(color=GREEN, opacity=0.3)
        self.objects["angle_arc_2"] = angle_arc_2
        self.play(Create(angle_arc_2), run_time=1.5)
        self.play(Circumscribe(angle_arc_2, color=YELLOW, run_time=1))
        remaining_10 = max(0.1, 6.144 - (1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_10))

        # Step 11: Write angle_label_2
        angle_label_2 = MathTex(r"\angle 2", color=GREEN, font_size=30)
        angle_label_2.next_to(angle_arc_2.point_from_proportion(0.5), UL, buff=0.1)
        self.objects["angle_label_2"] = angle_label_2
        self.play(Write(angle_label_2), run_time=1.0)
        remaining_11 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_11))

        # Step 12: Replace explanation_text with property_statement
        audio_step12 = "media/audio/Draw_two_parallel_li_865c978e39/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        self.play(ReplacementTransform(self.objects["explanation_text"], self.objects["property_statement"]), run_time=2.0)
        remaining_12 = max(0.1, 10.608 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_12))

        # Step 13: Transform angle_arc_1 (and its label) to angle_arc_2
        audio_step13 = "media/audio/Draw_two_parallel_li_865c978e39/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        # Signal action: Indicate angle_arc_1
        self.play(Indicate(self.objects["angle_arc_1"], color=WHITE, run_time=1))
        # Create a copy of angle_arc_1 and its label to animate, while keeping originals?
        # The JSON says "Transform" with target_id angle_arc_1 and transform_to angle_arc_2.
        # We'll transform the actual angle_arc_1 and angle_label_1 to the positions of angle_arc_2 and angle_label_2.
        # To keep the target visible, we can create a copy for the transformation.
        moving_arc = self.objects["angle_arc_1"].copy()
        moving_label = self.objects["angle_label_1"].copy()
        self.add(moving_arc, moving_label)
        # Animate the copy moving to the position of angle_arc_2 and angle_label_2
        self.play(
            moving_arc.animate.move_to(self.objects["angle_arc_2"].get_center()).rotate(
                angle_of_vector(self.objects["angle_arc_2"].get_start() - self.objects["angle_arc_2"].get_center()) -
                angle_of_vector(moving_arc.get_start() - moving_arc.get_center())
            ),
            moving_label.animate.move_to(self.objects["angle_label_2"].get_center()),
            run_time=3.0
        )
        self.remove(moving_arc, moving_label)
        remaining_13 = max(0.1, 8.304 - (1.0 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_13))

        # Step 14: Final indication
        audio_step14 = "media/audio/Draw_two_parallel_li_865c978e39/step_13.mp3"
        if os.path.exists(audio_step14):
            self.add_sound(audio_step14)
        elif os.path.exists(audio_step14.replace(".mp3", ".wav")):
            self.add_sound(audio_step14.replace(".mp3", ".wav"))
        self.play(Indicate(self.objects["angle_arc_2"], color=YELLOW, run_time=1))
        remaining_14 = max(0.1, 7.2 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_14))