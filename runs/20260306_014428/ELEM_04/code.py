'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the measurement of a 60-degree angle using a protractor.
# 2. Layout Strategy:
#    - Header Region: [y=3.0] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.0] for step explanation
# 3. Anti-Overlap Check:
#    - Strategy: All geometry centered at ORIGIN. Protractor labels placed relative to its arc.
#    - Use VGroup for protractor elements for easier management.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Show vertex and initial ray.
#    - Step 2: Show terminal ray, completing the angle.
#    - Step 3: Introduce protractor.
#    - Step 4: Animate the measurement wedge growing to 60 degrees.
#    - Step 5: Display the final angle label.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        vertex = ORIGIN
        title_anchor = 3 * UP
        explanation_anchor = 3 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Measuring a 60-Degree Angle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # ray_initial
        ray_initial = Line(start=[0, 0, 0], end=[3, 0, 0], color=YELLOW, stroke_width=6)
        ray_initial.move_to(ORIGIN)
        self.objects["ray_initial"] = ray_initial

        # ray_terminal
        ray_terminal = Line(start=[0, 0, 0], end=[1.5, 2.598, 0], color=YELLOW, stroke_width=6)
        ray_terminal.move_to(ORIGIN)
        self.objects["ray_terminal"] = ray_terminal

        # vertex_dot
        vertex_dot = Dot(radius=0.08, color=WHITE)
        vertex_dot.move_to(vertex)
        self.objects["vertex_dot"] = vertex_dot

        # protractor_semicircle
        protractor_semicircle = Arc(radius=3.5, start_angle=0, angle=PI, color=BLUE, stroke_width=3)
        protractor_semicircle.set_stroke(opacity=0.7)
        protractor_semicircle.move_to(vertex)
        self.objects["protractor_semicircle"] = protractor_semicircle

        # protractor_scale_0
        protractor_scale_0 = MathTex("0^\\circ", color=BLUE, font_size=24)
        protractor_scale_0.next_to([3.5, 0, 0], DOWN, buff=0.2)
        self.objects["protractor_scale_0"] = protractor_scale_0

        # protractor_scale_90
        protractor_scale_90 = MathTex("90^\\circ", color=BLUE, font_size=24)
        protractor_scale_90.next_to([0, 3.5, 0], LEFT, buff=0.2)
        self.objects["protractor_scale_90"] = protractor_scale_90

        # protractor_scale_180
        protractor_scale_180 = MathTex("180^\\circ", color=BLUE, font_size=24)
        protractor_scale_180.next_to([-3.5, 0, 0], DOWN, buff=0.2)
        self.objects["protractor_scale_180"] = protractor_scale_180

        # wedge_base (initial angle=0)
        wedge_base = Arc(radius=3.0, start_angle=0, angle=0, color=TEAL, stroke_width=0)
        wedge_base.set_fill(color=TEAL, opacity=0.4)
        wedge_base.move_to(vertex)
        self.objects["wedge_base"] = wedge_base

        # angle_label
        angle_label = MathTex("60^\\circ", color=TEAL, font_size=32)
        angle_label.move_to([1.2, 0.8, 0])
        self.objects["angle_label"] = angle_label

        # explanation_text (placeholder, will be updated per step)
        explanation_text = Text("Placeholder for step explanation.", color=GRAY_C, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # [missing audio] self.add_sound("media/audio/Create_a_Manim_anima_d413ce2cf2/step_00.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_0 = 2.00  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Indicate(self.objects["vertex_dot"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["ray_initial"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        # Update explanation for Step 1
        explanation_step1 = Text("We begin with a 60-degree angle. Its vertex is at the center, with one ray pointing along the zero-degree direction.", color=GRAY_C, font_size=28)
        explanation_step1.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], explanation_step1))
        self.objects["explanation_text"] = explanation_step1

        # [missing audio] self.add_sound("media/audio/Create_a_Manim_anima_d413ce2cf2/step_01.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["ray_terminal"]), run_time=1.5)
        self.play(FadeIn(self.objects["vertex_dot"]), run_time=0.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        explanation_step2 = Text("The second ray is rotated 60 degrees from the first, completing the angle.", color=GRAY_C, font_size=28)
        explanation_step2.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], explanation_step2))
        self.objects["explanation_text"] = explanation_step2

        # [missing audio] self.add_sound("media/audio/Create_a_Manim_anima_d413ce2cf2/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Circumscribe(self.objects["protractor_semicircle"], color=BLUE, run_time=1))
        self.play(FadeIn(self.objects["protractor_semicircle"]), run_time=1.0)
        self.play(FadeIn(self.objects["protractor_scale_0"]), FadeIn(self.objects["protractor_scale_90"]), FadeIn(self.objects["protractor_scale_180"]), run_time=1.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        explanation_step3 = Text("To measure this angle, we overlay a semicircular protractor, centered on the vertex.", color=GRAY_C, font_size=28)
        explanation_step3.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], explanation_step3))
        self.objects["explanation_text"] = explanation_step3

        # [missing audio] self.add_sound("media/audio/Create_a_Manim_anima_d413ce2cf2/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        # Create the target wedge with angle=PI/3 (60 degrees)
        wedge_target = Arc(radius=3.0, start_angle=0, angle=PI/3, color=TEAL, stroke_width=0)
        wedge_target.set_fill(color=TEAL, opacity=0.4)
        wedge_target.move_to(vertex)
        self.play(Transform(self.objects["wedge_base"], wedge_target), run_time=3.0)
        self.objects["wedge_base"] = wedge_target
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        explanation_step4 = Text("We measure by seeing how much of the protractor's circle is between the two rays. Watch as the colored sector grows to fill exactly 60 degrees.", color=GRAY_C, font_size=28)
        explanation_step4.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], explanation_step4))
        self.objects["explanation_text"] = explanation_step4

        # [missing audio] self.add_sound("media/audio/Create_a_Manim_anima_d413ce2cf2/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Indicate(self.objects["angle_label"], color=TEAL, run_time=1))
        self.play(Write(self.objects["angle_label"]), run_time=1.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        explanation_step5 = Text("This confirms the angle measures 60 degrees. The protractor gives us a visual and quantitative tool for understanding angles.", color=GRAY_C, font_size=28)
        explanation_step5.move_to(explanation_anchor)
        self.play(Transform(self.objects["explanation_text"], explanation_step5))
        self.objects["explanation_text"] = explanation_step5

        # Final hold
        self.wait(max(0.1, 2))