'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Solve the equation 2x = 6 using a concrete balance scale metaphor to visualize equality and the division step.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and initial equation.
#    - Main Content: [Center y=0] for the balance scale and objects.
#    - Footer Region: [Bottom y=-3.5] for step-by-step text narration.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for the scale (fulcrum, beam, pans) and for the circles to manage them as single units. Position the scale at the center, labels to the sides, and text at the bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] I will assign `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step.
# 5. Animation Flow:
#    - Step 1: Show title and equation.
#    - Step 2: Build the scale structure.
#    - Step 3: Add boxes and circles to the pans with labels.
#    - Step 4: Animate the scale balancing.
#    - Step 5: Rearrange circles into two groups (division).
#    - Step 6: Show new labels and transform equation to x = 3.
#    - Step 7: Highlight the final solution.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        scale_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Fulcrum (Triangle)
        fulcrum = Polygon(
            [-0.5, 0, 0],
            [0.5, 0, 0],
            [0, 1, 0],
            color=GREY,
            fill_opacity=0.8
        )
        fulcrum.move_to(scale_anchor)
        self.objects["fulcrum"] = fulcrum

        # Beam
        beam = Line(start=3*LEFT, end=3*RIGHT, color=GRAY_B, stroke_width=8)
        beam.move_to(scale_anchor + UP)
        self.objects["beam"] = beam

        # Left Pan
        left_pan = Square(side_length=1.2, color=GRAY_C, fill_opacity=0.3, stroke_width=2)
        # Position relative to beam after beam is created
        self.objects["left_pan"] = left_pan

        # Right Pan
        right_pan = Square(side_length=1.2, color=GRAY_C, fill_opacity=0.3, stroke_width=2)
        self.objects["right_pan"] = right_pan

        # Box1 (first 'x')
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        self.objects["box1"] = box1

        # Box2 (second 'x')
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        self.objects["box2"] = box2

        # Label 2x
        label_2x = MathTex("2x", color=BLUE)
        self.objects["label_2x"] = label_2x

        # Circles Group (6 circles in a 2x3 grid)
        circles = VGroup(*[Circle(radius=0.3, color=YELLOW, fill_opacity=0.7) for _ in range(6)])
        # Arrange in 2 rows, 3 columns
        circles.arrange_in_grid(rows=2, cols=3, buff=0.2)
        self.objects["circles_group"] = circles

        # Label 6
        label_6 = MathTex("6", color=YELLOW)
        self.objects["label_6"] = label_6

        # Initial Equation
        equation_initial = MathTex("2x = 6", color=WHITE, font_size=40)
        equation_initial.move_to(title_anchor + 0.8 * DOWN)
        self.objects["equation_initial"] = equation_initial

        # Step Explanation (placeholder, content will be updated per step)
        step_explanation = Text("Placeholder for step text.", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Additional objects needed for later steps (from sequence)
        # For step 6: labels 'x' next to circle groups
        label_x1 = MathTex("x", color=BLUE)
        self.objects["label_x1"] = label_x1
        label_x2 = MathTex("x", color=BLUE)
        self.objects["label_x2"] = label_x2

        # For step 6: final equation 'x = 3'
        equation_final = MathTex("x = 3", color=WHITE, font_size=40)
        equation_final.move_to(equation_initial.get_center()) # Place at same spot for transform
        self.objects["equation_final"] = equation_final

        # For step 7: highlight box around final equation
        solution_highlight = SurroundingRectangle(equation_final, color=GREEN, buff=0.2)
        self.objects["solution_highlight"] = solution_highlight

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_00.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1
        # Signal Action
        self.play(Indicate(self.objects["equation_initial"], color=YELLOW, run_time=1))
        # Visual Action
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_01.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        # No signal action
        # Visual Action: Create fulcrum, beam, pans
        # First, position pans relative to beam (which we will create now)
        beam = self.objects["beam"]
        left_pan = self.objects["left_pan"]
        right_pan = self.objects["right_pan"]
        left_pan.move_to(beam.get_start() + 0.6 * DOWN)
        right_pan.move_to(beam.get_end() + 0.6 * DOWN)

        self.play(Create(self.objects["fulcrum"]), run_time=0.5)
        self.play(Create(beam), run_time=0.5)
        self.play(Create(left_pan), Create(right_pan), run_time=0.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        # Signal Action
        self.play(Indicate(left_pan, color=WHITE, run_time=1))
        # Visual Action: Create boxes, circles, and labels
        # Position boxes on left pan
        box1 = self.objects["box1"]
        box2 = self.objects["box2"]
        box1.move_to(left_pan.get_center() + 0.2 * UP)
        box2.move_to(left_pan.get_center() + 0.2 * DOWN)

        # Position circles on right pan
        circles_group = self.objects["circles_group"]
        circles_group.move_to(right_pan.get_center())

        # Position labels
        label_2x = self.objects["label_2x"]
        label_6 = self.objects["label_6"]
        label_2x.next_to(left_pan, LEFT, buff=0.5)
        label_6.next_to(right_pan, RIGHT, buff=0.5)

        self.play(Create(box1), Create(box2), run_time=0.8)
        self.play(Create(circles_group), run_time=0.8)
        self.play(Write(label_2x), Write(label_6), run_time=0.8)
        anim_time_step3 = 0.8 + 0.8 + 0.8 + 1.0 # signal + three animations
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        # Signal Action
        self.play(Circumscribe(self.objects["equation_initial"], color=GREEN, run_time=1))
        # Visual Action: Animate scale balancing
        # Group the scale parts for unified animation
        scale_parts = VGroup(self.objects["fulcrum"], beam, left_pan, right_pan, box1, box2, circles_group, label_2x, label_6)
        # Slight rocking animation
        self.play(scale_parts.animate.rotate(0.1 * DEGREES, about_point=scale_anchor), run_time=0.5)
        self.play(scale_parts.animate.rotate(-0.2 * DEGREES, about_point=scale_anchor), run_time=0.5)
        self.play(scale_parts.animate.rotate(0.1 * DEGREES, about_point=scale_anchor), run_time=0.5)
        anim_time_step4 = 1.0 + 1.5 # signal + three rotate animations
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        # Signal Action
        self.play(Indicate(label_2x, color=RED, run_time=1))
        # Visual Action: Rearrange circles into two groups
        circles_group = self.objects["circles_group"]
        # Target positions: two columns of three circles each, spaced apart
        left_group_pos = right_pan.get_center() + 1.5 * LEFT
        right_group_pos = right_pan.get_center() + 1.5 * RIGHT

        # Create two new VGroups for the arrangement
        circles_list = list(circles_group)
        left_circles = VGroup(*circles_list[:3])
        right_circles = VGroup(*circles_list[3:])
        left_circles.arrange(DOWN, buff=0.4)
        right_circles.arrange(DOWN, buff=0.4)
        left_circles.move_to(left_group_pos)
        right_circles.move_to(right_group_pos)

        # Animate the transformation
        self.play(
            circles_list[0].animate.move_to(left_circles[0].get_center()),
            circles_list[1].animate.move_to(left_circles[1].get_center()),
            circles_list[2].animate.move_to(left_circles[2].get_center()),
            circles_list[3].animate.move_to(right_circles[0].get_center()),
            circles_list[4].animate.move_to(right_circles[1].get_center()),
            circles_list[5].animate.move_to(right_circles[2].get_center()),
            run_time=2.0, lag_ratio=0.2
        )
        anim_time_step5 = 1.0 + 2.0
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_05.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_5 = 2.00  # [audio-sync] actual TTS duration
        # Step 6
        # Signal Action
        self.play(Indicate(box1, color=BLUE, run_time=1))
        # Visual Action: Create 'x' labels and transform equation
        # Position 'x' labels next to each circle group
        label_x1 = self.objects["label_x1"]
        label_x2 = self.objects["label_x2"]
        label_x1.next_to(left_circles, LEFT, buff=0.5)
        label_x2.next_to(right_circles, RIGHT, buff=0.5)

        self.play(Write(label_x1), Write(label_x2), run_time=1.0)

        # Transform equation
        self.play(
            ReplacementTransform(self.objects["equation_initial"], self.objects["equation_final"]),
            run_time=1.5
        )
        anim_time_step6 = 1.0 + 1.0 + 1.5
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        # [missing audio] self.add_sound("media/audio/To_visualize_the_equ_64ed04f61e/step_06.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_6 = 2.00  # [audio-sync] actual TTS duration
        # Step 7
        # Signal Action
        self.play(Circumscribe(self.objects["equation_final"], color=GREEN, run_time=1))
        # Visual Action: Highlight final equation
        self.play(Create(self.objects["solution_highlight"]), run_time=1.5)
        anim_time_step7 = 1.0 + 1.5
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        # Final hold
        self.wait(max(0.1, 2))