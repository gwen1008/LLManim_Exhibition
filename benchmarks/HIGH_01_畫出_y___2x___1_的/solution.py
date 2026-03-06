from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Object Creation ==========
        self.objects = {}
        
        # Title
        title = Text("Graphing y = 2x - 1: Understanding Slope", color=WHITE, font_size=36)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title
        
        # Plane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"stroke_opacity": 1},
            background_line_style={"stroke_opacity": 0.2}
        )
        plane.move_to(ORIGIN)
        self.objects["plane"] = plane
        
        # Axes
        axes = Axes(
            x_range=[-5, 5],
            y_range=[-5, 5],
            x_length=10,
            y_length=10,
            color=WHITE
        )
        axes.move_to(ORIGIN)
        self.objects["axes"] = axes
        
        # Line Full
        line_full = axes.plot(lambda x: 2*x - 1, x_range=[-2, 3], color=BLUE, stroke_width=4)
        self.objects["line_full"] = line_full
        
        # Intercept Dot
        intercept_dot = Dot(point=axes.c2p(0, -1), radius=0.08, color=YELLOW)
        self.objects["intercept_dot"] = intercept_dot
        
        # Intercept Label
        intercept_label = MathTex("(0, -1)", color=YELLOW, font_size=24)
        intercept_label.next_to(intercept_dot, UP + LEFT, buff=0.1)
        self.objects["intercept_label"] = intercept_label
        
        # Points for triangle (initially invisible)
        p0 = Dot(point=axes.c2p(0, -1), radius=0.05, color=WHITE)
        p0.set_opacity(0.0)
        p1 = Dot(point=axes.c2p(1, -1), radius=0.05, color=WHITE)
        p1.set_opacity(0.0)
        p2 = Dot(point=axes.c2p(1, 1), radius=0.05, color=WHITE)
        p2.set_opacity(0.0)
        self.objects["p0"] = p0
        self.objects["p1"] = p1
        self.objects["p2"] = p2
        
        # Triangle
        triangle = Polygon(
            axes.c2p(0, -1),
            axes.c2p(1, -1),
            axes.c2p(1, 1),
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=3,
            stroke_color=GREEN
        )
        self.objects["triangle"] = triangle
        
        # Run Arrow
        run_arrow = Arrow(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, -1),
            color=RED,
            stroke_width=4,
            buff=0
        )
        self.objects["run_arrow"] = run_arrow
        
        # Rise Arrow
        rise_arrow = Arrow(
            start=axes.c2p(1, -1),
            end=axes.c2p(1, 1),
            color=RED,
            stroke_width=4,
            buff=0
        )
        self.objects["rise_arrow"] = rise_arrow
        
        # Run Label
        run_label = MathTex("\\text{run}=1", color=RED, font_size=24)
        run_label.next_to(run_arrow, DOWN, buff=0.1)
        self.objects["run_label"] = run_label
        
        # Rise Label
        rise_label = MathTex("\\text{rise}=2", color=RED, font_size=24)
        rise_label.next_to(rise_arrow, RIGHT, buff=0.1)
        self.objects["rise_label"] = rise_label
        
        # Hypotenuse
        hypotenuse = Line(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, 1),
            color=ORANGE,
            stroke_width=5
        )
        self.objects["hypotenuse"] = hypotenuse
        
        # Slope Label
        slope_label = MathTex("\\text{slope} = \\frac{\\text{rise}}{\\text{run}} = \\frac{2}{1} = 2", 
                             color=YELLOW, font_size=30)
        slope_label.to_edge(DOWN, buff=0.5).shift(UP * 0.5)
        self.objects["slope_label"] = slope_label
        
        # Step Explanation
        step_explanation = Text("Step 1: Set up the coordinate plane and equation.", 
                               color=LIGHT_GRAY, font_size=24)
        step_explanation.to_edge(DOWN, buff=0.5)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        audio_file = "media/audio/畫出_y_=_2x_-_1_的函數圖形。用「階梯動畫（Rise_Run）」呈現這條線的斜率是_2。/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(self.objects["plane"]), run_time=2)
        self.wait(6.816 - 2)
        
        # Step 2
        audio_file = "media/audio/畫出_y_=_2x_-_1_的函數圖形。用「階梯動畫（Rise_Run）」呈現這條線的斜率是_2。/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(self.objects["title"], color=YELLOW), run_time=1)
        self.play(Write(self.objects["title"]), run_time=1)
        self.play(Create(self.objects["axes"]), run_time=1)
        self.play(Create(self.objects["intercept_dot"]), run_time=1)
        self.play(Write(self.objects["intercept_label"]), run_time=1)
        
        new_explanation = Text("Step 2: Identify the y-intercept at (0, -1).", 
                              color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(self.objects["step_explanation"].get_center())
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=1)
        self.objects["step_explanation"] = new_explanation
        self.wait(8.976 - 5)
        
        # Step 3
        audio_file = "media/audio/畫出_y_=_2x_-_1_的函數圖形。用「階梯動畫（Rise_Run）」呈現這條線的斜率是_2。/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Circumscribe(self.objects["intercept_dot"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["run_arrow"]), run_time=1)
        self.play(Write(self.objects["run_label"]), run_time=1)
        self.play(Create(self.objects["rise_arrow"]), run_time=1)
        self.play(Write(self.objects["rise_label"]), run_time=1)
        self.play(Create(self.objects["triangle"]), run_time=1)
        
        new_explanation = Text("Step 3: Construct the slope triangle: run=1, rise=2.", 
                              color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(self.objects["step_explanation"].get_center())
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=1)
        self.objects["step_explanation"] = new_explanation
        self.wait(12.744 - 6)
        
        # Step 4
        audio_file = "media/audio/畫出_y_=_2x_-_1_的函數圖形。用「階梯動畫（Rise_Run）」呈現這條線的斜率是_2。/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(self.objects["hypotenuse"], color=ORANGE), run_time=1)
        self.play(Create(self.objects["hypotenuse"]), run_time=1)
        
        # Transform hypotenuse to full line
        self.play(Transform(self.objects["hypotenuse"], self.objects["line_full"]), run_time=2)
        self.play(Write(self.objects["slope_label"]), run_time=1)
        
        new_explanation = Text("Step 4: The hypotenuse defines the slope. Extending it draws the line y=2x-1.", 
                              color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(self.objects["step_explanation"].get_center())
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=1)
        self.objects["step_explanation"] = new_explanation
        self.wait(13.224 - 5)
        
        # Step 5
        audio_file = "media/audio/畫出_y_=_2x_-_1_的函數圖形。用「階梯動畫（Rise_Run）」呈現這條線的斜率是_2。/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(self.objects["line_full"], color=BLUE), run_time=1)
        
        # Create a copy of the triangle group and slide it
        triangle_group = VGroup(
            self.objects["triangle"].copy(),
            self.objects["run_arrow"].copy(),
            self.objects["rise_arrow"].copy(),
            self.objects["run_label"].copy(),
            self.objects["rise_label"].copy()
        )
        self.add(triangle_group)
        
        # Calculate new position (shift right 2 and up 4 to stay on line)
        self.play(
            triangle_group.animate.shift(RIGHT * 2 + UP * 4),
            run_time=2
        )
        self.wait(11.136 - 3)