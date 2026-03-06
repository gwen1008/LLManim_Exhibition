'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the derivative of y=0.5x² as the slope of a moving tangent line.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for axes and parabola
#    - Footer Region: [Bottom y=-3.5] for dynamic slope display
# 3. Anti-Overlap Check:
#    - Strategy: Use distinct zones. Labels placed in UR corner. Slope display at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create parabola, signal function label.
#    - Step 3: Write function/derivative labels, signal derivative.
#    - Step 4: Create moving dot and tangent line, signal dot.
#    - Step 5: Animate dot moving via ValueTracker, signal slope value.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        global_center = ORIGIN
        title_anchor = 3.5 * UP
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Tex("Derivative as Slope of a Tangent Line", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            color=GRAY_B
        )
        axes.move_to(global_center)
        self.objects["axes"] = axes
        
        # parabola
        parabola = axes.plot(lambda x: 0.5 * x**2, x_range=[-4, 4], color=BLUE, stroke_width=4)
        self.objects["parabola"] = parabola
        
        # moving_dot (initial position at x=-4)
        moving_dot = Dot(radius=0.08, color=YELLOW, z_index=2)
        moving_dot.move_to(axes.c2p(-4, 0.5 * (-4)**2))
        self.objects["moving_dot"] = moving_dot
        
        # tangent_line (initial dummy line, updater will set endpoints)
        tangent_line = Line(LEFT, RIGHT, color=YELLOW, stroke_width=3, z_index=1)
        self.objects["tangent_line"] = tangent_line
        
        # slope_label_static
        slope_label_static = Tex(r"Slope of Tangent Line, \, y' = ", color=WHITE, font_size=32)
        slope_label_static.move_to(footer_anchor + LEFT * 1.5)
        self.objects["slope_label_static"] = slope_label_static
        
        # slope_value
        slope_value = DecimalNumber(0.00, color=YELLOW, font_size=32, num_decimal_places=2)
        slope_value.next_to(slope_label_static, RIGHT, buff=0.3)
        self.objects["slope_value"] = slope_value
        
        # function_label
        function_label = MathTex(r"y = 0.5x^2", color=BLUE, font_size=28)
        function_label.move_to(axes.get_corner(UR) + LEFT * 2 + DOWN * 0.5)
        self.objects["function_label"] = function_label
        
        # derivative_label
        derivative_label = MathTex(r"y' = x", color=YELLOW, font_size=28)
        derivative_label.next_to(function_label, DOWN, aligned_edge=LEFT, buff=0.3)
        self.objects["derivative_label"] = derivative_label
        
        # ValueTracker for x-coordinate
        x_tracker = ValueTracker(-4.0)
        
        # Updaters for dynamic objects
        moving_dot.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)))
        
        tangent_line.add_updater(lambda l: l.put_start_and_end_on(
            axes.c2p(x_tracker.get_value() - 2, 0.5 * x_tracker.get_value()**2 - 2 * x_tracker.get_value()),
            axes.c2p(x_tracker.get_value() + 2, 0.5 * x_tracker.get_value()**2 + 2 * x_tracker.get_value())
        ))
        
        slope_value.add_updater(lambda d: d.set_value(x_tracker.get_value()))
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Create_an_animation__cc4579ed50/step_00.mp3")  # [auto-injected] duration=5.59s
        _audio_dur_0 = 5.59  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Create_an_animation__cc4579ed50/step_01.mp3")  # [auto-injected] duration=2.83s
        _audio_dur_1 = 2.83  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Circumscribe(self.objects["function_label"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parabola"]), run_time=3.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Create_an_animation__cc4579ed50/step_02.mp3")  # [auto-injected] duration=9.41s
        _audio_dur_2 = 9.41  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Indicate(self.objects["derivative_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["function_label"]), Write(self.objects["derivative_label"]), run_time=4.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Create_an_animation__cc4579ed50/step_03.mp3")  # [auto-injected] duration=8.16s
        _audio_dur_3 = 8.16  # [audio-sync] actual TTS duration
        # Step 4
        self.play(GrowFromCenter(self.objects["moving_dot"]), run_time=1)
        self.play(Create(self.objects["tangent_line"]), Write(self.objects["slope_label_static"]), Write(self.objects["slope_value"]), run_time=3.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Create_an_animation__cc4579ed50/step_04.mp3")  # [auto-injected] duration=16.49s
        _audio_dur_4 = 16.49  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Indicate(self.objects["slope_value"], color=YELLOW, run_time=1))
        self.play(x_tracker.animate.set_value(4.0), run_time=10.0, rate_func=linear)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))