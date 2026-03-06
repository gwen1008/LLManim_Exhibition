'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative as the slope of the tangent line to a parabola y = x²/2. Show the dynamic relationship as the point of tangency moves.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for axes, parabola, point, tangent line
#    - Footer Region: [Bottom y=-3.5] for slope explanation and dynamic value
# 3. Anti-Overlap Check:
#    - Strategy: Use zones to separate elements. Keep dynamic slope display in footer, main graph centered.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Draw parabola, circumscribe it.
#    - Step 3: Update step label, write slope formula in footer.
#    - Step 4: Update step label, create moving point P.
#    - Step 5: Indicate point label, write label P, create tangent line, write initial slope value.
#    - Step 6: Update step label, animate ValueTracker to move point, tangent, and slope.
#    - Step 7: Circumscribe slope display, hold final frame.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # title_text
        title_text = Text("The Tangent Line to a Parabola", color=WHITE, font_size=36)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # step_label
        step_label = Text("Step 1: The Curve y = x²/2", color=GRAY, font_size=24)
        step_label.next_to(title_text, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True, "color": GRAY_C}
        ).move_to(content_center)
        self.objects["axes"] = axes

        # parabola
        parabola = axes.plot(lambda x: 0.5 * x**2, x_range=[-4, 4], color=BLUE)
        self.objects["parabola"] = parabola

        # ValueTracker for the moving point's x-coordinate 'a'
        a_tracker = ValueTracker(-3.0)
        self.a_tracker = a_tracker

        # moving_point_p (will be updated via always_redraw)
        moving_point_p = always_redraw(
            lambda: Dot(
                axes.c2p(a_tracker.get_value(), 0.5 * a_tracker.get_value()**2),
                color=YELLOW,
                radius=0.08
            )
        )
        self.objects["moving_point_p"] = moving_point_p

        # point_label (will be updated via always_redraw)
        point_label = always_redraw(
            lambda: MathTex("P", color=YELLOW, font_size=24).next_to(
                axes.c2p(a_tracker.get_value(), 0.5 * a_tracker.get_value()**2),
                UP+RIGHT, buff=0.1
            )
        )
        self.objects["point_label"] = point_label

        # tangent_line (will be updated via always_redraw)
        # Equation: y = a*(x - a) + 0.5*a² = a*x - 0.5*a²
        tangent_line = always_redraw(
            lambda: axes.plot(
                lambda x: a_tracker.get_value() * x - 0.5 * a_tracker.get_value()**2,
                x_range=[-4, 4],
                color=RED,
                stroke_width=3
            )
        )
        self.objects["tangent_line"] = tangent_line

        # slope_display (static part)
        slope_display = Tex(r"$y' = x$ $\Rightarrow$ Slope at $P$: $m = $", color=GREEN, font_size=32)
        slope_display.move_to(footer_anchor)
        self.objects["slope_display"] = slope_display

        # slope_value (dynamic part, updated via always_redraw)
        slope_value = always_redraw(
            lambda: MathTex(f"{a_tracker.get_value():.1f}", color=RED, font_size=32).next_to(slope_display, RIGHT, buff=0.1)
        )
        self.objects["slope_value"] = slope_value

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_00.mp3")  # [auto-injected] duration=4.63s
        _audio_dur_0 = 4.63  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_01.mp3")  # [auto-injected] duration=4.32s
        _audio_dur_1 = 4.32  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Circumscribe(self.objects["parabola"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parabola"]), run_time=3.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_02.mp3")  # [auto-injected] duration=10.18s
        _audio_dur_2 = 10.18  # [audio-sync] actual TTS duration
        # Step 3
        step_label_2 = Text("Step 2: The Derivative y' = x", color=GRAY, font_size=24)
        step_label_2.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_2))
        self.objects["step_label"] = step_label_2
        self.play(Write(self.objects["slope_display"]), run_time=4.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_03.mp3")  # [auto-injected] duration=9.34s
        _audio_dur_3 = 9.34  # [audio-sync] actual TTS duration
        # Step 4
        step_label_3 = Text("Step 3: The Tangent Line at a Point", color=GRAY, font_size=24)
        step_label_3.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_3))
        self.objects["step_label"] = step_label_3
        # Add the moving point (it's already defined with always_redraw, so we just add it)
        self.add(self.objects["moving_point_p"])
        # We'll animate its appearance with GrowFromCenter effect
        self.play(GrowFromCenter(self.objects["moving_point_p"]), run_time=2.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_04.mp3")  # [auto-injected] duration=7.58s
        _audio_dur_4 = 7.58  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Indicate(self.objects["point_label"], color=YELLOW, run_time=1))
        # Add the label and tangent line (they are always_redraw, so just add)
        self.add(self.objects["point_label"], self.objects["tangent_line"], self.objects["slope_value"])
        # Write animations for the newly added objects
        self.play(
            Write(self.objects["point_label"]),
            Create(self.objects["tangent_line"]),
            Write(self.objects["slope_value"]),
            run_time=4.0
        )
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_05.mp3")  # [auto-injected] duration=10.32s
        _audio_dur_5 = 10.32  # [audio-sync] actual TTS duration
        # Step 6
        step_label_4 = Text("Step 4: The Moving Tangent", color=GRAY, font_size=24)
        step_label_4.next_to(self.objects["title_text"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_4))
        self.objects["step_label"] = step_label_4
        # Animate the ValueTracker from -3 to 3
        self.play(self.a_tracker.animate.set_value(3.0), run_time=10.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_a_Manim_anima_3b1a5a212e/step_06.mp3")  # [auto-injected] duration=9.38s
        _audio_dur_6 = 9.38  # [audio-sync] actual TTS duration
        # Step 7
        self.play(Circumscribe(self.objects["slope_display"], color=GREEN, run_time=1))
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))