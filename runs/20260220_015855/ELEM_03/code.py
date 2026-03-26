'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually distinguish area (space inside) from perimeter (distance around) for a rectangle.
# 2. Layout Strategy: Use LayoutEngine to manage zones.
#    - Header Region: [y=3.5] for Title "Area and Perimeter of a Rectangle"
#    - Main Content: [Center y=0] for the 4x3 rectangle, grid, and perimeter tracing.
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanations.
# 3. Anti-Overlap Check: LayoutEngine zones prevent header, content, and footer from overlapping. The grid squares are contained within the rectangle VGroup.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using the provided audio_path.
#    - [x] Files: "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_XX.mp3"
# 5. Animation Flow:
#    Step 1: Create rectangle outline.
#    Step 2: Write dimension label (4x3).
#    Step 3: Indicate rectangle, then fill with unit squares (area visualization).
#    Step 4: Circumscribe rectangle, fade in tracing dot.
#    Step 5: Animate dot moving along perimeter, leaving a traced path.
#    Step 6: Indicate grid (area), fade out dot, final scene shows area and perimeter.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Initialize Layout Engine
        layout = LayoutEngine()

        # Create objects as defined in layout_plan.objects
        # Object registry
        self.objects = {}

        # 1. Title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=40)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # 2. Rectangle Outline
        rect_outline = Rectangle(width=4.0, height=3.0, color=BLUE, stroke_width=4, fill_opacity=0.0)
        obj_rect = LayoutObject(rect_outline, "rect_outline")
        layout.add(obj_rect)
        layout.add_to_zone(obj_rect, "CONTENT")
        layout.add_constraint(obj_rect.center_x == 0)
        layout.add_constraint(obj_rect.center_y == 0)
        self.objects["rect_outline"] = rect_outline

        # 3. Dimension Label
        dim_label = MathTex("4 \\times 3", color=YELLOW, font_size=30)
        obj_dim = LayoutObject(dim_label, "dim_label")
        layout.add(obj_dim)
        # Position will be set relative to rectangle after solve, but we need a constraint.
        # We'll position it manually after solve using next_to for precise placement.
        self.objects["dim_label"] = dim_label

        # 4. Grid Squares VGroup (initially empty)
        grid_squares_vgroup = VGroup()
        obj_grid = LayoutObject(grid_squares_vgroup, "grid_squares_vgroup")
        layout.add(obj_grid)
        # Position it at the same center as the rectangle
        layout.align_to(obj_grid, obj_rect, 'CENTER')
        self.objects["grid_squares_vgroup"] = grid_squares_vgroup

        # 5. Tracing Dot (initially at bottom-left corner of rectangle)
        # We need the rectangle's position to place the dot. We'll create it after solve.
        tracing_dot = Dot(radius=0.08, color=YELLOW, z_index=5)
        # Position will be set manually after solve.
        self.objects["tracing_dot"] = tracing_dot
        # Note: We don't add to layout yet because its position depends on rect_outline's solved position.

        # 6. Perimeter Path (TracedPath) - Will be created when dot is added to scene.
        # We'll create it in step 5.
        self.objects["perimeter_path"] = None  # Placeholder

        # 7. Step Explanation
        step_explanation = Text("Step 1: The rectangle.", color=LIGHT_GRAY, font_size=24)
        obj_step = LayoutObject(step_explanation, "step_explanation")
        layout.add(obj_step)
        layout.add_to_zone(obj_step, "FOOTER")
        layout.add_constraint(obj_step.center_x == 0)
        self.objects["step_explanation"] = step_explanation

        # Solve the layout
        layout.solve()

        # Apply manual positions that depend on solved positions
        # Dim label next to rectangle (UP, buff=0.3)
        dim_label.next_to(rect_outline, UP, buff=0.3)
        # Tracing dot at bottom-left corner of rectangle
        tracing_dot.move_to(rect_outline.get_corner(DL))

        # ========== PHASE 2: Animation Sequence ==========
        sequence = self.get_sequence_data()  # Defined as a method for clarity

        for step in sequence:
            step_num = step["step"]
            narrative = step["narrative"]
            signal_action = step.get("signal_action")
            visual_action = step["visual_action"]
            duration = step["duration"]
            audio_path = step["audio_path"]

            # Update step explanation text if narrative is suitable (simplified)
            # We'll update it at the start of each step for clarity.
            new_explanation = f"Step {step_num}: {narrative[:40]}..." if len(narrative) > 40 else f"Step {step_num}: {narrative}"
            step_explanation_new = Text(new_explanation, color=LIGHT_GRAY, font_size=24)
            step_explanation_new.move_to(self.objects["step_explanation"].get_center())
            self.play(ReplacementTransform(self.objects["step_explanation"], step_explanation_new))
            self.objects["step_explanation"] = step_explanation_new

            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)

            # Signal Action
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_id = signal_action["target"]
                color_name = signal_action.get("color", "YELLOW")
                color = eval(color_name)  # Convert string to Manim color constant

                target_obj = self.objects[target_id]

                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal_type == "Write":
                    # This is unusual for signal_action, but we'll implement as Write
                    self.play(Write(target_obj))
                # Note: "FocusOn" not used in this sequence

            # Visual Action
            visual_type = visual_action["type"]
            target_id = visual_action["target_id"]
            details = visual_action.get("details", "")

            if visual_type == "Create":
                target_obj = self.objects[target_id]
                self.play(Create(target_obj))
            elif visual_type == "Write":
                target_obj = self.objects[target_id]
                self.play(Write(target_obj))
            elif visual_type == "LaggedStartMap":
                # Create the grid of unit squares inside the rectangle
                rect = self.objects["rect_outline"]
                width = 4
                height = 3
                unit = 1.0  # side length of unit square
                # Calculate bottom-left corner of grid to align with rectangle
                # Rectangle center is at origin, width=4, height=3
                # So bottom-left corner is at (-2, -1.5, 0)
                start_x = -width/2 + unit/2
                start_y = -height/2 + unit/2
                squares = []
                for i in range(width):      # columns
                    for j in range(height): # rows
                        sq = Square(side_length=unit, color=GREEN, fill_opacity=0.3, stroke_width=1)
                        sq.move_to([start_x + i*unit, start_y + j*unit, 0])
                        squares.append(sq)
                grid_group = VGroup(*squares)
                # Replace the empty vgroup
                old_grid = self.objects["grid_squares_vgroup"]
                grid_group.move_to(old_grid.get_center())
                self.objects["grid_squares_vgroup"] = grid_group
                self.play(LaggedStartMap(Create, grid_group, lag_ratio=0.05, run_time=3))
            elif visual_type == "FadeIn":
                target_obj = self.objects[target_id]
                self.play(FadeIn(target_obj))
            elif visual_type == "AnimationGroup":
                # Step 5: Animate dot along perimeter and show traced path
                tracing_dot = self.objects["tracing_dot"]
                rect = self.objects["rect_outline"]

                # Create the perimeter path (TracedPath)
                perimeter_path = TracedPath(tracing_dot.get_center, stroke_color=TEAL, stroke_width=6, z_index=4)
                self.objects["perimeter_path"] = perimeter_path
                self.add(perimeter_path)

                # Create the path for the dot to follow (rectangle perimeter)
                # Use the rectangle's vertices
                perimeter_mob = rect.copy().set_fill(opacity=0).set_stroke(opacity=0)  # Invisible, just for path
                # Animate the dot
                move_anim = MoveAlongPath(tracing_dot, perimeter_mob, run_time=4)
                self.play(move_anim)
            elif visual_type == "FadeOut":
                target_obj = self.objects[target_id]
                self.play(FadeOut(target_obj))

            # Wait for remaining audio duration
            # Since animation times are approximate, we'll use a fixed wait based on step duration minus estimated animation time.
            # We'll estimate animation time based on visual_type.
            est_animation_time = 0
            if visual_type in ["Create", "Write", "FadeIn", "FadeOut"]:
                est_animation_time = 1.0
            elif visual_type == "LaggedStartMap":
                est_animation_time = 3.0  # As set in run_time
            elif visual_type == "AnimationGroup":
                est_animation_time = 4.0  # As set in run_time for MoveAlongPath

            if signal_action is not None:
                est_animation_time += 1.0  # Signal action run_time

            remaining = duration - est_animation_time
            if remaining > 0:
                self.wait(remaining)
            else:
                self.wait(0.5)  # Minimum buffer

        # Final wait
        self.wait(2)

    def get_sequence_data(self):
        """Returns the sequence data from the Director's JSON."""
        return [
            {
                "step": 1,
                "narrative": "Let's start with a rectangle that is 4 units wide and 3 units tall.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "rect_outline",
                    "details": "Draw the blue rectangle outline."
                },
                "duration": 4.848,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "We write its dimensions: 4 by 3.",
                "signal_action": {
                    "type": "Write",
                    "target": "dim_label",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "dim_label",
                    "details": "Write the dimension label above the rectangle."
                },
                "duration": 3.192,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Its area is the space inside. We can visualize it by filling the rectangle with unit squares.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "rect_outline",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "LaggedStartMap",
                    "target_id": "grid_squares_vgroup",
                    "details": "Create 12 unit squares (side=1) in a 4x3 grid inside the rectangle, with a slight lag between each for a filling effect. Set fill_opacity=0.3, stroke_width=1, color=GREEN."
                },
                "duration": 6.984,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The perimeter is the distance around the boundary. Let's trace it.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "rect_outline",
                    "color": "TEAL"
                },
                "visual_action": {
                    "type": "FadeIn",
                    "target_id": "tracing_dot",
                    "details": "Introduce the yellow dot at the bottom-left corner."
                },
                "duration": 4.968,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "As the dot moves along the edges, it leaves a path showing the complete perimeter.",
                "signal_action": None,
                "visual_action": {
                    "type": "AnimationGroup",
                    "target_id": "perimeter_path",
                    "details": "Simultaneously: 1) Add the TracedPath object to the scene (it will generate the line as the dot moves). 2) Animate the dot moving along the rectangle's perimeter (MoveAlongPath) over 4 seconds."
                },
                "duration": 5.28,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "So, the area is 12 square units, and the perimeter is the length of this path, which is 4 + 3 + 4 + 3 = 14 units.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "grid_squares_vgroup",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "FadeOut",
                    "target_id": "tracing_dot",
                    "details": "Remove the dot, leaving the traced perimeter line and the filled rectangle."
                },
                "duration": 9.144,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_05.mp3"
            }
        ]