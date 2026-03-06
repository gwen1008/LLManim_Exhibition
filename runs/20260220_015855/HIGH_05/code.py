'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the head-to-tail method, showing geometric and algebraic equivalence.
# 2. Layout Strategy: Use LayoutEngine for zones.
#    - Header Region: Title at y ~ 3.0
#    - Main Content: Coordinate grid and vectors centered at origin.
#    - Footer Region: Explanation text at y ~ -3.0
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, content, and footer separated. VGroups for vector+label+dot.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using provided audio_path.
#    - [x] Files: "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_XX.mp3"
# 5. Animation Flow: Show axes -> Draw vector A -> Draw vector B from A's tip -> Show parallelogram concept -> Morph A+B into resultant C.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Helper to parse geometry_def strings (simplified)
        def parse_geometry(geom_str, obj_type):
            # For Arrow: "start=[0,0,0], end=[3,1,0]"
            # For NumberPlane: "x_range=[-1, 5, 1], y_range=[-1, 4, 1], x_length=10, y_length=8"
            # For Dot: "radius=0.07"
            # We'll extract values manually for each object.
            return geom_str

        # Create objects from layout_plan.objects
        # We'll create them first, then position using layout engine.
        obj_defs = [
            {
                "id": "title",
                "type": "Text",
                "content": "Vector Addition: Head-to-Tail Method",
                "properties": {"color": WHITE, "font_size": 40}
            },
            {
                "id": "axes",
                "type": "NumberPlane",
                "geometry_def": "x_range=[-1, 5, 1], y_range=[-1, 4, 1], x_length=10, y_length=8",
                "properties": {"stroke_opacity": 0.5, "background_line_style": {"stroke_opacity": 0.2}}
            },
            {
                "id": "x_label",
                "type": "MathTex",
                "content": "x",
                "properties": {"color": LIGHT_GRAY}
            },
            {
                "id": "y_label",
                "type": "MathTex",
                "content": "y",
                "properties": {"color": LIGHT_GRAY}
            },
            {
                "id": "vec_a",
                "type": "Arrow",
                "geometry_def": "start=[0,0,0], end=[3,1,0]",
                "properties": {"color": BLUE, "stroke_width": 8, "max_tip_length_to_length_ratio": 0.15}
            },
            {
                "id": "vec_a_label",
                "type": "MathTex",
                "content": r"\vec{A} = (3,1)",
                "properties": {"color": BLUE, "font_size": 30}
            },
            {
                "id": "point_a_tip",
                "type": "Dot",
                "geometry_def": "radius=0.07",
                "properties": {"color": BLUE}
            },
            {
                "id": "vec_b",
                "type": "Arrow",
                "geometry_def": "start=[3,1,0], end=[4,3,0]",
                "properties": {"color": GREEN, "stroke_width": 8, "max_tip_length_to_length_ratio": 0.15}
            },
            {
                "id": "vec_b_label",
                "type": "MathTex",
                "content": r"\vec{B} = (1,2)",
                "properties": {"color": GREEN, "font_size": 30}
            },
            {
                "id": "point_b_tip",
                "type": "Dot",
                "geometry_def": "radius=0.07",
                "properties": {"color": GREEN}
            },
            {
                "id": "vec_b_shifted",
                "type": "Arrow",
                "geometry_def": "start=[0,0,0], end=[1,2,0]",
                "properties": {"color": GREEN, "stroke_width": 8, "max_tip_length_to_length_ratio": 0.15, "opacity": 0.0}
            },
            {
                "id": "vec_c",
                "type": "Arrow",
                "geometry_def": "start=[0,0,0], end=[4,3,0]",
                "properties": {"color": YELLOW, "stroke_width": 8, "max_tip_length_to_length_ratio": 0.15, "opacity": 0.0}
            },
            {
                "id": "vec_c_label",
                "type": "MathTex",
                "content": r"\vec{C} = \vec{A} + \vec{B} = (4,3)",
                "properties": {"color": YELLOW, "font_size": 30, "opacity": 0.0}
            },
            {
                "id": "explanation_text",
                "type": "Text",
                "content": "We begin with a coordinate system.",
                "properties": {"color": LIGHT_GRAY, "font_size": 24}
            }
        ]

        for obj_def in obj_defs:
            obj_id = obj_def["id"]
            obj_type = obj_def["type"]
            content = obj_def.get("content", "")
            geom_str = obj_def.get("geometry_def", "")
            props = obj_def.get("properties", {})

            if obj_type == "Text":
                obj = Text(content, font_size=props.get("font_size", 24), color=props.get("color", WHITE))
            elif obj_type == "MathTex":
                obj = MathTex(content, color=props.get("color", WHITE), font_size=props.get("font_size", 30))
            elif obj_type == "NumberPlane":
                # Parse geometry_def: x_range=[-1, 5, 1], y_range=[-1, 4, 1], x_length=10, y_length=8
                # Simple extraction (not robust, but works for this specific string)
                import re
                x_range_match = re.search(r'x_range=\[([-\d., ]+)\]', geom_str)
                y_range_match = re.search(r'y_range=\[([-\d., ]+)\]', geom_str)
                x_length_match = re.search(r'x_length=([\d.]+)', geom_str)
                y_length_match = re.search(r'y_length=([\d.]+)', geom_str)
                x_range = eval(x_range_match.group(1)) if x_range_match else (-1, 5, 1)
                y_range = eval(y_range_match.group(1)) if y_range_match else (-1, 4, 1)
                x_length = float(x_length_match.group(1)) if x_length_match else 10
                y_length = float(y_length_match.group(1)) if y_length_match else 8
                obj = NumberPlane(
                    x_range=x_range,
                    y_range=y_range,
                    x_length=x_length,
                    y_length=y_length,
                    background_line_style={"stroke_opacity": props.get("background_line_style", {}).get("stroke_opacity", 0.2)},
                    stroke_opacity=props.get("stroke_opacity", 0.5)
                )
            elif obj_type == "Arrow":
                # Parse geometry_def: start=[0,0,0], end=[3,1,0]
                start_match = re.search(r'start=\[([-\d., ]+)\]', geom_str)
                end_match = re.search(r'end=\[([-\d., ]+)\]', geom_str)
                start = np.array(eval(start_match.group(1))) if start_match else ORIGIN
                end = np.array(eval(end_match.group(1))) if end_match else ORIGIN
                obj = Arrow(start=start, end=end, buff=0, color=props.get("color", WHITE), stroke_width=props.get("stroke_width", 8))
                # Manim Arrow doesn't have max_tip_length_to_length_ratio; we set tip_length proportionally.
                # We'll ignore that property for simplicity.
            elif obj_type == "Dot":
                radius_match = re.search(r'radius=([\d.]+)', geom_str)
                radius = float(radius_match.group(1)) if radius_match else 0.07
                obj = Dot(radius=radius, color=props.get("color", WHITE))
                # Position will be set later.
            else:
                continue

            # Apply additional properties
            if "opacity" in props:
                obj.set_opacity(props["opacity"])
            self.objects[obj_id] = obj
            layout.add(LayoutObject(obj, obj_id))

        # Position objects using layout engine zones and constraints
        title_obj = layout.get("title")
        axes_obj = layout.get("axes")
        x_label_obj = layout.get("x_label")
        y_label_obj = layout.get("y_label")
        vec_a_obj = layout.get("vec_a")
        vec_a_label_obj = layout.get("vec_a_label")
        point_a_tip_obj = layout.get("point_a_tip")
        vec_b_obj = layout.get("vec_b")
        vec_b_label_obj = layout.get("vec_b_label")
        point_b_tip_obj = layout.get("point_b_tip")
        vec_b_shifted_obj = layout.get("vec_b_shifted")
        vec_c_obj = layout.get("vec_c")
        vec_c_label_obj = layout.get("vec_c_label")
        explanation_obj = layout.get("explanation_text")

        # Add to zones
        layout.add_to_zone(title_obj, "HEADER")
        layout.add_to_zone(axes_obj, "CONTENT")
        layout.add_to_zone(explanation_obj, "FOOTER")

        # Center axes and title
        layout.add_constraint(title_obj.center_x == 0)
        layout.add_constraint(axes_obj.center_x == 0)
        layout.add_constraint(axes_obj.center_y == 0)
        layout.add_constraint(explanation_obj.center_x == 0)

        # Solve layout
        layout.solve()

        # Manually position labels and dots relative to axes/vectors (since they depend on other objects)
        # These positions are defined relative to other objects, not zones.
        x_label = self.objects["x_label"]
        y_label = self.objects["y_label"]
        axes = self.objects["axes"]
        x_label.next_to(axes.x_axis.get_right(), RIGHT, buff=0.2)
        y_label.next_to(axes.y_axis.get_top(), UP, buff=0.2)

        vec_a = self.objects["vec_a"]
        vec_a_label = self.objects["vec_a_label"]
        point_a_tip = self.objects["point_a_tip"]
        vec_a_label.next_to(vec_a.get_center(), UP+LEFT, buff=0.2)
        point_a_tip.move_to(vec_a.get_end())

        vec_b = self.objects["vec_b"]
        vec_b_label = self.objects["vec_b_label"]
        point_b_tip = self.objects["point_b_tip"]
        vec_b_label.next_to(vec_b.get_center(), RIGHT+UP, buff=0.2)
        point_b_tip.move_to(vec_b.get_end())

        vec_c = self.objects["vec_c"]
        vec_c_label = self.objects["vec_c_label"]
        vec_c_label.next_to(vec_c.get_center(), DOWN+RIGHT, buff=0.3)

        # vec_b_shifted and vec_c are already at correct positions (geometry_def defines start/end).

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We begin with a coordinate system.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw the coordinate grid and axes labels."},
                "duration": 2.712,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Draw vector A from the origin to the point (3, 1). This represents the displacement A equals (3, 1).",
                "signal_action": {"type": "Indicate", "target": "vec_a", "color": "BLUE"},
                "visual_action": {"type": "GrowArrow", "target_id": "vec_a", "details": "Animate the drawing of vector A. Then write its label and add a dot at its tip."},
                "duration": 8.328,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, draw vector B starting from the tip of vector A. Its components are (1, 2), so its tip lands at (4, 3).",
                "signal_action": {"type": "Indicate", "target": "vec_b", "color": "GREEN"},
                "visual_action": {"type": "GrowArrow", "target_id": "vec_b", "details": "Animate the drawing of vector B from (3,1) to (4,3). Then write its label and add a dot at its tip."},
                "duration": 8.856,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The head-to-tail path from the origin to (4,3) goes along A then B. The total displacement is the vector sum.",
                "signal_action": {"type": "Circumscribe", "target": "point_b_tip", "color": "YELLOW"},
                "visual_action": {"type": "ReplacementTransform", "target_id": "explanation_text", "details": "Update explanation text. Then, create a shifted copy of B (vec_b_shifted) at the origin with opacity 1, and indicate the parallelogram (implied)."},
                "duration": 7.512,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Animating the transformation: The sum vector C is the direct path from the start to the finish. Vector A plus vector B equals vector C.",
                "signal_action": None,
                "visual_action": {"type": "Transform", "target_id": ["vec_a", "vec_b_shifted"], "details": "Simultaneously Transform the VGroup containing vec_a and vec_b_shifted into the single vec_c. Fade in vec_c_label. This morph visually demonstrates A + B = C."},
                "duration": 9.408,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3"
            }
        ]

        for step in sequence:
            # === AUDIO (MANDATORY) ===
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "BLUE": BLUE, "GREEN": GREEN, "RED": RED}
                color = color_map.get(color_str, YELLOW)
                target_obj = self.objects[target_id]

                if signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color, run_time=1))
                elif signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))

            # Visual action
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual["target_id"]

            if action_type == "Create":
                # Create axes and labels
                self.play(Create(self.objects["axes"]))
                self.play(Write(self.objects["x_label"]), Write(self.objects["y_label"]))
                self.play(Write(self.objects["title"]))
                self.play(Write(self.objects["explanation_text"]))
                animation_time = 4.0  # Approximate
            elif action_type == "GrowArrow":
                if target_id == "vec_a":
                    self.play(GrowArrow(self.objects["vec_a"]))
                    self.play(Write(self.objects["vec_a_label"]))
                    self.play(FadeIn(self.objects["point_a_tip"]))
                    animation_time = 3.0
                elif target_id == "vec_b":
                    self.play(GrowArrow(self.objects["vec_b"]))
                    self.play(Write(self.objects["vec_b_label"]))
                    self.play(FadeIn(self.objects["point_b_tip"]))
                    # Update explanation text
                    new_text = Text("Now, draw vector B starting from the tip of vector A.", color=LIGHT_GRAY, font_size=24)
                    new_text.move_to(self.objects["explanation_text"].get_center())
                    self.play(ReplacementTransform(self.objects["explanation_text"], new_text))
                    self.objects["explanation_text"] = new_text
                    animation_time = 4.0
            elif action_type == "ReplacementTransform":
                # Update explanation text
                new_text = Text("The head-to-tail path from the origin to (4,3) goes along A then B.", color=LIGHT_GRAY, font_size=24)
                new_text.move_to(self.objects["explanation_text"].get_center())
                self.play(ReplacementTransform(self.objects["explanation_text"], new_text))
                self.objects["explanation_text"] = new_text
                # Show vec_b_shifted
                self.objects["vec_b_shifted"].set_opacity(1)
                self.play(FadeIn(self.objects["vec_b_shifted"]))
                animation_time = 3.0
            elif action_type == "Transform":
                # Create VGroup of vec_a and vec_b_shifted
                group = VGroup(self.objects["vec_a"], self.objects["vec_b_shifted"])
                # Transform into vec_c
                self.objects["vec_c"].set_opacity(1)
                self.play(Transform(group, self.objects["vec_c"]))
                # Fade in vec_c_label
                self.objects["vec_c_label"].set_opacity(1)
                self.play(Write(self.objects["vec_c_label"]))
                # Update explanation text
                new_text = Text("The sum vector C is the direct path from start to finish.", color=LIGHT_GRAY, font_size=24)
                new_text.move_to(self.objects["explanation_text"].get_center())
                self.play(ReplacementTransform(self.objects["explanation_text"], new_text))
                self.objects["explanation_text"] = new_text
                animation_time = 5.0
            else:
                animation_time = 0

            # Wait for remaining audio duration
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)

        # Final wait
        self.wait(2)