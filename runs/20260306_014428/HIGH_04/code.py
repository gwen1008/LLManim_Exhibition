'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative as the slope of the tangent line to a parabola (y = 0.5x²). Show a moving point, its dynamically updating tangent line, and the corresponding slope value (which equals x).
# 2. Layout Strategy: Three-zone layout.
#    - Header Region: [y=3.5] for Title and Step Indicator.
#    - Main Content: [Center y=0] for Axes, Parabola, Moving Dot, Tangent Line.
#    - Footer Region: [Bottom y=-3.5] for Slope Display and Explanation Text.
# 3. Anti-Overlap Check: Use relative positioning (next_to, move_to) and keep dynamic elements (dot, line, slope value) within the graph area. The footer text is placed below the slope display.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow: Show title, axes, parabola, introduce derivative, show moving point and tangent line, display slope value, animate point movement with real-time updates, show final explanation.
'''

from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define Anchors
        title_anchor = 3.5 * UP
        graph_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create Objects from layout_plan.objects
        # title
        title = Text("Tangent Line to a Parabola", color=WHITE, font_size=40)
        title.move_to(title_anchor).shift(UP*0.5)
        self.objects["title"] = title
        
        # step_indicator
        step_indicator = Text("Step 1: The Function", color=YELLOW, font_size=24)
        step_indicator.next_to(title, DOWN, buff=0.3)
        self.objects["step_indicator"] = step_indicator
        
        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True, "color": GRAY_C}
        ).move_to(graph_center)
        self.objects["axes"] = axes
        
        # parabola
        parabola = ParametricFunction(
            lambda t: np.array([t, 0.5*t**2, 0]),
            t_range=[-4, 4],
            color=BLUE,
            stroke_width=4
        ).move_to(graph_center)
        self.objects["parabola"] = parabola
        
        # func_label
        func_label = MathTex(r"y = \frac{1}{2}x^2", color=BLUE)
        func_label.next_to(parabola, UP+RIGHT, buff=0.2)
        self.objects["func_label"] = func_label
        
        # moving_dot (initial position at x=-3)
        moving_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        moving_dot.move_to(axes.c2p(-3, 0.5*(-3)**2))
        self.objects["moving_dot"] = moving_dot
        
        # tangent_line (initial dummy line, will be replaced by always_redraw)
        tangent_line = Line(LEFT*2, RIGHT*2, color=GREEN, stroke_width=3).move_to(graph_center)
        self.objects["tangent_line"] = tangent_line
        
        # slope_display_label
        slope_display_label = Text("Slope of tangent:", color=WHITE, font_size=24)
        slope_display_label.move_to(footer_anchor).shift(LEFT*2 + UP*0.5)
        self.objects["slope_display_label"] = slope_display_label
        
        # slope_value (initial value -3.00)
        slope_value = DecimalNumber(-3.00, num_decimal_places=2, color=YELLOW, font_size=28)
        slope_value.next_to(slope_display_label, RIGHT, buff=0.3)
        self.objects["slope_value"] = slope_value
        
        # explanation_text
        explanation_text = Text("The slope equals the x-coordinate of the point of tangency.", color=GRAY_C, font_size=20)
        explanation_text.next_to(slope_display_label, DOWN, buff=0.5)
        self.objects["explanation_text"] = explanation_text
        
        # Additional objects needed for the sequence
        # derivative_label for step 4
        derivative_label = MathTex(r"y' = x", color=YELLOW)
        derivative_label.next_to(func_label, RIGHT, buff=0.5)
        self.objects["derivative_label"] = derivative_label
        
        # Updated step indicator for step 4
        step_indicator_2 = Text("Step 2: The Derivative", color=YELLOW, font_size=24)
        step_indicator_2.next_to(title, DOWN, buff=0.3)
        self.objects["step_indicator_2"] = step_indicator_2
        
        # ValueTracker for the moving point (x-coordinate)
        x_tracker = ValueTracker(-3.0)
        self.objects["x_tracker"] = x_tracker
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_00.mp3")  # [auto-injected] duration=8.16s
        _audio_dur_0 = 8.16  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_01.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_1 = 2.00  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_02.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_2 = 2.00  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Indicate(self.objects["func_label"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parabola"]), run_time=3.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_03.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_3 = 2.00  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Circumscribe(self.objects["func_label"], color=YELLOW, run_time=1))
        self.play(
            ReplacementTransform(self.objects["step_indicator"], self.objects["step_indicator_2"]),
            Write(self.objects["derivative_label"])
        )
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration = ~2s total anim
        self.wait(max(0.1, remaining_4))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_04.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_4 = 2.00  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Create(self.objects["moving_dot"]), run_time=2.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_05.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_5 = 2.00  # [audio-sync] actual TTS duration
        # Step 6
        self.play(Indicate(self.objects["moving_dot"], color=RED, run_time=1))
        # Create the tangent line (static for now, will be made dynamic later)
        self.play(Create(self.objects["tangent_line"]), run_time=4.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_06.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_6 = 2.00  # [audio-sync] actual TTS duration
        # Step 7
        self.play(
            Write(self.objects["slope_display_label"]),
            Write(self.objects["slope_value"])
        )
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration # Write animations ~1s
        self.wait(max(0.1, remaining_7))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_07.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_7 = 2.00  # [audio-sync] actual TTS duration
        # Step 8: Set up dynamic updates and animate the point movement
        # Remove the static tangent line and replace with always_redraw version
        self.remove(self.objects["tangent_line"])
        
        # Define dynamic tangent line using always_redraw
        def update_tangent_line():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative y' = x
            # Create a line segment centered at the point, length 4
            start = axes.c2p(x - 1, y - slope * 1)
            end = axes.c2p(x + 1, y + slope * 1)
            return Line(start, end, color=GREEN, stroke_width=3)
        
        dynamic_tangent_line = always_redraw(update_tangent_line)
        self.add(dynamic_tangent_line)
        
        # Update moving dot position based on x_tracker
        moving_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)))
        
        # Update slope value display
        slope_value.add_updater(lambda d: d.set_value(x_tracker.get_value()))
        
        self.play(Indicate(self.objects["slope_value"], color=YELLOW, run_time=1))
        # Animate the x_tracker from -3 to 3
        self.play(x_tracker.animate.set_value(3.0), run_time=8.0, rate_func=linear)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))
        
        # [missing audio] self.add_sound("media/audio/Animate_the_graph_of_e6bb3798b3/step_08.mp3")  # [auto-injected] duration=2.00s
        _audio_dur_8 = 2.00  # [audio-sync] actual TTS duration
        # Step 9
        self.play(Write(self.objects["explanation_text"]), run_time=4.0)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))