from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        axes_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title_eq_final
        title_eq_final = MathTex("y = (x-2)^2 - 3", color=BLUE).scale(1.2)
        title_eq_final.move_to(title_anchor)
        self.objects["title_eq_final"] = title_eq_final

        # axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": True},
            color=WHITE
        ).scale(0.8).move_to(axes_anchor)
        self.objects["axes"] = axes

        # parent_parabola
        parent_parabola = axes.plot(lambda x: x**2, color=GRAY, stroke_width=3)
        self.objects["parent_parabola"] = parent_parabola

        # final_parabola
        final_parabola = axes.plot(lambda x: (x-2)**2 - 3, color=BLUE, stroke_width=4)
        final_parabola.set_opacity(0.0)
        self.objects["final_parabola"] = final_parabola

        # vertex_dot
        vertex_dot = Dot(axes.c2p(2, -3), color=RED, radius=0.08)
        vertex_dot.set_opacity(0.0)
        self.objects["vertex_dot"] = vertex_dot

        # vertex_label
        vertex_label = MathTex("(2,-3)", color=RED)
        vertex_label.next_to(vertex_dot, UP + LEFT, buff=0.1)
        vertex_label.set_opacity(0.0)
        self.objects["vertex_label"] = vertex_label

        # axis_symmetry
        axis_symmetry = DashedLine(
            start=axes.c2p(2, axes.y_range[1]),
            end=axes.c2p(2, axes.y_range[0]),
            color=YELLOW,
            stroke_width=2
        )
        axis_symmetry.set_opacity(0.0)
        self.objects["axis_symmetry"] = axis_symmetry

        # explanation_text
        explanation_text = Text("We start with the parent function: y = x².", color=WHITE, font_size=24)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 10.704,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(axes, run_time=2))
        animation_time = 2
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "parent_parabola", "color": "GRAY"},
            "duration": 8.376,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else GRAY if signal["color"] == "GRAY" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color, run_time=1))
        self.play(Create(parent_parabola, run_time=2))
        animation_time = 1 + 2
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Circumscribe", "target": "title_eq_final", "color": "YELLOW", "parts": "(-2)"},
            "visual_action": {"subaction": {"type": "ReplacementTransform", "from_id": "explanation_text", "to_content": "Horizontal shift: (x)² → (x-2)²"}},
            "duration": 8.424,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else GRAY if signal["color"] == "GRAY" else eval(signal["color"])
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Create temporary shifted parabola for visual shift effect
        shifted_parabola = axes.plot(lambda x: (x-2)**2, color=GRAY, stroke_width=3)
        self.play(Transform(parent_parabola, shifted_parabola, run_time=2))
        # Update explanation text
        new_explanation = Text("Horizontal shift: (x)² → (x-2)²", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        animation_time = 1 + 2 + 1
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "title_eq_final", "color": "GREEN", "parts": "-3"},
            "duration": 8.496,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else GREEN if signal["color"] == "GREEN" else eval(signal["color"])
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        self.play(FadeOut(parent_parabola, run_time=1))
        final_parabola.set_opacity(1.0)
        self.play(FadeIn(final_parabola, run_time=2))
        animation_time = 1 + 1 + 2
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "vertex_dot", "color": "RED"},
            "duration": 9.216,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else RED if signal["color"] == "RED" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color, run_time=1))
        vertex_dot.set_opacity(1.0)
        self.play(FadeIn(vertex_dot, run_time=1))
        vertex_label.set_opacity(1.0)
        self.play(Write(vertex_label, run_time=1))
        animation_time = 1 + 1 + 1
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "signal_action": {"type": "Indicate", "target": "axis_symmetry", "color": "YELLOW"},
            "visual_action": {"subaction": {"type": "ReplacementTransform", "from_id": "explanation_text", "to_content": "Vertex: (2,-3). Axis of symmetry: x=2."}},
            "duration": 9.984,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_05.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal["color"] == "YELLOW" else RED if signal["color"] == "RED" else eval(signal["color"])
            self.play(Indicate(target_obj, color=color, run_time=1))
        axis_symmetry.set_opacity(1.0)
        self.play(Create(axis_symmetry, run_time=2))
        # Update explanation text
        new_explanation = Text("Vertex: (2,-3). Axis of symmetry: x=2.", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["explanation_text"], new_explanation))
        self.objects["explanation_text"] = new_explanation
        animation_time = 1 + 2 + 1
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))