'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as combining equal groups (3 groups of 4).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for star grid and final cluster
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep Title, Content, and Footer separated.
#    - The star grid (3 rows) will be positioned in CONTENT zone.
#    - The final cluster will replace the grid at the same anchor.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create first row (red stars).
#    - Step 2: Indicate and create second row (teal stars).
#    - Step 3: Indicate and create third row (yellow stars).
#    - Step 4: Circumscribe title, then transform three rows into a circular cluster.
#    - Step 5: Indicate and write the final count "12".
'''

from manim import *
import os
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Initialize Layout Engine
        layout = LayoutEngine()

        # Create objects from layout_plan.objects
        # title
        title = MathTex(r"3 \times 4 = 12", color=WHITE)
        title.scale(1.2)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title

        # step_label
        step_label = Text("Step 1: Three groups of four stars", color=YELLOW)
        step_label.scale(0.7)
        obj_step_label = LayoutObject(step_label, "step_label")
        layout.add(obj_step_label)
        layout.align_to(obj_step_label, obj_title, "BOTTOM", buff=0.3)
        layout.add_constraint(obj_step_label.center_x == 0)
        self.objects["step_label"] = step_label

        # Create stars for rows
        # row1: red stars at positions relative to grid_anchor
        row1_stars = VGroup()
        row1_positions = [(-1.5, 1.2, 0), (-0.5, 1.2, 0), (0.5, 1.2, 0), (1.5, 1.2, 0)]
        for pos in row1_positions:
            star = Star(color="#FF6B6B", outer_radius=0.2)
            star.move_to(pos)
            row1_stars.add(star)
        obj_row1 = LayoutObject(row1_stars, "row1")
        layout.add(obj_row1)
        layout.add_to_zone(obj_row1, "CONTENT")
        layout.add_constraint(obj_row1.center_y == 1.2)  # UP*1.2 from grid_anchor (which is y=0)
        layout.add_constraint(obj_row1.center_x == 0)
        self.objects["row1"] = row1_stars

        # row2: teal stars
        row2_stars = VGroup()
        row2_positions = [(-1.5, 0.0, 0), (-0.5, 0.0, 0), (0.5, 0.0, 0), (1.5, 0.0, 0)]
        for pos in row2_positions:
            star = Star(color="#4ECDC4", outer_radius=0.2)
            star.move_to(pos)
            row2_stars.add(star)
        obj_row2 = LayoutObject(row2_stars, "row2")
        layout.add(obj_row2)
        layout.add_to_zone(obj_row2, "CONTENT")
        layout.add_constraint(obj_row2.center_y == 0)
        layout.add_constraint(obj_row2.center_x == 0)
        self.objects["row2"] = row2_stars

        # row3: yellow stars
        row3_stars = VGroup()
        row3_positions = [(-1.5, -1.2, 0), (-0.5, -1.2, 0), (0.5, -1.2, 0), (1.5, -1.2, 0)]
        for pos in row3_positions:
            star = Star(color="#FFD166", outer_radius=0.2)
            star.move_to(pos)
            row3_stars.add(star)
        obj_row3 = LayoutObject(row3_stars, "row3")
        layout.add(obj_row3)
        layout.add_to_zone(obj_row3, "CONTENT")
        layout.add_constraint(obj_row3.center_y == -1.2)
        layout.add_constraint(obj_row3.center_x == 0)
        self.objects["row3"] = row3_stars

        # combined_stars: 12 stars arranged in a circle
        combined_stars = VGroup()
        radius = 1.5
        for i in range(12):
            angle = i * 2 * PI / 12
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            star = Star(color=WHITE, outer_radius=0.2)
            star.move_to([x, y, 0])
            combined_stars.add(star)
        obj_combined = LayoutObject(combined_stars, "combined_stars")
        layout.add(obj_combined)
        layout.add_to_zone(obj_combined, "CONTENT")
        layout.add_constraint(obj_combined.center_x == 0)
        layout.add_constraint(obj_combined.center_y == 0)
        self.objects["combined_stars"] = combined_stars
        # Initially hide combined_stars (it will be transformed into)
        combined_stars.set_opacity(0)

        # count_label
        count_label = MathTex("12", color=GREEN)
        count_label.scale(1.5)
        obj_count = LayoutObject(count_label, "count_label")
        layout.add(obj_count)
        layout.align_to(obj_count, obj_combined, "BOTTOM", buff=0.5)
        layout.add_constraint(obj_count.center_x == 0)
        self.objects["count_label"] = count_label
        count_label.set_opacity(0)

        # explanation
        explanation = Text("3 groups of 4 combine to make 12 total", color=LIGHT_GRAY)
        explanation.scale(0.8)
        obj_explanation = LayoutObject(explanation, "explanation")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == 0)
        self.objects["explanation"] = explanation
        explanation.set_opacity(0)

        # Solve layout constraints
        layout.solve()

        # Apply positions to mobjects
        title.move_to(obj_title.get_center())
        step_label.move_to(obj_step_label.get_center())
        row1_stars.move_to(obj_row1.get_center())
        row2_stars.move_to(obj_row2.get_center())
        row3_stars.move_to(obj_row3.get_center())
        combined_stars.move_to(obj_combined.get_center())
        count_label.move_to(obj_count.get_center())
        explanation.move_to(obj_explanation.get_center())

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's visualize 3 times 4. We start with three separate groups, each containing four stars.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "row1",
                    "details": "Draw first row of 4 red stars"
                },
                "duration": 7.104,
                "audio_path": "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Here is our second group of four stars.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "row2",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "row2",
                    "details": "Draw second row of 4 teal stars"
                },
                "duration": 2.976,
                "audio_path": "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "And our third group of four stars. Together, we have three groups of four.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "row3",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "row3",
                    "details": "Draw third row of 4 yellow stars"
                },
                "duration": 5.568,
                "audio_path": "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now let's combine all the groups. This is what multiplication does: it combines equal groups.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "title",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "ReplacementTransform",
                    "target_id": ["row1", "row2", "row3"],
                    "details": "Transform the three separate VGroups into the single combined_stars VGroup",
                    "new_target": "combined_stars"
                },
                "duration": 7.08,
                "audio_path": "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "When we combine three groups of four, we get twelve stars total. So 3 times 4 equals 12.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "count_label",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "count_label",
                    "details": "Write the number 12 below the combined cluster"
                },
                "duration": 7.248,
                "audio_path": "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
            }
        ]

        for step in sequence:
            step_num = step["step"]
            duration = step["duration"]
            audio_file = step.get("audio_path")

            # === AUDIO (MANDATORY) ===
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)

            # Signal Action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects[target_id]
                color_str = signal.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "RED": RED, "GREEN": GREEN, "BLUE": BLUE}
                color = color_map.get(color_str, YELLOW)

                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                elif signal["type"] == "FocusOn":
                    self.play(FocusOn(target_obj))

            # Visual Action
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual.get("target_id")

            if action_type == "Create":
                obj = self.objects[target_id]
                self.play(Create(obj))
                animation_time = 1.0  # approximate run_time for Create
            elif action_type == "Write":
                obj = self.objects[target_id]
                obj.set_opacity(1)
                self.play(Write(obj))
                animation_time = 1.0
            elif action_type == "ReplacementTransform":
                # Transform multiple source groups into one target group
                source_ids = target_id  # this is a list
                new_target_id = visual.get("new_target")
                source_objs = [self.objects[sid] for sid in source_ids]
                target_obj = self.objects[new_target_id]
                target_obj.set_opacity(1)
                # We'll transform each source group into the target group.
                # Since target is a single VGroup, we need to create a transformation.
                # We'll use ReplacementTransform from the first source, and transform others into it.
                self.play(ReplacementTransform(source_objs[0], target_obj))
                for src in source_objs[1:]:
                    self.play(ReplacementTransform(src, target_obj))
                animation_time = 2.0  # approximate total run_time
            else:
                animation_time = 0

            # Wait for remaining audio duration
            remaining = duration - animation_time + 0.5
            if remaining > 0:
                self.wait(remaining)

        # Final wait
        self.wait(2)