from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create objects from layout_plan
        # title
        title = Text("Slope of the Tangent: y = 0.5x²", color=WHITE, font_size=36)
        self.objects["title"] = title
        title.to_edge(UP, buff=0.5)

        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            color=LIGHT_GRAY
        )
        self.objects["axes"] = axes
        axes.move_to(ORIGIN)

        # graph (parabola)
        graph = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=3)
        self.objects["graph"] = graph

        # moving_dot (initial at x=-3)
        moving_dot = Dot(radius=0.08, color=YELLOW, z_index=3)
        moving_dot.move_to(axes.c2p(-3, 0.5 * (-3)**2))
        self.objects["moving_dot"] = moving_dot

        # tangent_line (initial placeholder for x=-3)
        x0 = -3
        y0 = 0.5 * x0**2
        m = x0
        seg_x_start = x0 - 1.5
        seg_x_end = x0 + 1.5
        seg_start = axes.c2p(seg_x_start, m * (seg_x_start - x0) + y0)
        seg_end = axes.c2p(seg_x_end, m * (seg_x_end - x0) + y0)
        tangent_line = Line(seg_start, seg_end, color=RED, stroke_width=4, z_index=2)
        self.objects["tangent_line"] = tangent_line

        # slope_label (initial m = -3.00)
        slope_label = MathTex("m = -3.00", color=GREEN, font_size=30, z_index=4)
        slope_label.next_to(moving_dot, UP+RIGHT, buff=0.3)
        self.objects["slope_label"] = slope_label

        # derivative_reminder
        derivative_reminder = MathTex(r"\frac{dy}{dx} = x", color=TEAL, font_size=32)
        self.objects["derivative_reminder"] = derivative_reminder
        derivative_reminder.to_edge(DOWN, buff=0.5)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's visualize the function y equals one-half x squared.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 4.368,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We begin by drawing its graph, a parabola, on a coordinate plane.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw the axes with numbers."},
                "duration": 4.824,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, we plot the curve itself.",
                "signal_action": {"type": "Indicate", "target": "axes", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "graph", "details": "Draw the parabola smoothly."},
                "duration": 2.736,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The derivative of this function is dy/dx equals x. This tells us the slope of the tangent line at any point.",
                "signal_action": None,
                "visual_action": {"type": "Write", "target_id": "derivative_reminder", "details": "Show the derivative formula at the bottom."},
                "duration": 7.536,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Let's pick a point on the curve and see its tangent line. At this point, x is negative three, so the slope m is also negative three.",
                "signal_action": {"type": "Indicate", "target": "moving_dot", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "moving_dot", "details": "Show the initial dot at x=-3."},
                "duration": 9.096,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The tangent line just touches the curve at this point. Its slope is displayed here.",
                "signal_action": {"type": "Circumscribe", "target": "slope_label", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "tangent_line", "details": "Draw the initial tangent line (should be calculated for x=-3)."},
                "duration": 6.024,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Now, watch as the point moves. The tangent line and its slope update in real time, following the rule: slope equals x.",
                "signal_action": None,
                "visual_action": {"type": "Transform", "target_id": "moving_dot", "details": "Animate the dot moving along the curve from x=-3 to x=3 over 8 seconds. Simultaneously, use Transform to update the tangent_line and TransformMatchingTex to update the slope_label at each frame based on the dot's x-coordinate."},
                "duration": 8.976,
                "audio_path": "media/audio/畫出_y_=_0_5_x_x^2_的曲線。顯示一條沿著曲線移動的切線，並即時顯示更新的斜率數值。/step_06.mp3"
            }
        ]

        for step in sequence:
            # Audio
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_obj = self.objects[signal["target"]]
                color = eval(signal["color"]) if signal.get("color") else YELLOW
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))

            # Visual Action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            obj = self.objects[target_id]

            if visual["type"] == "Create":
                self.play(Create(obj))
            elif visual["type"] == "Write":
                self.play(Write(obj))
            elif visual["type"] == "Transform":
                # Special handling for step 7: animate dot moving and update tangent line and slope label
                if target_id == "moving_dot":
                    # Use ValueTracker for x0
                    x_tracker = ValueTracker(-3)
                    
                    # Update moving dot position
                    moving_dot.add_updater(lambda d: d.move_to(
                        axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)
                    ))
                    
                    # Update tangent line
                    def update_tangent(line):
                        x0 = x_tracker.get_value()
                        y0 = 0.5 * x0**2
                        m = x0
                        seg_x_start = x0 - 1.5
                        seg_x_end = x0 + 1.5
                        seg_start = axes.c2p(seg_x_start, m * (seg_x_start - x0) + y0)
                        seg_end = axes.c2p(seg_x_end, m * (seg_x_end - x0) + y0)
                        line.put_start_and_end_on(seg_start, seg_end)
                    
                    tangent_line.add_updater(update_tangent)
                    
                    # Update slope label
                    def update_slope_label(label):
                        x0 = x_tracker.get_value()
                        new_label = MathTex(f"m = {x0:.2f}", color=GREEN, font_size=30, z_index=4)
                        new_label.next_to(moving_dot, UP+RIGHT, buff=0.3)
                        label.become(new_label)
                    
                    slope_label.add_updater(update_slope_label)
                    
                    # Animate x_tracker from -3 to 3
                    self.play(x_tracker.animate.set_value(3), run_time=8)
                    
                    # Remove updaters
                    moving_dot.clear_updaters()
                    tangent_line.clear_updaters()
                    slope_label.clear_updaters()

            # Wait for remaining duration
            anim_time = 0
            if signal is not None:
                anim_time += 1
            if visual["type"] == "Create" or visual["type"] == "Write":
                anim_time += 1
            elif visual["type"] == "Transform" and target_id == "moving_dot":
                anim_time += 8  # run_time of the x_tracker animation
            
            remaining = step["duration"] - anim_time
            if remaining > 0:
                self.wait(remaining)

        self.wait(2)