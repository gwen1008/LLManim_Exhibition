'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate fraction equivalence 1/2 = 2/4 using a concrete pizza analogy.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Fraction Equivalence: 1/2 = 2/4"
#    - Main Content: [Center y=0] for two pizzas side-by-side (left at x=-3.5, right at x=3.5)
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanations and final equation.
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each pizza (base + sectors + cuts + label) to manage positioning as a unit.
#    - Keep pizzas horizontally separated (LEFT*3.5 and RIGHT*3.5) to prevent overlap.
#    - Center stage (origin) reserved for final equivalence overlay, which will be faded out.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow:
#    - Step 1-4: Introduce two whole pizzas, title, and initial explanation.
#    - Step 5-7: Cut and color the left pizza (1/2).
#    - Step 8-12: Cut and color the right pizza (2/4).
#    - Step 13-14: Compare colored regions.
#    - Step 15: Overlay and morph colored sectors at center to show equivalence.
#    - Step 16: Display final equation.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        left_pizza_anchor = 3.5 * LEFT
        right_pizza_anchor = 3.5 * RIGHT
        footer_anchor = 3.5 * DOWN
        center_stage = ORIGIN

        # Object registry
        self.objects = {}

        # Helper to parse geometry_def strings (simplified for this specific JSON)
        def create_object(obj_def):
            obj_id = obj_def["id"]
            obj_type = obj_def["type"]
            initial_pos_cmd = obj_def.get("initial_pos", "")
            properties = obj_def.get("properties", {})
            content = obj_def.get("content", "")

            # Map color names to Manim constants (correcting deprecated ones)
            color_map = {
                "GRAY_C": GRAY_B,
                "BLUE": BLUE,
                "GREEN": GREEN,
                "WHITE": WHITE,
                "YELLOW": YELLOW,
                "GRAY_C": GRAY_B,
            }
            for key, value in properties.items():
                if key == "color" and value in color_map:
                    properties[key] = color_map[value]

            # Create object based on type
            if obj_type == "Text":
                obj = Text(content, color=properties.get("color", WHITE), font_size=properties.get("font_size", 36))
            elif obj_type == "MathTex":
                obj = MathTex(content, color=properties.get("color", WHITE), font_size=properties.get("font_size", 36))
            elif obj_type == "Circle":
                # geometry_def: "radius=2"
                radius = float(obj_def["geometry_def"].split("=")[1])
                obj = Circle(radius=radius, color=properties.get("color", WHITE),
                             fill_opacity=properties.get("fill_opacity", 0),
                             stroke_width=properties.get("stroke_width", 4))
            elif obj_type == "Sector":
                # geometry_def: "outer_radius=2, angle=PI, start_angle=0"
                parts = obj_def["geometry_def"].split(", ")
                import math
                params = {}
                for part in parts:
                    key, val = part.split("=")
                    params[key] = eval(val, {"PI": math.pi, "math": math})
                # Note: In Manim v0.19.2, Sector's first argument is radius (not outer_radius)
                obj = Sector(radius=params.get("outer_radius", 2),
                             angle=params.get("angle", PI),
                             start_angle=params.get("start_angle", 0),
                             color=properties.get("color", WHITE),
                             fill_opacity=properties.get("fill_opacity", 0),
                             stroke_width=properties.get("stroke_width", 0))
            elif obj_type == "Line":
                # geometry_def: "start=UP*2, end=DOWN*2"
                # This is a simplified parser for the specific format in JSON
                import re
                import math
                def parse_vec(s):
                    s = s.strip()
                    if s.startswith("UP"):
                        multiplier_str = s[2:].strip()
                        if multiplier_str == '':
                            multiplier = 1.0
                        else:
                            # Handle cases like '*2' by prepending '1'
                            if multiplier_str.startswith('*'):
                                multiplier_str = '1' + multiplier_str
                            multiplier = eval(multiplier_str, {"PI": math.pi, "math": math})
                        return multiplier * UP
                    elif s.startswith("DOWN"):
                        multiplier_str = s[4:].strip()
                        if multiplier_str == '':
                            multiplier = 1.0
                        else:
                            if multiplier_str.startswith('*'):
                                multiplier_str = '1' + multiplier_str
                            multiplier = eval(multiplier_str, {"PI": math.pi, "math": math})
                        return multiplier * DOWN
                    elif s.startswith("LEFT"):
                        multiplier_str = s[4:].strip()
                        if multiplier_str == '':
                            multiplier = 1.0
                        else:
                            if multiplier_str.startswith('*'):
                                multiplier_str = '1' + multiplier_str
                            multiplier = eval(multiplier_str, {"PI": math.pi, "math": math})
                        return multiplier * LEFT
                    elif s.startswith("RIGHT"):
                        multiplier_str = s[5:].strip()
                        if multiplier_str == '':
                            multiplier = 1.0
                        else:
                            if multiplier_str.startswith('*'):
                                multiplier_str = '1' + multiplier_str
                            multiplier = eval(multiplier_str, {"PI": math.pi, "math": math})
                        return multiplier * RIGHT
                    else:
                        return ORIGIN
                start_str, end_str = obj_def["geometry_def"].split(", ")
                start_vec = parse_vec(start_str.split("=")[1].strip())
                end_vec = parse_vec(end_str.split("=")[1].strip())
                obj = Line(start=start_vec, end=end_vec,
                           color=properties.get("color", WHITE),
                           stroke_width=properties.get("stroke_width", 4))
            else:
                # Fallback (should not happen with given JSON)
                obj = Text(f"Unknown: {obj_id}")

            # Apply initial position
            if "move_to(title_anchor)" in initial_pos_cmd:
                obj.move_to(title_anchor)
            elif "move_to(left_pizza_anchor)" in initial_pos_cmd:
                obj.move_to(left_pizza_anchor)
            elif "move_to(right_pizza_anchor)" in initial_pos_cmd:
                obj.move_to(right_pizza_anchor)
            elif "move_to(footer_anchor)" in initial_pos_cmd:
                obj.move_to(footer_anchor)
            elif "move_to(center_stage)" in initial_pos_cmd:
                obj.move_to(center_stage)
            elif "next_to(pizza_left_base, DOWN, buff=0.5)" in initial_pos_cmd:
                # Will be positioned after pizza_left_base is created
                pass
            elif "next_to(pizza_right_base, DOWN, buff=0.5)" in initial_pos_cmd:
                # Will be positioned after pizza_right_base is created
                pass

            self.objects[obj_id] = obj
            return obj

        # Create all objects from layout_plan.objects
        # We'll create them in an order that allows dependent positioning
        objects_def = [
            {
                "id": "title",
                "type": "Text",
                "content": "Fraction Equivalence: 1/2 = 2/4",
                "initial_pos": "move_to(title_anchor)",
                "properties": {
                    "color": "WHITE",
                    "font_size": 40
                }
            },
            {
                "id": "pizza_left_base",
                "type": "Circle",
                "geometry_def": "radius=2",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {
                    "color": "GRAY_C",
                    "fill_opacity": 0.3,
                    "stroke_width": 3
                }
            },
            {
                "id": "pizza_right_base",
                "type": "Circle",
                "geometry_def": "radius=2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "GRAY_C",
                    "fill_opacity": 0.3,
                    "stroke_width": 3
                }
            },
            {
                "id": "left_half1",
                "type": "Sector",
                "geometry_def": "outer_radius=2, angle=PI, start_angle=0",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {
                    "color": "BLUE",
                    "fill_opacity": 0.0,
                    "stroke_width": 0
                }
            },
            {
                "id": "left_half2",
                "type": "Sector",
                "geometry_def": "outer_radius=2, angle=PI, start_angle=PI",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {
                    "color": "WHITE",
                    "fill_opacity": 0.0,
                    "stroke_width": 0
                }
            },
            {
                "id": "right_quarter1",
                "type": "Sector",
                "geometry_def": "outer_radius=2, angle=PI/2, start_angle=0",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "GREEN",
                    "fill_opacity": 0.0,
                    "stroke_width": 0
                }
            },
            {
                "id": "right_quarter2",
                "type": "Sector",
                "geometry_def": "outer_radius=2, angle=PI/2, start_angle=PI/2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "GREEN",
                    "fill_opacity": 0.0,
                    "stroke_width": 0
                }
            },
            {
                "id": "right_quarter3",
                "type": "Sector",
                "geometry_def": "outer_radius=2, angle=PI/2, start_angle=PI",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "WHITE",
                    "fill_opacity": 0.0,
                    "stroke_width": 0
                }
            },
            {
                "id": "right_quarter4",
                "type": "Sector",
                "geometry_def": "outer_radius=2, angle=PI/2, start_angle=3*PI/2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "WHITE",
                    "fill_opacity": 0.0,
                    "stroke_width": 0
                }
            },
            {
                "id": "cut_line_left",
                "type": "Line",
                "geometry_def": "start=UP*2, end=DOWN*2",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {
                    "color": "WHITE",
                    "stroke_width": 4
                }
            },
            {
                "id": "cut_line_right_h",
                "type": "Line",
                "geometry_def": "start=LEFT*2, end=RIGHT*2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "WHITE",
                    "stroke_width": 4
                }
            },
            {
                "id": "cut_line_right_v",
                "type": "Line",
                "geometry_def": "start=UP*2, end=DOWN*2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {
                    "color": "WHITE",
                    "stroke_width": 4
                }
            },
            {
                "id": "footer_text",
                "type": "Text",
                "content": "Let's start with two identical whole pizzas.",
                "initial_pos": "move_to(footer_anchor)",
                "properties": {
                    "color": "GRAY_C",
                    "font_size": 28
                }
            }
        ]

        for obj_def in objects_def:
            create_object(obj_def)

        # Create labels that need positioning relative to bases
        label_left = MathTex(r"\frac{1}{2}", color=BLUE, font_size=36)
        label_left.next_to(self.objects["pizza_left_base"], DOWN, buff=0.5)
        self.objects["label_left"] = label_left

        label_right = MathTex(r"\frac{2}{4}", color=GREEN, font_size=36)
        label_right.next_to(self.objects["pizza_right_base"], DOWN, buff=0.5)
        self.objects["label_right"] = label_right

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_00.mp3")  # [auto-injected] duration=3.12s
        _audio_dur_0 = 3.12  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Create(self.objects["pizza_left_base"]), run_time=1.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_04.mp3")  # [auto-injected] duration=3.86s
        _audio_dur_1 = 3.86  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Create(self.objects["pizza_right_base"]), run_time=1.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_05.mp3")  # [auto-injected] duration=3.94s
        _audio_dur_2 = 3.94  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Write(self.objects["title"]), run_time=1.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_06.mp3")  # [auto-injected] duration=3.02s
        _audio_dur_3 = 3.02  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Write(self.objects["footer_text"]), run_time=1.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_07.mp3")  # [auto-injected] duration=4.08s
        _audio_dur_4 = 4.08  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Indicate(self.objects["pizza_left_base"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_left"]), run_time=2.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_09.mp3")  # [auto-injected] duration=4.61s
        _audio_dur_5 = 4.61  # [audio-sync] actual TTS duration
        # Step 6
        self.play(Indicate(self.objects["left_half1"], color=YELLOW, run_time=1))
        # Transform: change fill_opacity from 0.0 to 0.7
        left_half1_filled = self.objects["left_half1"].copy().set_fill(opacity=0.7)
        self.play(Transform(self.objects["left_half1"], left_half1_filled), run_time=2.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_11.mp3")  # [auto-injected] duration=3.31s
        _audio_dur_6 = 3.31  # [audio-sync] actual TTS duration
        # Step 7
        self.play(Write(self.objects["label_left"]), run_time=2.0)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_12.mp3")  # [auto-injected] duration=5.23s
        _audio_dur_7 = 5.23  # [audio-sync] actual TTS duration
        # Step 8
        self.play(Indicate(self.objects["pizza_right_base"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_right_v"]), run_time=1.5)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_13.mp3")  # [auto-injected] duration=3.14s
        _audio_dur_8 = 3.14  # [audio-sync] actual TTS duration
        # Step 9
        self.play(Create(self.objects["cut_line_right_h"]), run_time=1.5)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_14.mp3")  # [auto-injected] duration=8.18s
        _audio_dur_9 = 8.18  # [audio-sync] actual TTS duration
        # Step 10
        self.play(Indicate(self.objects["right_quarter1"], color=YELLOW, run_time=1))
        right_quarter1_filled = self.objects["right_quarter1"].copy().set_fill(opacity=0.7)
        self.play(Transform(self.objects["right_quarter1"], right_quarter1_filled), run_time=1.5)
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))

        self.add_sound("media/audio/Create_two_identical_ef36b15d3f/step_15.mp3")  # [auto-injected] duration=7.32s
        _audio_dur_10 = 7.32  # [audio-sync] actual TTS duration
        # Step 11
        right_quarter2_filled = self.objects["right_quarter2"].copy().set_fill(opacity=0.7)
        self.play(Transform(self.objects["right_quarter2"], right_quarter2_filled), run_time=1.5)
        remaining_11 = _audio_dur_10  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_11))

        # Step 12
        self.play(Write(self.objects["label_right"]), run_time=2.0)
        remaining_12 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_12))

        # Step 13
        self.play(Circumscribe(self.objects["left_half1"], color=YELLOW, run_time=1))
        self.play(FadeOut(self.objects["footer_text"]), run_time=2.5)
        remaining_13 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_13))

        # Step 14
        green_group = VGroup(self.objects["right_quarter1"], self.objects["right_quarter2"])
        self.play(Circumscribe(green_group, color=YELLOW, run_time=1))
        # Update footer text
        new_footer = Text("Comparing the colored areas...", color=GRAY_B, font_size=28).move_to(footer_anchor)
        self.play(Write(new_footer), run_time=2.5)
        self.objects["footer_text"] = new_footer  # Update registry
        remaining_14 = max(0.1, 2.5 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_14))

        # Step 15: Equivalence demonstration overlay
        # 1) Create a copy of left_half1 (blue) at center
        blue_copy = self.objects["left_half1"].copy().move_to(center_stage)
        # 2) Create a VGroup copy of the two green quarters at center, slightly offset
        green_copy1 = self.objects["right_quarter1"].copy().move_to(center_stage).shift(0.5 * LEFT)
        green_copy2 = self.objects["right_quarter2"].copy().move_to(center_stage).shift(0.5 * LEFT)
        green_vgroup = VGroup(green_copy1, green_copy2)
        # Add them to scene
        self.play(FadeIn(blue_copy), FadeIn(green_vgroup), run_time=1.0)
        # 3) Animate green VGroup to rotate and merge into blue shape
        # Target position for merged green sectors: same as blue sector
        # We'll animate each green sector to the correct angle and position
        target_green1 = Sector(radius=2, angle=PI/2, start_angle=0, color=GREEN, fill_opacity=0.7, stroke_width=0).move_to(center_stage)
        target_green2 = Sector(radius=2, angle=PI/2, start_angle=PI/2, color=GREEN, fill_opacity=0.7, stroke_width=0).move_to(center_stage)
        self.play(
            Transform(green_copy1, target_green1),
            Transform(green_copy2, target_green2),
            run_time=3.0
        )
        # Brief pause to show they match
        self.wait(max(0.1, 1.0))
        # 4) Fade out both temporary sectors
        self.play(FadeOut(blue_copy), FadeOut(green_vgroup), run_time=1.0)
        remaining_15 = max(0.1, 6.0 - (1.0 + 3.0 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_15))

        # Step 16
        final_eq = Text("Therefore: 1/2 = 2/4", color=YELLOW, font_size=28).move_to(footer_anchor)
        self.play(ReplacementTransform(self.objects["footer_text"], final_eq), run_time=4.0)
        self.objects["footer_text"] = final_eq
        remaining_16 = max(0.1, 4.0 - 4.0 + 0.5)
        self.wait(max(0.1, remaining_16))