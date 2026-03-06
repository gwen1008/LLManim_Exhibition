from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects
        # title
        title = Text("Derivative & Tangent Line: y = 0.5x²", color=WHITE, font_size=40)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 8, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True, "color": LIGHT_GRAY},
            color=LIGHT_GRAY
        )
        self.objects["axes"] = axes
        
        # parabola
        parabola = axes.plot(lambda x: 0.5 * x**2, color=BLUE, stroke_width=3)
        self.objects["parabola"] = parabola
        
        # tangent_point (initial position at x=-4)
        tangent_point = Dot(radius=0.08, color=YELLOW)
        tangent_point.move_to(axes.c2p(-4, 0.5 * (-4)**2))
        self.objects["tangent_point"] = tangent_point
        
        # tangent_line (initial dummy line, will be updated)
        tangent_line = Line(LEFT, RIGHT, color=RED, stroke_width=3)
        self.objects["tangent_line"] = tangent_line
        
        # slope_label (initial dummy, will be updated)
        slope_label = MathTex("f'(x) = x", color=GREEN, font_size=30)
        self.objects["slope_label"] = slope_label
        
        # derivation_title
        derivation_title = Text("Derivative via Power Rule:", color=LIGHT_GRAY, font_size=28)
        self.objects["derivation_title"] = derivation_title
        
        # derivation_step1
        derivation_step1 = MathTex("y = 0.5x^2", color=BLUE, font_size=28)
        self.objects["derivation_step1"] = derivation_step1
        
        # derivation_step2
        derivation_step2 = MathTex("y' = 0.5 \\cdot 2x^{2-1}", color=WHITE, font_size=28)
        self.objects["derivation_step2"] = derivation_step2
        
        # derivation_step3
        derivation_step3 = MathTex("y' = x", color=GREEN, font_size=28)
        self.objects["derivation_step3"] = derivation_step3
        
        # Position objects according to layout plan
        # Header: title at top
        title.to_edge(UP, buff=0.5)
        
        # Content: axes, parabola, tangent elements in center
        axes.move_to(ORIGIN)
        
        # Footer: derivation steps at bottom
        # Create a VGroup for footer elements and arrange vertically
        footer_group = VGroup(
            derivation_title,
            derivation_step1,
            derivation_step2,
            derivation_step3
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        footer_group.to_edge(DOWN, buff=0.5)
        
        # ValueTracker for tangent point x-coordinate
        x_tracker = ValueTracker(-4)
        
        # Updater for tangent_point
        tangent_point.add_updater(lambda d: d.move_to(
            axes.c2p(x_tracker.get_value(), 0.5 * x_tracker.get_value()**2)
        ))
        
        # Updater for tangent_line (using derivative slope = x)
        def update_tangent_line(line):
            x = x_tracker.get_value()
            y = 0.5 * x**2
            slope = x  # derivative
            # Create a line segment centered at (x, y) with slope
            dx = 1.5
            start = axes.c2p(x - dx, y - slope * dx)
            end = axes.c2p(x + dx, y + slope * dx)
            line.put_start_and_end_on(start, end)
            return line
        
        tangent_line.add_updater(update_tangent_line)
        
        # Updater for slope_label (text and position)
        def update_slope_label(label):
            x = x_tracker.get_value()
            # Create new label with current x value
            new_label = MathTex(f"f'(x) = {x:.2f}", color=GREEN, font_size=30)
            # Position it relative to tangent_line's center
            new_label.move_to(tangent_line.get_center() + UP * 0.5)
            label.become(new_label)
            return label
        
        slope_label.add_updater(update_slope_label)
        
        # Initially, don't add dynamic objects to scene yet
        # They will be added via Create/Write in sequence
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.sequence_data()  # Get sequence from JSON
        
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")
            
            # === AUDIO ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            
            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                color_name = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE, "LIGHT_GRAY": LIGHT_GRAY}
                color = color_map.get(color_name, YELLOW)
                target_obj = self.objects[target_id]
                
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))
            
            # Visual action
            visual = step["visual_action"]
            target_id = visual["target_id"]
            action_type = visual["type"]
            target_obj = self.objects[target_id]
            
            if action_type == "Create":
                self.play(Create(target_obj))
            elif action_type == "Write":
                self.play(Write(target_obj))
            elif action_type == "Animation":
                # Special case for step 6: animate x_tracker
                if target_id == "tangent_point":
                    # First create the tangent line and slope label
                    self.play(Create(tangent_line), Write(slope_label))
                    # Then animate the x_tracker
                    self.play(x_tracker.animate.set_value(4), run_time=8)
            
            # Wait for remaining duration
            # Estimate animation time: signal (1s if present) + visual (1s default) + special run_time
            anim_time = 0
            if signal is not None:
                anim_time += 1
            if action_type == "Create" or action_type == "Write":
                anim_time += 1
            elif action_type == "Animation" and target_id == "tangent_point":
                anim_time += 8  # run_time=8 for the tracker animation
            
            remaining = duration - anim_time + 0.5
            if remaining > 0:
                self.wait(remaining)
        
        # Cleanup updaters
        tangent_point.clear_updaters()
        tangent_line.clear_updaters()
        slope_label.clear_updaters()
    
    def sequence_data(self):
        # This method returns the sequence data from the JSON.
        # In a real system, this would be parsed from the input.
        # Here we hardcode it as per the provided JSON.
        return [
            {
                "step": 1,
                "narrative": "Let's visualize the function y equals one-half x squared.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 4.368,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We begin with its graph on a coordinate plane.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw the axes with numbers."},
                "duration": 3.24,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, plot the parabola itself.",
                "signal_action": {"type": "Indicate", "target": "parabola", "color": "BLUE"},
                "visual_action": {"type": "Create", "target_id": "parabola", "details": "Draw the curve of the function."},
                "duration": 2.88,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The derivative of this function, found using the power rule, is simply x.",
                "signal_action": {"type": "Circumscribe", "target": "derivation_step3", "color": "YELLOW"},
                "visual_action": {"type": "Write", "target_id": "derivation_title", "details": "Show the derivation steps in the footer area, writing them sequentially."},
                "duration": 5.208,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Consider a point moving along this curve. At each point, we can draw a tangent line, whose slope is given by the derivative.",
                "signal_action": {"type": "Indicate", "target": "tangent_point", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "tangent_point", "details": "Show the yellow dot on the parabola. Then, create the tangent line and slope label at its initial position."},
                "duration": 8.52,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "As the point moves, the tangent line rotates, and its slope updates in real time. Watch how the slope value changes according to the derivative, y prime equals x.",
                "signal_action": {"type": "Indicate", "target": "slope_label", "color": "GREEN"},
                "visual_action": {"type": "Animation", "target_id": "tangent_point", "details": "Animate the x_tracker from -4 to 4 over 8 seconds. The tangent_line and slope_label should be defined with updaters (always_redraw) that depend on x_tracker. The slope_label update should use TransformMatchingTex to smoothly change the numerical value."},
                "duration": 11.496,
                "audio_path": "media/audio/畫出_y___0_5___x_2_的曲線_72ed3ec72d/step_05.mp3"
            }
        ]