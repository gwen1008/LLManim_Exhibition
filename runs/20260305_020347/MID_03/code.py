'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Use a concrete balance scale model to visualize solving the equation 2x = 6. The scale represents equality, and removing half the items from each side visually demonstrates dividing both sides by 2.
# 2. Layout Strategy:
#    - Header Region: [y=3.2] for Title
#    - Main Content: [Center y=0] for the balance scale and equation display
#    - Footer Region: [Bottom y=-2.8] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - The scale is centered at origin. Equation display is placed at UP*2.0, well above the scale's beam.
#    - Explanation text is at DOWN*2.8, below the pans.
#    - Use VGroups for boxes and circles to manage them collectively.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] I have assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step.
# 5. Animation Flow:
#    - Build the scale structure (fulcrum, beam, pans, connectors).
#    - Populate left pan with two 'x' boxes and right pan with six circles.
#    - Show equation 2x = 6.
#    - Update explanation text.
#    - Animate removal of one box and three circles (dividing by 2).
#    - Transform equation to x = 3 and update final explanation.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors from layout_plan
        title_anchor = UP * 3.2
        scale_anchor = ORIGIN
        explanation_anchor = DOWN * 2.8

        # Create objects from layout_plan.objects
        # Title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Fulcrum (Triangle)
        fulcrum = Triangle(color=GREY, fill_opacity=1.0)
        fulcrum.scale(0.5)  # Triangle has no height/width params, use scale
        fulcrum.move_to(scale_anchor + DOWN * 0.5)
        self.objects["fulcrum"] = fulcrum

        # Beam
        beam = Line(start=LEFT * 4, end=RIGHT * 4, color=GRAY_B, stroke_width=8)
        beam.move_to(scale_anchor)
        self.objects["beam"] = beam

        # Left Pan
        left_pan = Rectangle(width=2.5, height=0.3, color=GREY, fill_opacity=0.7)
        left_pan.move_to(scale_anchor + LEFT * 4 + DOWN * 2)
        self.objects["left_pan"] = left_pan

        # Right Pan
        right_pan = Rectangle(width=2.5, height=0.3, color=GREY, fill_opacity=0.7)
        right_pan.move_to(scale_anchor + RIGHT * 4 + DOWN * 2)
        self.objects["right_pan"] = right_pan

        # Left Connector (Line from beam end to left pan top)
        left_connector = Line(
            start=scale_anchor + LEFT * 4,
            end=left_pan.get_top(),
            color=GREY,
            stroke_width=4
        )
        self.objects["left_connector"] = left_connector

        # Right Connector
        right_connector = Line(
            start=scale_anchor + RIGHT * 4,
            end=right_pan.get_top(),
            color=GREY,
            stroke_width=4
        )
        self.objects["right_connector"] = right_connector

        # Boxes Group (VGroup, initially empty, will be populated)
        boxes_group = VGroup()
        boxes_group.move_to(left_pan.get_center())
        self.objects["boxes_group"] = boxes_group

        # Circles Group (VGroup, initially empty)
        circles_group = VGroup()
        circles_group.move_to(right_pan.get_center())
        self.objects["circles_group"] = circles_group

        # Equation Display
        eq_display = MathTex("2x = 6", color=YELLOW, font_size=48)
        eq_display.move_to(scale_anchor + UP * 2.0)
        self.objects["eq_display"] = eq_display

        # Explanation Text
        explanation_text = Text("We start with the equation 2x = 6.", color=GRAY_C, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_00.mp3")  # [auto-injected] duration=5.54s
        _audio_dur_0 = 5.54  # [audio-sync] actual TTS duration
        # Step 1
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_01.mp3")  # [auto-injected] duration=4.18s
        _audio_dur_1 = 4.18  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["fulcrum"]), run_time=1.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_02.mp3")  # [auto-injected] duration=2.23s
        _audio_dur_2 = 2.23  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Create(self.objects["beam"]), run_time=1.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_03.mp3")  # [auto-injected] duration=2.33s
        _audio_dur_3 = 2.33  # [audio-sync] actual TTS duration
        # Step 4
        self.play(
            Create(self.objects["left_pan"]),
            Create(self.objects["right_pan"]),
            Create(self.objects["left_connector"]),
            Create(self.objects["right_connector"]),
            run_time=2.0
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_04.mp3")  # [auto-injected] duration=7.27s
        _audio_dur_4 = 7.27  # [audio-sync] actual TTS duration
        # Step 5
        # Signal Action: Indicate left_pan
        self.play(Indicate(self.objects["left_pan"], color=BLUE, run_time=1))
        # Visual Action: Populate boxes_group with two blue squares labeled 'x'
        box1 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        label1 = MathTex("x", color=WHITE, font_size=36)
        box1_group = VGroup(box1, label1)
        box2 = Square(side_length=0.8, color=BLUE, fill_opacity=0.7)
        label2 = MathTex("x", color=WHITE, font_size=36)
        box2_group = VGroup(box2, label2)
        # Stack vertically within left pan
        boxes_group = VGroup(box1_group, box2_group)
        boxes_group.arrange(DOWN, buff=0.2)
        boxes_group.move_to(self.objects["left_pan"].get_center())
        self.objects["boxes_group"] = boxes_group
        self.play(FadeIn(boxes_group), run_time=1.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_05.mp3")  # [auto-injected] duration=6.07s
        _audio_dur_5 = 6.07  # [audio-sync] actual TTS duration
        # Step 6
        # Signal Action: Indicate right_pan
        self.play(Indicate(self.objects["right_pan"], color=ORANGE, run_time=1))
        # Visual Action: Populate circles_group with six orange circles
        circles = []
        for i in range(6):
            circle = Circle(radius=0.4, color=ORANGE, fill_opacity=0.7)
            circles.append(circle)
        circles_group = VGroup(*circles)
        # Arrange in 2 rows of 3
        circles_group.arrange_in_grid(rows=2, cols=3, buff=0.3)
        circles_group.move_to(self.objects["right_pan"].get_center())
        self.objects["circles_group"] = circles_group
        self.play(FadeIn(circles_group), run_time=1.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_06.mp3")  # [auto-injected] duration=8.06s
        _audio_dur_6 = 8.06  # [audio-sync] actual TTS duration
        # Step 7
        # Signal Action: Circumscribe eq_display
        self.play(Circumscribe(self.objects["eq_display"], color=YELLOW, run_time=1))
        # Visual Action: Write eq_display
        self.play(Write(self.objects["eq_display"]), run_time=1.5)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_07.mp3")  # [auto-injected] duration=6.67s
        _audio_dur_7 = 6.67  # [audio-sync] actual TTS duration
        # Step 8
        # Signal Action: Indicate explanation_text
        self.play(Indicate(self.objects["explanation_text"], color=WHITE, run_time=1))
        # Visual Action: ReplacementTransform explanation text
        new_explanation = Text("To solve for x, we divide both sides by 2.", color=GRAY_C, font_size=28)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation), run_time=1.5)
        self.objects["explanation_text"] = new_explanation
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_08.mp3")  # [auto-injected] duration=6.98s
        _audio_dur_8 = 6.98  # [audio-sync] actual TTS duration
        # Step 9
        # Signal Action: Indicate boxes_group
        self.play(Indicate(self.objects["boxes_group"], color=RED, run_time=1))
        # Visual Action: Animate removal of one box (the top one)
        box_to_remove = self.objects["boxes_group"][0]
        self.play(
            box_to_remove.animate.shift(UP * 2).set_opacity(0),
            run_time=1.5
        )
        # Update boxes_group to contain only the remaining box
        remaining_box = self.objects["boxes_group"][1]
        new_boxes_group = VGroup(remaining_box)
        new_boxes_group.move_to(self.objects["left_pan"].get_center())
        self.objects["boxes_group"] = new_boxes_group
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_09.mp3")  # [auto-injected] duration=5.02s
        _audio_dur_9 = 5.02  # [audio-sync] actual TTS duration
        # Step 10
        # Signal Action: Indicate circles_group
        self.play(Indicate(self.objects["circles_group"], color=RED, run_time=1))
        # Visual Action: Animate removal of three circles (top row)
        circles_to_remove = VGroup(*self.objects["circles_group"][:3])
        self.play(
            circles_to_remove.animate.shift(UP * 2).set_opacity(0),
            run_time=1.5
        )
        # Update circles_group to contain only the remaining three circles
        remaining_circles = VGroup(*self.objects["circles_group"][3:])
        new_circles_group = VGroup(*remaining_circles)
        new_circles_group.arrange_in_grid(rows=1, cols=3, buff=0.3)
        new_circles_group.move_to(self.objects["right_pan"].get_center())
        self.objects["circles_group"] = new_circles_group
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_10.mp3")  # [auto-injected] duration=6.43s
        _audio_dur_10 = 6.43  # [audio-sync] actual TTS duration
        # Step 11
        # Signal Action: Circumscribe eq_display
        self.play(Circumscribe(self.objects["eq_display"], color=GREEN, run_time=1))
        # Visual Action: ReplacementTransform eq_display from "2x = 6" to "x = 3"
        new_eq = MathTex("x = 3", color=YELLOW, font_size=48)
        new_eq.move_to(self.objects["eq_display"].get_center())
        self.play(TransformMatchingTex(self.objects["eq_display"], new_eq), run_time=1.5)
        self.objects["eq_display"] = new_eq
        remaining_11 = _audio_dur_10  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_11))

        self.add_sound("media/audio/To_visualize_the_equ_49ca423580/step_11.mp3")  # [auto-injected] duration=6.67s
        _audio_dur_11 = 6.67  # [audio-sync] actual TTS duration
        # Step 12
        # Signal Action: None
        # Visual Action: ReplacementTransform explanation text
        final_explanation = Text("One x balances three units. Therefore, x = 3.", color=GRAY_C, font_size=28)
        final_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], final_explanation), run_time=2.0)
        self.objects["explanation_text"] = final_explanation
        remaining_12 = _audio_dur_11  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_12))

        # Final pause
        self.wait(max(0.1, 2))