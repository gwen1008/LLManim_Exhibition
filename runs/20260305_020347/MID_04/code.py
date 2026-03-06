'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the theorem that when two parallel lines are cut by a transversal, corresponding angles and alternate interior angles are congruent.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the geometric diagram
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: Place angle labels (equations) to the left and right of the diagram, outside the main construction. Keep explanation text at the bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Draw the three lines (two parallels, one transversal).
#    - Highlight and create corresponding angle arcs (green), then demonstrate congruence via transformation.
#    - Highlight and create alternate interior angle arcs (blue), then show their equality label.
#    - Display final angle equality labels.
'''

from manim import *

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
        title = Text("Parallel Lines and a Transversal", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Lines
        line_top = Line(start=[-3.5, 1, 0], end=[3.5, 1, 0], color=WHITE, stroke_width=4)
        line_top.move_to(diagram_center + UP)
        self.objects["line_top"] = line_top

        line_bottom = Line(start=[-3.5, -1, 0], end=[3.5, -1, 0], color=WHITE, stroke_width=4)
        line_bottom.move_to(diagram_center + DOWN)
        self.objects["line_bottom"] = line_bottom

        line_transversal = Line(start=[-3.5, -1, 0], end=[3.5, 1, 0], color=WHITE, stroke_width=4)
        line_transversal.move_to(diagram_center)
        self.objects["line_transversal"] = line_transversal

        # Angles (will be positioned relative to lines, created but not added yet)
        # Corresponding angles
        angle_corr_top = Angle(line_transversal, line_top, radius=0.4, color=GREEN, stroke_width=6)
        self.objects["angle_corr_top"] = angle_corr_top

        angle_corr_bottom = Angle(line_transversal, line_bottom, radius=0.4, other_angle=True, color=GREEN, stroke_width=6)
        self.objects["angle_corr_bottom"] = angle_corr_bottom

        # Alternate interior angles
        angle_alt_int_top = Angle(line_bottom, line_transversal, radius=0.5, other_angle=True, color=BLUE, stroke_width=6)
        self.objects["angle_alt_int_top"] = angle_alt_int_top

        angle_alt_int_bottom = Angle(line_transversal, line_top, radius=0.5, other_angle=True, color=BLUE, stroke_width=6)
        self.objects["angle_alt_int_bottom"] = angle_alt_int_bottom

        # Angle labels (equations)
        label_corr_eq = MathTex(r"\angle 1 = \angle 2", color=GREEN, font_size=36)
        label_corr_eq.next_to(diagram_center, LEFT, buff=2.0)
        self.objects["label_corr_eq"] = label_corr_eq

        label_alt_eq = MathTex(r"\angle 3 = \angle 4", color=BLUE, font_size=36)
        label_alt_eq.next_to(diagram_center, RIGHT, buff=2.0)
        self.objects["label_alt_eq"] = label_alt_eq

        # Step explanation text (initial content)
        step_explanation = Text("Step 1: Draw two parallel lines and a transversal.", color=YELLOW, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_00.mp3")  # [auto-injected] duration=5.23s
        _audio_dur_0 = 5.23  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # Update explanation text for Step 1
        new_explanation_1 = Text("Step 1: Draw two parallel lines and a transversal.", color=YELLOW, font_size=28)
        new_explanation_1.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_1))
        self.objects["step_explanation"] = new_explanation_1

        self.play(Create(self.objects["line_top"]), run_time=1.0)
        remaining_1b = max(0.1, 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1b))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_03.mp3")  # [auto-injected] duration=7.06s
        _audio_dur_1 = 7.06  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["line_bottom"]), run_time=1.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_04.mp3")  # [auto-injected] duration=3.67s
        _audio_dur_2 = 3.67  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Create(self.objects["line_transversal"]), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_05.mp3")  # [auto-injected] duration=9.22s
        _audio_dur_3 = 9.22  # [audio-sync] actual TTS duration
        # Step 4
        new_explanation_4 = Text("Let's identify a pair of corresponding angles. These are in the same relative position at each intersection.", color=YELLOW, font_size=28)
        new_explanation_4.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4

        self.play(Indicate(self.objects["angle_corr_top"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle_corr_top"]), run_time=1.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_06.mp3")  # [auto-injected] duration=8.14s
        _audio_dur_4 = 8.14  # [audio-sync] actual TTS duration
        # Step 5
        new_explanation_5 = Text("And its corresponding partner on the other parallel line.", color=YELLOW, font_size=28)
        new_explanation_5.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5

        self.play(Indicate(self.objects["angle_corr_bottom"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle_corr_bottom"]), run_time=1.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_07.mp3")  # [auto-injected] duration=2.52s
        _audio_dur_5 = 2.52  # [audio-sync] actual TTS duration
        # Step 6
        new_explanation_6 = Text("Because the lines are parallel, these corresponding angles are congruent. We can imagine sliding one angle down to perfectly match the other.", color=YELLOW, font_size=28)
        new_explanation_6.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_6))
        self.objects["step_explanation"] = new_explanation_6

        # Create a copy of the top angle and transform it to overlay the bottom angle
        angle_copy = self.objects["angle_corr_top"].copy()
        self.play(Transform(angle_copy, self.objects["angle_corr_bottom"]), run_time=2.0)
        self.play(FadeOut(angle_copy))
        self.play(Write(self.objects["label_corr_eq"]), run_time=2.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_08.mp3")  # [auto-injected] duration=8.30s
        _audio_dur_6 = 8.30  # [audio-sync] actual TTS duration
        # Step 7
        new_explanation_7 = Text("Now, let's look at alternate interior angles. These are on opposite sides of the transversal and inside the parallel lines.", color=YELLOW, font_size=28)
        new_explanation_7.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_7))
        self.objects["step_explanation"] = new_explanation_7

        self.play(Circumscribe(self.objects["angle_alt_int_top"], color=BLUE, run_time=1))
        self.play(Create(self.objects["angle_alt_int_top"]), run_time=2.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_parallel_lines__0c7a74c0c9/step_09.mp3")  # [auto-injected] duration=8.21s
        _audio_dur_7 = 8.21  # [audio-sync] actual TTS duration
        # Step 8
        new_explanation_8 = Text("And its alternate interior partner.", color=YELLOW, font_size=28)
        new_explanation_8.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_8))
        self.objects["step_explanation"] = new_explanation_8

        self.play(Circumscribe(self.objects["angle_alt_int_bottom"], color=BLUE, run_time=1))
        self.play(Create(self.objects["angle_alt_int_bottom"]), run_time=1.5)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        # Step 9
        new_explanation_9 = Text("Using what we know about corresponding angles and vertical angles, we can conclude these alternate interior angles are also equal.", color=YELLOW, font_size=28)
        new_explanation_9.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_9))
        self.objects["step_explanation"] = new_explanation_9

        self.play(Write(self.objects["label_alt_eq"]), run_time=2.0)
        remaining_9 = max(0.1, 3.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Step 10
        new_explanation_10 = Text("Thus, for parallel lines cut by a transversal, corresponding angles and alternate interior angles are congruent.", color=YELLOW, font_size=28)
        new_explanation_10.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation_10))
        self.objects["step_explanation"] = new_explanation_10

        self.play(Indicate(self.objects["label_corr_eq"], color=GREEN, run_time=1))
        # label_corr_eq is already written, so we just indicate it
        remaining_10 = max(0.1, 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))