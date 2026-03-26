'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the angles formed by a transversal intersecting two parallel lines, focusing on the property that same-side interior angles are supplementary.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the geometric diagram (parallel lines, transversal, angles)
#    - Footer Region: [Bottom y=-3.5] for explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: The diagram is centered. Angle arcs and labels are positioned relative to intersection points (A, B) using offsets. Use VGroups for related elements (e.g., arcs and labels) for easier management.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] I will assign `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step.
# 5. Animation Flow:
#    - Build the parallel lines and transversal.
#    - Mark and label intersection points A and B.
#    - Label the four interior angles (3,4,5,6).
#    - Highlight angle pairs (3 & 5, then 4 & 6) with green arcs.
#    - Display and emphasize the supplementary property.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Angles Formed by a Transversal and Parallel Lines", font_size=36, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Parallel Lines
        line_parallel_top = Line(start=[-4, 1.5, 0], end=[4, 1.5, 0], color=BLUE, stroke_width=4)
        line_parallel_top.move_to(diagram_center + UP*1.5)
        self.objects["line_parallel_top"] = line_parallel_top

        line_parallel_bottom = Line(start=[-4, -1.5, 0], end=[4, -1.5, 0], color=BLUE, stroke_width=4)
        line_parallel_bottom.move_to(diagram_center + DOWN*1.5)
        self.objects["line_parallel_bottom"] = line_parallel_bottom

        # Transversal Line
        line_transversal = Line(start=[-4, 2, 0], end=[4, -2, 0], color=YELLOW, stroke_width=4)
        line_transversal.move_to(diagram_center)
        self.objects["line_transversal"] = line_transversal

        # Intersection Points and Labels
        point_A = Dot(point=[-3, 1.5, 0], color=WHITE, radius=0.06)
        self.objects["point_A"] = point_A

        point_B = Dot(point=[3, -1.5, 0], color=WHITE, radius=0.06)
        self.objects["point_B"] = point_B

        label_A = MathTex("A", color=WHITE, font_size=24)
        label_A.next_to(point_A, UP+LEFT, buff=0.15)
        self.objects["label_A"] = label_A

        label_B = MathTex("B", color=WHITE, font_size=24)
        label_B.next_to(point_B, DOWN+RIGHT, buff=0.15)
        self.objects["label_B"] = label_B

        # Angle Arcs
        angle_arc_3 = Arc(radius=0.4, start_angle=180 * DEGREES, angle=45 * DEGREES, color=GREEN, stroke_width=6)
        angle_arc_3.move_to(point_A.get_center())
        self.objects["angle_arc_3"] = angle_arc_3

        angle_arc_5 = Arc(radius=0.4, start_angle=0 * DEGREES, angle=45 * DEGREES, color=GREEN, stroke_width=6)
        angle_arc_5.move_to(point_B.get_center())
        self.objects["angle_arc_5"] = angle_arc_5

        angle_arc_4 = Arc(radius=0.4, start_angle=225 * DEGREES, angle=45 * DEGREES, color=GREEN, stroke_width=6)
        angle_arc_4.move_to(point_A.get_center())
        self.objects["angle_arc_4"] = angle_arc_4

        angle_arc_6 = Arc(radius=0.4, start_angle=45 * DEGREES, angle=45 * DEGREES, color=GREEN, stroke_width=6)
        angle_arc_6.move_to(point_B.get_center())
        self.objects["angle_arc_6"] = angle_arc_6

        # Angle Labels
        label_angle_3 = MathTex("3", color=WHITE, font_size=24)
        label_angle_3.move_to(point_A.get_center() + 0.6 * UL)
        self.objects["label_angle_3"] = label_angle_3

        label_angle_4 = MathTex("4", color=WHITE, font_size=24)
        label_angle_4.move_to(point_A.get_center() + 0.6 * DR)
        self.objects["label_angle_4"] = label_angle_4

        label_angle_5 = MathTex("5", color=WHITE, font_size=24)
        label_angle_5.move_to(point_B.get_center() + 0.6 * UR)
        self.objects["label_angle_5"] = label_angle_5

        label_angle_6 = MathTex("6", color=WHITE, font_size=24)
        label_angle_6.move_to(point_B.get_center() + 0.6 * DL)
        self.objects["label_angle_6"] = label_angle_6

        # Explanation Text
        explanation_text = Text("Same-side interior angles are supplementary: ∠3 + ∠5 = 180°, ∠4 + ∠6 = 180°.",
                                font_size=28, color=GRAY_B)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_00.mp3")  # [auto-injected] duration=5.69s
        _audio_dur_0 = 5.69  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["line_parallel_top"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_01.mp3")  # [auto-injected] duration=4.87s
        _audio_dur_1 = 4.87  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["line_parallel_bottom"]), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_02.mp3")  # [auto-injected] duration=8.57s
        _audio_dur_2 = 8.57  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Create(self.objects["line_transversal"]), run_time=2.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_03.mp3")  # [auto-injected] duration=8.81s
        _audio_dur_3 = 8.81  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Indicate(self.objects["point_A"], color=RED, run_time=1))
        self.play(GrowFromCenter(self.objects["point_A"]), Write(self.objects["label_A"]), run_time=1.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_04.mp3")  # [auto-injected] duration=13.39s
        _audio_dur_4 = 13.39  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Circumscribe(self.objects["label_angle_3"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_angle_3"]), Write(self.objects["label_angle_4"]),
                  Write(self.objects["label_angle_5"]), Write(self.objects["label_angle_6"]), run_time=2.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_05.mp3")  # [auto-injected] duration=14.02s
        _audio_dur_5 = 14.02  # [audio-sync] actual TTS duration
        # Step 6
        self.play(Indicate(self.objects["angle_arc_3"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle_arc_3"]), run_time=1.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_06.mp3")  # [auto-injected] duration=6.07s
        _audio_dur_6 = 6.07  # [audio-sync] actual TTS duration
        # Step 7
        self.play(Indicate(self.objects["angle_arc_5"], color=GREEN, run_time=1))
        self.play(Create(self.objects["angle_arc_5"]), run_time=1.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_07.mp3")  # [auto-injected] duration=8.66s
        _audio_dur_7 = 8.66  # [audio-sync] actual TTS duration
        # Step 8
        self.play(Create(self.objects["angle_arc_4"]), Create(self.objects["angle_arc_6"]), run_time=1.5)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_08.mp3")  # [auto-injected] duration=12.50s
        _audio_dur_8 = 12.50  # [audio-sync] actual TTS duration
        # Step 9
        self.play(Circumscribe(self.objects["explanation_text"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["explanation_text"]), run_time=2.5)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Draw_two_parallel_li_95a8a25892/step_09.mp3")  # [auto-injected] duration=11.28s
        _audio_dur_9 = 11.28  # [audio-sync] actual TTS duration
        # Step 10
        self.play(Indicate(self.objects["angle_arc_3"], color=RED, run_time=1))
        self.play(FadeOut(self.objects["explanation_text"]), run_time=1.5)
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))