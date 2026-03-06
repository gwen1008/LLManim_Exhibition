'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the equivalence of fractions 1/2 and 2/4 using the area model of two identical circles (pizzas).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two pizzas side-by-side
#    - Footer Region: [Bottom y=-3.5] for equivalence statement
# 3. Anti-Overlap Check:
#    - Strategy: Place left pizza at LEFT*3, right pizza at RIGHT*3. Use VGroups for each pizza's components.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/visualizing_equivalent_fractions/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title and two whole pizzas.
#    - Step 2-4: Cut and color left pizza (1/2).
#    - Step 5-7: Cut and color right pizza (2/4).
#    - Step 8: Compare colored areas.
#    - Step 9: Show equivalence equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_an_animation__86dbc6609a/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        left_pizza_anchor = 3 * LEFT
        right_pizza_anchor = 3 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Helper to parse geometry_def (simplified for this specific case)
        def create_object(obj_spec):
            obj_id = obj_spec["id"]
            obj_type = obj_spec["type"]
            content = obj_spec.get("content", "")
            geometry_def = obj_spec.get("geometry_def", "")
            properties = obj_spec.get("properties", {})
            initial_pos = obj_spec.get("initial_pos", "")

            obj = None

            if obj_type == "Text":
                obj = Text(content, font_size=properties.get("font_size", 36))
            elif obj_type == "MathTex":
                obj = MathTex(content, font_size=properties.get("font_size", 36))
            elif obj_type == "Circle":
                # Parse radius from geometry_def string like "radius=2"
                radius = float(geometry_def.split("=")[1])
                obj = Circle(radius=radius, stroke_width=properties.get("stroke_width", 3))
            elif obj_type == "Line":
                # Parse start and end from geometry_def string like "start=UP*2, end=DOWN*2"
                # This is a simplified parser for the given definitions
                parts = geometry_def.split(", ")
                start_str = parts[0].replace("start=", "")
                end_str = parts[1].replace("end=", "")
                # Evaluate the vectors (safe within our controlled context)
                start = eval(start_str)
                end = eval(end_str)
                obj = Line(start, end, stroke_width=properties.get("stroke_width", 2))
            elif obj_type == "Sector":
                # Parse geometry_def: "outer_radius=2, inner_radius=0, angle=PI, start_angle=-PI/2"
                params = {}
                for part in geometry_def.split(", "):
                    key, val = part.split("=")
                    try:
                        params[key] = float(val)
                    except:
                        # Handle PI, PI/2 etc.
                        params[key] = eval(val)
                # Note: In Manim v0.19.2, first arg is 'radius' (outer_radius)
                obj = Sector(
                    radius=params.get("outer_radius", 2),
                    angle=params.get("angle", PI),
                    start_angle=params.get("start_angle", 0),
                    fill_opacity=properties.get("fill_opacity", 0.7),
                    stroke_width=properties.get("stroke_width", 0)
                )
                # Inner radius for Sector is always 0, we ignore inner_radius param

            if obj is not None:
                # Apply color if specified
                color_str = properties.get("color", "WHITE")
                color_map = {
                    "YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE,
                    "WHITE": WHITE, "BLACK": BLACK, "#FF9900": "#FF9900", "#0099FF": "#0099FF"
                }
                if color_str in color_map:
                    obj.set_color(color_map[color_str])
                else:
                    obj.set_color(color_str)  # For hex colors

                # Apply initial position
                if "move_to(title_anchor)" in initial_pos:
                    obj.move_to(title_anchor)
                elif "move_to(left_pizza_anchor)" in initial_pos:
                    obj.move_to(left_pizza_anchor)
                elif "move_to(right_pizza_anchor)" in initial_pos:
                    obj.move_to(right_pizza_anchor)
                elif "move_to(footer_anchor)" in initial_pos:
                    obj.move_to(footer_anchor)
                elif "next_to(pizza_left, DOWN, buff=0.5)" in initial_pos:
                    # Will be positioned after pizza_left is created
                    pass
                elif "next_to(pizza_right, DOWN, buff=0.5)" in initial_pos:
                    # Will be positioned after pizza_right is created
                    pass

                self.objects[obj_id] = obj

        # Create all objects from layout_plan
        objects_spec = [
            {
                "id": "title",
                "type": "Text",
                "content": "Visualizing Equivalent Fractions: 1/2 = 2/4",
                "initial_pos": "move_to(title_anchor)",
                "properties": {"color": "WHITE", "font_size": 40}
            },
            {
                "id": "pizza_left",
                "type": "Circle",
                "geometry_def": "radius=2",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {"color": "WHITE", "stroke_width": 3}
            },
            {
                "id": "pizza_right",
                "type": "Circle",
                "geometry_def": "radius=2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {"color": "WHITE", "stroke_width": 3}
            },
            {
                "id": "label_left_whole",
                "type": "MathTex",
                "content": "1",
                "initial_pos": "next_to(pizza_left, DOWN, buff=0.5)",
                "properties": {"color": "YELLOW"}
            },
            {
                "id": "label_right_whole",
                "type": "MathTex",
                "content": "1",
                "initial_pos": "next_to(pizza_right, DOWN, buff=0.5)",
                "properties": {"color": "YELLOW"}
            },
            {
                "id": "cut_line_left",
                "type": "Line",
                "geometry_def": "start=UP*2, end=DOWN*2",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {"color": "WHITE", "stroke_width": 2}
            },
            {
                "id": "slice_left",
                "type": "Sector",
                "geometry_def": "outer_radius=2, inner_radius=0, angle=PI, start_angle=-PI/2",
                "initial_pos": "move_to(left_pizza_anchor)",
                "properties": {"color": "#FF9900", "fill_opacity": 0.7, "stroke_width": 0}
            },
            {
                "id": "label_left_half",
                "type": "MathTex",
                "content": r"\frac{1}{2}",
                "initial_pos": "next_to(pizza_left, DOWN, buff=0.5)",
                "properties": {"color": "#FF9900"}
            },
            {
                "id": "cut_line_right_v",
                "type": "Line",
                "geometry_def": "start=UP*2, end=DOWN*2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {"color": "WHITE", "stroke_width": 2}
            },
            {
                "id": "cut_line_right_h",
                "type": "Line",
                "geometry_def": "start=LEFT*2, end=RIGHT*2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {"color": "WHITE", "stroke_width": 2}
            },
            {
                "id": "slice_right_1",
                "type": "Sector",
                "geometry_def": "outer_radius=2, inner_radius=0, angle=PI/2, start_angle=0",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {"color": "#0099FF", "fill_opacity": 0.7, "stroke_width": 0}
            },
            {
                "id": "slice_right_2",
                "type": "Sector",
                "geometry_def": "outer_radius=2, inner_radius=0, angle=PI/2, start_angle=PI/2",
                "initial_pos": "move_to(right_pizza_anchor)",
                "properties": {"color": "#0099FF", "fill_opacity": 0.7, "stroke_width": 0}
            },
            {
                "id": "label_right_quarters",
                "type": "MathTex",
                "content": r"\frac{2}{4}",
                "initial_pos": "next_to(pizza_right, DOWN, buff=0.5)",
                "properties": {"color": "#0099FF"}
            },
            {
                "id": "equivalence_statement",
                "type": "MathTex",
                "content": r"\frac{1}{2} = \frac{2}{4}",
                "initial_pos": "move_to(footer_anchor)",
                "properties": {"color": "GREEN", "font_size": 48}
            }
        ]

        for spec in objects_spec:
            create_object(spec)

        # Position labels relative to pizzas (now that pizzas exist)
        self.objects["label_left_whole"].next_to(self.objects["pizza_left"], DOWN, buff=0.5)
        self.objects["label_right_whole"].next_to(self.objects["pizza_right"], DOWN, buff=0.5)
        self.objects["label_left_half"].next_to(self.objects["pizza_left"], DOWN, buff=0.5)
        self.objects["label_right_quarters"].next_to(self.objects["pizza_right"], DOWN, buff=0.5)

        # Set z_index for slices to be above cut lines
        self.objects["slice_left"].set_z_index(1)
        self.objects["slice_right_1"].set_z_index(1)
        self.objects["slice_right_2"].set_z_index(1)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/visualizing_equivalent_fractions/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(
            Indicate(self.objects["pizza_left"], color=YELLOW, run_time=1),
            Indicate(self.objects["pizza_right"], color=YELLOW, run_time=1)
        )
        self.play(
            Write(self.objects["title"], run_time=1),
            Create(self.objects["pizza_left"], run_time=1),
            Create(self.objects["pizza_right"], run_time=1),
            Write(self.objects["label_left_whole"], run_time=0.5),
            Write(self.objects["label_right_whole"], run_time=0.5)
        )
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/visualizing_equivalent_fractions/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["pizza_left"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_line_left"], run_time=1))
        remaining_2 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/visualizing_equivalent_fractions/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["slice_left"], color=WHITE, run_time=1))
        self.play(FadeIn(self.objects["slice_left"], run_time=1))
        remaining_3 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/visualizing_equivalent_fractions/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(ReplacementTransform(
            self.objects["label_left_whole"],
            self.objects["label_left_half"]
        ), run_time=1.5)
        remaining_4 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/visualizing_equivalent_fractions/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["pizza_right"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["cut_line_right_v"], run_time=0.75),
            Create(self.objects["cut_line_right_h"], run_time=0.75)
        )
        remaining_5 = max(0.1, 2.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/visualizing_equivalent_fractions/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(
            Indicate(self.objects["slice_right_1"], color=WHITE, run_time=0.5),
            Indicate(self.objects["slice_right_2"], color=WHITE, run_time=0.5)
        )
        self.play(
            FadeIn(self.objects["slice_right_1"], run_time=0.75),
            FadeIn(self.objects["slice_right_2"], run_time=0.75)
        )
        remaining_6 = max(0.1, 2.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/visualizing_equivalent_fractions/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(ReplacementTransform(
            self.objects["label_right_whole"],
            self.objects["label_right_quarters"]
        ), run_time=1.5)
        remaining_7 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # ========== Step 8 ==========
        audio_step8 = "media/audio/visualizing_equivalent_fractions/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        self.play(
            Indicate(self.objects["slice_left"], color=YELLOW, run_time=0.5),
            Indicate(self.objects["slice_right_1"], color=YELLOW, run_time=0.5),
            Indicate(self.objects["slice_right_2"], color=YELLOW, run_time=0.5)
        )
        # Pulsate fill colors
        self.play(
            self.objects["slice_left"].animate.set_fill(opacity=0.9),
            self.objects["slice_right_1"].animate.set_fill(opacity=0.9),
            self.objects["slice_right_2"].animate.set_fill(opacity=0.9),
            run_time=0.5
        )
        self.play(
            self.objects["slice_left"].animate.set_fill(opacity=0.7),
            self.objects["slice_right_1"].animate.set_fill(opacity=0.7),
            self.objects["slice_right_2"].animate.set_fill(opacity=0.7),
            run_time=0.5
        )
        remaining_8 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))

        # ========== Step 9 ==========
        audio_step9 = "media/audio/visualizing_equivalent_fractions/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))

        self.play(Write(self.objects["equivalence_statement"], run_time=2))
        remaining_9 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))

        # Final hold
        self.wait(max(0.1, 2))