from manim import *
import os

# Import LayoutEngine for robust zone management
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Initialize Layout Engine
        layout = LayoutEngine()

        # Create a registry for objects to reference later
        self.objects = {}

        # --- Create Objects from layout_plan.objects ---
        # Title
        title = Text("Unrolling a Circle: Discovering π", color=WHITE, font_size=40)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # Circle (radius=2, D=4)
        circle = Circle(radius=2.0, color=BLUE, stroke_width=4)
        obj_circle = LayoutObject(circle, "circle")
        layout.add(obj_circle)
        layout.add_to_zone(obj_circle, "CONTENT")
        # Position circle to the left within content zone
        layout.add_constraint(obj_circle.center_x == -3.0)
        layout.add_constraint(obj_circle.center_y == 0.0)
        self.objects["circle"] = circle

        # Diameter Line (from circle's left to right)
        diameter_line = Line(circle.get_left(), circle.get_right(), color=YELLOW, stroke_width=6)
        diameter_line.move_to(circle.get_center())
        obj_diameter_line = LayoutObject(diameter_line, "diameter_line")
        layout.add(obj_diameter_line)
        # Keep it with the circle
        layout.add_constraint(obj_diameter_line.center_x == obj_circle.center_x)
        layout.add_constraint(obj_diameter_line.center_y == obj_circle.center_y)
        self.objects["diameter_line"] = diameter_line

        # Label D
        label_d = MathTex("D", color=YELLOW)
        obj_label_d = LayoutObject(label_d, "label_d")
        layout.add(obj_label_d)
        # Position above diameter line
        layout.align_to(obj_label_d, obj_diameter_line, "TOP", buff=0.2)
        layout.align_to(obj_label_d, obj_diameter_line, "CENTER_X")
        self.objects["label_d"] = label_d

        # Circumference String (Arc matching circle)
        circumference_string = Arc(radius=2.0, angle=TAU, start_angle=0, color=GREEN, stroke_width=8)
        circumference_string.move_to(circle.get_center())
        obj_circumference_string = LayoutObject(circumference_string, "circumference_string")
        layout.add(obj_circumference_string)
        # Overlay on circle
        layout.add_constraint(obj_circumference_string.center_x == obj_circle.center_x)
        layout.add_constraint(obj_circumference_string.center_y == obj_circle.center_y)
        self.objects["circumference_string"] = circumference_string

        # Straight Line (unrolled circumference, length = 2πr ≈ 12.566)
        straight_line = Line(start=[0, 0.5, 0], end=[12.566, 0.5, 0], color=GREEN, stroke_width=8)
        # Center the line horizontally in the right part of content zone
        obj_straight_line = LayoutObject(straight_line, "straight_line")
        layout.add(obj_straight_line)
        layout.add_to_zone(obj_straight_line, "CONTENT")
        layout.add_constraint(obj_straight_line.center_x == 3.0)
        layout.add_constraint(obj_straight_line.center_y == 0.5)
        self.objects["straight_line"] = straight_line

        # Label C
        label_c = MathTex("C", color=GREEN)
        obj_label_c = LayoutObject(label_c, "label_c")
        layout.add(obj_label_c)
        # Position above straight line
        layout.align_to(obj_label_c, obj_straight_line, "TOP", buff=0.2)
        layout.align_to(obj_label_c, obj_straight_line, "CENTER_X")
        self.objects["label_c"] = label_c

        # Ruler (expanding rectangle to measure line)
        ruler = Rectangle(height=0.5, width=0.0, color=WHITE, fill_opacity=0.2, stroke_width=2)
        obj_ruler = LayoutObject(ruler, "ruler")
        layout.add(obj_ruler)
        # Position below straight line, left-aligned
        layout.align_to(obj_ruler, obj_straight_line, "BOTTOM", buff=0.5)
        layout.align_to(obj_ruler, obj_straight_line, "LEFT")
        self.objects["ruler"] = ruler

        # D Segment (one unit of length D=4)
        d_segment = Line(start=[0, 0, 0], end=[4, 0, 0], color=YELLOW, stroke_width=6)
        obj_d_segment = LayoutObject(d_segment, "d_segment")
        layout.add(obj_d_segment)
        # Position in comparison area (below main content)
        layout.add_to_zone(obj_d_segment, "CONTENT")
        layout.add_constraint(obj_d_segment.center_y == -2.0)
        layout.add_constraint(obj_d_segment.center_x == -4.0)  # Start left
        self.objects["d_segment"] = d_segment

        # Label for D segment copy
        label_d_copy = MathTex("D", color=YELLOW)
        obj_label_d_copy = LayoutObject(label_d_copy, "label_d_copy")
        layout.add(obj_label_d_copy)
        layout.align_to(obj_label_d_copy, obj_d_segment, "TOP", buff=0.1)
        layout.align_to(obj_label_d_copy, obj_d_segment, "CENTER_X")
        self.objects["label_d_copy"] = label_d_copy

        # Three D Group (container for three segments)
        three_d_group = VGroup()
        obj_three_d_group = LayoutObject(three_d_group, "three_d_group")
        layout.add(obj_three_d_group)
        # Position at comparison anchor (center below)
        layout.add_constraint(obj_three_d_group.center_x == 0)
        layout.add_constraint(obj_three_d_group.center_y == -2.0)
        self.objects["three_d_group"] = three_d_group

        # Gap Line (leftover after 3D, length ≈ 0.566)
        gap_line = Line(start=[0, 0, 0], end=[0.566, 0, 0], color=RED, stroke_width=6)
        obj_gap_line = LayoutObject(gap_line, "gap_line")
        layout.add(obj_gap_line)
        # Position to the right of the three D group
        layout.align_to(obj_gap_line, obj_three_d_group, "RIGHT", buff=0.0)
        layout.align_to(obj_gap_line, obj_three_d_group, "CENTER_Y")
        self.objects["gap_line"] = gap_line

        # Formula C = ? * D
        formula_c_eq_d = MathTex(r"C \,=\, ? \times D", color=WHITE, font_size=36)
        obj_formula_c_eq_d = LayoutObject(formula_c_eq_d, "formula_c_eq_d")
        layout.add(obj_formula_c_eq_d)
        layout.add_to_zone(obj_formula_c_eq_d, "FOOTER")
        layout.add_constraint(obj_formula_c_eq_d.center_x == 0)
        self.objects["formula_c_eq_d"] = formula_c_eq_d

        # Formula π approximation
        formula_pi = MathTex(r"\pi \approx 3.14159...", color=PINK, font_size=30)
        obj_formula_pi = LayoutObject(formula_pi, "formula_pi")
        layout.add(obj_formula_pi)
        layout.add_to_zone(obj_formula_pi, "FOOTER")
        layout.align_to(obj_formula_pi, obj_formula_c_eq_d, "BOTTOM", buff=0.3)
        layout.align_to(obj_formula_pi, obj_formula_c_eq_d, "CENTER_X")
        self.objects["formula_pi"] = formula_pi

        # Final formula C = πD - FIXED: Use GREEN instead of undefined GREEN_YELLOW
        formula_final = MathTex(r"C = \pi D", color=GREEN, font_size=40)
        obj_formula_final = LayoutObject(formula_final, "formula_final")
        layout.add(obj_formula_final)
        layout.add_to_zone(obj_formula_final, "FOOTER")
        layout.add_constraint(obj_formula_final.center_x == 0)
        layout.add_constraint(obj_formula_final.center_y == obj_formula_c_eq_d.center_y)
        self.objects["formula_final"] = formula_final

        # Solve all layout constraints
        layout.solve()

        # Initially hide objects that appear later
        straight_line.set_opacity(0)
        label_c.set_opacity(0)
        ruler.set_opacity(0)
        d_segment.set_opacity(0)
        label_d_copy.set_opacity(0)
        three_d_group.set_opacity(0)
        gap_line.set_opacity(0)
        formula_pi.set_opacity(0)
        formula_final.set_opacity(0)

        # Add title to scene from the start
        self.add(title)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start with a circle. Its diameter, labeled D, is the distance across it through the center.",
                "signal_action": {
                    "type": "Create",
                    "target": "circle"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "circle",
                    "details": "Draw the blue circle."
                },
                "duration": 6.912,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓。將圓周「展開」成一條直線，證明其長度略大於_3_倍的直徑_(Pi)。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Now, imagine wrapping a green string tightly around the circle. This string's length is the circumference, C.",
                "signal_action": {
                    "type": "Create",
                    "target": "circumference_string"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "circumference_string",
                    "details": "Overlay the green arc (string) on the circle."
                },
                "duration": 7.68,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓。將圓周「展開」成一條直線，證明其長度略大於_3_倍的直徑_(Pi)。/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Let's carefully unroll the string, transforming it from the circular path into a straight line.",
                "signal_action": {
                    "type": "ReplacementTransform",
                    "target": "circumference_string",
                    "source": "circumference_string",
                    "target_obj": "straight_line"
                },
                "visual_action": {
                    "type": "ReplacementTransform",
                    "target_id": "circumference_string",
                    "details": "Morph the green arc into the straight horizontal line. The circle can fade out to reduce clutter.",
                    "additional_actions": [
                        {
                            "type": "FadeOut",
                            "target_id": "circle"
                        },
                        {
                            "type": "FadeOut",
                            "target_id": "diameter_line"
                        },
                        {
                            "type": "FadeOut",
                            "target_id": "label_d"
                        }
                    ]
                },
                "duration": 5.976,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓。將圓周「展開」成一條直線，證明其長度略大於_3_倍的直徑_(Pi)。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "We can measure this line, C. Now, how does it compare to the diameter D? Let's place three copies of D end-to-end below C.",
                "signal_action": {
                    "type": "GrowFromCenter",
                    "target": "ruler"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "label_c",
                    "details": "Label the line as C."
                },
                "duration": 8.904,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓。將圓周「展開」成一條直線，證明其長度略大於_3_倍的直徑_(Pi)。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Three D's reach most of the way, but don't quite cover C. There's a small gap left.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "gap_line",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "gap_line",
                    "details": "Show the red gap line. Simultaneously, write the evolving formula C = ? * D at the bottom."
                },
                "duration": 5.568,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓。將圓周「展開」成一條直線，證明其長度略大於_3_倍的直徑_(Pi)。/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The number we need to multiply D by to get C is a special constant, Pi. It's approximately 3.14159. So, the circumference is Pi times the diameter.",
                "signal_action": {
                    "type": "TransformMatchingTex",
                    "target": "formula_c_eq_d",
                    "source": "formula_c_eq_d",
                    "target_obj": "formula_final"
                },
                "visual_action": {
                    "type": "ReplacementTransform",
                    "target_id": "formula_c_eq_d",
                    "details": "Morph the formula into C = πD. Fade in the pi approximation text below it.",
                    "additional_actions": [
                        {
                            "type": "Write",
                            "target_id": "formula_pi"
                        }
                    ]
                },
                "duration": 12.216,
                "audio_path": "media/audio/呈現一個直徑為_D_的圓。將圓周「展開」成一條直線，證明其長度略大於_3_倍的直徑_(Pi)。/step_05.mp3"
            }
        ]

        # Process each step
        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step["audio_path"]

            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            else:
                # Fallback path construction (legacy)
                file_index = step_num - 1
                mp3_path = f"media/audio/step_{file_index:02d}.mp3"
                wav_path = f"media/audio/step_{file_index:02d}.wav"
                if os.path.exists(mp3_path):
                    self.add_sound(mp3_path)
                elif os.path.exists(wav_path):
                    self.add_sound(wav_path)

            # Track animation runtime for this step
            animation_time = 0

            # --- Signal Action ---
            signal_action = step.get("signal_action")
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_id = signal_action["target"]

                target_obj = self.objects.get(target_id)
                if target_obj is not None:
                    if signal_type == "Create":
                        self.play(Create(target_obj), run_time=1)
                        animation_time += 1
                    elif signal_type == "ReplacementTransform":
                        source_id = signal_action.get("source")
                        target_obj_id = signal_action.get("target_obj")
                        source_obj = self.objects.get(source_id)
                        new_target_obj = self.objects.get(target_obj_id)
                        if source_obj and new_target_obj:
                            self.play(ReplacementTransform(source_obj, new_target_obj), run_time=1)
                            animation_time += 1
                    elif signal_type == "GrowFromCenter":
                        self.play(GrowFromCenter(target_obj), run_time=1)
                        animation_time += 1
                    elif signal_type == "Indicate":
                        color_str = signal_action.get("color", "YELLOW")
                        color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                        color = color_map.get(color_str, YELLOW)
                        self.play(Indicate(target_obj, color=color), run_time=1)
                        animation_time += 1
                    elif signal_type == "TransformMatchingTex":
                        source_id = signal_action.get("source")
                        target_obj_id = signal_action.get("target_obj")
                        source_obj = self.objects.get(source_id)
                        new_target_obj = self.objects.get(target_obj_id)
                        if source_obj and new_target_obj:
                            self.play(TransformMatchingTex(source_obj, new_target_obj), run_time=1)
                            animation_time += 1

            # --- Visual Action ---
            visual_action = step.get("visual_action")
            if visual_action is not None:
                action_type = visual_action["type"]
                target_id = visual_action.get("target_id")

                if action_type == "Create":
                    target_obj = self.objects.get(target_id)
                    if target_obj:
                        self.play(Write(target_obj), run_time=1)
                        animation_time += 1
                elif action_type == "ReplacementTransform":
                    target_obj = self.objects.get(target_id)
                    # In step 3, the ReplacementTransform is already handled by signal_action.
                    # Here we handle additional_actions.
                    additional_actions = visual_action.get("additional_actions", [])
                    for add_action in additional_actions:
                        add_type = add_action["type"]
                        add_target_id = add_action["target_id"]
                        add_target = self.objects.get(add_target_id)
                        if add_target:
                            if add_type == "FadeOut":
                                self.play(FadeOut(add_target), run_time=0.5)
                                animation_time += 0.5
                            elif add_type == "Write":
                                self.play(Write(add_target), run_time=1)
                                animation_time += 1

                # For step 4, we also need to create the three D segments and label
                if step_num == 4:
                    # Make ruler visible and grow it to the length of straight_line
                    ruler.set_opacity(1)
                    # FIXED: Use set_width without stretch parameter
                    self.play(ruler.animate.set_width(straight_line.get_length()).align_to(straight_line, LEFT), run_time=1.5)
                    animation_time += 1.5

                    # Create three D segments end-to-end
                    d1 = d_segment.copy()
                    d2 = d_segment.copy()
                    d3 = d_segment.copy()
                    d1.move_to(three_d_group.get_center())
                    d2.next_to(d1, RIGHT, buff=0)
                    d3.next_to(d2, RIGHT, buff=0)
                    three_d_group.add(d1, d2, d3)
                    self.objects["three_d_group"] = three_d_group

                    # Create labels for each segment
                    label1 = label_d_copy.copy()
                    label2 = label_d_copy.copy()
                    label3 = label_d_copy.copy()
                    label1.next_to(d1, UP, buff=0.1)
                    label2.next_to(d2, UP, buff=0.1)
                    label3.next_to(d3, UP, buff=0.1)

                    # Animate segments and labels appearing
                    self.play(
                        FadeIn(d1), Write(label1),
                        FadeIn(d2), Write(label2),
                        FadeIn(d3), Write(label3),
                        run_time=2
                    )
                    animation_time += 2

                # For step 5, show the formula C = ? * D
                if step_num == 5:
                    formula_c_eq_d.set_opacity(1)
                    self.play(Write(formula_c_eq_d), run_time=1)
                    animation_time += 1

            # Wait for remaining audio duration
            remaining = duration - animation_time
            if remaining > 0:
                self.wait(remaining)

        # Final wait
        self.wait(2)