from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # 1. Create static elements
        # Define anchors
        title_anchor = UP * 3.2
        circle_anchor = LEFT * 4 + DOWN * 0.5
        comparison_anchor = RIGHT * 3 + DOWN * 0.5
        explanation_anchor = DOWN * 2.8
        
        # Create title
        title = Text("Unfolding a Circle: Circumference and π", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        
        # Create circle with diameter D=4 (radius=2)
        circle = Circle(radius=2, color="#1E90FF", stroke_width=4)
        circle.move_to(circle_anchor)
        
        # Create diameter line
        diameter_line = Line(LEFT*2, RIGHT*2, color="#FF6B6B", stroke_width=6)
        diameter_line.move_to(circle_anchor)
        
        # Create diameter label
        label_d = MathTex("D", color="#FF6B6B")
        label_d.next_to(diameter_line, UP, buff=0.2)
        
        # Create rolling path (dashed line)
        rolling_path = DashedLine(
            circle_anchor + DOWN*2.5 + LEFT*1,
            circle_anchor + DOWN*2.5 + RIGHT*13.566,
            color="GREY",
            stroke_width=2,
            stroke_opacity=0.7,
            dash_length=0.2
        )
        
        # Create trace point (yellow dot)
        trace_point = Dot(radius=0.08, color=YELLOW)
        trace_point.move_to(circle_anchor + RIGHT*2)  # Start at rightmost point
        
        # Create circumference trace as a cycloid (pre-calculated)
        # Parametric equation for a cycloid: x = r(θ - sinθ), y = -r(1 - cosθ)
        # Starting from rightmost point, moving right
        circumference_trace = ParametricFunction(
            lambda t: circle_anchor + np.array([
                2 * (t - np.sin(t)) - 2,  # x: shift so it starts at 0
                -2 * (1 - np.cos(t)) - 0.5,  # y: align with circle center
                0
            ]),
            t_range=[0, 2*np.pi],
            color="#1E90FF",
            stroke_width=5
        )
        
        # Create straight circumference line for comparison
        line_circumference = Line(
            LEFT*6.283, RIGHT*6.283, 
            color="#1E90FF", 
            stroke_width=6
        )
        line_circumference.move_to(comparison_anchor + UP*1.0)
        
        # Create label for circumference line
        label_c = MathTex("C = \\pi D", color="#1E90FF")
        label_c.next_to(line_circumference, UP, buff=0.3)
        
        # Create 3D line (three diameters end-to-end)
        line_3d = VGroup()
        for i in range(3):
            segment = Line(LEFT*2, RIGHT*2, color="#FF6B6B", stroke_width=6)
            segment.shift(RIGHT * (4 * i - 2))  # Position segments end-to-end
            line_3d.add(segment)
        line_3d.move_to(comparison_anchor + DOWN*0.5)
        
        # Create label for 3D line
        label_3d = MathTex("3D", color="#FF6B6B")
        label_3d.next_to(line_3d, DOWN, buff=0.3)
        
        # Create explanation text
        explanation_text = Text(
            "The circumference C is slightly longer than 3 times the diameter D.",
            color="LIGHT_GREY",
            font_size=28
        )
        explanation_text.move_to(explanation_anchor)
        
        # Create pi approximation
        pi_value = MathTex("\\pi \\approx 3.14159", color="YELLOW", font_size=36)
        pi_value.next_to(explanation_text, DOWN, buff=0.4)
        
        # Create final formula
        final_formula = MathTex("C = \\pi D", color="#1E90FF", font_size=40)
        final_formula.next_to(pi_value, DOWN, buff=0.4)
        
        # 2. Build the main diagram step-by-step with audio synchronization
        
        # Step 1: Show circle
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_01.mp3")
        self.play(Create(circle), run_time=2)
        self.wait(0.5)
        
        # Step 2: Show diameter
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_02.mp3")
        self.play(Create(diameter_line), Write(label_d), run_time=2)
        self.wait(0.5)
        
        # Step 3: Show rolling path and trace point
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_03.mp3")
        self.play(Create(rolling_path), FadeIn(trace_point), run_time=2)
        self.wait(0.5)
        
        # Step 4: Animate rolling
        # Create a copy of the circle for rolling animation
        rolling_circle = circle.copy()
        self.add(rolling_circle, trace_point)
        
        # Animate rolling: translate by circumference length and rotate
        roll_animation = Succession(
            ApplyMethod(rolling_circle.shift, RIGHT * (2 * np.pi * 2)),  # 2πr = circumference
            ApplyMethod(rolling_circle.rotate, -2 * np.pi),  # Negative for clockwise rotation
            lag_ratio=0
        )
        
        # Animate trace point along the cycloid
        trace_animation = MoveAlongPath(trace_point, circumference_trace)
        
        # Create the trace as we go
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_04.mp3")
        self.play(
            roll_animation,
            trace_animation,
            Create(circumference_trace),
            run_time=4
        )
        self.wait(0.5)
        
        # Step 5: Transform trace to straight line
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_05.mp3")
        self.play(
            circumference_trace.animate.move_to(line_circumference.get_center()).rotate(
                angle=line_circumference.get_angle() - 0,  # Trace is initially horizontal
                about_point=line_circumference.get_center()
            ).stretch_to_fit_width(line_circumference.get_width()),
            Write(label_c),
            run_time=2
        )
        self.wait(0.5)
        
        # Step 6: Create 3D line
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_06.mp3")
        self.play(Create(line_3d), Write(label_3d), run_time=2)
        self.wait(0.5)
        
        # Step 7: Align and compare
        # Align left ends
        line_3d_target = line_3d.copy()
        line_3d_target.align_to(line_circumference, LEFT)
        
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_07.mp3")
        self.play(
            Transform(line_3d, line_3d_target),
            run_time=2
        )
        self.wait(0.5)
        
        # Step 8: Show pi approximation
        self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_08.mp3")
        self.play(Write(pi_value), run_time=2)
        self.wait(0.5)
        
        # Step 9: Show final formula
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_09.mp3")
        self.play(Write(final_formula), run_time=2)
        
        # Final wait with audio
        # [missing audio] self.add_sound("media/audio/Create_an_animation__e8423c56b5/step_10.mp3")
        self.wait(3)