from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Exploring Derivatives: y = 0.5x²", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": LIGHT_GRAY}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes
        
        # Graph (Parabola)
        def parabola_func(x):
            return 0.5 * x**2
        graph = axes.plot(parabola_func, color=BLUE, stroke_width=4)
        graph.move_to(content_center)
        self.objects["graph"] = graph
        
        # Moving Point (initial at x0 = -3)
        x0_initial = -3
        y0_initial = parabola_func(x0_initial)
        moving_point = Dot(axes.c2p(x0_initial, y0_initial), color=YELLOW, radius=0.08)
        self.objects["moving_point"] = moving_point
        
        # Tangent Line (initial for x0 = -3)
        # Slope m = x0 = -3
        # Tangent line equation: y = m*(x - x0) + y0
        # We'll draw it from x0-1 to x0+1
        tangent_start_x = x0_initial - 1
        tangent_end_x = x0_initial + 1
        tangent_start_y = x0_initial * (tangent_start_x - x0_initial) + y0_initial
        tangent_end_y = x0_initial * (tangent_end_x - x0_initial) + y0_initial
        tangent_line = Line(
            axes.c2p(tangent_start_x, tangent_start_y),
            axes.c2p(tangent_end_x, tangent_end_y),
            color=RED,
            stroke_width=3
        )
        self.objects["tangent_line"] = tangent_line
        
        # Slope Label (initial)
        slope_label = MathTex("m = -3.00", color=GREEN, font_size=30)
        # Position will be set relative to moving_point later
        self.objects["slope_label"] = slope_label
        
        # Derivation (footer)
        derivation = MathTex(
            r"\frac{d}{dx}\left(\frac{1}{2}x^2\right) = \frac{1}{2} \cdot 2x^{1} = x",
            color=WHITE,
            font_size=35
        )
        derivation.move_to(footer_anchor)
        self.objects["derivation"] = derivation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "duration": 4.584,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(FadeIn(self.objects["title"]))
        animation_time = 1.0  # Approximate run_time for FadeIn
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        step = {
            "step": 2,
            "duration": 3.792,
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Create(self.objects["axes"]))
        animation_time = 1.5
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        step = {
            "step": 3,
            "duration": 5.808,
            "signal_action": {"type": "Indicate", "target": "graph", "color": "BLUE"},
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else BLUE
            self.play(Indicate(target_obj, color=color))
        # Visual action
        self.play(Create(self.objects["graph"]))
        animation_time = 2.0  # Create graph + Indicate
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        step = {
            "step": 4,
            "duration": 10.296,
            "signal_action": {"type": "Circumscribe", "target": "derivation", "color": "YELLOW"},
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Visual action first (Write derivation)
        self.play(Write(self.objects["derivation"]))
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else BLUE
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        animation_time = 3.0  # Write + Circumscribe
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        step = {
            "step": 5,
            "duration": 16.8,
            "signal_action": {"type": "Indicate", "target": "moving_point", "color": "YELLOW"},
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else BLUE
            self.play(Indicate(target_obj, color=color))
        # Visual actions: Create moving_point, tangent_line, slope_label
        # First, position slope_label relative to moving_point
        self.objects["slope_label"].next_to(self.objects["moving_point"], UP+RIGHT, buff=0.2)
        self.play(
            Create(self.objects["moving_point"]),
            Create(self.objects["tangent_line"]),
            Write(self.objects["slope_label"])
        )
        animation_time = 3.0  # Indicate + three Creates
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 6
        step = {
            "step": 6,
            "duration": 11.712,
            "signal_action": {"type": "Indicate", "target": "slope_label", "color": "GREEN"},
            "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = GREEN if signal["color"] == "GREEN" else YELLOW
            self.play(Indicate(target_obj, color=color))
        
        # Now set up dynamic updates using ValueTracker and always_redraw
        x0_tracker = ValueTracker(x0_initial)
        
        # Update moving_point position
        moving_point_updater = always_redraw(
            lambda: self.objects["moving_point"].move_to(
                self.objects["axes"].c2p(
                    x0_tracker.get_value(),
                    parabola_func(x0_tracker.get_value())
                )
            )
        )
        self.add(moving_point_updater)
        
        # Update tangent_line
        tangent_line_updater = always_redraw(
            lambda: Line(
                self.objects["axes"].c2p(
                    x0_tracker.get_value() - 1,
                    x0_tracker.get_value() * ((x0_tracker.get_value() - 1) - x0_tracker.get_value()) + parabola_func(x0_tracker.get_value())
                ),
                self.objects["axes"].c2p(
                    x0_tracker.get_value() + 1,
                    x0_tracker.get_value() * ((x0_tracker.get_value() + 1) - x0_tracker.get_value()) + parabola_func(x0_tracker.get_value())
                ),
                color=RED,
                stroke_width=3
            )
        )
        self.add(tangent_line_updater)
        # Remove the static tangent line
        self.remove(self.objects["tangent_line"])
        
        # Update slope_label (text and position)
        def update_slope_label():
            current_x = x0_tracker.get_value()
            # Format slope to two decimal places
            slope_text = f"m = {current_x:.2f}"
            new_label = MathTex(slope_text, color=GREEN, font_size=30)
            new_label.next_to(moving_point_updater, UP+RIGHT, buff=0.2)
            return new_label
        
        slope_label_updater = always_redraw(update_slope_label)
        self.add(slope_label_updater)
        # Remove the static slope label
        self.remove(self.objects["slope_label"])
        
        # Animate the point moving from x=-3 to x=3
        self.play(
            x0_tracker.animate.set_value(3),
            run_time=8,
            rate_func=linear
        )
        
        # Calculate remaining wait time
        animation_time_step6 = 1.0 + 8.0  # Indicate + movement
        remaining = max(0.1, step["duration"] - animation_time_step6 + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))