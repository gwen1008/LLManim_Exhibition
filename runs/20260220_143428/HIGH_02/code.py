'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Graph the parabola y = (x-2)² - 3 by transforming the parent function y = x², showing horizontal and vertical shifts, vertex, and axis of symmetry.
# 2. Layout Strategy: Use LayoutEngine for three zones.
#    - Header Region: [y=3.5] for Title (equation)
#    - Main Content: [Center y=0] for axes and parabola graphs
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, graph, and explanation in separate safe areas. All main graph content centered at origin.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using provided audio_path.
#    - [x] Files: "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_XX.mp3"
# 5. Animation Flow: Show axes -> parent parabola -> transform to target parabola -> add vertex dot -> add vertex label, axis line, and axis label. Explanation text updates each step.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Create LayoutEngine
        layout = LayoutEngine()

        # 1. Create objects from layout_plan.objects
        # Title
        title = MathTex(r"y = (x-2)^2 - 3", color=BLUE, font_size=48)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # Axes
        axes = Axes(
            x_range=[-3, 7, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True, "color": LIGHT_GRAY},
            color=LIGHT_GRAY
        )
        self.objects["axes"] = axes
        obj_axes = LayoutObject(axes, "axes")
        layout.add(obj_axes)
        layout.add_to_zone(obj_axes, "CONTENT")
        layout.add_constraint(obj_axes.center_x == 0)
        layout.add_constraint(obj_axes.center_y == 0)

        # Parent parabola: y = x², plotted for t in [-2, 2] to get x in [-2,2]
        parent_parabola = axes.plot(lambda x: x**2, x_range=[-2, 2], color=YELLOW, stroke_width=4)
        self.objects["parent_parabola"] = parent_parabola

        # Target parabola: y = (x-2)² - 3. We can plot it directly.
        # For x from 0 to 4 (since t from -2 to 2, x = t+2)
        target_parabola = axes.plot(lambda x: (x-2)**2 - 3, x_range=[0, 4], color=GREEN, stroke_width=4)
        self.objects["target_parabola"] = target_parabola

        # Vertex dot
        vertex_dot = Dot(axes.c2p(2, -3), color=RED, radius=0.08, fill_opacity=1.0)
        self.objects["vertex_dot"] = vertex_dot

        # Vertex label
        vertex_label = MathTex(r"(2,\,-3)", color=RED, font_size=36)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.1)
        self.objects["vertex_label"] = vertex_label

        # Axis line (vertical line at x=2)
        axis_line = Line(
            start=axes.c2p(2, -5),
            end=axes.c2p(2, 5),
            color=PURPLE,
            stroke_width=3,
            stroke_opacity=0.7
        )
        self.objects["axis_line"] = axis_line

        # Axis label
        axis_label = MathTex(r"x = 2", color=PURPLE, font_size=36)
        axis_label.next_to(axis_line.get_top(), UP, buff=0.1)
        self.objects["axis_label"] = axis_label

        # Explanation text (initial content)
        explanation_text = Text("We start with the basic parabola y = x².", color=WHITE, font_size=28)
        self.objects["explanation_text"] = explanation_text
        obj_expl = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_expl)
        layout.add_to_zone(obj_expl, "FOOTER")
        layout.add_constraint(obj_expl.center_x == 0)

        # Solve layout to position title, axes, and explanation
        layout.solve()

        # Apply positions from layout
        title.move_to(obj_title.get_center())
        axes.move_to(obj_axes.get_center())
        explanation_text.move_to(obj_expl.get_center())

        # Note: parent_parabola, target_parabola, vertex_dot, vertex_label, axis_line, axis_label
        # are positioned relative to axes, so they move with axes.

        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        step = {
            "step": 1,
            "narrative": "Let's graph the parabola y equals x minus two squared minus three. We'll start with its parent function, y equals x squared.",
            "signal_action": {
                "type": "Circumscribe",
                "target": "title",
                "color": "YELLOW"
            },
            "visual_action": {
                "type": "Create",
                "target_id": "axes",
                "details": "Draw the coordinate axes."
            },
            "duration": 9.072,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
        }
        # Audio
        if "audio_path" in step and step["audio_path"]:
            self.add_sound(step["audio_path"])
        # Signal action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Visual action
        visual = step["visual_action"]
        target_id = visual["target_id"]
        obj = self.objects[target_id]
        self.play(Create(obj))
        # Wait for remaining audio
        animation_time = 1 + 1  # Circumscribe (1) + Create axes (1)
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "narrative": "Here is the basic parabola, y equals x squared, symmetric about the y-axis and with its vertex at the origin.",
            "signal_action": None,
            "visual_action": {
                "type": "Create",
                "target_id": "parent_parabola",
                "details": "Draw the yellow parent parabola."
            },
            "duration": 7.584,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
        }
        if "audio_path" in step and step["audio_path"]:
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            # Not needed for this step
            pass
        visual = step["visual_action"]
        target_id = visual["target_id"]
        obj = self.objects[target_id]
        self.play(Create(obj))
        # Update explanation text (implicitly via replacement)
        new_expl = Text("Here is the basic parabola y = x².", color=WHITE, font_size=28)
        new_expl.move_to(explanation_text.get_center())
        self.play(ReplacementTransform(explanation_text, new_expl))
        explanation_text = new_expl
        self.objects["explanation_text"] = explanation_text
        animation_time = 1 + 0.5  # Create parabola (1) + text transform (0.5)
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "narrative": "The expression x minus two inside the square causes a horizontal shift. The entire graph moves two units to the right.",
            "signal_action": {
                "type": "Indicate",
                "target": "title",
                "color": "ORANGE",
                "details": "Highlight the '(x-2)' part of the title."
            },
            "visual_action": {
                "type": "ReplacementTransform",
                "target_id": "parent_parabola",
                "details": "Morph the yellow parabola into the green target parabola.",
                "new_object_ref": "target_parabola"
            },
            "duration": 8.424,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
        }
        if "audio_path" in step and step["audio_path"]:
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = ORANGE  # ORANGE is a valid Manim constant
            self.play(Indicate(target_obj, color=color))
        visual = step["visual_action"]
        source = self.objects[visual["target_id"]]
        target = self.objects[visual["new_object_ref"]]
        self.play(ReplacementTransform(source, target))
        # Update explanation text
        new_expl = Text("Shift right by 2: y = (x-2)²", color=WHITE, font_size=28)
        new_expl.move_to(explanation_text.get_center())
        self.play(ReplacementTransform(explanation_text, new_expl))
        explanation_text = new_expl
        self.objects["explanation_text"] = explanation_text
        animation_time = 1 + 1 + 0.5  # Indicate (1) + ReplacementTransform (1) + text (0.5)
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "narrative": "The minus three outside the square shifts the graph down by three units. This gives us our final parabola.",
            "signal_action": {
                "type": "Indicate",
                "target": "title",
                "color": "TEAL",
                "details": "Highlight the '-3' part of the title."
            },
            "visual_action": {
                "type": "Create",
                "target_id": "vertex_dot",
                "details": "Add a red dot at the new vertex location (2, -3)."
            },
            "duration": 7.392,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
        }
        if "audio_path" in step and step["audio_path"]:
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = TEAL  # TEAL is a valid Manim constant
            self.play(Indicate(target_obj, color=color))
        visual = step["visual_action"]
        target_id = visual["target_id"]
        obj = self.objects[target_id]
        self.play(FadeIn(obj, scale=0.5))
        # Update explanation text
        new_expl = Text("Shift down by 3: y = (x-2)² - 3", color=WHITE, font_size=28)
        new_expl.move_to(explanation_text.get_center())
        self.play(ReplacementTransform(explanation_text, new_expl))
        explanation_text = new_expl
        self.objects["explanation_text"] = explanation_text
        animation_time = 1 + 0.5 + 0.5  # Indicate (1) + FadeIn dot (0.5) + text (0.5)
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "narrative": "The vertex is now at the point two, negative three. The parabola is symmetric about the vertical line x equals two, which passes through the vertex.",
            "signal_action": {
                "type": "Indicate",
                "target": "vertex_dot",
                "color": "RED"
            },
            "visual_action": [
                {
                    "type": "Write",
                    "target_id": "vertex_label",
                    "details": "Label the vertex."
                },
                {
                    "type": "Create",
                    "target_id": "axis_line",
                    "details": "Draw the purple vertical line."
                },
                {
                    "type": "Write",
                    "target_id": "axis_label",
                    "details": "Label the axis."
                }
            ],
            "duration": 9.96,
            "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
        }
        if "audio_path" in step and step["audio_path"]:
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = RED
            self.play(Indicate(target_obj, color=color))
        visual_actions = step["visual_action"]
        # Since visual_action is a list, play them together
        anims = []
        for va in visual_actions:
            target_id = va["target_id"]
            obj = self.objects[target_id]
            if va["type"] == "Write":
                anims.append(Write(obj))
            elif va["type"] == "Create":
                anims.append(Create(obj))
        self.play(*anims)
        # Update explanation text
        new_expl = Text("Vertex at (2, -3), axis of symmetry x = 2.", color=WHITE, font_size=28)
        new_expl.move_to(explanation_text.get_center())
        self.play(ReplacementTransform(explanation_text, new_expl))
        explanation_text = new_expl
        self.objects["explanation_text"] = explanation_text
        animation_time = 1 + 1 + 0.5  # Indicate (1) + group anims (1) + text (0.5)
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))