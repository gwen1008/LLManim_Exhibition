from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_an_animation__488174d73b/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        info_panel_anchor = DOWN * 2.5  # Fixed: moved up to ensure full visibility
        
        # Create objects from layout_plan.objects
        # title
        title = MathTex(r"y = \frac{1}{2}x^2", color=BLUE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes
        
        # parabola
        parabola = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=4)
        parabola.move_to(graph_anchor)
        self.objects["parabola"] = parabola
        
        # moving_dot (initial position at x=-3)
        moving_dot = Dot(radius=0.08, color=YELLOW)
        moving_dot.move_to(axes.c2p(-3, 0.5 * (-3)**2))
        self.objects["moving_dot"] = moving_dot
        
        # dot_label
        dot_label = MathTex(r"P", color=YELLOW, font_size=36)
        dot_label.next_to(moving_dot, UP+RIGHT, buff=0.1)
        self.objects["dot_label"] = dot_label
        
        # tangent_line (initial dummy line, will be updated)
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=3)
        tangent_line.move_to(graph_anchor)
        self.objects["tangent_line"] = tangent_line
        
        # slope_label (initial, will be updated)
        slope_label = MathTex(r"m = x", color=GREEN, font_size=36)
        slope_label.next_to(moving_dot, UP+LEFT, buff=0.5)
        self.objects["slope_label"] = slope_label
        
        # info_panel_bg
        info_panel_bg = Rectangle(width=9, height=1.2, color="#222222", fill_opacity=0.8, stroke_width=2, stroke_color=WHITE)
        info_panel_bg.move_to(info_panel_anchor)
        self.objects["info_panel_bg"] = info_panel_bg
        
        # info_x_label (initial)
        info_x_label = MathTex(r"x = -3.00", color=YELLOW, font_size=32)
        info_x_label.move_to(info_panel_anchor + LEFT*3)
        self.objects["info_x_label"] = info_x_label
        
        # info_slope_label (initial)
        info_slope_label = MathTex(r"\mathrm{Slope} = -3.00", color=GREEN, font_size=32)
        info_slope_label.move_to(info_panel_anchor)
        self.objects["info_slope_label"] = info_slope_label
        
        # info_eq_label
        info_eq_label = MathTex(r"y' = x", color=RED, font_size=32)
        info_eq_label.move_to(info_panel_anchor + RIGHT*3)
        self.objects["info_eq_label"] = info_eq_label
        
        # ValueTracker for x-coordinate
        x_tracker = ValueTracker(-3.0)
        self.x_tracker = x_tracker
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/tangent_line_derivative/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["title"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["title"]), run_time=1.0)
        remaining_1 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/tangent_line_derivative/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["axes"]), run_time=1.5)
        remaining_2 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/tangent_line_derivative/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["parabola"], color=BLUE, run_time=1))
        self.play(Create(self.objects["parabola"]), run_time=2.0)
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/tangent_line_derivative/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["moving_dot"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["moving_dot"]), Write(self.objects["dot_label"]), run_time=1.5)
        remaining_4 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/tangent_line_derivative/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Define updaters for tangent line and slope label before animating
        line_length = 4.0
        def update_tangent_line(line):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative
            point = axes.c2p(x, y)
            # direction vector for line
            dx = 1.0
            dy = slope * dx
            dir_vec = np.array([dx, dy, 0])
            dir_vec = dir_vec / np.linalg.norm(dir_vec) * line_length / 2
            start = point - dir_vec
            end = point + dir_vec
            line.put_start_and_end_on(start, end)
        
        # Define functions that create fresh labels
        def make_slope_label():
            x = x_tracker.get_value()
            label = MathTex(f"m = {x:.2f}", color=GREEN, font_size=36)
            label.next_to(self.objects["moving_dot"], UP+LEFT, buff=0.5)
            return label
        
        def make_info_x_label():
            x = x_tracker.get_value()
            label = MathTex(f"x = {x:.2f}", color=YELLOW, font_size=32)
            label.move_to(info_panel_anchor + LEFT*3)
            return label
        
        def make_info_slope_label():
            x = x_tracker.get_value()
            label = MathTex(f"\\mathrm{{Slope}} = {x:.2f}", color=GREEN, font_size=32)
            label.move_to(info_panel_anchor)
            return label
        
        def update_dot(dot):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            dot.move_to(axes.c2p(x, y))
        
        def update_dot_label(label):
            label.next_to(self.objects["moving_dot"], UP+RIGHT, buff=0.1)
        
        # Replace the original labels with always_redraw versions
        self.remove(self.objects["slope_label"])
        self.objects["slope_label"] = always_redraw(make_slope_label)
        self.add(self.objects["slope_label"])
        
        self.remove(self.objects["info_x_label"])
        self.objects["info_x_label"] = always_redraw(make_info_x_label)
        self.add(self.objects["info_x_label"])
        
        self.remove(self.objects["info_slope_label"])
        self.objects["info_slope_label"] = always_redraw(make_info_slope_label)
        self.add(self.objects["info_slope_label"])
        
        # Add updaters (only for non-become updaters)
        self.objects["tangent_line"].add_updater(update_tangent_line)
        self.objects["moving_dot"].add_updater(update_dot)
        self.objects["dot_label"].add_updater(update_dot_label)
        
        # Force initial update
        update_tangent_line(self.objects["tangent_line"])
        
        self.play(Indicate(self.objects["tangent_line"], color=RED, run_time=1))
        self.play(Create(self.objects["tangent_line"]), run_time=2.0)
        remaining_5 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/tangent_line_derivative/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Create info panel background and labels
        self.play(FadeIn(self.objects["info_panel_bg"]), run_time=0.5)
        self.play(Circumscribe(self.objects["info_eq_label"], color=RED, run_time=1))
        self.play(Write(self.objects["info_eq_label"]), Write(self.objects["info_x_label"]), Write(self.objects["info_slope_label"]), run_time=2.5)
        remaining_6 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/tangent_line_derivative/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["slope_label"], color=GREEN, run_time=1))
        self.play(Write(self.objects["slope_label"]), run_time=2.0)
        remaining_7 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/tangent_line_derivative/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Animate the ValueTracker
        self.play(x_tracker.animate.set_value(3.0), run_time=5.0, rate_func=linear)
        self.play(x_tracker.animate.set_value(-3.0), run_time=5.0, rate_func=linear)
        remaining_8 = max(0.1, 10.0 - 10.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # Cleanup updaters
        self.objects["tangent_line"].clear_updaters()
        self.objects["slope_label"].clear_updaters()
        self.objects["moving_dot"].clear_updaters()
        self.objects["dot_label"].clear_updaters()
        self.objects["info_x_label"].clear_updaters()
        self.objects["info_slope_label"].clear_updaters()
        self.wait(3)  # [Auto-injected by Shift-Left Repair]