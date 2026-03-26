'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual proof that corresponding interior angles are congruent when two parallel lines are cut by a transversal.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for geometric diagram
#    - Footer Region: [Bottom y=-3.0] for explanation text
# 3. Anti-Overlap Check:
#    - Diagram centered at origin. Labels placed with buff to avoid overlap.
#    - Explanation text at bottom, scaled to fit width.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_XX.mp3"
# 5. Animation Flow:
#    - Draw parallel lines and transversal.
#    - Add labels and intersection points.
#    - Highlight the two corresponding interior angles with green arcs.
#    - Label the angles.
#    - State the postulate and show congruence via transformation of one arc onto the other.
#    - Conclude.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        diagram_center = ORIGIN
        title_anchor = 3.0 * UP
        explanation_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Corresponding Interior Angles", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # line_l1
        line_l1 = Line(start=[-4, 1.5, 0], end=[4, 1.5, 0], color=BLUE, stroke_width=3)
        self.objects["line_l1"] = line_l1

        # line_l2
        line_l2 = Line(start=[-4, -1.5, 0], end=[4, -1.5, 0], color=BLUE, stroke_width=3)
        self.objects["line_l2"] = line_l2

        # line_t
        line_t = Line(start=[-4, 2.5, 0], end=[4, -2.5, 0], color=RED, stroke_width=3)
        self.objects["line_t"] = line_t

        # label_l1
        label_l1 = MathTex("l_1", color=BLUE, font_size=30)
        label_l1.next_to(line_l1.get_end(), RIGHT, buff=0.2)
        self.objects["label_l1"] = label_l1

        # label_l2
        label_l2 = MathTex("l_2", color=BLUE, font_size=30)
        label_l2.next_to(line_l2.get_end(), RIGHT, buff=0.2)
        self.objects["label_l2"] = label_l2

        # label_t
        label_t = MathTex("t", color=RED, font_size=30)
        label_t.next_to(line_t.get_end(), DOWN+RIGHT, buff=0.2)
        self.objects["label_t"] = label_t

        # point_A
        point_A = Dot(point=[-2.4, 1.5, 0], color=WHITE, radius=0.05)
        self.objects["point_A"] = point_A

        # point_B
        point_B = Dot(point=[-2.4, -1.5, 0], color=WHITE, radius=0.05)
        self.objects["point_B"] = point_B

        # green_arc1 - Angle at A between LEFT (along l1) and vector down along t (from A to B)
        # Vector from A to B is (0, -3, 0)
        point_A_center = point_A.get_center()
        green_arc1 = Angle(
            line1=Line(point_A_center, point_A_center + LEFT), 
            line2=Line(point_A_center, point_A_center + DOWN), 
            radius=0.4, 
            other_angle=False, 
            color=GREEN, 
            stroke_width=4
        )
        self.objects["green_arc1"] = green_arc1

        # green_arc2 - Angle at B between vector up along t (from B to A) and LEFT (along l2)
        # Vector from B to A is (0, 3, 0)
        point_B_center = point_B.get_center()
        green_arc2 = Angle(
            line1=Line(point_B_center, point_B_center + UP), 
            line2=Line(point_B_center, point_B_center + LEFT), 
            radius=0.4, 
            other_angle=False, 
            color=GREEN, 
            stroke_width=4
        )
        self.objects["green_arc2"] = green_arc2

        # angle_label1
        angle_label1 = MathTex("\\angle 1", color=GREEN).scale(0.7)
        angle_label1.next_to(green_arc1, UP+LEFT, buff=0.1)
        self.objects["angle_label1"] = angle_label1

        # angle_label2
        angle_label2 = MathTex("\\angle 5", color=GREEN).scale(0.7)
        angle_label2.next_to(green_arc2, DOWN+LEFT, buff=0.1)
        self.objects["angle_label2"] = angle_label2

        # explanation_text (initial empty)
        explanation_text = Text("", color=YELLOW, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["line_l1"]))
        animation_time = 1.0 + 1.0  # Write title + Create line
        remaining = 6.024 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        self.play(Create(self.objects["line_l2"]))
        self.wait(max(0.1, 2.0))

        # Step 3
        self.play(Create(self.objects["line_t"]))
        self.wait(max(0.1, 2.0))

        # Step 4
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            Write(self.objects["label_l1"]),
            Write(self.objects["label_l2"]),
            Write(self.objects["label_t"]),
            Create(self.objects["point_A"]),
            Create(self.objects["point_B"])
        )
        animation_time = 1.0  # estimated for AnimationGroup
        remaining = 3.792 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["green_arc1"]))
        animation_time = 1.0
        remaining = 8.376 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        self.play(Create(self.objects["green_arc2"]))
        self.wait(max(0.1, 2.0))

        # Step 7
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["angle_label1"]))
        animation_time = 1.0
        remaining = 3.576 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 8
        self.play(Write(self.objects["angle_label2"]))
        self.wait(max(0.1, 2.0))

        # Step 9
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # signal_action: Circumscribe both arcs
        self.play(
            Circumscribe(self.objects["green_arc1"], color=YELLOW, run_time=1),
            Circumscribe(self.objects["green_arc2"], color=YELLOW, run_time=1)
        )
        # visual_action: Update explanation text
        new_text = Text("Corresponding Angles Postulate: If lines are parallel, corresponding angles are congruent.", color=YELLOW, font_size=24)
        new_text.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_text))
        self.objects["explanation_text"] = new_text
        animation_time = 1.0 + 1.0  # Circumscribe + ReplacementTransform
        remaining = 8.688 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 10
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_09.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Create a copy of green_arc1 and transform it to green_arc2
        arc_copy = self.objects["green_arc1"].copy()
        self.add(arc_copy)
        self.play(
            Transform(arc_copy, self.objects["green_arc2"]),
            run_time=2
        )
        self.remove(arc_copy)
        animation_time = 2.0
        remaining = 7.776 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 11
        audio_file = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_10.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # signal_action: Indicate green_arc2
        self.play(Indicate(self.objects["green_arc2"], color=GREEN))
        # visual_action: Update explanation text
        final_text = Text("Conclusion: ∠1 ≅ ∠5. Corresponding interior angles are congruent.", color=YELLOW, font_size=24)
        final_text.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], final_text))
        self.objects["explanation_text"] = final_text
        animation_time = 1.0 + 1.0  # Indicate + ReplacementTransform
        remaining = 8.88 - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final pause
        self.wait(max(0.1, 2))