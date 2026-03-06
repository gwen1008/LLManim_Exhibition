from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        # === SKELETON: DO NOT CHANGE THIS ARCHITECTURE ===
        theta = ValueTracker(0)
        TWO_PI = 2 * np.pi

        # --- LEFT: Unit Circle ---
        circle_center = LEFT * 3
        circle = Circle(radius=2, color=BLUE).move_to(circle_center)
        circle_dot = always_redraw(lambda: Dot(
            circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            color=RED
        ))
        radius_line = always_redraw(lambda: Line(
            circle_center,
            circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            color=WHITE
        ))

        # --- RIGHT: Sine Graph ---
        axes = Axes(
            x_range=[0, TWO_PI, np.pi/2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5, y_length=3,
        ).move_to(RIGHT * 3)
        sine_curve = axes.plot(lambda x: np.sin(x), x_range=[0, TWO_PI], color=YELLOW)
        graph_dot = always_redraw(lambda: Dot(
            axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=RED
        ))
        proj_line = always_redraw(lambda: DashedLine(
            circle_center + 2 * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=GRAY, stroke_width=1
        ))

        # === Setup ===
        # Step 0: Add audio for initial setup
        self.add_sound("media/audio/Create_a_Manim_anima_873bad1e37/step_00.mp3")
        self.play(Create(circle), Create(axes))
        
        # Step 1: Add audio for sine curve creation
        self.add_sound("media/audio/Create_a_Manim_anima_873bad1e37/step_01.mp3")
        self.play(Create(sine_curve), run_time=2)
        
        # Step 2: Add audio for adding dots and lines
        self.add_sound("media/audio/Create_a_Manim_anima_873bad1e37/step_02.mp3")
        self.add(circle_dot, radius_line, graph_dot, proj_line)

        # === Main animation: ONE ValueTracker drives ALL movement ===
        # Step 3: Add audio for main animation
        self.add_sound("media/audio/Create_a_Manim_anima_873bad1e37/step_03.mp3")
        self.play(theta.animate.set_value(TWO_PI), run_time=8, rate_func=linear)
        self.wait(1)