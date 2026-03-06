'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the process of rounding 3.7 to the nearest whole number using a number line.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line and markers
#    - Footer Region: [Bottom y=-3.5] for explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for number line components. Position labels above/below ticks. Keep footer text separate.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? (Yes, will calculate per step)
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Number line, ticks, labels, and the point 3.7 appear.
#    - Step 3: Midpoint (3.5) line and label appear.
#    - Step 4: Green marker appears, moves to midpoint and back, showing comparison.
#    - Step 5: Marker moves to 4, red dot and label appear, showing rounding up.
#    - Step 6: Cleanup: fade out marker and midpoint, final result highlighted.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole Number", font_size=36, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(x_range=[2.5, 4.5, 0.5], length=6, include_numbers=False, color=GRAY_B)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # Ticks and Labels for 3 and 4
        tick_3 = Line(start=DOWN*0.15, end=UP*0.15, color=WHITE, stroke_width=4)
        tick_3.move_to(number_line.number_to_point(3))
        self.objects["tick_3"] = tick_3

        tick_4 = Line(start=DOWN*0.15, end=UP*0.15, color=WHITE, stroke_width=4)
        tick_4.move_to(number_line.number_to_point(4))
        self.objects["tick_4"] = tick_4

        label_3 = MathTex("3", color=WHITE)
        label_3.next_to(tick_3, DOWN, buff=0.2)
        self.objects["label_3"] = label_3

        label_4 = MathTex("4", color=WHITE)
        label_4.next_to(tick_4, DOWN, buff=0.2)
        self.objects["label_4"] = label_4

        # Point 3.7 and its label
        point_3_7 = Dot(radius=0.08, color=BLUE, fill_opacity=1.0)
        point_3_7.move_to(number_line.number_to_point(3.7))
        self.objects["point_3_7"] = point_3_7

        label_3_7 = MathTex("3.7", color=BLUE)
        label_3_7.next_to(point_3_7, UP, buff=0.2)
        self.objects["label_3_7"] = label_3_7

        # Midpoint indicator and label (initially invisible)
        midpoint_indicator = Line(start=DOWN*0.5, end=UP*0.5, color=YELLOW, stroke_width=3)
        midpoint_indicator.move_to(number_line.number_to_point(3.5))
        midpoint_indicator.set_opacity(0.0)
        self.objects["midpoint_indicator"] = midpoint_indicator

        label_mid = MathTex("3.5", color=YELLOW)
        label_mid.next_to(midpoint_indicator, DOWN, buff=0.25)
        label_mid.set_opacity(0.0)
        self.objects["label_mid"] = label_mid

        # Green triangle marker (initially invisible)
        marker = Triangle(fill_opacity=1.0, stroke_width=2, color=GREEN)
        marker.scale(0.15)  # Use scale instead of height parameter
        marker.move_to(point_3_7.get_center() + UP*0.5)
        marker.set_opacity(0.0)
        self.objects["marker"] = marker

        # Rounded dot and label at 4 (initially invisible)
        rounded_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        rounded_dot.move_to(number_line.number_to_point(4))
        rounded_dot.set_opacity(0.0)
        self.objects["rounded_dot"] = rounded_dot

        label_4_rounded = MathTex("4", color=RED)
        label_4_rounded.next_to(rounded_dot, UP, buff=0.2)
        label_4_rounded.set_opacity(0.0)
        self.objects["label_4_rounded"] = label_4_rounded

        # Footer text
        footer_text = Text("We begin with a number line showing the integers 3 and 4.", font_size=24, color=GRAY_B)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_anima_ecd62629ed/step_00.mp3")  # [auto-injected] duration=4.25s
        _audio_dur_0 = 4.25  # [audio-sync] actual TTS duration
        # Step 1
        self.play(FadeIn(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_anima_ecd62629ed/step_01.mp3")  # [auto-injected] duration=7.08s
        _audio_dur_1 = 7.08  # [audio-sync] actual TTS duration
        # Step 2
        # Signal action: Indicate point_3_7
        self.play(Indicate(self.objects["point_3_7"], color=BLUE, run_time=1))
        # Visual action: GroupedCreate
        group_step2 = VGroup(
            self.objects["number_line"],
            self.objects["tick_3"],
            self.objects["tick_4"],
            self.objects["label_3"],
            self.objects["label_4"],
            self.objects["point_3_7"],
            self.objects["label_3_7"],
            self.objects["footer_text"]
        )
        self.play(LaggedStart(
            Create(self.objects["number_line"]),
            Create(self.objects["tick_3"]),
            Create(self.objects["tick_4"]),
            Write(self.objects["label_3"]),
            Write(self.objects["label_4"]),
            Create(self.objects["point_3_7"]),
            Write(self.objects["label_3_7"]),
            Write(self.objects["footer_text"]),
            lag_ratio=0.2
        ), run_time=3.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_anima_ecd62629ed/step_02.mp3")  # [auto-injected] duration=9.65s
        _audio_dur_2 = 9.65  # [audio-sync] actual TTS duration
        # Step 3
        # Signal action: Circumscribe midpoint_indicator
        self.play(Circumscribe(self.objects["midpoint_indicator"], color=YELLOW, run_time=1))
        # Visual action: Fade in midpoint and update footer
        new_footer_3 = Text("The midpoint, 3.5, is the threshold.", font_size=24, color=GRAY_B)
        new_footer_3.move_to(footer_anchor)
        self.play(
            self.objects["midpoint_indicator"].animate.set_opacity(0.7),
            self.objects["label_mid"].animate.set_opacity(1.0),
            ReplacementTransform(self.objects["footer_text"], new_footer_3),
            run_time=2.0
        )
        self.objects["footer_text"] = new_footer_3
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_anima_ecd62629ed/step_03.mp3")  # [auto-injected] duration=7.68s
        _audio_dur_3 = 7.68  # [audio-sync] actual TTS duration
        # Step 4
        # Signal action: Indicate marker
        self.play(Indicate(self.objects["marker"], color=GREEN, run_time=1))
        # Visual action: Fade in marker, move to midpoint and back, update footer
        self.play(self.objects["marker"].animate.set_opacity(1.0), run_time=0.5)
        marker_target_mid = self.objects["midpoint_indicator"].get_center() + UP*0.5
        self.play(
            self.objects["marker"].animate.move_to(marker_target_mid),
            run_time=1.5
        )
        self.play(
            self.objects["marker"].animate.move_to(self.objects["point_3_7"].get_center() + UP*0.5),
            run_time=1.5
        )
        new_footer_4 = Text("3.7 is greater than the midpoint 3.5.", font_size=24, color=GRAY_B)
        new_footer_4.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer_4), run_time=1.0)
        self.objects["footer_text"] = new_footer_4
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_anima_ecd62629ed/step_04.mp3")  # [auto-injected] duration=6.79s
        _audio_dur_4 = 6.79  # [audio-sync] actual TTS duration
        # Step 5
        # Signal action: Indicate rounded_dot
        self.play(Indicate(self.objects["rounded_dot"], color=RED, run_time=1))
        # Visual action: Move marker to 4, fade in red dot and label, update footer
        marker_target_4 = self.objects["rounded_dot"].get_center() + UP*0.5
        self.play(
            self.objects["marker"].animate.move_to(marker_target_4),
            self.objects["rounded_dot"].animate.set_opacity(1.0),
            self.objects["label_4_rounded"].animate.set_opacity(1.0),
            run_time=1.5
        )
        new_footer_5 = Text("Therefore, 3.7 rounds up to 4.", font_size=24, color=GRAY_B)
        new_footer_5.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer_5), run_time=1.0)
        self.objects["footer_text"] = new_footer_5
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_Manim_anima_ecd62629ed/step_05.mp3")  # [auto-injected] duration=8.95s
        _audio_dur_5 = 8.95  # [audio-sync] actual TTS duration
        # Step 6
        # No signal action
        # Visual action: Fade out marker and midpoint, update footer, indicate points
        self.play(
            FadeOut(self.objects["marker"]),
            self.objects["midpoint_indicator"].animate.set_opacity(0.0),
            self.objects["label_mid"].animate.set_opacity(0.0),
            run_time=1.0
        )
        new_footer_6 = Text("Result: 3.7 rounded to the nearest whole number is 4.", font_size=24, color=GRAY_B)
        new_footer_6.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], new_footer_6), run_time=1.0)
        self.objects["footer_text"] = new_footer_6
        self.play(
            Indicate(self.objects["point_3_7"], color=BLUE, run_time=0.8),
            Indicate(self.objects["rounded_dot"], color=RED, run_time=0.8),
            lag_ratio=0.5
        )
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))