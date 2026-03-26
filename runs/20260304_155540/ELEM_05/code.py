'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize rounding decimals using a number line, highlighting the midpoint as the decision boundary.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and zones
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for number line components. Position zones behind the line.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Draw number line, ticks, labels for 3 and 4.
#    - Step 2: Show the point 3.7.
#    - Step 3: Reveal the midpoint 3.5.
#    - Step 4: Show color-coded rounding zones.
#    - Step 5: Animate the point snapping from 3.7 to 4.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Rounding on a Number Line: 3.7 to 4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(x_range=[3, 4, 0.1], length=7, include_numbers=False, color=GRAY_B)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Tick and label for 3
        tick_3 = Line(start=UP*0.15, end=DOWN*0.15, color=WHITE, stroke_width=4)
        tick_3.move_to(number_line.n2p(3))
        self.objects["tick_3"] = tick_3

        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(tick_3, DOWN, buff=0.2)
        self.objects["label_3"] = label_3

        # Tick and label for 4
        tick_4 = Line(start=UP*0.15, end=DOWN*0.15, color=WHITE, stroke_width=4)
        tick_4.move_to(number_line.n2p(4))
        self.objects["tick_4"] = tick_4

        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(tick_4, DOWN, buff=0.2)
        self.objects["label_4"] = label_4

        # Zone rectangles (initially invisible)
        zone_round_down = Rectangle(width=3.5, height=1.2, color=RED, fill_opacity=0.2, stroke_opacity=0.0)
        zone_round_down.move_to(content_center + LEFT*1.75)
        self.objects["zone_round_down"] = zone_round_down

        zone_round_up = Rectangle(width=3.5, height=1.2, color=GREEN, fill_opacity=0.2, stroke_opacity=0.0)
        zone_round_up.move_to(content_center + RIGHT*1.75)
        self.objects["zone_round_up"] = zone_round_up

        # Point 3.7 and its label
        point_3_7 = Dot(radius=0.08, color=YELLOW)
        point_3_7.move_to(number_line.n2p(3.7))
        self.objects["point_3_7"] = point_3_7

        label_3_7 = MathTex("3.7", color=YELLOW)
        label_3_7.next_to(point_3_7, UP, buff=0.15)
        self.objects["label_3_7"] = label_3_7

        # Midpoint tick and label (initially invisible)
        midpoint_tick = Line(start=UP*0.25, end=DOWN*0.25, color=WHITE, stroke_width=3, stroke_opacity=0.0)
        midpoint_tick.move_to(number_line.n2p(3.5))
        self.objects["midpoint_tick"] = midpoint_tick

        label_midpoint = MathTex("3.5", color=WHITE).set_opacity(0.0)
        label_midpoint.next_to(midpoint_tick, UP, buff=0.2)
        self.objects["label_midpoint"] = label_midpoint

        # Explanation text (dynamic, initially empty)
        explanation_text = Text("", color=GRAY_B, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_anima_aa5ee864c5/step_00.mp3")  # [auto-injected] duration=4.75s
        _audio_dur_0 = 4.75  # [audio-sync] actual TTS duration
        # Step 1: Draw number line, ticks, labels for 3 and 4.
        self.play(Write(title), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.play(Create(number_line), run_time=1.5)
        self.play(Create(tick_3), Write(label_3), Create(tick_4), Write(label_4), run_time=1.5)
        remaining_1b = max(0.1, 3.0 - (1.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_1b))

        self.add_sound("media/audio/Create_a_Manim_anima_aa5ee864c5/step_01.mp3")  # [auto-injected] duration=4.32s
        _audio_dur_1 = 4.32  # [audio-sync] actual TTS duration
        # Step 2: Place the number 3.7.
        # Signal action: Indicate the point
        self.play(Indicate(point_3_7, color=YELLOW, run_time=1))
        # Visual action: Grow the point and write its label
        self.play(GrowFromCenter(point_3_7), Write(label_3_7), run_time=1.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_anima_aa5ee864c5/step_02.mp3")  # [auto-injected] duration=8.16s
        _audio_dur_2 = 8.16  # [audio-sync] actual TTS duration
        # Step 3: Reveal the midpoint 3.5.
        # Signal action: Circumscribe the midpoint tick
        self.play(Circumscribe(midpoint_tick, color=ORANGE, run_time=1))
        # Visual action: Fade in midpoint tick and label
        self.play(
            midpoint_tick.animate.set_stroke(opacity=1),
            label_midpoint.animate.set_opacity(1),
            run_time=2.0
        )
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_anima_aa5ee864c5/step_03.mp3")  # [auto-injected] duration=11.09s
        _audio_dur_3 = 11.09  # [audio-sync] actual TTS duration
        # Step 4: Show color-coded rounding zones.
        # Signal action: Indicate the round-up zone
        self.play(Indicate(zone_round_up, color=GREEN, run_time=1))
        # Visual action: Fade in both zones (round-up and round-down for contrast)
        self.play(
            FadeIn(zone_round_up),
            FadeIn(zone_round_down),
            run_time=3.0
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_anima_aa5ee864c5/step_04.mp3")  # [auto-injected] duration=5.16s
        _audio_dur_4 = 5.16  # [audio-sync] actual TTS duration
        # Step 5: Animate rounding from 3.7 to 4.
        # Signal action: Indicate the label 4
        self.play(Indicate(label_4, color=GREEN, run_time=1))
        # Visual action: Succession - Indicate point, then transform to 4
        self.play(Indicate(point_3_7, color=YELLOW, run_time=1))
        
        # Create target dot and label at position of 4
        target_dot = Dot(radius=0.08, color=YELLOW)
        target_dot.move_to(number_line.n2p(4))
        target_label = MathTex("4", color=YELLOW)
        target_label.next_to(target_dot, UP, buff=0.15)

        self.play(
            Transform(point_3_7, target_dot),
            Transform(label_3_7, target_label),
            run_time=1.5
        )
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))