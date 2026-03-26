'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually distinguish area (interior covering) from perimeter (boundary length) of a rectangle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for rectangle, grid, and perimeter animation
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine to place Title (HEADER), Main Content (CONTENT), and Explanation (FOOTER) in separate zones.
#    - Area and Perimeter formulas will be placed to the right of the rectangle using `next_to` with buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step? Yes, using provided audio_path.
#    - [x] Files: "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw rectangle outline.
#    - Step 2: Indicate rectangle, then create grid of unit squares inside.
#    - Step 3: Write area formula.
#    - Step 4: Draw bold perimeter line.
#    - Step 5: Write perimeter formula.
#    - Step 6: Indicate tracer dot, then animate it moving along the perimeter.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Initialize Layout Engine
        layout = LayoutEngine()

        # Create objects from layout_plan.objects
        # Object: title
        title = Text("Area and Perimeter of a Rectangle", color=WHITE, font_size=36)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # Object: rect_outline
        rect_outline = Rectangle(width=4, height=3, color=BLUE, stroke_width=4, fill_opacity=0)
        self.objects["rect_outline"] = rect_outline
        obj_rect = LayoutObject(rect_outline, "rect_outline")
        layout.add(obj_rect)
        layout.add_to_zone(obj_rect, "CONTENT")
        layout.add_constraint(obj_rect.center_x == 0)
        layout.add_constraint(obj_rect.center_y == 0)

        # Object: grid_vgroup (initially empty VGroup)
        grid_vgroup = VGroup()
        self.objects["grid_vgroup"] = grid_vgroup
        # Position will be set to match rect_outline later

        # Object: perimeter_line
        perimeter_line = Rectangle(width=4, height=3, color=YELLOW, stroke_width=6, fill_opacity=0)
        self.objects["perimeter_line"] = perimeter_line
        # Position will be set to match rect_outline later

        # Object: tracer_dot
        tracer_dot = Circle(radius=0.08, color=RED, fill_opacity=1)
        self.objects["tracer_dot"] = tracer_dot
        # Initial position set later relative to rect_outline

        # Object: area_label
        area_label = MathTex(r"\text{Area} = 4 \times 3 = 12", color=GREEN)
        self.objects["area_label"] = area_label

        # Object: perimeter_label
        perimeter_label = MathTex(r"\text{Perimeter} = 2\times(4+3)=14", color=YELLOW)
        self.objects["perimeter_label"] = perimeter_label

        # Object: explanation_text
        explanation_text = Text("Area: covered by squares. Perimeter: length of the boundary.", color=LIGHT_GRAY, font_size=24)
        self.objects["explanation_text"] = explanation_text
        obj_expl = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_expl)
        layout.add_to_zone(obj_expl, "FOOTER")
        layout.add_constraint(obj_expl.center_x == 0)

        # Solve layout for title, rect_outline, and explanation_text
        layout.solve()

        # Position objects not managed by LayoutEngine (relative to rect_outline)
        area_label.next_to(rect_outline, RIGHT, buff=1.5)
        perimeter_label.next_to(area_label, DOWN, buff=0.5)
        perimeter_line.move_to(rect_outline.get_center())
        grid_vgroup.move_to(rect_outline.get_center())
        tracer_dot.move_to(rect_outline.get_corner(DL))

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's start with a rectangle that is 4 units wide and 3 units tall.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "rect_outline",
                    "details": "Draw the blue rectangle outline"
                },
                "duration": 4.848,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "To find its area, we fill it with unit squares. Each square represents one square unit.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "rect_outline",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "CreateGrid",
                    "target_id": "grid_vgroup",
                    "details": "Create 12 unit squares (0.9x0.9 with 0.1 gap) in a 4x3 grid, filling the rectangle. Animate row by row from bottom left."
                },
                "duration": 6.744,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "There are 12 squares, so the area is 12 square units.",
                "signal_action": {
                    "type": "Write",
                    "target": "area_label"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "area_label",
                    "details": "Display the area formula and result"
                },
                "duration": 4.632,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now, let's look at the perimeter: the total distance around the rectangle.",
                "signal_action": {
                    "type": "Create",
                    "target": "perimeter_line"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "perimeter_line",
                    "details": "Draw the bold yellow perimeter line over the rectangle"
                },
                "duration": 4.992,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "The perimeter is the sum of all sides: 4 + 3 + 4 + 3, or 2 times (4 plus 3), which equals 14 units.",
                "signal_action": {
                    "type": "Write",
                    "target": "perimeter_label"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "perimeter_label",
                    "details": "Display the perimeter formula and result"
                },
                "duration": 8.928,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Watch as a dot traces the entire boundary, emphasizing the path of the perimeter.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "tracer_dot",
                    "color": "RED"
                },
                "visual_action": {
                    "type": "MoveAlongPath",
                    "target_id": "tracer_dot",
                    "details": "Animate the red dot moving along the perimeter_line path over 4 seconds"
                },
                "duration": 5.4,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_05.mp3"
            }
        ]

        # Step 0: Show title and explanation (not in sequence but part of setup)
        self.play(Write(title))
        self.play(Write(explanation_text))
        self.wait(0.5)

        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_path = step.get("audio_path")

            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)
            # Note: We'll calculate remaining wait time after animations

            # === SIGNAL ACTION ===
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects.get(target_id)
                if target_obj is not None:
                    if signal["type"] == "Indicate":
                        color = signal.get("color", "YELLOW")
                        color_map = {"YELLOW": YELLOW, "GREEN": GREEN, "RED": RED, "BLUE": BLUE}
                        self.play(Indicate(target_obj, color=color_map.get(color, YELLOW)), run_time=1)
                    elif signal["type"] == "Write":
                        # For signal action "Write", we just write the object (it will be created in visual_action)
                        pass
                    elif signal["type"] == "Create":
                        # For signal action "Create", we create the object (it will be created in visual_action)
                        pass

            # === VISUAL ACTION ===
            visual = step["visual_action"]
            target_id = visual["target_id"]
            details = visual.get("details", "")

            if visual["type"] == "Create":
                obj = self.objects[target_id]
                self.play(Create(obj))
                anim_time = 1.0  # estimated run_time for Create
            elif visual["type"] == "CreateGrid":
                # Create 4x3 grid of unit squares
                width = 4
                height = 3
                square_size = 0.9
                gap = 0.1
                total_size = square_size + gap
                start_x = - (width - 1) * total_size / 2
                start_y = - (height - 1) * total_size / 2

                squares = VGroup()
                for row in range(height):
                    for col in range(width):
                        sq = Square(side_length=square_size, color=BLUE, fill_opacity=0.3, stroke_width=2)
                        sq.move_to([start_x + col * total_size, start_y + row * total_size, 0])
                        squares.add(sq)
                squares.move_to(rect_outline.get_center())
                self.objects["grid_vgroup"] = squares
                # Animate row by row from bottom left
                anim_time = 0.0
                for sq in squares:
                    self.play(Create(sq), run_time=0.15)
                    anim_time += 0.15
            elif visual["type"] == "Write":
                obj = self.objects[target_id]
                self.play(Write(obj))
                anim_time = 1.0  # estimated run_time for Write
            elif visual["type"] == "MoveAlongPath":
                obj = self.objects[target_id]
                path = self.objects["perimeter_line"]
                self.play(MoveAlongPath(obj, path), run_time=4.0)
                anim_time = 4.0
            else:
                anim_time = 0.0

            # === WAIT FOR REMAINING AUDIO DURATION ===
            remaining = duration - anim_time + 0.5  # 0.5s safety buffer
            if remaining > 0:
                self.wait(remaining)
            else:
                self.wait(0.1)  # minimal wait

        # Final wait
        self.wait(2)