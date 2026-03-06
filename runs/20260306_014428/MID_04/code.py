'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the Corresponding Angles Theorem using a geometric diagram with parallel lines and a transversal.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the parallel lines and transversal diagram
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for angle arcs and labels to keep them together. Position explanation text at the bottom, replacing content to avoid clutter.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Draw the three lines (l1, l2, t) and label them.
#    - Show explanation text.
#    - Create and highlight angle 1 and angle 5 arcs and labels.
#    - Update explanation text.
#    - Animate the translation of angle 1 to overlap angle 5 to demonstrate congruence.
#    - Show final conclusion.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Corresponding Angles Theorem", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Lines
        line_l1 = Line(start=[-4, 1.5, 0], end=[4, 1.5, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center + UP * 1.5)
        self.objects["line_l1"] = line_l1

        line_l2 = Line(start=[-4, -1.5, 0], end=[4, -1.5, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN * 1.5)
        self.objects["line_l2"] = line_l2

        line_t = Line(start=[-3, -2.5, 0], end=[3, 2.5, 0], color=RED, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t

        # Line Labels
        label_l1 = MathTex("l_1", color=BLUE, font_size=30)
        label_l1.next_to(line_l1.get_end(), RIGHT, buff=0.2)
        self.objects["label_l1"] = label_l1

        label_l2 = MathTex("l_2", color=BLUE, font_size=30)
        label_l2.next_to(line_l2.get_end(), RIGHT, buff=0.2)
        self.objects["label_l2"] = label_l2

        label_t = MathTex("t", color=RED, font_size=30)
        label_t.next_to(line_t.get_end(), UP + RIGHT, buff=0.2)
        self.objects["label_t"] = label_t

        # Calculate intersection points for angle arcs
        import numpy as np
        # Intersection A: line_t and line_l1
        def line_intersection(line1, line2):
            p1, p2 = line1.get_start_and_end()
            p3, p4 = line2.get_start_and_end()
            
            x1, y1, _ = p1
            x2, y2, _ = p2
            x3, y3, _ = p3
            x4, y4, _ = p4
            
            denom = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
            if abs(denom) < 1e-9:
                return None
            
            px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denom
            py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denom
            return np.array([px, py, 0])
        
        inter_A = line_intersection(line_t, line_l1)
        # Intersection B: line_t and line_l2
        inter_B = line_intersection(line_t, line_l2)

        # Angle 1 arc and label
        angle_1_arc = Arc(
            radius=0.4,
            start_angle=line_t.get_angle(),
            angle=PI - line_t.get_angle(),
            color=WHITE,
            stroke_width=3
        )
        angle_1_arc.move_to(inter_A)
        self.objects["angle_1_arc"] = angle_1_arc

        angle_1_label = MathTex("1", color=WHITE, font_size=24)
        angle_1_label.scale(0.6)
        # Position label relative to arc center
        angle_1_label.next_to(angle_1_arc.get_center(), UR, buff=0.1)
        self.objects["angle_1_label"] = angle_1_label

        # Angle 5 arc and label
        angle_5_arc = Arc(
            radius=0.4,
            start_angle=line_t.get_angle() - PI,
            angle=PI - line_t.get_angle(),
            color=WHITE,
            stroke_width=3
        )
        angle_5_arc.move_to(inter_B)
        self.objects["angle_5_arc"] = angle_5_arc

        angle_5_label = MathTex("5", color=WHITE, font_size=24)
        angle_5_label.scale(0.6)
        angle_5_label.next_to(angle_5_arc.get_center(), UR, buff=0.1)
        self.objects["angle_5_label"] = angle_5_label

        # Step explanation text (initial placeholder)
        step_explanation = Text("Placeholder for step-by-step narration.", font_size=24, color=YELLOW)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Create VGroups for angles (for step 9 animation)
        angle_1_group = VGroup(angle_1_arc, angle_1_label)
        self.objects["angle_1_group"] = angle_1_group
        angle_5_group = VGroup(angle_5_arc, angle_5_label)
        self.objects["angle_5_group"] = angle_5_group

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # [missing audio] self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_00.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # [missing audio] self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["line_l1"]), run_time=1.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        # [missing audio] self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Create(self.objects["line_l2"]), run_time=1.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        # [missing audio] self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_05.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Create(self.objects["line_t"]), run_time=1.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        # [missing audio] self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_07.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        self.play(
            Write(self.objects["label_l1"]),
            Write(self.objects["label_l2"]),
            Write(self.objects["label_t"]),
            run_time=2.5
        )
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_08.mp3")  # [auto-injected] duration=13.68s
        _audio_dur_5 = 13.68  # [audio-sync] actual TTS duration
        # Step 6: Update explanation and signal
        new_explanation_1 = Text("Angles between the parallel lines are interior angles.", font_size=24, color=YELLOW)
        new_explanation_1.move_to(explanation_anchor)
        self.play(Circumscribe(self.objects["step_explanation"], color=YELLOW, run_time=1))
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_1))
        self.objects["step_explanation"] = new_explanation_1
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration  # Signal run_time=1, transform ~0.5
        self.wait(max(0.1, remaining_6))

        # [missing audio] self.add_sound("media/audio/Draw_two_parallel_li_65f764498b/step_09.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_6 = 2.00  # [audio-sync] actual TTS duration
        # Step 7: Create and highlight angle 1
        self.play(Indicate(self.objects["angle_1_arc"], color=GREEN, run_time=1))
        self.play(
            Create(self.objects["angle_1_arc"]),
            Write(self.objects["angle_1_label"]),
            run_time=2.0
        )
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        # Step 8: Create and highlight angle 5
        self.play(Indicate(self.objects["angle_5_arc"], color=GREEN, run_time=1))
        self.play(
            Create(self.objects["angle_5_arc"]),
            Write(self.objects["angle_5_label"]),
            run_time=2.0
        )
        remaining_8 = max(0.1, 2.0 - (1.0 + 2.0) + 0.5)
        self.wait(max(0.1, remaining_8))

        # Step 9: Update explanation
        new_explanation_2 = Text("Corresponding angles (like ∠1 and ∠5) are equal when lines are parallel.", font_size=24, color=YELLOW)
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        remaining_9 = max(0.1, 3.5 - 0.5 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10: Animate translation of angle 1 to angle 5
        # Create a copy of angle_1_group for the animation
        moving_group = self.objects["angle_1_group"].copy()
        moving_group.set_color(GREEN)
        self.add(moving_group)

        # Calculate translation vector from inter_A to inter_B
        translation_vector = inter_B - inter_A
        self.play(
            moving_group.animate.shift(translation_vector),
            run_time=3.0
        )
        # After translation, change angle 5 group to green to match
        self.play(
            self.objects["angle_5_arc"].animate.set_color(GREEN),
            self.objects["angle_5_label"].animate.set_color(GREEN),
            run_time=1.0
        )
        self.remove(moving_group)
        remaining_10 = max(0.1, 4.0 - (3.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_10))

        # Step 11: Final conclusion with signal
        self.play(Indicate(self.objects["angle_5_arc"], color=GREEN, run_time=1))
        new_explanation_3 = Text("Conclusion: Corresponding angles are equal. ∠1 ≅ ∠5.", font_size=24, color=YELLOW)
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        remaining_11 = max(0.1, 3.0 - (1.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_11))

        # Final hold
        self.wait(max(0.1, 2))