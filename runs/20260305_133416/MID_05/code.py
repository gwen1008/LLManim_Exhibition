'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually prove the relationship between a circle's circumference (C) and its diameter (D), showing C = πD and that π is approximately 3.14, meaning the circumference is slightly more than three times the diameter.
# 2. Layout Strategy: High-Low Split.
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] Left side for circle, right side for unfolded line and measurement.
#    - Footer Region: [Bottom y=-2.8] for final equation.
# 3. Anti-Overlap Check: Objects are positioned left and right of center. The circle is at LEFT*3, the unfolded line starts near the circle and extends to the right. Diameter copies are placed end-to-end on the line. All text labels are placed with buff to avoid collisions.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] I will assign `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step.
# 5. Animation Flow: Show circle → highlight diameter → label D → transform circle perimeter into a straight line (circumference) → measure the line using three copies of the diameter → show the leftover remainder → label the remainder → display final equation C = πD ≈ 3.14D > 3D.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        global_center = ORIGIN
        title_anchor = 3.0 * UP
        explanation_anchor = 2.8 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Unfolding a Circle's Circumference", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Circle (D=4, radius=2)
        circle = Circle(radius=2, color=BLUE, stroke_width=4)
        circle.move_to(global_center + 3 * LEFT)
        self.objects["circle"] = circle

        # Diameter Line (defined relative to circle)
        diameter_line = Line(
            start=circle.get_left(),
            end=circle.get_right(),
            color=YELLOW,
            stroke_width=6
        )
        self.objects["diameter_line"] = diameter_line

        # Label D
        label_d = MathTex("D", color=YELLOW)
        label_d.next_to(diameter_line, UP, buff=0.2)
        self.objects["label_d"] = label_d

        # Unfolded Line (Circumference C = π*4 ≈ 12.566)
        # Start near the circle's center for transformation, final position extends right.
        unfolded_line_start = np.array([-3, 0, 0])
        unfolded_line_end = np.array([9.566, 0, 0])  # 12.566 total length from start
        unfolded_line = Line(
            start=unfolded_line_start,
            end=unfolded_line_end,
            color=GREEN,
            stroke_width=4
        )
        # Position it initially at the circle's center for the morph
        unfolded_line.move_to(circle.get_center())
        self.objects["unfolded_line"] = unfolded_line

        # Diameter copies for measuring (each length = 4)
        # They will be created at the circle initially and moved/transformed.
        diameter_copy_1 = Line(
            start=unfolded_line.get_start(),
            end=unfolded_line.get_start() + 4 * RIGHT,
            color=YELLOW,
            stroke_width=4
        )
        diameter_copy_1.move_to(diameter_line.get_center())  # Start at original diameter
        self.objects["diameter_copy_1"] = diameter_copy_1

        diameter_copy_2 = Line(
            start=diameter_copy_1.get_end(),
            end=diameter_copy_1.get_end() + 4 * RIGHT,
            color=YELLOW,
            stroke_width=4
        )
        diameter_copy_2.move_to(diameter_line.get_center())
        self.objects["diameter_copy_2"] = diameter_copy_2

        diameter_copy_3 = Line(
            start=diameter_copy_2.get_end(),
            end=diameter_copy_2.get_end() + 4 * RIGHT,
            color=YELLOW,
            stroke_width=4
        )
        diameter_copy_3.move_to(diameter_line.get_center())
        self.objects["diameter_copy_3"] = diameter_copy_3

        # Label for measuring diameters
        label_d_measuring = MathTex("D", color=YELLOW)
        # Position will be set relative to diameter_copy_2 later
        self.objects["label_d_measuring"] = label_d_measuring

        # Remainder segment
        remainder_segment = Line(
            start=diameter_copy_3.get_end(),
            end=unfolded_line.get_end(),
            color=RED,
            stroke_width=6
        )
        self.objects["remainder_segment"] = remainder_segment

        # Label for remainder
        label_remainder = MathTex(r"(\pi - 3)D \approx 0.14D", color=RED)
        # Position will be set relative to remainder_segment later
        self.objects["label_remainder"] = label_remainder

        # Final equation
        final_equation = MathTex(r"C = \pi D \approx 3.14 D > 3D", color=WHITE, font_size=36)
        final_equation.move_to(explanation_anchor)
        self.objects["final_equation"] = final_equation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_00.mp3")  # [auto-injected] duration=6.12s
        _audio_dur_0 = 6.12  # [audio-sync] actual TTS duration
        # Step 1: Draw the circle
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.play(Create(self.objects["circle"]), run_time=2.0)
        remaining_1b = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1b))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_01.mp3")  # [auto-injected] duration=2.04s
        _audio_dur_1 = 2.04  # [audio-sync] actual TTS duration
        # Step 2: Highlight and draw diameter
        # Signal action: Indicate diameter_line (but it doesn't exist yet, so we indicate the circle's horizontal axis?)
        # We'll create the diameter line first, then indicate it.
        self.play(Create(self.objects["diameter_line"]), run_time=1.5)
        self.play(Indicate(self.objects["diameter_line"], color=YELLOW, run_time=1))
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_02.mp3")  # [auto-injected] duration=1.73s
        _audio_dur_2 = 1.73  # [audio-sync] actual TTS duration
        # Step 3: Label D
        self.play(Write(self.objects["label_d"]), run_time=1.5)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_03.mp3")  # [auto-injected] duration=7.22s
        _audio_dur_3 = 7.22  # [audio-sync] actual TTS duration
        # Step 4: Transform circle perimeter into unfolded line
        # Signal: Circumscribe circle in GREEN
        self.play(Circumscribe(self.objects["circle"], color=GREEN, run_time=1))
        # For a clean morph, we create a copy of the circle's perimeter (just the stroke)
        circle_perimeter = self.objects["circle"].copy()
        circle_perimeter.set_color(GREEN).set_stroke(width=4)
        # The unfolded_line is already created at the circle's center.
        # We'll transform the perimeter copy into the final unfolded line position.
        # First, add the perimeter copy to the scene.
        self.add(circle_perimeter)
        # We'll also fade out the original circle's stroke, leaving the diameter.
        self.objects["circle"].set_stroke(opacity=0)
        # Transform the perimeter copy to the unfolded line.
        self.play(Transform(circle_perimeter, self.objects["unfolded_line"]), run_time=3.0)
        # Remove the temporary perimeter copy, add the final unfolded_line
        self.remove(circle_perimeter)
        self.add(self.objects["unfolded_line"])
        # Restore the circle's stroke? The plan says to leave the diameter. We'll keep circle invisible.
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_04.mp3")  # [auto-injected] duration=8.81s
        _audio_dur_4 = 8.81  # [audio-sync] actual TTS duration
        # Step 5: Indicate unfolded line and prepare measuring label
        self.play(Indicate(self.objects["unfolded_line"], color=GREEN, run_time=1))
        # Position the measuring label
        self.objects["label_d_measuring"].next_to(self.objects["diameter_copy_2"], UP, buff=0.2)
        self.play(FadeIn(self.objects["label_d_measuring"]), run_time=1.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_05.mp3")  # [auto-injected] duration=2.54s
        _audio_dur_5 = 2.54  # [audio-sync] actual TTS duration
        # Step 6: Transform original diameter to first copy on the line
        # Move diameter_copy_1 to its final start position (aligned with unfolded_line start)
        self.objects["diameter_copy_1"].move_to(self.objects["unfolded_line"].get_start() + 2 * RIGHT) # center of segment
        self.play(Transform(self.objects["diameter_line"], self.objects["diameter_copy_1"]), run_time=2.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_06.mp3")  # [auto-injected] duration=1.80s
        _audio_dur_6 = 1.80  # [audio-sync] actual TTS duration
        # Step 7: Draw second diameter copy
        self.objects["diameter_copy_2"].move_to(self.objects["diameter_copy_1"].get_end() + 2 * RIGHT) # center
        self.play(Create(self.objects["diameter_copy_2"]), run_time=2.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_07.mp3")  # [auto-injected] duration=1.92s
        _audio_dur_7 = 1.92  # [audio-sync] actual TTS duration
        # Step 8: Draw third diameter copy
        self.objects["diameter_copy_3"].move_to(self.objects["diameter_copy_2"].get_end() + 2 * RIGHT) # center
        self.play(Create(self.objects["diameter_copy_3"]), run_time=2.0)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_08.mp3")  # [auto-injected] duration=7.75s
        _audio_dur_8 = 7.75  # [audio-sync] actual TTS duration
        # Step 9: Indicate and draw remainder segment
        self.play(Indicate(self.objects["remainder_segment"], color=RED, run_time=1))
        self.play(Create(self.objects["remainder_segment"]), run_time=2.0)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_09.mp3")  # [auto-injected] duration=10.44s
        _audio_dur_9 = 10.44  # [audio-sync] actual TTS duration
        # Step 10: Label remainder
        self.objects["label_remainder"].next_to(self.objects["remainder_segment"], UP, buff=0.2)
        self.play(Write(self.objects["label_remainder"]), run_time=2.5)
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/Present_a_circle_wit_267be8e770/step_10.mp3")  # [auto-injected] duration=15.89s
        _audio_dur_10 = 15.89  # [audio-sync] actual TTS duration
        # Step 11: Display final equation
        self.play(Write(self.objects["final_equation"]), run_time=3.0)
        remaining_11 = _audio_dur_10  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_11))

        # Final hold
        self.wait(max(0.1, 2))