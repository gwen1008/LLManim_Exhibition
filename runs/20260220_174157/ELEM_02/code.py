from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Initialize Layout Engine
        layout = LayoutEngine()
        
        # Create Anchors (as dummy mobjects for reference)
        title_anchor = Dot(ORIGIN).set_opacity(0)
        content_center = Dot(ORIGIN).set_opacity(0)
        explanation_anchor = Dot(ORIGIN).set_opacity(0)
        row1_pos = Dot(ORIGIN).set_opacity(0)
        row2_pos = Dot(ORIGIN).set_opacity(0)
        row3_pos = Dot(ORIGIN).set_opacity(0)
        
        # Register anchors with layout (for zone assignment)
        layout.add(LayoutObject(title_anchor, "title_anchor"))
        layout.add(LayoutObject(content_center, "content_center"))
        layout.add(LayoutObject(explanation_anchor, "explanation_anchor"))
        layout.add(LayoutObject(row1_pos, "row1_pos"))
        layout.add(LayoutObject(row2_pos, "row2_pos"))
        layout.add(LayoutObject(row3_pos, "row3_pos"))
        
        # Assign zones to anchors
        layout.add_to_zone(layout.get("title_anchor"), "HEADER")
        layout.add_to_zone(layout.get("content_center"), "CONTENT")
        layout.add_to_zone(layout.get("explanation_anchor"), "FOOTER")
        layout.add_to_zone(layout.get("row1_pos"), "CONTENT")
        layout.add_to_zone(layout.get("row2_pos"), "CONTENT")
        layout.add_to_zone(layout.get("row3_pos"), "CONTENT")
        
        # Center all anchors horizontally
        layout.add_constraint(layout.get("title_anchor").center_x == 0)
        layout.add_constraint(layout.get("content_center").center_x == 0)
        layout.add_constraint(layout.get("explanation_anchor").center_x == 0)
        layout.add_constraint(layout.get("row1_pos").center_x == 0)
        layout.add_constraint(layout.get("row2_pos").center_x == 0)
        layout.add_constraint(layout.get("row3_pos").center_x == 0)
        
        # Vertical spacing for row positions
        layout.add_constraint(layout.get("row1_pos").center_y == 1.5)
        layout.add_constraint(layout.get("row2_pos").center_y == 0)
        layout.add_constraint(layout.get("row3_pos").center_y == -1.5)
        
        # Solve layout to get actual positions
        layout.solve()
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Multiplication as Repeated Addition: 3 × 4", color=WHITE, font_size=36)
        title.move_to(layout.get("title_anchor").get_center())
        self.objects["title"] = title
        
        # step_label
        step_label = Text("Let's build 3 groups of 4.", color=YELLOW, font_size=28)
        step_label.move_to(layout.get("explanation_anchor").get_center())
        self.objects["step_label"] = step_label
        
        # row1, row2, row3 (VGroups of 4 Dots each)
        dot_positions = [(-1.2, 0, 0), (-0.4, 0, 0), (0.4, 0, 0), (1.2, 0, 0)]
        row1 = VGroup(*[Dot(point=pos, color=BLUE, radius=0.15) for pos in dot_positions])
        row1.move_to(layout.get("row1_pos").get_center())
        self.objects["row1"] = row1
        
        row2 = VGroup(*[Dot(point=pos, color=GREEN, radius=0.15) for pos in dot_positions])
        row2.move_to(layout.get("row2_pos").get_center())
        self.objects["row2"] = row2
        
        row3 = VGroup(*[Dot(point=pos, color=RED, radius=0.15) for pos in dot_positions])
        row3.move_to(layout.get("row3_pos").get_center())
        self.objects["row3"] = row3
        
        # labels
        label1 = MathTex(r"1 \text{ group of } 4", color=BLUE, font_size=28)
        label1.next_to(row1, RIGHT, buff=1.0)
        self.objects["label1"] = label1
        
        label2 = MathTex(r"2 \text{ groups of } 4", color=GREEN, font_size=28)
        label2.next_to(row2, RIGHT, buff=1.0)
        self.objects["label2"] = label2
        
        label3 = MathTex(r"3 \text{ groups of } 4", color=RED, font_size=28)
        label3.next_to(row3, RIGHT, buff=1.0)
        self.objects["label3"] = label3
        
        # combined_cluster (3x4 grid of dots)
        # Create rows for the grid
        grid_rows = []
        row_colors = [BLUE, GREEN, RED]
        for i in range(3):
            row_dots = VGroup(*[Dot(point=(j*0.8 - 1.2, 0, 0), color=row_colors[i], radius=0.15) for j in range(4)])
            grid_rows.append(row_dots)
        combined_cluster = VGroup(*grid_rows)
        combined_cluster.arrange(DOWN, buff=0.8, aligned_edge=ORIGIN)
        combined_cluster.move_to(layout.get("content_center").get_center())
        self.objects["combined_cluster"] = combined_cluster
        
        # final_equation
        final_equation = MathTex(r"3 \times 4 = 12", color=YELLOW, font_size=40)
        final_equation.next_to(combined_cluster, DOWN, buff=1.0)
        self.objects["final_equation"] = final_equation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        self.add_sound(audio_file)
        self.play(Write(self.objects["title"]), Write(self.objects["step_label"]))
        self.play(Create(self.objects["row1"]))
        animation_time = 2.0 + 1.5  # Write title+label + Create row1
        remaining = 6.552 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["row1"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label1"]))
        animation_time = 1.0 + 1.0  # Circumscribe + Write
        remaining = 4.728 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        self.add_sound(audio_file)
        self.play(Indicate(self.objects["row2"], color=GREEN))
        self.play(Create(self.objects["row2"]), Write(self.objects["label2"]),
                  Create(self.objects["row3"]), Write(self.objects["label3"]))
        animation_time = 1.0 + 2.0  # Indicate + Create/Write (grouped)
        remaining = 4.848 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        self.add_sound(audio_file)
        self.play(Indicate(self.objects["label3"], color=RED))
        # Update step_label
        new_step_label = Text("Combining 3 groups of 4...", color=YELLOW, font_size=28)
        new_step_label.move_to(self.objects["step_label"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label
        
        # Move rows to grid positions (transform to pre-created combined_cluster rows)
        target_row1 = self.objects["combined_cluster"][0]
        target_row2 = self.objects["combined_cluster"][1]
        target_row3 = self.objects["combined_cluster"][2]
        
        self.play(
            Transform(self.objects["row1"], target_row1),
            Transform(self.objects["row2"], target_row2),
            Transform(self.objects["row3"], target_row3),
            FadeOut(self.objects["label1"]),
            FadeOut(self.objects["label2"]),
            FadeOut(self.objects["label3"])
        )
        animation_time = 1.0 + 1.0 + 3.0  # Indicate + ReplacementTransform + Transform/FadeOut
        remaining = 5.352 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["combined_cluster"], color=YELLOW, run_time=1))
        self.play(ReplacementTransform(self.objects["combined_cluster"], self.objects["final_equation"]))
        animation_time = 1.0 + 2.0  # Circumscribe + ReplacementTransform
        remaining = 8.472 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))