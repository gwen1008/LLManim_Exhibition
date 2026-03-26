'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between the unit circle definition of sine and its Cartesian graph.
# 2. Layout Strategy: Left-right split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: Left side for unit circle, right side for sine graph.
#    - Footer Region: [Bottom y=-3.5] for real-time numerical feedback.
# 3. Anti-Overlap Check: Keep circle and graph in separate halves. Use ValueTracker for synchronization.
# 4. Audio Check (CRITICAL):
#    - [ ] Have I included self.add_sound() for EVERY step? (Audio paths not provided in JSON, will be omitted)
# 5. Animation Flow: Build circle and axes, then animate a point moving around the circle while projecting its y-coordinate to trace the sine wave.
'''

from manim import *
import numpy as np

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        # Left side: Unit Circle
        circle_center = LEFT * 3
        circle_radius = 1.5
        unit_circle = Circle(radius=circle_radius, color=WHITE).move_to(circle_center)
        circle_axes = VGroup(
            Line(LEFT * circle_radius * 1.2, RIGHT * circle_radius * 1.2, stroke_width=1),
            Line(DOWN * circle_radius * 1.2, UP * circle_radius * 1.2, stroke_width=1)
        ).move_to(circle_center)

        # Right side: Sine Graph Axes
        axes = Axes(
            x_range=[0, 2 * PI + 0.5, PI/2],
            y_range=[-1.5, 1.5, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": GREY},
            tips=False
        ).to_edge(RIGHT)
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("\\sin(x)")

        # Title
        title = Text("正弦函數：從單位圓到圖形", font_size=36, color=BLUE_C).to_edge(UP)

        # Footer for angle display
        angle_label = Text("角度 θ = ", font_size=24, color=WHITE).to_edge(DOWN).shift(LEFT * 2)
        angle_value = DecimalNumber(0, num_decimal_places=2, font_size=24, color=YELLOW).next_to(angle_label, RIGHT)
        angle_group = VGroup(angle_label, angle_value)

        # Shared ValueTracker for synchronization
        theta = ValueTracker(0)

        # Dynamic objects defined with always_redraw
        # Point on unit circle
        circle_point = always_redraw(lambda: Dot(
            point=circle_center + circle_radius * np.array([np.cos(theta.get_value()), np.sin(theta.get_value()), 0]),
            color=RED
        ))
        # Radius line
        radius_line = always_redraw(lambda: Line(
            circle_center,
            circle_point.get_center(),
            color=YELLOW,
            stroke_width=2
        ))
        # Angle arc
        angle_arc = always_redraw(lambda: Arc(
            radius=0.4,
            start_angle=0,
            angle=theta.get_value(),
            color=ORANGE,
            arc_center=circle_center
        ))
        # Point on sine graph
        graph_point = always_redraw(lambda: Dot(
            point=axes.c2p(theta.get_value(), np.sin(theta.get_value())),
            color=RED
        ))
        # Projection line (dashed)
        projection_line = always_redraw(lambda: DashedLine(
            start=circle_point.get_center(),
            end=graph_point.get_center(),
            color=BLUE_A,
            stroke_width=2
        ))
        # Traced path of sine wave
        trace = TracedPath(graph_point.get_center, dissipating_time=None, stroke_color=RED, stroke_width=4)

        # Update angle display
        angle_value.add_updater(lambda d: d.set_value(theta.get_value()))

        # Store objects in registry (though we will add them directly in sequence)
        self.objects = {
            "title": title,
            "unit_circle": unit_circle,
            "circle_axes": circle_axes,
            "axes": axes,
            "x_label": x_label,
            "y_label": y_label,
            "angle_group": angle_group,
            "circle_point": circle_point,
            "radius_line": radius_line,
            "angle_arc": angle_arc,
            "graph_point": graph_point,
            "projection_line": projection_line,
            "trace": trace,
        }

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1: Introduce title and unit circle
        self.play(Write(title), run_time=1.5)
        self.wait(max(0.1, 0.5))

        # Step 2: Show unit circle and its axes
        self.play(Create(unit_circle), Create(circle_axes), run_time=2)
        self.wait(max(0.1, 0.5))

        # Step 3: Show sine graph axes
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        self.wait(max(0.1, 0.5))

        # Step 4: Show angle display
        self.play(FadeIn(angle_group), run_time=1)
        self.wait(max(0.1, 0.5))

        # Step 5: Introduce the moving point and radius on the circle
        self.play(Create(radius_line), Create(angle_arc), FadeIn(circle_point), run_time=2)
        self.wait(max(0.1, 0.5))

        # Step 6: Show the corresponding point on the sine graph and the projection line
        self.play(FadeIn(graph_point), Create(projection_line), run_time=2)
        self.wait(max(0.1, 0.5))

        # Step 7: Start tracing and animate one full revolution
        self.add(trace)
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=8,
            rate_func=linear
        )
        self.wait(max(0.1, 2))