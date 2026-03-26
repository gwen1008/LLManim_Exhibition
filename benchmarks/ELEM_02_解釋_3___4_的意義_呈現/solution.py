from manim import *
import numpy as np
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Create title
        title = Text("Multiplication: 3 × 4", color=WHITE, font_size=48)
        self.objects["title"] = title

        # Create dot template (not added to scene yet, used for cloning)
        dot_template = Dot(radius=0.1, color=YELLOW, fill_opacity=1.0)
        self.objects["dot_template"] = dot_template

        # Create empty VGroups for grid and cluster
        grid_vgroup = VGroup()
        self.objects["grid_vgroup"] = grid_vgroup

        cluster_vgroup = VGroup()
        self.objects["cluster_vgroup"] = cluster_vgroup

        # Create labels
        label_groups = Text("3 groups", color=BLUE, font_size=32)
        self.objects["label_groups"] = label_groups

        label_items = Text("4 in each", color=GREEN, font_size=32)
        self.objects["label_items"] = label_items

        # Create equation
        equation = MathTex("3 \\times 4 = 12", color=ORANGE, font_size=48)
        self.objects["equation"] = equation

        # Position objects manually (simplified layout)
        title.to_edge(UP, buff=0.5)
        equation.to_edge(DOWN, buff=0.5)
        
        # Initially hide labels and equation
        label_groups.set_opacity(0)
        label_items.set_opacity(0)
        equation.set_opacity(0)

        # Add title to scene
        self.add(title)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "Let's visualize multiplication. We want to understand what three times four means.",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "title",
                    "details": "Fade in the title at the top of the screen."
                },
                "duration": 6.312,
                "audio_path": "media/audio/解釋_3_x_4_的意義：呈現_3_組各有_4_顆星星，並將它們聚集起來總計為_12_顆。/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "One way to think of it is as three groups, with four stars in each group.",
                "signal_action": None,
                "visual_action": {
                    "type": "CreateGrid",
                    "target_id": "grid_vgroup",
                    "details": "Create a 3 by 4 grid of yellow dots (stars) at the center, using the dot_template. Animate them appearing row by row to emphasize the 'groups of four' structure."
                },
                "duration": 4.92,
                "audio_path": "media/audio/解釋_3_x_4_的意義：呈現_3_組各有_4_顆星星，並將它們聚集起來總計為_12_顆。/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Here we have our three rows, or groups. And each row contains four stars.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "label_groups",
                    "color": "BLUE"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "label_groups",
                    "details": "Write the '3 groups' label to the left of the grid."
                },
                "duration": 5.928,
                "audio_path": "media/audio/解釋_3_x_4_的意義：呈現_3_組各有_4_顆星星，並將它們聚集起來總計為_12_顆。/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "And here, above, we see there are four stars in each group.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "label_items",
                    "color": "GREEN"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "label_items",
                    "details": "Write the '4 in each' label above the grid."
                },
                "duration": 4.272,
                "audio_path": "media/audio/解釋_3_x_4_的意義：呈現_3_組各有_4_顆星星，並將它們聚集起來總計為_12_顆。/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Now, let's combine all the stars from every group into one big collection.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "grid_vgroup",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "ReplacementTransform",
                    "target_id": "grid_vgroup",
                    "details": "Animate the transformation of the structured grid into a single, clustered group of 12 dots at the center. Fade out the group labels during this transformation."
                },
                "duration": 5.016,
                "audio_path": "media/audio/解釋_3_x_4_的意義：呈現_3_組各有_4_顆星星，並將它們聚集起來總計為_12_顆。/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "When we combine three groups of four, we get a total of twelve stars. This is what we mean by three times four equals twelve.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "cluster_vgroup",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "equation",
                    "details": "Write the equation '3 × 4 = 12' at the bottom of the screen, emphasizing the result."
                },
                "duration": 8.352,
                "audio_path": "media/audio/解釋_3_x_4_的意義：呈現_3_組各有_4_顆星星，並將它們聚集起來總計為_12_顆。/step_05.mp3"
            }
        ]

        for step_data in sequence:
            step_num = step_data["step"]
            duration = step_data["duration"]
            audio_path = step_data.get("audio_path")

            # === AUDIO (MANDATORY) ===
            if audio_path and os.path.exists(audio_path):
                self.add_sound(audio_path)

            # Track animation runtime
            anim_time = 0

            # === SIGNAL ACTION ===
            signal_action = step_data.get("signal_action")
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_id = signal_action["target"]
                color_str = signal_action.get("color", "YELLOW")
                color_map = {"YELLOW": YELLOW, "BLUE": BLUE, "GREEN": GREEN, "RED": RED, "ORANGE": ORANGE}
                color = color_map.get(color_str, YELLOW)
                target_obj = self.objects[target_id]

                if signal_type == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                    anim_time += 1
                elif signal_type == "Indicate":
                    self.play(Indicate(target_obj, color=color))
                    anim_time += 1
                elif signal_type == "FocusOn":
                    self.play(FocusOn(target_obj))
                    anim_time += 1

            # === VISUAL ACTION ===
            visual_action = step_data["visual_action"]
            action_type = visual_action["type"]
            target_id = visual_action["target_id"]

            if action_type == "Create" and target_id == "title":
                # Title is already added, just fade it in
                self.play(FadeIn(self.objects["title"]))
                anim_time += 1
                remaining = duration - anim_time
                if remaining > 0:
                    self.wait(remaining)

            elif action_type == "CreateGrid" and target_id == "grid_vgroup":
                # Build 3x4 grid of dots row by row
                grid_vgroup = self.objects["grid_vgroup"]
                dot_template = self.objects["dot_template"]
                rows = 3
                cols = 4
                spacing = 0.5
                dot_radius = 0.1

                # Clear existing dots by creating new VGroup
                new_grid = VGroup()
                
                animations = []
                for r in range(rows):
                    row_dots = VGroup()
                    for c in range(cols):
                        dot = dot_template.copy()
                        dot.move_to(np.array([(c - (cols-1)/2) * spacing, 
                                             (r - (rows-1)/2) * spacing, 0]))
                        row_dots.add(dot)
                    
                    # Animate each row as a group
                    new_grid.add(row_dots)
                    animations.append(FadeIn(row_dots))
                
                # Replace the grid_vgroup with new dots
                grid_vgroup.become(new_grid)
                
                # Add to scene if not already added
                if grid_vgroup not in self.mobjects:
                    self.add(grid_vgroup)
                
                # Animate rows appearing
                self.play(LaggedStart(*animations, lag_ratio=0.3))
                anim_time += 2.0

                # Position labels relative to grid
                label_groups = self.objects["label_groups"]
                label_items = self.objects["label_items"]
                label_groups.next_to(grid_vgroup, LEFT, buff=1.0)
                label_items.next_to(grid_vgroup, UP, buff=0.5)

                remaining = duration - anim_time
                if remaining > 0:
                    self.wait(remaining)

            elif action_type == "Write" and target_id == "label_groups":
                label_groups = self.objects["label_groups"]
                label_groups.set_opacity(1)
                self.add(label_groups)
                self.play(Write(label_groups))
                anim_time += 1
                remaining = duration - anim_time
                if remaining > 0:
                    self.wait(remaining)

            elif action_type == "Write" and target_id == "label_items":
                label_items = self.objects["label_items"]
                label_items.set_opacity(1)
                self.add(label_items)
                self.play(Write(label_items))
                anim_time += 1
                remaining = duration - anim_time
                if remaining > 0:
                    self.wait(remaining)

            elif action_type == "ReplacementTransform" and target_id == "grid_vgroup":
                # Transform grid dots into a clustered group
                grid_vgroup = self.objects["grid_vgroup"]
                cluster_vgroup = self.objects["cluster_vgroup"]

                # Flatten the grid to get ALL 12 stars
                all_stars = VGroup(*[star for row in grid_vgroup for star in row])
                
                # Create target cluster dots (12 dots)
                cluster_dots = VGroup()
                for i in range(12):
                    angle = i * (2 * np.pi / 12)
                    radius = 0.8
                    pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
                    dot = Dot(radius=0.15, color=YELLOW, fill_opacity=1.0)
                    dot.move_to(pos)
                    cluster_dots.add(dot)

                self.play(
                    ReplacementTransform(all_stars, cluster_dots),
                    FadeOut(self.objects["label_groups"]),
                    FadeOut(self.objects["label_items"]),
                    run_time=2
                )
                self.objects["cluster_vgroup"] = cluster_dots
                
                # OPTIONAL: Add a quick "count" highlight
                self.play(LaggedStart(*[Indicate(d, scale_factor=1.5) for d in cluster_dots], lag_ratio=0.1), run_time=2)
                
                anim_time += 4.0
                remaining = duration - anim_time
                if remaining > 0:
                    self.wait(remaining)

            elif action_type == "Write" and target_id == "equation":
                equation = self.objects["equation"]
                equation.set_opacity(1)
                self.add(equation)
                self.play(Write(equation))
                anim_time += 1
                remaining = duration - anim_time
                if remaining > 0:
                    self.wait(remaining)

            else:
                # Fallback: wait full duration if no matching action
                self.wait(duration)