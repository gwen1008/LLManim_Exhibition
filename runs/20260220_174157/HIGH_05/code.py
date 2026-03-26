'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the triangle method, showing geometric and component-wise equivalence.
# 2. Layout Strategy: Use high-low split.
#    - Header Region: [y=3.5] for Title "Vector Addition: The Triangle Method"
#    - Main Content: [Center y=0] for coordinate axes, vectors, and main equation.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text.
# 3. Anti-Overlap Check:
#    - Use VGroups for vector+label pairs to keep them together.
#    - Position main equation above axes (y=2.0) and explanation at bottom (y=-3.0).
#    - Ensure z_index: vectors/labels=1, explanation=0 to prevent overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Create axes.
#    Step 2: Create vector A and label.
#    Step 3: Create vector B attached to A's tip and label.
#    Step 4: Draw dashed triangle closing side, update explanation.
#    Step 5: Transform dashed line into solid vector C, show label, update equation.
#    Step 6: Fade in translated vector B, update equation to component addition, update explanation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors based on layout_plan zones
        title_anchor = 3.5 * UP
        grid_center = ORIGIN
        explanation_anchor = 3.0 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Vector Addition: The Triangle Method", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Axes (NumberPlane + Axes as per hint)
        # First create NumberPlane for grid
        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            background_line_style={
                "stroke_color": GRAY_C,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        # Then create Axes for coordinate lines
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 2,
                "include_numbers": True,
                "font_size": 24
            }
        )
        axes_group = VGroup(plane, axes)
        axes_group.move_to(grid_center)
        self.objects["axes"] = axes_group

        # Vector A Arrow
        vec_A_arrow = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color=BLUE,
            stroke_width=6,
            buff=0
        )
        vec_A_arrow.move_to(grid_center)
        self.objects["vec_A_arrow"] = vec_A_arrow

        # Vector A Label
        vec_A_label = MathTex(r"\vec{A} = (3, 1)", color=BLUE, font_size=30)
        # Position will be set relative to arrow after creation (in step 2)
        self.objects["vec_A_label"] = vec_A_label

        # Vector B Attached Arrow
        vec_B_attached_arrow = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color=GREEN,
            stroke_width=6,
            buff=0
        )
        vec_B_attached_arrow.move_to(grid_center)
        self.objects["vec_B_attached_arrow"] = vec_B_attached_arrow

        # Vector B Attached Label
        vec_B_attached_label = MathTex(r"\vec{B} = (1, 2)", color=GREEN, font_size=30)
        # Position will be set relative to arrow after creation
        self.objects["vec_B_attached_label"] = vec_B_attached_label

        # Vector B Translated Arrow (initially invisible)
        vec_B_translated_arrow = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            color=GREEN,
            stroke_width=6,
            buff=0
        )
        vec_B_translated_arrow.move_to(grid_center)
        vec_B_translated_arrow.set_opacity(0.0)
        self.objects["vec_B_translated_arrow"] = vec_B_translated_arrow

        # Vector C Arrow (initially invisible)
        vec_C_arrow = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=YELLOW,
            stroke_width=8,
            buff=0
        )
        vec_C_arrow.move_to(grid_center)
        vec_C_arrow.set_opacity(0.0)
        self.objects["vec_C_arrow"] = vec_C_arrow

        # Vector C Label
        vec_C_label = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color=YELLOW, font_size=32)
        # Position will be set relative to arrow later
        self.objects["vec_C_label"] = vec_C_label

        # Triangle Dashed Line (initially invisible)
        triangle_dashed_line = DashedLine(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=WHITE,
            stroke_width=3,
            dash_length=0.1
        )
        triangle_dashed_line.move_to(grid_center)
        triangle_dashed_line.set_opacity(0.0)
        self.objects["triangle_dashed_line"] = triangle_dashed_line

        # Main Equation
        main_equation = MathTex(r"\vec{C} = \vec{A} + \vec{B}", color=WHITE, font_size=36)
        main_equation.move_to(grid_center + 2.0 * UP)
        self.objects["main_equation"] = main_equation

        # Step Explanation
        step_explanation = Text("Let's set up our coordinate system.", color=GRAY_C, font_size=28)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation

        # Set z_index as per hint
        for key in ["vec_A_arrow", "vec_A_label", "vec_B_attached_arrow", "vec_B_attached_label",
                    "vec_B_translated_arrow", "vec_C_arrow", "vec_C_label", "triangle_dashed_line",
                    "main_equation"]:
            if key in self.objects:
                self.objects[key].set_z_index(1)
        self.objects["step_explanation"].set_z_index(0)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3",
            "duration": 3.48,
            "signal_action": {"type": "Indicate", "target": "axes", "color": "WHITE"},
            "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw the coordinate axes and grid."}
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["axes"]))
        # Wait for remaining audio
        animation_time = 1.0  # Approximate for Indicate + Create
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3",
            "duration": 4.8,
            "signal_action": {"type": "Circumscribe", "target": "vec_A_label", "color": "YELLOW"},
            "visual_action": {"type": "Create", "target_id": "vec_A_arrow", "details": "Animate the drawing of vector A."}
        }
        # Position label relative to arrow (now that arrow exists)
        self.objects["vec_A_label"].next_to(self.objects["vec_A_arrow"].get_center(), UP + LEFT, buff=0.2)
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Visual Action
        self.play(Create(self.objects["vec_A_arrow"]))
        self.play(Write(self.objects["vec_A_label"]))
        # Wait
        animation_time = 1.0 + 1.0 + 0.5  # Circumscribe + Create + Write
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3",
            "duration": 10.44,
            "signal_action": {"type": "Indicate", "target": "vec_B_attached_arrow", "color": "GREEN"},
            "visual_action": {"type": "Create", "target_id": "vec_B_attached_arrow", "details": "Animate the drawing of vector B attached to A's tip."}
        }
        # Position label
        self.objects["vec_B_attached_label"].next_to(self.objects["vec_B_attached_arrow"].get_center(), RIGHT, buff=0.2)
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Action
        self.play(Create(self.objects["vec_B_attached_arrow"]))
        self.play(Write(self.objects["vec_B_attached_label"]))
        # Wait
        animation_time = 1.0 + 1.0 + 0.5  # Indicate + Create + Write
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3",
            "duration": 7.704,
            "signal_action": {"type": "Indicate", "target": "triangle_dashed_line", "color": "WHITE"},
            "visual_action": [
                {"type": "Create", "target_id": "triangle_dashed_line", "details": "Draw the dashed closing side of the triangle."},
                {"type": "ReplacementTransform", "target_id": "step_explanation", "details": "Change explanation text to 'The closing side is the resultant vector C.'"}
            ]
        }
        # Create new explanation text
        new_explanation = Text("The closing side is the resultant vector C.", color=GRAY_C, font_size=28)
        new_explanation.move_to(explanation_anchor)
        new_explanation.set_z_index(0)
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Actions
        self.objects["triangle_dashed_line"].set_opacity(1.0)
        self.play(Create(self.objects["triangle_dashed_line"]))
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Wait
        animation_time = 1.0 + 1.0 + 0.5  # Indicate + Create + ReplacementTransform
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3",
            "duration": 6.384,
            "signal_action": {"type": "Indicate", "target": "vec_C_arrow", "color": "YELLOW"},
            "visual_action": [
                {"type": "ReplacementTransform", "target_id": "triangle_dashed_line", "details": "Morph the dashed line into the solid yellow vector C at the origin."},
                {"type": "Write", "target_id": "vec_C_label", "details": "Write the label for vector C."},
                {"type": "ReplacementTransform", "target_id": "main_equation", "details": "Update the main equation to '\\vec{C} = (4, 3)'."}
            ]
        }
        # Position vec_C_label
        self.objects["vec_C_label"].next_to(self.objects["vec_C_arrow"].get_center(), UP + RIGHT, buff=0.3)
        # Create new equation
        new_equation = MathTex(r"\vec{C} = (4, 3)", color=WHITE, font_size=36)
        new_equation.move_to(self.objects["main_equation"].get_center())
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Actions
        self.objects["vec_C_arrow"].set_opacity(1.0)
        self.play(ReplacementTransform(self.objects["triangle_dashed_line"], self.objects["vec_C_arrow"]))
        self.play(Write(self.objects["vec_C_label"]))
        self.play(ReplacementTransform(self.objects["main_equation"], new_equation))
        self.objects["main_equation"] = new_equation
        # Wait
        animation_time = 1.0 + 1.0 + 0.5 + 0.5  # Indicate + ReplacementTransform + Write + ReplacementTransform
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3",
            "duration": 10.296,
            "signal_action": {"type": "Indicate", "target": "vec_B_translated_arrow", "color": "GREEN"},
            "visual_action": [
                {"type": "FadeIn", "target_id": "vec_B_translated_arrow", "details": "Fade in the translated copy of vector B at the origin."},
                {"type": "ReplacementTransform", "target_id": "main_equation", "details": "Transform the equation to show component addition."},
                {"type": "ReplacementTransform", "target_id": "step_explanation", "details": "Change explanation text."}
            ]
        }
        # Create new equation for component addition
        new_equation2 = MathTex(r"\vec{C} = (3,1) + (1,2) = (4,3)", color=WHITE, font_size=36)
        new_equation2.move_to(self.objects["main_equation"].get_center())
        # Create new explanation text
        new_explanation2 = Text("Vector addition is component-wise: (3+1, 1+2) = (4,3).", color=GRAY_C, font_size=28)
        new_explanation2.move_to(explanation_anchor)
        new_explanation2.set_z_index(0)
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = eval(signal.get("color", "YELLOW"))
            self.play(Indicate(target_obj, color=color))
        # Visual Actions
        self.play(FadeIn(self.objects["vec_B_translated_arrow"]))
        self.play(TransformMatchingTex(self.objects["main_equation"], new_equation2))
        self.objects["main_equation"] = new_equation2
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation2))
        self.objects["step_explanation"] = new_explanation2
        # Wait
        animation_time = 1.0 + 1.0 + 1.0 + 0.5  # Indicate + FadeIn + TransformMatchingTex + ReplacementTransform
        remaining = step["duration"] - animation_time
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final pause
        self.wait(max(0.1, 2))