'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the relationship between the unit circle and the sine function graph.
# 2. Layout Strategy: Split-screen with zones.
#    - Header Region: [y=3.5] for Title "Sine Function from the Unit Circle"
#    - Main Content: [Center y=0] Left column for unit circle, right column for sine graph.
#    - Footer Region: [Bottom y=-3.5] for explanation text.
# 3. Anti-Overlap Check: Use LayoutEngine to place Title, Content, and Footer in separate zones.
#    - Strategy: Use VGroups for composite objects (e.g., circle with axes).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/演示單位圓運動同步正弦波。左邊有一個點在單位圓上移動，右邊同步描繪出_y_=_sin(x)_的圖形。/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create unit circle.
#    - Step 2: Add faint axes to circle.
#    - Step 3: Create sine graph axes on the right.
#    - Step 4: Indicate point P, create projection line and point Q.
#    - Step 5: Indicate point Q, attach TracedPath, animate theta from 0 to 2π.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.objects = {}  # Registry for objects by ID

        # ========== PHASE 1: Layout & Object Creation ==========
        layout = LayoutEngine()

        # Create anchors as per layout_plan
        title_anchor = UP * 3.5
        left_anchor = LEFT * 3.5
        right_anchor = RIGHT * 3.5
        footer_anchor = DOWN * 3.5

        # Create objects from layout_plan.objects
        # title
        title = Text("Sine Function from the Unit Circle", color=WHITE, font_size=40)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # unit_circle
        unit_circle = Circle(radius=1.5, color=BLUE, stroke_width=3)
        unit_circle.move_to(left_anchor)
        obj_circle = LayoutObject(unit_circle, "unit_circle")
        layout.add(obj_circle)
        layout.add_to_zone(obj_circle, "CONTENT")
        self.objects["unit_circle"] = unit_circle

        # circle_axes
        circle_axes = Axes(
            x_range=[-1.8, 1.8, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=3.6,
            y_length=3.6,
            axis_config={"stroke_opacity": 0.5, "color": GREY}
        ).move_to(left_anchor)
        obj_circle_axes = LayoutObject(circle_axes, "circle_axes")
        layout.add(obj_circle_axes)
        layout.add_to_zone(obj_circle_axes, "CONTENT")
        self.objects["circle_axes"] = circle_axes

        # point_P (initial at θ=0, i.e., (1.5, 0) relative to left_anchor)
        point_P = Dot(radius=0.08, color=RED).move_to(left_anchor + RIGHT * 1.5)
        obj_point_P = LayoutObject(point_P, "point_P")
        layout.add(obj_point_P)
        layout.add_to_zone(obj_point_P, "CONTENT")
        self.objects["point_P"] = point_P

        # label_P
        label_P = MathTex(r"P(\cos\theta,\sin\theta)", color=RED, font_size=28)
        label_P.next_to(point_P, UP+RIGHT, buff=0.1)
        obj_label_P = LayoutObject(label_P, "label_P")
        layout.add(obj_label_P)
        layout.add_to_zone(obj_label_P, "CONTENT")
        self.objects["label_P"] = label_P

        # angle_arc (initial angle 0)
        angle_arc = Arc(radius=0.5, start_angle=0, angle=0, color=YELLOW, stroke_width=2)
        angle_arc.move_to(left_anchor)
        obj_angle_arc = LayoutObject(angle_arc, "angle_arc")
        layout.add(obj_angle_arc)
        layout.add_to_zone(obj_angle_arc, "CONTENT")
        self.objects["angle_arc"] = angle_arc

        # angle_label
        angle_label = MathTex(r"\theta = 0", color=YELLOW, font_size=28)
        angle_label.next_to(angle_arc, UP, buff=0.1)
        obj_angle_label = LayoutObject(angle_label, "angle_label")
        layout.add(obj_angle_label)
        layout.add_to_zone(obj_angle_label, "CONTENT")
        self.objects["angle_label"] = angle_label

        # sine_axes
        sine_axes = Axes(
            x_range=[0, 6.283, 1.571],
            y_range=[-1.2, 1.2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True, "color": WHITE}
        ).move_to(right_anchor)
        obj_sine_axes = LayoutObject(sine_axes, "sine_axes")
        layout.add(obj_sine_axes)
        layout.add_to_zone(obj_sine_axes, "CONTENT")
        self.objects["sine_axes"] = sine_axes

        # axes_label_x
        axes_label_x = MathTex(r"\theta\text{ (radians)}", color=WHITE, font_size=28)
        axes_label_x.next_to(sine_axes.x_axis.get_end(), DOWN)
        obj_axes_label_x = LayoutObject(axes_label_x, "axes_label_x")
        layout.add(obj_axes_label_x)
        layout.add_to_zone(obj_axes_label_x, "CONTENT")
        self.objects["axes_label_x"] = axes_label_x

        # axes_label_y
        axes_label_y = MathTex(r"\sin(\theta)", color=WHITE, font_size=28)
        axes_label_y.next_to(sine_axes.y_axis.get_top(), LEFT)
        obj_axes_label_y = LayoutObject(axes_label_y, "axes_label_y")
        layout.add(obj_axes_label_y)
        layout.add_to_zone(obj_axes_label_y, "CONTENT")
        self.objects["axes_label_y"] = axes_label_y

        # point_Q (initial at (0,0) on sine axes)
        point_Q = Dot(radius=0.08, color=RED).move_to(sine_axes.c2p(0, 0))
        obj_point_Q = LayoutObject(point_Q, "point_Q")
        layout.add(obj_point_Q)
        layout.add_to_zone(obj_point_Q, "CONTENT")
        self.objects["point_Q"] = point_Q

        # label_Q
        label_Q = MathTex(r"(\theta, \sin\theta)", color=RED, font_size=28)
        label_Q.next_to(point_Q, UP, buff=0.1)
        obj_label_Q = LayoutObject(label_Q, "label_Q")
        layout.add(obj_label_Q)
        layout.add_to_zone(obj_label_Q, "CONTENT")
        self.objects["label_Q"] = label_Q

        # explanation_text
        explanation_text = Text("The y-coordinate of point P is plotted against the angle θ.", color=LIGHT_GREY, font_size=30)
        obj_explanation = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == 0)
        self.objects["explanation_text"] = explanation_text

        # Solve layout constraints
        layout.solve()

        # Add objects that are initially visible (title, explanation)
        self.add(title, explanation_text)

        # ValueTracker for theta (angle)
        theta = ValueTracker(0)

        # Updaters for dynamic objects (defined here but added later)
        # point_P updater
        point_P.add_updater(lambda m: m.move_to(left_anchor + np.array([
            np.cos(theta.get_value()) * 1.5,
            np.sin(theta.get_value()) * 1.5,
            0
        ])))
        # label_P updater (follow point_P)
        label_P.add_updater(lambda m: m.next_to(self.objects["point_P"], UP+RIGHT, buff=0.1))
        # angle_arc updater
        angle_arc.add_updater(lambda m: m.become(Arc(
            radius=0.5,
            start_angle=0,
            angle=theta.get_value(),
            color=YELLOW,
            stroke_width=2,
            arc_center=left_anchor
        )))
        # angle_label updater
        angle_label.add_updater(lambda m: m.become(MathTex(
            f"\\theta = {theta.get_value():.2f}",
            color=YELLOW,
            font_size=28
        ).next_to(self.objects["angle_arc"], UP, buff=0.1)))
        # point_Q updater
        point_Q.add_updater(lambda m: m.move_to(sine_axes.c2p(
            theta.get_value(),
            np.sin(theta.get_value())
        )))
        # label_Q updater (follow point_Q)
        label_Q.add_updater(lambda m: m.next_to(self.objects["point_Q"], UP, buff=0.1))

        # projection_line (will be created in step 4)
        projection_line = DashedLine(
            start=left_anchor + RIGHT * 1.5,
            end=right_anchor + LEFT * 3,
            color=GREEN,
            stroke_width=2,
            dash_length=0.05
        )
        # projection_line updater (connects P to Q)
        projection_line.add_updater(lambda m: m.become(DashedLine(
            start=self.objects["point_P"].get_center(),
            end=self.objects["point_Q"].get_center(),
            color=GREEN,
            stroke_width=2,
            dash_length=0.05
        )))
        self.objects["projection_line"] = projection_line

        # sine_wave_trace (TracedPath attached to point_Q, added in step 5)
        sine_wave_trace = TracedPath(point_Q.get_center, stroke_color=YELLOW, stroke_width=4)
        self.objects["sine_wave_trace"] = sine_wave_trace

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start with the unit circle. A point P moves along its circumference.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "unit_circle", "details": "Draw the unit circle"},
                "duration": 5.472,
                "audio_path": "media/audio/演示單位圓運動同步正弦波。左邊有一個點在單位圓上移動，右邊同步描繪出_y_=_sin(x)_的圖形。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We add coordinate axes through the center. The point P has coordinates (cos θ, sin θ), where θ is the angle from the positive x-axis.",
                "signal_action": {"type": "Create", "target": "circle_axes"},
                "visual_action": {"type": "Create", "target_id": "circle_axes", "details": "Fade in the faint axes"},
                "duration": 10.296,
                "audio_path": "media/audio/演示單位圓運動同步正弦波。左邊有一個點在單位圓上移動，右邊同步描繪出_y_=_sin(x)_的圖形。/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, we introduce a graph on the right. Its horizontal axis represents the angle θ in radians, and its vertical axis represents the sine of θ.",
                "signal_action": {"type": "Create", "target": "sine_axes"},
                "visual_action": {"type": "Create", "target_id": "sine_axes", "details": "Draw the axes for the sine graph"},
                "duration": 10.44,
                "audio_path": "media/audio/演示單位圓運動同步正弦波。左邊有一個點在單位圓上移動，右邊同步描繪出_y_=_sin(x)_的圖形。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "As point P moves around the circle, we plot its y-coordinate, sin θ, against the angle θ on the right graph. This creates a new point, Q.",
                "signal_action": {"type": "Indicate", "target": "point_P", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "projection_line", "details": "Show the dashed projection line from P to Q (using an updater). Then create point Q."},
                "duration": 10.608,
                "audio_path": "media/audio/演示單位圓運動同步正弦波。左邊有一個點在單位圓上移動，右邊同步描繪出_y_=_sin(x)_的圖形。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Let's animate. As θ increases from 0 to 2π, point P moves around the circle, and point Q traces out the sine wave y = sin(x).",
                "signal_action": {"type": "Indicate", "target": "point_Q", "color": "RED"},
                "visual_action": {"type": "AddUpdater", "target_id": "sine_wave_trace", "details": "Attach a TracedPath to point_Q. Then animate the ValueTracker for theta from 0 to 2*PI over 10 seconds, moving both P and Q synchronously."},
                "duration": 10.296,
                "audio_path": "media/audio/演示單位圓運動同步正弦波。左邊有一個點在單位圓上移動，右邊同步描繪出_y_=_sin(x)_的圖形。/step_04.mp3"
            }
        ]

        for step in sequence:
            step_num = step["step"]
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects.get(target_id)
                if target_obj:
                    if signal["type"] == "Create":
                        # For signal_action of type Create, we just create the object (it's already added in layout)
                        pass  # Object already added in layout phase
                    elif signal["type"] == "Indicate":
                        self.play(Indicate(target_obj, color=RED), run_time=1)
                    elif signal["type"] == "Circumscribe":
                        self.play(Circumscribe(target_obj, color=YELLOW), run_time=1)
                    elif signal["type"] == "FocusOn":
                        self.play(FocusOn(target_obj), run_time=1)

            # Visual action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            target_obj = self.objects.get(target_id)

            if visual["type"] == "Create":
                if target_id == "projection_line":
                    # Add projection_line and point_Q, label_Q together
                    self.add(projection_line, point_Q, label_Q)
                    # Also add point_P and label_P if not already
                    if point_P not in self.mobjects:
                        self.add(point_P, label_P, angle_arc, angle_label)
                else:
                    self.play(Create(target_obj))
            elif visual["type"] == "AddUpdater":
                # Attach TracedPath and animate theta
                self.add(sine_wave_trace)
                self.play(theta.animate.set_value(2 * PI), run_time=10, rate_func=linear)

            # Wait for remaining duration
            animation_time = 0
            if signal is not None and signal["type"] != "Create":
                animation_time += 1  # signal action run_time
            if visual["type"] == "Create":
                animation_time += 1  # approximate creation time
            elif visual["type"] == "AddUpdater":
                animation_time += 10  # theta animation run_time
            remaining = step["duration"] - animation_time
            if remaining > 0:
                self.wait(remaining)

        self.wait(2)