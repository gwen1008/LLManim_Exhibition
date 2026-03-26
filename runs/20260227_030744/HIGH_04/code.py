from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        slope_display_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Derivative as Slope: y = 0.5x²", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 9, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            color=GRAY_B
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes
        
        # parabola - defined as a graph on the axes
        parabola = axes.plot(lambda x: 0.5 * x**2, x_range=[-4, 4], color=BLUE, stroke_width=4)
        self.objects["parabola"] = parabola
        
        # moving_point - initial position at x=-3
        moving_point = Dot(radius=0.08, color=YELLOW, fill_opacity=1.0)
        moving_point.move_to(axes.c2p(-3, 0.5 * (-3)**2))
        self.objects["moving_point"] = moving_point
        
        # tangent_line - placeholder, will be updated via always_redraw
        tangent_line = Line(start=ORIGIN, end=RIGHT*0.1, color=RED, stroke_width=4)
        self.objects["tangent_line"] = tangent_line
        
        # slope_formula_label
        slope_formula_label = MathTex(r"y' = x", color=GREEN, font_size=36)
        slope_formula_label.move_to(slope_display_anchor).shift(LEFT * 3)
        self.objects["slope_formula_label"] = slope_formula_label
        
        # dynamic_slope_value - initial text
        dynamic_slope_value = MathTex(r"x = -3.00,\quad \text{slope} = -3.00", color=YELLOW, font_size=36)
        dynamic_slope_value.move_to(slope_display_anchor).shift(RIGHT * 1.5)
        self.objects["dynamic_slope_value"] = dynamic_slope_value
        
        # Create ValueTracker for x-coordinate as per implementation_hints
        x_tracker = ValueTracker(-3.0)
        self.objects["x_tracker"] = x_tracker
        
        # Set up updaters for dynamic objects
        # moving_point updater
        moving_point.add_updater(lambda m: m.move_to(axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)))
        
        # tangent_line updater using always_redraw
        def update_tangent_line():
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x
            # Adjust line length to avoid overlap with parabola
            dx = 0.8  # Reduced from 1.0 to make line shorter
            start_point = axes.c2p(x - dx, y - slope * dx)
            end_point = axes.c2p(x + dx, y + slope * dx)
            return Line(start=start_point, end=end_point, color=RED, stroke_width=4)
        
        # Replace placeholder with always_redraw version
        tangent_line_always = always_redraw(update_tangent_line)
        self.objects["tangent_line"] = tangent_line_always
        
        # dynamic_slope_value updater using always_redraw
        def update_slope_value():
            x = x_tracker.get_value()
            return MathTex(f"x = {x:.2f},\\quad \\text{{slope}} = {x:.2f}", color=YELLOW, font_size=36).move_to(slope_display_anchor).shift(RIGHT * 1.5)
        
        slope_value_always = always_redraw(update_slope_value)
        self.objects["dynamic_slope_value"] = slope_value_always
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1: Create axes
        audio_step1 = "media/audio/Create_an_animation__e3e114d6bc/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_1 = max(0.1, 5.808 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2: Create parabola, indicate it
        audio_step2 = "media/audio/Create_an_animation__e3e114d6bc/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["parabola"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parabola"]), run_time=2.5)
        remaining_2 = max(0.1, 4.536 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3: Create moving point and tangent line, indicate point
        audio_step3 = "media/audio/Create_an_animation__e3e114d6bc/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["moving_point"], color=YELLOW, run_time=1))
        self.add(self.objects["tangent_line"], self.objects["dynamic_slope_value"])
        self.play(FadeIn(self.objects["moving_point"]), run_time=1.5)
        remaining_3 = max(0.1, 11.328 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4: Write derivative formula and initial slope value, circumscribe formula
        audio_step4 = "media/audio/Create_an_animation__e3e114d6bc/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["slope_formula_label"], color=GREEN, run_time=1))
        self.play(Write(self.objects["slope_formula_label"]), run_time=1.5)
        self.play(Write(self.objects["dynamic_slope_value"]), run_time=1.5)
        remaining_4 = max(0.1, 10.008 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5: Indicate dynamic value, then animate point moving from x=-3 to 3
        audio_step5 = "media/audio/Create_an_animation__e3e114d6bc/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["dynamic_slope_value"], color=YELLOW, run_time=1))
        self.play(x_tracker.animate.set_value(3), run_time=8, rate_func=linear)
        remaining_5 = max(0.1, 12.264 - 9.0 + 0.5)
        self.wait(max(0.1, remaining_5))