'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing displacement on a number line as the change in position from -2 to +3, showing the displacement arrow's magnitude (5 units) is independent of the path.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, marker, arrow, labels
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use relative positioning (next_to, move_to). Arrow shifts down after animation to avoid clutter with the marker.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? Yes, for each step.
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Number line, marker at -2, start label, and initial explanation appear. Start label is highlighted.
#    - Step 3: Marker moves to +3 while a blue arrow grows from start to end point simultaneously.
#    - Step 4: End label appears, arrow shifts down, length label appears, explanation text updates to show the displacement equation.
#    - Step 5: Final hold with arrow highlighted.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Displacement on a Number Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        # Note: GRAY_C is not a standard color. Use GRAY_B or LIGHT_GREY. We'll use LIGHT_GREY.
        number_line = NumberLine(x_range=[-5.5, 5.5, 1], length=11, include_numbers=True, color=LIGHT_GREY)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # marker (Triangle pointing RIGHT)
        marker = Triangle(color=YELLOW, fill_opacity=1, stroke_width=0)
        marker.scale(0.2)  # Using scale instead of radius parameter
        marker.move_to(number_line.n2p(-2))
        marker.rotate(-PI/2)  # Default triangle points UP, rotate to point RIGHT
        self.objects["marker"] = marker

        # start_label
        start_label = MathTex("-2", color=YELLOW)
        start_label.next_to(number_line.n2p(-2), DOWN, buff=0.2)
        self.objects["start_label"] = start_label

        # end_label (initially invisible)
        end_label = MathTex("+3", color=GREEN)
        end_label.next_to(number_line.n2p(3), UP, buff=0.2)
        end_label.set_opacity(0)
        self.objects["end_label"] = end_label

        # displacement_arrow (initially zero length at start point)
        # Arrow start and end are the same initially
        arrow_start = number_line.n2p(-2)
        displacement_arrow = Arrow(start=arrow_start, end=arrow_start, color=BLUE, stroke_width=6, max_tip_length_to_length_ratio=0.15, buff=0)
        self.objects["displacement_arrow"] = displacement_arrow

        # arrow_length_label (initially invisible)
        arrow_length_label = MathTex("5", color=BLUE)
        # Position will be set after arrow is shifted down in step 4
        arrow_length_label.next_to(displacement_arrow, DOWN, buff=0.1)
        arrow_length_label.set_opacity(0)
        self.objects["arrow_length_label"] = arrow_length_label

        # explanation_text
        explanation_text = Text("We start at position -2.", color=LIGHT_GREY, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_scene_413438f974/step_00.mp3")  # [auto-injected] duration=5.04s
        _audio_dur_0 = 5.04  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_scene_413438f974/step_01.mp3")  # [auto-injected] duration=3.38s
        _audio_dur_1 = 3.38  # [audio-sync] actual TTS duration
        # Step 2
        # Signal action: Circumscribe start_label
        self.play(Circumscribe(self.objects["start_label"], color=YELLOW, run_time=1))
        # Visual action: Create number_line, marker, start_label, explanation_text
        self.play(
            Create(self.objects["number_line"]),
            Create(self.objects["marker"]),
            Write(self.objects["start_label"]),
            Write(self.objects["explanation_text"])
        )
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration  # Assuming animation group takes ~2.0 seconds
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_scene_413438f974/step_02.mp3")  # [auto-injected] duration=10.56s
        _audio_dur_2 = 10.56  # [audio-sync] actual TTS duration
        # Step 3
        # No signal action
        # Visual action: Simultaneous marker move and arrow growth
        # We need to create the final arrow for the growth animation.
        arrow_end_point = number_line.n2p(3)
        final_arrow = Arrow(start=number_line.n2p(-2), end=arrow_end_point, color=BLUE, stroke_width=6, max_tip_length_to_length_ratio=0.15, buff=0)
        # We'll use Transform to grow the arrow from zero length to full length.
        # But the JSON says "Create(displacement_arrow, rate_func=linear)". We'll interpret as animating its creation.
        # Since the arrow already exists (zero length), we can transform it to the final arrow.
        self.play(
            self.objects["marker"].animate.move_to(arrow_end_point),
            Transform(self.objects["displacement_arrow"], final_arrow, rate_func=linear),
            run_time=4.0
        )
        # Update the stored arrow to the final one for later steps
        self.objects["displacement_arrow"] = final_arrow
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_scene_413438f974/step_03.mp3")  # [auto-injected] duration=11.30s
        _audio_dur_3 = 11.30  # [audio-sync] actual TTS duration
        # Step 4
        # Signal action: Indicate end_label
        self.play(Indicate(self.objects["end_label"], color=GREEN, run_time=1))
        # Visual action: FadeIn end_label, shift arrow down, FadeIn length label, update explanation text
        self.play(
            self.objects["end_label"].animate.set_opacity(1),
            self.objects["displacement_arrow"].animate.shift(DOWN * 1.5),
            self.objects["arrow_length_label"].animate.set_opacity(1),
        )
        # Update explanation text using ReplacementTransform
        new_explanation = Text("Displacement = 3 - (-2) = 5", color=LIGHT_GREY, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        # Reposition arrow length label relative to the shifted arrow
        self.objects["arrow_length_label"].next_to(self.objects["displacement_arrow"], DOWN, buff=0.1)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration  # Assuming the above takes ~3.0 seconds
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_scene_413438f974/step_04.mp3")  # [auto-injected] duration=7.27s
        _audio_dur_4 = 7.27  # [audio-sync] actual TTS duration
        # Step 5
        # Signal action: Circumscribe displacement_arrow
        self.play(Circumscribe(self.objects["displacement_arrow"], color=BLUE, run_time=1))
        # Visual action: Wait (hold final frame)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))