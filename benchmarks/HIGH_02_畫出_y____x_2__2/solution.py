from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create all objects first, then position them
        
        # Title
        title = Text("Graphing a Parabola: y = (x-2)² - 3", color=WHITE, font_size=40)
        title.to_edge(UP, buff=0.5)
        
        # Axes
        axes = Axes(
            x_range=[-3, 7, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            color=LIGHT_GRAY
        )
        axes.center()
        
        # Equations
        parent_eq = MathTex("y = x^2", color=BLUE)
        parent_eq.next_to(title, DOWN, buff=0.5)
        
        shifted_eq_h = MathTex("y = (x-2)^2", color=GREEN)
        shifted_eq_h.move_to(parent_eq.get_center())
        
        final_eq = MathTex("y = (x-2)^2 - 3", color=YELLOW)
        final_eq.move_to(parent_eq.get_center())
        
        # Graphs
        parent_graph = axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE, stroke_width=3)
        shifted_graph_h = axes.plot(lambda x: (x-2)**2, x_range=[0, 4], color=GREEN, stroke_width=3)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[0, 4], color=YELLOW, stroke_width=4)
        
        # Vertex and Axis
        vertex_dot = Dot(axes.c2p(2, -3), color=RED, radius=0.08, fill_opacity=1.0)
        vertex_label = MathTex("(2,\\,-3)", color=RED, font_size=30).next_to(vertex_dot, UP+RIGHT, buff=0.1)
        vertex_group = VGroup(vertex_dot, vertex_label)
        
        axis_line = DashedLine(
            axes.c2p(2, 5), 
            axes.c2p(2, -5), 
            color=PINK, 
            stroke_width=2, 
            stroke_opacity=0.7, 
            dash_length=0.1
        )
        axis_label = MathTex("x = 2", color=PINK, font_size=30).next_to(axis_line.get_top(), UP, buff=0.1)
        
        # Explanations
        step1_explanation = Text("Start with the parent function: y = x²", color=BLUE, font_size=28)
        step1_explanation.to_edge(DOWN, buff=0.5)
        
        step2_explanation = Text("Shift right by 2 units: replace x with (x-2)", color=GREEN, font_size=28)
        step2_explanation.move_to(step1_explanation.get_center())
        
        step3_explanation = Text("Shift down by 3 units: subtract 3 from the function", color=YELLOW, font_size=28)
        step3_explanation.move_to(step1_explanation.get_center())
        
        step4_explanation = Text("Vertex is at (2, -3). Axis of symmetry is x = 2.", color=WHITE, font_size=28)
        step4_explanation.move_to(step1_explanation.get_center())
        
        # Object registry for easy access
        obj_registry = {
            "title": title,
            "axes": axes,
            "parent_eq": parent_eq,
            "shifted_eq_h": shifted_eq_h,
            "final_eq": final_eq,
            "parent_graph": parent_graph,
            "shifted_graph_h": shifted_graph_h,
            "final_graph": final_graph,
            "vertex_dot": vertex_dot,
            "vertex_label": vertex_label,
            "vertex_group": vertex_group,
            "axis_line": axis_line,
            "axis_label": axis_label,
            "step1_explanation": step1_explanation,
            "step2_explanation": step2_explanation,
            "step3_explanation": step3_explanation,
            "step4_explanation": step4_explanation,
        }
        
        # Add initial objects to scene
        self.add(title, axes, parent_eq, step1_explanation)
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        step = {
            "step": 1,
            "audio_path": "media/audio/畫出_y_=_(x-2)^2_-_3_的拋物線。標註頂點_(2,_-3)_並畫出垂直的對稱軸。/step_00.mp3",
            "duration": 5.256,
            "signal_action": {"type": "Circumscribe", "target": "parent_eq", "color": "BLUE"},
            "visual_action": {"type": "Create", "target_id": "parent_graph"}
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action"):
            target = obj_registry[step["signal_action"]["target"]]
            self.play(Circumscribe(target, color=BLUE, run_time=1))
        # Visual Action
        self.play(Create(obj_registry["parent_graph"]), run_time=2)
        # Wait
        remaining = step["duration"] - 1 - 2
        if remaining > 0:
            self.wait(remaining)

        # Step 2
        step = {
            "step": 2,
            "audio_path": "media/audio/畫出_y_=_(x-2)^2_-_3_的拋物線。標註頂點_(2,_-3)_並畫出垂直的對稱軸。/step_01.mp3",
            "duration": 6.816,
            "signal_action": {"type": "Indicate", "target": "shifted_eq_h", "color": "GREEN"},
            "visual_action": {"type": "ReplacementTransform", "target_id": "parent_eq", "new_target_id": "shifted_eq_h"}
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action (Indicate the target before it exists, so we create it first but invisible)
        shifted_eq_h.set_opacity(0)
        self.add(shifted_eq_h)
        if step.get("signal_action"):
            target = obj_registry[step["signal_action"]["target"]]
            self.play(Indicate(target, color=GREEN))
            target.set_opacity(1)
        # Visual Action
        self.play(
            ReplacementTransform(obj_registry["parent_eq"], obj_registry["shifted_eq_h"]),
            ReplacementTransform(obj_registry["parent_graph"], obj_registry["shifted_graph_h"]),
            ReplacementTransform(obj_registry["step1_explanation"], obj_registry["step2_explanation"]),
            run_time=2
        )
        # Wait
        remaining = step["duration"] - 1 - 2
        if remaining > 0:
            self.wait(remaining)

        # Step 3
        step = {
            "step": 3,
            "audio_path": "media/audio/畫出_y_=_(x-2)^2_-_3_的拋物線。標註頂點_(2,_-3)_並畫出垂直的對稱軸。/step_02.mp3",
            "duration": 5.472,
            "signal_action": {"type": "Indicate", "target": "final_eq", "color": "YELLOW"},
            "visual_action": {"type": "ReplacementTransform", "target_id": "shifted_eq_h", "new_target_id": "final_eq"}
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        final_eq.set_opacity(0)
        self.add(final_eq)
        if step.get("signal_action"):
            target = obj_registry[step["signal_action"]["target"]]
            self.play(Indicate(target, color=YELLOW))
            target.set_opacity(1)
        # Visual Action
        self.play(
            ReplacementTransform(obj_registry["shifted_eq_h"], obj_registry["final_eq"]),
            ReplacementTransform(obj_registry["shifted_graph_h"], obj_registry["final_graph"]),
            ReplacementTransform(obj_registry["step2_explanation"], obj_registry["step3_explanation"]),
            run_time=2
        )
        # Wait
        remaining = step["duration"] - 1 - 2
        if remaining > 0:
            self.wait(remaining)

        # Step 4
        step = {
            "step": 4,
            "audio_path": "media/audio/畫出_y_=_(x-2)^2_-_3_的拋物線。標註頂點_(2,_-3)_並畫出垂直的對稱軸。/step_03.mp3",
            "duration": 5.832,
            "signal_action": {"type": "Indicate", "target": "vertex_dot", "color": "RED"},
            "visual_action": {"type": "Create", "target_id": "vertex_dot"}
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action (Indicate the dot before creating it)
        vertex_dot.set_opacity(0)
        vertex_label.set_opacity(0)
        self.add(vertex_dot, vertex_label)
        if step.get("signal_action"):
            target = obj_registry[step["signal_action"]["target"]]
            self.play(Indicate(target, color=RED))
            target.set_opacity(1)
            vertex_label.set_opacity(1)
        # Visual Action
        self.play(
            Create(obj_registry["vertex_dot"]),
            Write(obj_registry["vertex_label"]),
            ReplacementTransform(obj_registry["step3_explanation"], obj_registry["step4_explanation"]),
            run_time=2
        )
        # Wait
        remaining = step["duration"] - 1 - 2
        if remaining > 0:
            self.wait(remaining)

        # Step 5
        step = {
            "step": 5,
            "audio_path": "media/audio/畫出_y_=_(x-2)^2_-_3_的拋物線。標註頂點_(2,_-3)_並畫出垂直的對稱軸。/step_04.mp3",
            "duration": 6.888,
            "signal_action": {"type": "Indicate", "target": "axis_line", "color": "PINK"},
            "visual_action": {"type": "Create", "target_id": "axis_line"}
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        axis_line.set_opacity(0)
        axis_label.set_opacity(0)
        self.add(axis_line, axis_label)
        if step.get("signal_action"):
            target = obj_registry[step["signal_action"]["target"]]
            self.play(Indicate(target, color=PINK))
            target.set_opacity(1)
            axis_label.set_opacity(1)
        # Visual Action
        self.play(
            Create(obj_registry["axis_line"]),
            Write(obj_registry["axis_label"]),
            run_time=2
        )
        # Wait
        remaining = step["duration"] - 1 - 2
        if remaining > 0:
            self.wait(remaining)

        # Final hold
        self.wait(2)