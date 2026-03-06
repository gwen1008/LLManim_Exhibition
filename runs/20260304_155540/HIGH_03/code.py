'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between a point moving on a unit circle and the corresponding point on the sine wave graph y = sin(x).
# 2. Layout Strategy:
#    - Header Region: Not used for this scene.
#    - Main Content: Left side for unit circle, right side for sine graph.
#    - Footer Region: Not used for this scene.
# 3. Anti-Overlap Check:
#    - Strategy: Place circle on left (x=-3), axes on right (x=3). Use ValueTracker to synchronize all dynamic elements.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [ ] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? (JSON duration not provided, using default run_time)
# 5. Animation Flow:
#    - Setup static elements (circle, axes).
#    - Create dynamic elements (dots, lines, arc, trace) using always_redraw.
#    - Animate the angle from 0 to 2π to show the synchronized motion.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"

        # ========== PHASE 1: Layout & Object Creation ==========
        # 1. Define Anchors
        unit_circle_center = LEFT * 3
        radius = 1.5

        # 2. Create Static Objects
        # Left: Unit Circle System
        circle = Circle(radius=radius, color=WHITE).move_to(unit_circle_center)
        circle_axes = VGroup(
            Line(LEFT * radius * 1.2, RIGHT * radius * 1.2, stroke_width=1),
            Line(DOWN * radius * 1.2, UP * radius * 1.2, stroke_width=1)
        ).move_to(unit_circle_center)

        # Right: Sine Graph Axes
        axes = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=7,
            y_length=4,
            axis_config={"color": GREY},
            tips=False
        ).to_edge(RIGHT)
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("\\sin(x)")

        # 3. Core Driver: Angle Theta
        theta = ValueTracker(0)

        # 4. Define Dynamic Objects with always_redraw
        # A. Point on circle
        def get_circle_point():
            return unit_circle_center + radius * np.array([
                np.cos(theta.get_value()),
                np.sin(theta.get_value()),
                0
            ])

        point_on_circle = always_redraw(
            lambda: Dot(get_circle_point(), color=RED)
        )

        # B. Radius line from circle center to point
        radius_line = always_redraw(
            lambda: Line(unit_circle_center, point_on_circle.get_center(), color=YELLOW)
        )

        # C. Angle arc
        angle_arc = always_redraw(
            lambda: Arc(
                radius=0.4,
                start_angle=0,
                angle=theta.get_value(),
                color=ORANGE,
                arc_center=unit_circle_center
            )
        )

        # D. Point on sine graph
        def get_graph_point():
            angle = theta.get_value()
            return axes.c2p(angle, np.sin(angle))

        point_on_graph = always_redraw(
            lambda: Dot(get_graph_point(), color=RED)
        )

        # E. Projection line connecting the two points
        projection_line = always_redraw(
            lambda: DashedLine(
                point_on_circle.get_center(),
                point_on_graph.get_center(),
                color=BLUE_A,
                stroke_width=2
            )
        )

        # F. Traced path on the sine graph
        trace = TracedPath(point_on_graph.get_center, dissipating_time=None, stroke_color=RED, stroke_width=4)

        # Store objects in a registry (though not heavily used here)
        self.objects = {
            "circle": circle,
            "circle_axes": circle_axes,
            "axes": axes,
            "x_label": x_label,
            "y_label": y_label,
            "point_on_circle": point_on_circle,
            "radius_line": radius_line,
            "angle_arc": angle_arc,
            "point_on_graph": point_on_graph,
            "projection_line": projection_line,
            "trace": trace,
        }

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1: Show static elements
        self.play(
            Create(circle),
            Create(circle_axes),
            run_time=2
        )
        remaining_1 = max(0.1, 3.0 - 2.0 + 0.5)  # Assume 3.0s audio
        self.wait(max(0.1, remaining_1))

        # Step 2: Show axes
        self.play(
            Write(axes),
            Write(x_label),
            Write(y_label),
            run_time=2
        )
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3: Introduce dynamic elements on circle
        self.play(
            Create(point_on_circle),
            Create(radius_line),
            Create(angle_arc),
            run_time=2
        )
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4: Introduce projection and graph point
        self.play(
            Create(projection_line),
            Create(point_on_graph),
            run_time=2
        )
        remaining_4 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5: Start trace and animate full rotation
        self.add(trace)
        self.play(
            theta.animate.set_value(2 * PI),
            run_time=8,
            rate_func=linear
        )
        remaining_5 = max(0.1, 9.0 - 8.0 + 0.5)  # Assume 9.0s audio for final sweep
        self.wait(max(0.1, remaining_5))