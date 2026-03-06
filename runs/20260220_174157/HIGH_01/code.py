from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create Layout Engine
        from utils.layout_engine import LayoutEngine, LayoutObject
        layout = LayoutEngine()
        
        # Create objects from layout_plan
        # Title
        title = Text("Graphing y = 2x - 1: Understanding Slope", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title
        
        # Equation
        eq_main = MathTex("y = 2x - 1", color=YELLOW, font_size=32)
        obj_eq = LayoutObject(eq_main, "eq_main")
        layout.add(obj_eq)
        layout.add_to_zone(obj_eq, "HEADER")
        layout.align_to(obj_eq, obj_title, 'CENTER_X')
        layout.add_constraint(obj_eq.center_y == obj_title.center_y - 0.8)
        self.objects["eq_main"] = eq_main
        
        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=9.6,
            y_length=7.2,
            axis_config={"color": LIGHT_GRAY}
        )
        obj_axes = LayoutObject(axes, "axes")
        layout.add(obj_axes)
        layout.add_to_zone(obj_axes, "CONTENT")
        layout.add_constraint(obj_axes.center_x == 0)
        layout.add_constraint(obj_axes.center_y == 0)
        self.objects["axes"] = axes
        
        # Dot Intercept
        dot_intercept = Dot(radius=0.08, color=GREEN)
        dot_intercept.move_to(axes.c2p(0, -1))
        obj_dot_int = LayoutObject(dot_intercept, "dot_intercept")
        layout.add(obj_dot_int)
        self.objects["dot_intercept"] = dot_intercept
        
        # Label Intercept
        label_intercept = MathTex("(0, -1)", color=GREEN, font_size=24)
        obj_label_int = LayoutObject(label_intercept, "label_intercept")
        layout.add(obj_label_int)
        self.objects["label_intercept"] = label_intercept
        
        # Dot Mover
        dot_mover = Dot(radius=0.08, color=BLUE)
        dot_mover.move_to(axes.c2p(0, -1))
        obj_dot_mover = LayoutObject(dot_mover, "dot_mover")
        layout.add(obj_dot_mover)
        self.objects["dot_mover"] = dot_mover
        
        # Run Segment (initially zero length)
        run_segment = Line(
            start=axes.c2p(0, -1),
            end=axes.c2p(0, -1),
            color=RED,
            stroke_width=4
        )
        obj_run = LayoutObject(run_segment, "run_segment")
        layout.add(obj_run)
        self.objects["run_segment"] = run_segment
        
        # Rise Segment (initially zero length)
        rise_segment = Line(
            start=axes.c2p(1, -1),
            end=axes.c2p(1, -1),
            color=RED,
            stroke_width=4
        )
        obj_rise = LayoutObject(rise_segment, "rise_segment")
        layout.add(obj_rise)
        self.objects["rise_segment"] = rise_segment
        
        # Line Partial (initially zero length)
        line_partial = Line(
            start=axes.c2p(0, -1),
            end=axes.c2p(0, -1),
            color=YELLOW,
            stroke_width=6
        )
        obj_line = LayoutObject(line_partial, "line_partial")
        layout.add(obj_line)
        self.objects["line_partial"] = line_partial
        
        # Slope Label
        label_slope = MathTex(
            r"\text{slope} = \frac{\text{rise}}{\text{run}} = \frac{2}{1} = 2",
            color=ORANGE,
            font_size=28
        )
        obj_slope = LayoutObject(label_slope, "label_slope")
        layout.add(obj_slope)
        layout.add_to_zone(obj_slope, "FOOTER")
        layout.add_constraint(obj_slope.center_x == 0)
        layout.add_constraint(obj_slope.center_y == -2.8)
        self.objects["label_slope"] = label_slope
        
        # Explanation Step 1
        explanation_step1 = Text(
            "Step 1: Identify the y-intercept at (0, -1).",
            color=LIGHT_GRAY,
            font_size=22
        )
        obj_exp1 = LayoutObject(explanation_step1, "explanation_step1")
        layout.add(obj_exp1)
        layout.add_to_zone(obj_exp1, "FOOTER")
        layout.add_constraint(obj_exp1.center_x == 0)
        layout.add_constraint(obj_exp1.center_y == -3.2)
        self.objects["explanation_step1"] = explanation_step1
        
        # Solve layout
        layout.solve()
        
        # Apply positions from layout
        title.move_to(obj_title.get_center())
        eq_main.move_to(obj_eq.get_center())
        axes.move_to(obj_axes.get_center())
        dot_intercept.move_to(obj_dot_int.get_center())
        label_intercept.move_to(obj_label_int.get_center())
        dot_mover.move_to(obj_dot_mover.get_center())
        run_segment.move_to(obj_run.get_center())
        rise_segment.move_to(obj_rise.get_center())
        line_partial.move_to(obj_line.get_center())
        label_slope.move_to(obj_slope.get_center())
        explanation_step1.move_to(obj_exp1.get_center())
        
        # Position label_intercept relative to dot_intercept (as per JSON)
        label_intercept.next_to(dot_intercept, LEFT+UP, buff=0.1)
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "narrative": "We begin with the linear function y equals 2x minus 1. Let's first identify its y-intercept.",
            "signal_action": {
                "type": "Circumscribe",
                "target": "eq_main",
                "color": "YELLOW"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "axes",
                "details": "Draw the coordinate axes and grid."
            },
            "duration": 7.512,
            "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_00.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Animations
        self.play(Write(title), Write(eq_main))
        self.wait(max(0.1, 0.5))
        
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else eval(signal["color"])
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        
        # Visual action
        self.play(Create(axes, run_time=2))
        
        # Wait for remaining audio
        animation_time = 0.5 + 1 + 2  # Write wait + Circumscribe + Create
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        step = {
            "step": 2,
            "narrative": "When x is zero, y is negative one. This point is the y-intercept.",
            "signal_action": {
                "type": "Indicate",
                "target": "dot_intercept",
                "color": "GREEN"
            },
            "visual_action": {
                "type": "Create",
                "target_ids": [
                    "dot_intercept",
                    "label_intercept"
                ],
                "details": "Fade in the intercept point and its label."
            },
            "duration": 5.976,
            "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_01.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = GREEN if signal["color"] == "GREEN" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color))
        
        # Visual action
        self.play(FadeIn(self.objects["dot_intercept"]), FadeIn(self.objects["label_intercept"]))
        
        # Wait for remaining audio
        animation_time = 1 + 1  # Indicate + FadeIn
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        step = {
            "step": 3,
            "narrative": "The slope is 2. This means for every 1 unit we move to the right, we must move 2 units up. Let's animate this rule.",
            "signal_action": {
                "type": "ReplacementTransform",
                "target": "explanation_step1",
                "new_content": "Step 2: Slope = 2 means Rise/Run = 2/1. Animate the movement.",
                "details": "Update the explanation text."
            },
            "visual_action": {
                "type": "Create",
                "target_id": "dot_mover",
                "details": "Create the blue dot at the intercept."
            },
            "duration": 9.024,
            "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_02.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Signal action (update explanation text)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            new_exp = Text(
                "Step 2: Slope = 2 means Rise/Run = 2/1. Animate the movement.",
                color=LIGHT_GRAY,
                font_size=22
            )
            new_exp.move_to(self.objects["explanation_step1"].get_center())
            self.play(ReplacementTransform(self.objects["explanation_step1"], new_exp))
            self.objects["explanation_step1"] = new_exp
        
        # Visual action
        self.play(FadeIn(self.objects["dot_mover"]))
        
        # Wait for remaining audio
        animation_time = 1 + 1  # ReplacementTransform + FadeIn
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        step = {
            "step": 4,
            "narrative": "We run 1 unit to the right... and rise 2 units up. The path of this dot defines the line.",
            "signal_action": None,
            "visual_action": {
                "type": "Animate",
                "target_id": "dot_mover",
                "details": "Use Transform to move the dot from axes.c2p(0,-1) to axes.c2p(1,1). Simultaneously, use Transform to grow line_partial from a point to connect the intercept to the moving dot. Also, use Transform to grow run_segment horizontally and rise_segment vertically, forming the triangle."
            },
            "duration": 6.672,
            "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_03.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Create target objects for animation
        axes = self.objects["axes"]
        
        # Target positions
        dot_target_pos = axes.c2p(1, 1)
        run_target = Line(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, -1),
            color=RED,
            stroke_width=4
        )
        rise_target = Line(
            start=axes.c2p(1, -1),
            end=axes.c2p(1, 1),
            color=RED,
            stroke_width=4
        )
        line_target = Line(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, 1),
            color=YELLOW,
            stroke_width=6
        )
        
        # Animate all together
        self.play(
            self.objects["dot_mover"].animate.move_to(dot_target_pos),
            Transform(self.objects["run_segment"], run_target),
            Transform(self.objects["rise_segment"], rise_target),
            Transform(self.objects["line_partial"], line_target),
            run_time=3
        )
        
        # Wait for remaining audio
        animation_time = 3
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        step = {
            "step": 5,
            "narrative": "The slope is the ratio of this vertical rise to the horizontal run: two over one, which equals two.",
            "signal_action": {
                "type": "Circumscribe",
                "target": "label_slope",
                "color": "ORANGE"
            },
            "visual_action": {
                "type": "Write",
                "target_id": "label_slope",
                "details": "Write the slope label below the graph."
            },
            "duration": 6.912,
            "audio_path": "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_04.mp3"
        }
        
        # Audio
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Visual action
        self.play(Write(self.objects["label_slope"]))
        
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = ORANGE if signal["color"] == "ORANGE" else eval(signal["color"])
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        
        # Wait for remaining audio
        animation_time = 1 + 1  # Write + Circumscribe
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))