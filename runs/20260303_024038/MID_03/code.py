'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize solving the linear equation 2x = 6 using a balance scale metaphor. The unknown 'x' is represented by blue boxes, and units by orange circles. Dividing both sides by 2 is shown by removing half the objects from each pan.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for the balance scale and objects
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: The scale is centered. Objects are placed inside pans using relative positioning. Labels are placed next to pans. The final equation appears below the scale, separate from the explanation.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/solving_2x_equals_6/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Title appears.
#    - Step 2: Build the scale structure.
#    - Step 3: Add left side boxes and label.
#    - Step 4: Add right side circles and label.
#    - Step 5: Update explanation text for division.
#    - Step 6: Animate removal of one box and three circles.
#    - Step 7: Transform labels from "2x" to "x" and "6" to "3".
#    - Step 8: Write final solution "x = 3" and highlight remaining objects.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors from layout_plan
        title_anchor = 3.5 * UP
        scale_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Helper to parse position strings (simplified for this specific JSON)
        def parse_position(pos_str, ref_obj=None):
            if pos_str == "move_to(title_anchor)":
                return title_anchor
            elif pos_str == "move_to(scale_anchor)":
                return scale_anchor
            elif pos_str == "move_to(scale_anchor + UP*1.0)":
                return scale_anchor + UP
            elif pos_str == "move_to(scale_anchor + DOWN*2.2)":
                return scale_anchor + DOWN * 2.2
            elif pos_str == "move_to(explanation_anchor)":
                return explanation_anchor
            elif pos_str == "move_to(scale_beam.get_center() + DOWN*0.5)":
                # Will be set after scale_beam is created
                return None
            elif pos_str == "move_to(scale_anchor + LEFT*2.5 + DOWN*1.0)":
                return scale_anchor + LEFT * 2.5 + DOWN
            elif pos_str == "move_to(scale_anchor + RIGHT*2.5 + DOWN*1.0)":
                return scale_anchor + RIGHT * 2.5 + DOWN
            elif pos_str == "move_to(left_pan.get_center() + UP*0.35)":
                # Will be set after left_pan is created
                return None
            elif pos_str == "move_to(left_pan.get_center() + DOWN*0.35)":
                return None
            elif pos_str == "move_to(right_pan.get_center() + LEFT*0.4 + UP*0.4)":
                return None
            elif pos_str == "move_to(right_pan.get_center() + RIGHT*0.4 + UP*0.4)":
                return None
            elif pos_str == "move_to(right_pan.get_center() + LEFT*0.4)":
                return None
            elif pos_str == "move_to(right_pan.get_center() + RIGHT*0.4)":
                return None
            elif pos_str == "move_to(right_pan.get_center() + LEFT*0.4 + DOWN*0.4)":
                return None
            elif pos_str == "move_to(right_pan.get_center() + RIGHT*0.4 + DOWN*0.4)":
                return None
            elif pos_str.startswith("next_to("):
                # Will be handled after the reference object is created
                return None
            else:
                return ORIGIN

        # Create objects from layout_plan.objects
        # We'll create them in two passes: first the independent ones, then the dependent ones.

        # Pass 1: Create objects with independent positions
        obj_defs = [
            {
                "id": "title",
                "type": "Text",
                "content": "Solving 2x = 6 with a Balance Scale",
                "pos": title_anchor,
                "props": {"color": WHITE, "font_size": 36}
            },
            {
                "id": "scale_beam",
                "type": "Line",
                "start": LEFT * 3,
                "end": RIGHT * 3,
                "pos": scale_anchor + UP,
                "props": {"color": GRAY_C, "stroke_width": 8}
            },
            {
                "id": "left_pan",
                "type": "Circle",
                "radius": 0.8,
                "pos": scale_anchor + LEFT * 2.5 + DOWN,
                "props": {"color": WHITE, "stroke_width": 3}
            },
            {
                "id": "right_pan",
                "type": "Circle",
                "radius": 0.8,
                "pos": scale_anchor + RIGHT * 2.5 + DOWN,
                "props": {"color": WHITE, "stroke_width": 3}
            },
            {
                "id": "box1",
                "type": "Square",
                "side_length": 0.7,
                "pos": None,  # Will set after left_pan
                "props": {"color": BLUE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "box2",
                "type": "Square",
                "side_length": 0.7,
                "pos": None,
                "props": {"color": BLUE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "circle1",
                "type": "Circle",
                "radius": 0.3,
                "pos": None,
                "props": {"color": ORANGE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "circle2",
                "type": "Circle",
                "radius": 0.3,
                "pos": None,
                "props": {"color": ORANGE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "circle3",
                "type": "Circle",
                "radius": 0.3,
                "pos": None,
                "props": {"color": ORANGE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "circle4",
                "type": "Circle",
                "radius": 0.3,
                "pos": None,
                "props": {"color": ORANGE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "circle5",
                "type": "Circle",
                "radius": 0.3,
                "pos": None,
                "props": {"color": ORANGE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "circle6",
                "type": "Circle",
                "radius": 0.3,
                "pos": None,
                "props": {"color": ORANGE, "fill_opacity": 0.8, "stroke_width": 2}
            },
            {
                "id": "step_explanation",
                "type": "Text",
                "content": "We start with the equation 2x = 6.",
                "pos": explanation_anchor,
                "props": {"color": GRAY_C, "font_size": 28}
            },
            {
                "id": "final_eq",
                "type": "MathTex",
                "content": "x = 3",
                "pos": scale_anchor + DOWN * 2.2,
                "props": {"color": GREEN, "font_size": 48}
            },
        ]

        for defn in obj_defs:
            obj_id = defn["id"]
            if defn["type"] == "Text":
                obj = Text(defn["content"], font_size=defn["props"]["font_size"])
                obj.set_color(defn["props"]["color"])
            elif defn["type"] == "MathTex":
                obj = MathTex(defn["content"], font_size=defn["props"]["font_size"])
                obj.set_color(defn["props"]["color"])
            elif defn["type"] == "Line":
                obj = Line(defn["start"], defn["end"], stroke_width=defn["props"]["stroke_width"])
                obj.set_color(defn["props"]["color"])
            elif defn["type"] == "Circle":
                obj = Circle(radius=defn["radius"], stroke_width=defn["props"]["stroke_width"])
                obj.set_color(defn["props"]["color"])
                if "fill_opacity" in defn["props"]:
                    obj.set_fill(color=defn["props"]["color"], opacity=defn["props"]["fill_opacity"])
            elif defn["type"] == "Square":
                obj = Square(side_length=defn["side_length"], stroke_width=defn["props"]["stroke_width"])
                obj.set_color(defn["props"]["color"])
                if "fill_opacity" in defn["props"]:
                    obj.set_fill(color=defn["props"]["color"], opacity=defn["props"]["fill_opacity"])
            else:
                continue

            if defn["pos"] is not None:
                obj.move_to(defn["pos"])
            self.objects[obj_id] = obj

        # Pass 2: Create dependent objects (need references)
        # Scale pivot (triangle)
        scale_pivot = Polygon(
            self.objects["scale_beam"].get_center(),
            self.objects["scale_beam"].get_center() + LEFT * 0.3 + DOWN * 0.5,
            self.objects["scale_beam"].get_center() + RIGHT * 0.3 + DOWN * 0.5,
            color=GRAY, fill_opacity=1.0
        )
        self.objects["scale_pivot"] = scale_pivot

        # Connectors
        left_connector = Line(
            self.objects["scale_beam"].get_start() + DOWN * 0.1,
            self.objects["left_pan"].get_top(),
            color=GRAY_C, stroke_width=4
        )
        self.objects["left_connector"] = left_connector

        right_connector = Line(
            self.objects["scale_beam"].get_end() + DOWN * 0.1,
            self.objects["right_pan"].get_top(),
            color=GRAY_C, stroke_width=4
        )
        self.objects["right_connector"] = right_connector

        # Position boxes relative to left pan
        self.objects["box1"].move_to(self.objects["left_pan"].get_center() + UP * 0.35)
        self.objects["box2"].move_to(self.objects["left_pan"].get_center() + DOWN * 0.35)

        # Position circles in a 2x3 grid in right pan
        pan_center = self.objects["right_pan"].get_center()
        offsets = [
            (LEFT * 0.4 + UP * 0.4),
            (RIGHT * 0.4 + UP * 0.4),
            (LEFT * 0.4),
            (RIGHT * 0.4),
            (LEFT * 0.4 + DOWN * 0.4),
            (RIGHT * 0.4 + DOWN * 0.4),
        ]
        circles = ["circle1", "circle2", "circle3", "circle4", "circle5", "circle6"]
        for i, circle_id in enumerate(circles):
            self.objects[circle_id].move_to(pan_center + offsets[i])

        # Labels
        label_2x = MathTex("2x", font_size=36, color=BLUE)
        label_2x.next_to(self.objects["left_pan"], LEFT, buff=0.5)
        self.objects["label_2x"] = label_2x

        label_6 = MathTex("6", font_size=36, color=ORANGE)
        label_6.next_to(self.objects["right_pan"], RIGHT, buff=0.5)
        self.objects["label_6"] = label_6

        # Group objects for easier animation
        self.objects["left_boxes"] = VGroup(self.objects["box1"], self.objects["box2"])
        self.objects["right_circles"] = VGroup(*[self.objects[c] for c in circles])
        self.objects["scale_structure"] = VGroup(
            self.objects["scale_beam"],
            self.objects["scale_pivot"],
            self.objects["left_connector"],
            self.objects["right_connector"],
            self.objects["left_pan"],
            self.objects["right_pan"]
        )

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/solving_2x_equals_6/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/solving_2x_equals_6/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        self.play(Create(self.objects["scale_structure"]), run_time=2.5)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/solving_2x_equals_6/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        # Signal action: Indicate label_2x
        self.play(Indicate(self.objects["label_2x"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["box1"]),
            Create(self.objects["box2"]),
            Write(self.objects["label_2x"]),
            run_time=2.0
        )
        remaining_3 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/solving_2x_equals_6/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        # Signal action: Indicate label_6
        self.play(Indicate(self.objects["label_6"], color=YELLOW, run_time=1))
        self.play(
            Create(self.objects["right_circles"]),
            Write(self.objects["label_6"]),
            run_time=2.0
        )
        remaining_4 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/solving_2x_equals_6/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        # Signal action: Circumscribe left boxes
        self.play(Circumscribe(self.objects["left_boxes"], color=YELLOW, run_time=1))
        # Update explanation text
        new_explanation = Text("Divide both sides by 2: Remove half from each side.", font_size=28, color=GRAY_C)
        new_explanation.move_to(self.objects["step_explanation"].get_center())
        self.play(Transform(self.objects["step_explanation"], new_explanation), run_time=1.5)
        remaining_5 = max(0.1, 4.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_05.mp3")  # [auto-injected]
        # Step 6
        audio_step6 = "media/audio/solving_2x_equals_6/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        # Signal action: Indicate objects to be removed
        to_remove = VGroup(
            self.objects["box2"],
            self.objects["circle4"],
            self.objects["circle5"],
            self.objects["circle6"]
        )
        self.play(Indicate(to_remove, color=RED, run_time=1))
        # Animate removal: move down and fade out
        self.play(
            self.objects["box2"].animate.shift(DOWN * 2),
            self.objects["circle4"].animate.shift(DOWN * 2),
            self.objects["circle5"].animate.shift(DOWN * 2),
            self.objects["circle6"].animate.shift(DOWN * 2),
            run_time=1.5
        )
        self.play(
            FadeOut(self.objects["box2"]),
            FadeOut(self.objects["circle4"]),
            FadeOut(self.objects["circle5"]),
            FadeOut(self.objects["circle6"]),
            run_time=1.0
        )
        remaining_6 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_06.mp3")  # [auto-injected]
        # Step 7
        audio_step7 = "media/audio/solving_2x_equals_6/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        # Create new labels
        label_x = MathTex("x", font_size=36, color=BLUE)
        label_x.next_to(self.objects["left_pan"], LEFT, buff=0.5)
        label_3 = MathTex("3", font_size=36, color=ORANGE)
        label_3.next_to(self.objects["right_pan"], RIGHT, buff=0.5)
        # Transform labels
        self.play(
            TransformMatchingTex(self.objects["label_2x"], label_x),
            TransformMatchingTex(self.objects["label_6"], label_3),
            run_time=2.0
        )
        # Update stored objects
        self.objects["label_2x"] = label_x
        self.objects["label_6"] = label_3
        remaining_7 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/To_visualize_the_equ_6368e57065/step_07.mp3")  # [auto-injected]
        # Step 8
        audio_step8 = "media/audio/solving_2x_equals_6/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        # Signal action: Circumscribe remaining objects
        remaining = VGroup(
            self.objects["box1"],
            self.objects["circle1"],
            self.objects["circle2"],
            self.objects["circle3"]
        )
        self.play(Circumscribe(remaining, color=GREEN, run_time=1))
        self.play(Write(self.objects["final_eq"]), run_time=1.5)
        remaining_8 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))