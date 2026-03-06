'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Model solving the linear equation 2x = 6 using a concrete balance scale metaphor. Blue boxes represent 'x', yellow circles represent units. The animation demonstrates the principle of performing the same operation (division by 2) on both sides to maintain equality.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the balance scale, fulcrum, pans, boxes, and circles.
#    - Footer Region: [Bottom y=-3.5] for step explanation and equation.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for left items (boxes) and right items (circles) to manage positioning. The scale is centered. The footer text is kept at the bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow: Show title -> build scale -> add boxes -> add circles -> show equation -> remove items in pairs (box + 3 circles) -> transform equation -> show final solution.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Scale Structure
        fulcrum = Polygon(
            [-0.5, 0, 0],
            [0.5, 0, 0],
            [0, 0.8, 0],
            color=GREY,
            fill_opacity=0.8
        )
        fulcrum.move_to(content_center)
        self.objects["fulcrum"] = fulcrum

        beam = Line(start=[-3, 0.4, 0], end=[3, 0.4, 0], color=GRAY_B, stroke_width=8)
        beam.move_to(content_center + UP * 0.4)
        self.objects["beam"] = beam

        left_pan = Rectangle(height=0.8, width=0.8, color=GRAY_C, fill_opacity=0.3, stroke_width=2)
        left_pan.move_to([-3, -0.5, 0])
        self.objects["left_pan"] = left_pan

        right_pan = Rectangle(height=0.8, width=0.8, color=GRAY_C, fill_opacity=0.3, stroke_width=2)
        right_pan.move_to([3, -0.5, 0])
        self.objects["right_pan"] = right_pan

        # Boxes (left side)
        box1 = Rectangle(height=0.7, width=0.7, color="#1E90FF", fill_opacity=0.8, stroke_width=2)
        box1.move_to(left_pan.get_center() + UP * 0.4)
        self.objects["box1"] = box1

        box1_label = MathTex("x", color=WHITE, font_size=30)
        box1_label.move_to(box1.get_center())
        self.objects["box1_label"] = box1_label

        box2 = Rectangle(height=0.7, width=0.7, color="#1E90FF", fill_opacity=0.8, stroke_width=2)
        box2.move_to(left_pan.get_center() + DOWN * 0.4)
        self.objects["box2"] = box2

        box2_label = MathTex("x", color=WHITE, font_size=30)
        box2_label.move_to(box2.get_center())
        self.objects["box2_label"] = box2_label

        # Circles (right side) - arranged in a 2x3 grid
        circle1 = Circle(radius=0.3, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        circle1.move_to(right_pan.get_center() + LEFT * 0.6 + UP * 0.3)
        self.objects["circle1"] = circle1

        circle2 = Circle(radius=0.3, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        circle2.move_to(right_pan.get_center() + RIGHT * 0.6 + UP * 0.3)
        self.objects["circle2"] = circle2

        circle3 = Circle(radius=0.3, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        circle3.move_to(right_pan.get_center() + LEFT * 0.6 + DOWN * 0.3)
        self.objects["circle3"] = circle3

        circle4 = Circle(radius=0.3, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        circle4.move_to(right_pan.get_center() + RIGHT * 0.6 + DOWN * 0.3)
        self.objects["circle4"] = circle4

        circle5 = Circle(radius=0.3, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        circle5.move_to(right_pan.get_center() + LEFT * 0.0 + UP * 0.3)
        self.objects["circle5"] = circle5

        circle6 = Circle(radius=0.3, color="#FFD700", fill_opacity=0.8, stroke_width=2)
        circle6.move_to(right_pan.get_center() + LEFT * 0.0 + DOWN * 0.3)
        self.objects["circle6"] = circle6

        # Footer text
        step_explanation = Text("Initial Setup: The scale is balanced.", color=GRAY_C, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        equation_display = MathTex("2x = 6", color=WHITE, font_size=36)
        equation_display.next_to(step_explanation, DOWN, buff=0.3)
        self.objects["equation_display"] = equation_display

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_00.mp3")  # [auto-injected] duration=5.98s
        _audio_dur_0 = 5.98  # [audio-sync] actual TTS duration
        # Step 1
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_01.mp3")  # [auto-injected] duration=7.73s
        _audio_dur_1 = 7.73  # [audio-sync] actual TTS duration
        # Step 2
        self.play(
            Create(self.objects["fulcrum"]),
            Create(self.objects["beam"]),
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            run_time=3.0
        )
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_02.mp3")  # [auto-injected] duration=7.06s
        _audio_dur_2 = 7.06  # [audio-sync] actual TTS duration
        # Step 3
        self.play(
            Indicate(self.objects["box1"], color=YELLOW),
            Indicate(self.objects["box2"], color=YELLOW),
            Indicate(self.objects["box1_label"], color=YELLOW),
            Indicate(self.objects["box2_label"], color=YELLOW),
            run_time=1.0
        )
        self.play(
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            Write(self.objects["box1_label"]),
            Write(self.objects["box2_label"]),
            run_time=2.0
        )
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_03.mp3")  # [auto-injected] duration=9.55s
        _audio_dur_3 = 9.55  # [audio-sync] actual TTS duration
        # Step 4
        self.play(
            Indicate(self.objects["circle1"], color=YELLOW),
            Indicate(self.objects["circle2"], color=YELLOW),
            Indicate(self.objects["circle3"], color=YELLOW),
            Indicate(self.objects["circle4"], color=YELLOW),
            Indicate(self.objects["circle5"], color=YELLOW),
            Indicate(self.objects["circle6"], color=YELLOW),
            run_time=1.0
        )
        self.play(
            Create(self.objects["circle1"]),
            Create(self.objects["circle2"]),
            Create(self.objects["circle3"]),
            Create(self.objects["circle4"]),
            Create(self.objects["circle5"]),
            Create(self.objects["circle6"]),
            run_time=2.0
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_04.mp3")  # [auto-injected] duration=8.21s
        _audio_dur_4 = 8.21  # [audio-sync] actual TTS duration
        # Step 5
        self.play(
            Write(self.objects["step_explanation"]),
            Write(self.objects["equation_display"]),
            run_time=3.0
        )
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_05.mp3")  # [auto-injected] duration=8.57s
        _audio_dur_5 = 8.57  # [audio-sync] actual TTS duration
        # Step 6
        self.play(
            Circumscribe(self.objects["box1"], color=RED),
            Circumscribe(self.objects["circle1"], color=RED),
            Circumscribe(self.objects["circle2"], color=RED),
            Circumscribe(self.objects["circle3"], color=RED),
            run_time=1.0
        )
        fade_up_shift = UP * 1.5
        self.play(
            self.objects["box1"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["box1_label"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["circle1"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["circle2"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["circle3"].animate.shift(fade_up_shift).set_opacity(0),
            run_time=3.0
        )
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_06.mp3")  # [auto-injected] duration=7.30s
        _audio_dur_6 = 7.30  # [audio-sync] actual TTS duration
        # Step 7
        self.play(
            Circumscribe(self.objects["box2"], color=RED),
            Circumscribe(self.objects["circle4"], color=RED),
            Circumscribe(self.objects["circle5"], color=RED),
            Circumscribe(self.objects["circle6"], color=RED),
            run_time=1.0
        )
        self.play(
            self.objects["box2"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["box2_label"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["circle4"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["circle5"].animate.shift(fade_up_shift).set_opacity(0),
            self.objects["circle6"].animate.shift(fade_up_shift).set_opacity(0),
            run_time=3.0
        )
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_07.mp3")  # [auto-injected] duration=10.27s
        _audio_dur_7 = 10.27  # [audio-sync] actual TTS duration
        # Step 8
        new_equation = MathTex("x = 3", color=WHITE, font_size=36)
        new_equation.move_to(self.objects["equation_display"].get_center())
        self.play(TransformMatchingTex(self.objects["equation_display"], new_equation), run_time=2.0)
        self.objects["equation_display"] = new_equation
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/To_visualize_the_equ_348feeeee6/step_08.mp3")  # [auto-injected] duration=10.15s
        _audio_dur_8 = 10.15  # [audio-sync] actual TTS duration
        # Step 9
        self.play(Indicate(self.objects["equation_display"], color=GREEN, run_time=1.0))
        final_text = Text("Solution: x = 3", color=GRAY_C, font_size=28)
        final_text.move_to(self.objects["step_explanation"].get_center())
        self.play(ReplacementTransform(self.objects["step_explanation"], final_text), run_time=2.0)
        self.objects["step_explanation"] = final_text
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))