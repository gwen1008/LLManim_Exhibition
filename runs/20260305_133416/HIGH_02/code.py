'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the transformation of the parent parabola y=x^2 into y=(x-2)^2-3 through horizontal and vertical shifts.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for Axes and parabolas
#    - Footer Region: [Bottom y=-3.5] for dynamic equation display
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroup for vertex dot+label and axis line+label. Keep footer equation centered at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Setup axes and parent parabola.
#    - Show vertex and axis for parent.
#    - Transform equation to (x-2)^2, shift graph right.
#    - Transform equation to (x-2)^2-3, shift graph down.
#    - Finalize with green parabola, highlight vertex and axis.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        footer_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # Title
        title = Text("Graphing a Parabola: y = (x-2)² - 3", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-4, 6, 1],
            axis_config={"include_numbers": True},
            color=GRAY_C
        )
        axes.move_to(global_center).scale(0.9)
        self.objects["axes"] = axes

        # Parent parabola (y = x^2)
        parent_parabola = axes.plot(lambda x: x**2, color=BLUE_C, stroke_width=4)
        self.objects["parent_parabola"] = parent_parabola

        # Final parabola (y = (x-2)^2 - 3) - initially invisible
        final_parabola = axes.plot(lambda x: (x-2)**2 - 3, color=GREEN, stroke_width=4)
        final_parabola.set_opacity(0)  # Start invisible
        self.objects["final_parabola"] = final_parabola

        # Vertex point and label
        vertex_point = Dot(radius=0.08, color=YELLOW, fill_opacity=1.0)
        vertex_point.move_to(axes.c2p(0, 0))
        self.objects["vertex_point"] = vertex_point

        vertex_label = MathTex("V(0,0)", color=YELLOW, font_size=30)
        vertex_label.next_to(vertex_point, UP+RIGHT, buff=0.1)
        self.objects["vertex_label"] = vertex_label

        # Axis line and label
        axis_line = DashedLine(start=3*UP, end=3*DOWN, color=RED, stroke_width=3, stroke_opacity=0.7, dash_length=0.05)
        axis_line.move_to(axes.c2p(0, 0))
        self.objects["axis_line"] = axis_line

        axis_label = MathTex("x=0", color=RED, font_size=30)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        self.objects["axis_label"] = axis_label

        # Footer equation
        eq_display_footer = MathTex("y = x^2", color=WHITE, font_size=36)
        eq_display_footer.move_to(footer_anchor)
        self.objects["eq_display_footer"] = eq_display_footer

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_00.mp3")  # [auto-injected] duration=14.81s
        _audio_dur_0 = 14.81  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Circumscribe(self.objects["eq_display_footer"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["axes"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_01.mp3")  # [auto-injected] duration=2.26s
        _audio_dur_1 = 2.26  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["parent_parabola"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_02.mp3")  # [auto-injected] duration=3.31s
        _audio_dur_2 = 3.31  # [audio-sync] actual TTS duration
        # Step 3
        self.play(
            Create(self.objects["vertex_point"]),
            Write(self.objects["vertex_label"]),
            Create(self.objects["axis_line"]),
            Write(self.objects["axis_label"]),
            run_time=2.5
        )
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_03.mp3")  # [auto-injected] duration=13.49s
        _audio_dur_3 = 13.49  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Indicate(self.objects["eq_display_footer"], color=ORANGE, run_time=1))
        eq_step4 = MathTex("y = (x-2)^2", color=WHITE, font_size=36)
        eq_step4.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["eq_display_footer"], eq_step4), run_time=2.0)
        self.objects["eq_display_footer"] = eq_step4
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_04.mp3")  # [auto-injected] duration=8.93s
        _audio_dur_4 = 8.93  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Indicate(self.objects["vertex_point"], color=YELLOW, run_time=1))
        # Create updated labels for the shift
        vertex_label_step5 = MathTex("V(2,0)", color=YELLOW, font_size=30)
        vertex_label_step5.next_to(axes.c2p(2, 0), UP+RIGHT, buff=0.1)
        axis_label_step5 = MathTex("x=2", color=RED, font_size=30)
        axis_label_step5.next_to(axes.c2p(2, 3), UP, buff=0.1)
        # Animate the shift
        self.play(
            self.objects["parent_parabola"].animate.shift(2*RIGHT),
            self.objects["vertex_point"].animate.shift(2*RIGHT),
            ReplacementTransform(self.objects["vertex_label"], vertex_label_step5),
            self.objects["axis_line"].animate.shift(2*RIGHT),
            ReplacementTransform(self.objects["axis_label"], axis_label_step5),
            run_time=2.5
        )
        self.objects["vertex_label"] = vertex_label_step5
        self.objects["axis_label"] = axis_label_step5
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_05.mp3")  # [auto-injected] duration=6.29s
        _audio_dur_5 = 6.29  # [audio-sync] actual TTS duration
        # Step 6
        self.play(Indicate(self.objects["eq_display_footer"], color=ORANGE, run_time=1))
        eq_step6 = MathTex("y = (x-2)^2 - 3", color=WHITE, font_size=36)
        eq_step6.move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["eq_display_footer"], eq_step6), run_time=1.5)
        self.objects["eq_display_footer"] = eq_step6
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_06.mp3")  # [auto-injected] duration=7.13s
        _audio_dur_6 = 7.13  # [audio-sync] actual TTS duration
        # Step 7
        self.play(Indicate(self.objects["vertex_point"], color=YELLOW, run_time=1))
        # Create final vertex label
        vertex_label_final = MathTex("V(2,-3)", color=YELLOW, font_size=30)
        vertex_label_final.next_to(axes.c2p(2, -3), UP+RIGHT, buff=0.1)
        # Animate the downward shift and transform parabola
        self.play(
            self.objects["parent_parabola"].animate.shift(3*DOWN),
            self.objects["vertex_point"].animate.shift(3*DOWN),
            ReplacementTransform(self.objects["vertex_label"], vertex_label_final),
            run_time=2.5
        )
        # Now transform the blue parent parabola into the green final parabola
        self.play(
            ReplacementTransform(self.objects["parent_parabola"], self.objects["final_parabola"]),
            run_time=1.0
        )
        self.objects["vertex_label"] = vertex_label_final
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_07.mp3")  # [auto-injected] duration=9.89s
        _audio_dur_7 = 9.89  # [audio-sync] actual TTS duration
        # Step 8
        self.play(
            Circumscribe(self.objects["vertex_point"], color=YELLOW, run_time=1),
            Circumscribe(self.objects["axis_line"], color=RED, run_time=1)
        )
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_a_Manim_anima_18021745b6/step_08.mp3")  # [auto-injected] duration=12.48s
        _audio_dur_8 = 12.48  # [audio-sync] actual TTS duration
        # Step 9
        self.play(FadeOut(self.objects["parent_parabola"]), run_time=1.0)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))