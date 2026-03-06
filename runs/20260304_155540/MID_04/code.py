'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between same-side interior angles when a transversal crosses parallel lines, correcting the misconception that they are equal by proving they are supplementary.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for the parallel lines and transversal diagram
#    - Footer Region: [Bottom y=-3.0] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Keep diagram centered. Use VGroups for related objects (lines+labels, angles+labels). Position explanation text at the bottom with sufficient buff.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Phase 1: Draw the three lines (L1, L2, T) and label them.
#    - Phase 2: Highlight the two same-side interior angles (∠4, ∠5) in green.
#    - Phase 3: Introduce the corresponding angle ∠1 (red) and the equality ∠1 = ∠5.
#    - Phase 4: Show ∠4 and ∠1 are a linear pair (supplementary).
#    - Phase 5: Substitute ∠5 for ∠1 to conclude ∠4 + ∠5 = 180°.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        title_anchor = 3.0 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.0 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Same-Side Interior Angles & Parallel Lines", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Lines
        line_l1 = Line(start=[-3, 0.5, 0], end=[3, 0.5, 0], color=BLUE, stroke_width=4)
        line_l1.move_to(diagram_center)
        self.objects["line_l1"] = line_l1

        line_l2 = Line(start=[-3, -0.5, 0], end=[3, -0.5, 0], color=BLUE, stroke_width=4)
        line_l2.move_to(diagram_center + DOWN * 1.0)
        self.objects["line_l2"] = line_l2

        line_t = Line(start=[-4, 1.0, 0], end=[4, -1.0, 0], color=YELLOW, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t

        # Line labels
        label_l1 = MathTex("L_1", color=BLUE, font_size=24)
        label_l1.next_to(line_l1.get_end(), RIGHT, buff=0.1)
        self.objects["label_l1"] = label_l1

        label_l2 = MathTex("L_2", color=BLUE, font_size=24)
        label_l2.next_to(line_l2.get_end(), RIGHT, buff=0.1)
        self.objects["label_l2"] = label_l2

        label_t = MathTex("T", color=YELLOW, font_size=24)
        label_t.next_to(line_t.get_end(), RIGHT + DOWN, buff=0.1)
        self.objects["label_t"] = label_t

        # Angles (will be positioned after lines are created)
        # Angle 4 (between transversal and L1, on the right side)
        angle_4 = Angle(line_t, line_l1, radius=0.4, color=GREEN, stroke_width=3)
        angle_4.set_fill(opacity=0.0)
        self.objects["angle_4"] = angle_4

        # Angle 5 (between L2 and transversal, on the right side)
        angle_5 = Angle(line_l2, line_t, radius=0.4, color=GREEN, stroke_width=3)
        angle_5.set_fill(opacity=0.0)
        self.objects["angle_5"] = angle_5

        # Angle labels
        label_angle_4 = MathTex("4", color=WHITE, font_size=20)
        # Position near the angle using next_to instead of arc_center
        label_angle_4.next_to(angle_4, UR, buff=0.1)
        self.objects["label_angle_4"] = label_angle_4

        label_angle_5 = MathTex("5", color=WHITE, font_size=20)
        label_angle_5.next_to(angle_5, UR, buff=0.1)
        self.objects["label_angle_5"] = label_angle_5

        # Corresponding angle ∠1 (other_angle=True to get the angle on the other side of the transversal at intersection P)
        angle_1 = Angle(line_l1, line_t, radius=0.5, other_angle=True, color=RED, stroke_width=3)
        angle_1.set_fill(opacity=0.0)
        self.objects["angle_1"] = angle_1

        label_angle_1 = MathTex("1", color=WHITE, font_size=20)
        label_angle_1.next_to(angle_1, UL, buff=0.1)
        self.objects["label_angle_1"] = label_angle_1

        # Explanation text (initial)
        explanation_text = Text("Step 1: Draw two parallel lines and a transversal.", color=WHITE, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # Equation for ∠1 = ∠5 (will be created later)
        eq_angle1_eq_angle5 = MathTex(r"\angle 1 = \angle 5", color=WHITE, font_size=28)
        eq_angle1_eq_angle5.next_to(explanation_text, UP, buff=0.5)
        self.objects["eq_angle1_eq_angle5"] = eq_angle1_eq_angle5

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_00.mp3")  # [auto-injected] duration=7.58s
        _audio_dur_0 = 7.58  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["line_l1"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_01.mp3")  # [auto-injected] duration=3.74s
        _audio_dur_1 = 3.74  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["line_l2"]), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_02.mp3")  # [auto-injected] duration=5.33s
        _audio_dur_2 = 5.33  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Create(self.objects["line_t"]), run_time=2.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_03.mp3")  # [auto-injected] duration=3.98s
        _audio_dur_3 = 3.98  # [audio-sync] actual TTS duration
        # Step 4
        self.play(
            Write(self.objects["label_l1"]),
            Write(self.objects["label_l2"]),
            Write(self.objects["label_t"]),
            run_time=2.0
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_04.mp3")  # [auto-injected] duration=7.46s
        _audio_dur_4 = 7.46  # [audio-sync] actual TTS duration
        # Step 5
        # Signal action: Indicate angle_4
        self.play(Indicate(self.objects["angle_4"], color=GREEN, run_time=1))
        # Visual action: Create angle_4 and its label, set fill opacity
        self.objects["angle_4"].set_fill(opacity=0.3)
        self.play(
            Create(self.objects["angle_4"]),
            Write(self.objects["label_angle_4"]),
            run_time=1.5
        )
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_05.mp3")  # [auto-injected] duration=6.34s
        _audio_dur_5 = 6.34  # [audio-sync] actual TTS duration
        # Step 6
        # Signal action: Indicate angle_5
        self.play(Indicate(self.objects["angle_5"], color=GREEN, run_time=1))
        # Visual action: Create angle_5 and its label, set fill opacity
        self.objects["angle_5"].set_fill(opacity=0.3)
        self.play(
            Create(self.objects["angle_5"]),
            Write(self.objects["label_angle_5"]),
            run_time=1.5
        )
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_06.mp3")  # [auto-injected] duration=11.93s
        _audio_dur_6 = 11.93  # [audio-sync] actual TTS duration
        # Step 7
        # Update explanation text
        new_explanation_7 = Text("Step 2: Identify corresponding angles.", color=WHITE, font_size=28)
        new_explanation_7.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_7), run_time=1.5)
        self.objects["explanation_text"] = new_explanation_7
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_07.mp3")  # [auto-injected] duration=11.45s
        _audio_dur_7 = 11.45  # [audio-sync] actual TTS duration
        # Step 8
        # Signal action: Circumscribe angle_1
        self.play(Circumscribe(self.objects["angle_1"], color=YELLOW, run_time=1))
        # Visual action: Create angle_1 and its label
        self.play(
            Create(self.objects["angle_1"]),
            Write(self.objects["label_angle_1"]),
            run_time=2.0
        )
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_08.mp3")  # [auto-injected] duration=5.69s
        _audio_dur_8 = 5.69  # [audio-sync] actual TTS duration
        # Step 9
        # Signal action: Indicate label_angle_1
        self.play(Indicate(self.objects["label_angle_1"], color=RED, run_time=1))
        # Visual action: Write equation ∠1 = ∠5
        self.play(Write(self.objects["eq_angle1_eq_angle5"]), run_time=2.0)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_09.mp3")  # [auto-injected] duration=8.62s
        _audio_dur_9 = 8.62  # [audio-sync] actual TTS duration
        # Step 10
        # Signal action: Circumscribe angle_4
        self.play(Circumscribe(self.objects["angle_4"], color=YELLOW, run_time=1))
        # Visual action: Indicate angle_1
        self.play(Indicate(self.objects["angle_1"], color=RED, run_time=1.5))
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_10.mp3")  # [auto-injected] duration=11.35s
        _audio_dur_10 = 11.35  # [audio-sync] actual TTS duration
        # Step 11
        # Update explanation text
        new_explanation_11 = Text("Step 3: ∠4 and ∠1 are a linear pair: ∠4 + ∠1 = 180°", color=WHITE, font_size=28)
        new_explanation_11.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_11), run_time=2.0)
        self.objects["explanation_text"] = new_explanation_11
        remaining_11 = _audio_dur_10  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_11))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_11.mp3")  # [auto-injected] duration=8.95s
        _audio_dur_11 = 8.95  # [audio-sync] actual TTS duration
        # Step 12
        # Signal action: TransformMatchingTex on equation_1 (we'll use the explanation text)
        # Visual action: Morph the equation in explanation text
        new_explanation_12 = Text("Step 3: ∠4 and ∠5 are a linear pair: ∠4 + ∠5 = 180°", color=WHITE, font_size=28)
        new_explanation_12.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation_12), run_time=2.0)
        self.objects["explanation_text"] = new_explanation_12
        remaining_12 = _audio_dur_11  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_12))

        self.add_sound("media/audio/Draw_two_parallel_li_424db85fc7/step_12.mp3")  # [auto-injected] duration=12.72s
        _audio_dur_12 = 12.72  # [audio-sync] actual TTS duration
        # Step 13
        # Signal action: Circumscribe angle_4
        self.play(Circumscribe(self.objects["angle_4"], color=GREEN, run_time=1))
        # Visual action: Update final explanation text
        final_explanation = Text("Conclusion: Same-side interior angles are supplementary (sum to 180°), not equal.", color=WHITE, font_size=28)
        final_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], final_explanation), run_time=2.5)
        self.objects["explanation_text"] = final_explanation
        remaining_13 = _audio_dur_12  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_13))

        # Final hold
        self.wait(max(0.1, 2))