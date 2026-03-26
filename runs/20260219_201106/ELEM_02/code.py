from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create Layout Engine
        layout = LayoutEngine()
        
        # 1. Create Title
        title = Text("3 × 4 = 12: Multiplication as Repeated Addition", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title
        
        # 2. Create Star Prototype (Group of 4 stars)
        star_prototype = VGroup(*[Star(n=5, outer_radius=0.15, color=YELLOW, fill_opacity=1) for _ in range(4)])
        star_prototype.arrange(RIGHT, buff=0.3)
        obj_star_proto = LayoutObject(star_prototype, "star_prototype")
        layout.add(obj_star_proto)
        layout.add_to_zone(obj_star_proto, "CONTENT")
        layout.add_constraint(obj_star_proto.center_x == 0)
        self.objects["star_prototype"] = star_prototype
        
        # 3. Create Group Labels
        group1_label = MathTex("4", color=BLUE)
        obj_label1 = LayoutObject(group1_label, "group1_label")
        layout.add(obj_label1)
        layout.align_to(obj_label1, obj_star_proto, "TOP", buff=0.3)
        layout.add_constraint(obj_label1.center_x == obj_star_proto.center_x)
        self.objects["group1_label"] = group1_label
        
        # Create copies for groups 2 and 3 (initially invisible)
        group2 = star_prototype.copy()
        group2.set_opacity(0)
        obj_group2 = LayoutObject(group2, "group2")
        layout.add(obj_group2)
        layout.align_to(obj_group2, obj_star_proto, "TOP", buff=1.2)
        layout.add_constraint(obj_group2.center_x == obj_star_proto.center_x)
        self.objects["group2"] = group2
        
        group2_label = MathTex("4", color=BLUE)
        group2_label.set_opacity(0)
        obj_label2 = LayoutObject(group2_label, "group2_label")
        layout.add(obj_label2)
        layout.align_to(obj_label2, obj_group2, "TOP", buff=0.3)
        layout.add_constraint(obj_label2.center_x == obj_group2.center_x)
        self.objects["group2_label"] = group2_label
        
        group3 = star_prototype.copy()
        group3.set_opacity(0)
        obj_group3 = LayoutObject(group3, "group3")
        layout.add(obj_group3)
        layout.align_to(obj_group3, obj_star_proto, "BOTTOM", buff=1.2)
        layout.add_constraint(obj_group3.center_x == obj_star_proto.center_x)
        self.objects["group3"] = group3
        
        group3_label = MathTex("4", color=BLUE)
        group3_label.set_opacity(0)
        obj_label3 = LayoutObject(group3_label, "group3_label")
        layout.add(obj_label3)
        layout.align_to(obj_label3, obj_group3, "TOP", buff=0.3)
        layout.add_constraint(obj_label3.center_x == obj_group3.center_x)
        self.objects["group3_label"] = group3_label
        
        # Create container for all groups
        all_groups = VGroup(star_prototype, group2, group3)
        obj_all_groups = LayoutObject(all_groups, "all_groups")
        layout.add(obj_all_groups)
        self.objects["all_groups"] = all_groups
        
        # Create final grid (3x4 arrangement, initially invisible)
        final_grid_stars = []
        for _ in range(12):
            final_grid_stars.append(Star(n=5, outer_radius=0.15, color=YELLOW, fill_opacity=1))
        final_grid = VGroup(*final_grid_stars)
        final_grid.arrange_in_grid(rows=3, cols=4, buff=0.3)
        final_grid.set_opacity(0)
        obj_final_grid = LayoutObject(final_grid, "final_grid")
        layout.add(obj_final_grid)
        layout.add_to_zone(obj_final_grid, "CONTENT")
        layout.add_constraint(obj_final_grid.center_x == 0)
        self.objects["final_grid"] = final_grid
        
        # Create equation steps
        equation_step1 = MathTex("4", color=WHITE, font_size=36)
        obj_eq1 = LayoutObject(equation_step1, "equation_step1")
        layout.add(obj_eq1)
        layout.add_to_zone(obj_eq1, "FOOTER")
        layout.add_constraint(obj_eq1.center_x == 0)
        self.objects["equation_step1"] = equation_step1
        
        equation_step2 = MathTex("4 + 4", color=WHITE, font_size=36)
        equation_step2.set_opacity(0)
        obj_eq2 = LayoutObject(equation_step2, "equation_step2")
        layout.add(obj_eq2)
        layout.align_to(obj_eq2, obj_eq1, "CENTER")
        self.objects["equation_step2"] = equation_step2
        
        equation_step3 = MathTex("4 + 4 + 4", color=WHITE, font_size=36)
        equation_step3.set_opacity(0)
        obj_eq3 = LayoutObject(equation_step3, "equation_step3")
        layout.add(obj_eq3)
        layout.align_to(obj_eq3, obj_eq1, "CENTER")
        self.objects["equation_step3"] = equation_step3
        
        equation_final = MathTex("4 + 4 + 4 = 12", color=WHITE, font_size=36)
        equation_final.set_opacity(0)
        obj_eq_final = LayoutObject(equation_final, "equation_final")
        layout.add(obj_eq_final)
        layout.align_to(obj_eq_final, obj_eq1, "CENTER")
        self.objects["equation_final"] = equation_final
        
        multiplication_eq = MathTex("3 \\times 4 = 12", color=GREEN, font_size=40)
        multiplication_eq.set_opacity(0)
        obj_mult_eq = LayoutObject(multiplication_eq, "multiplication_eq")
        layout.add(obj_mult_eq)
        layout.align_to(obj_mult_eq, obj_eq_final, "BOTTOM", buff=0.5)
        layout.add_constraint(obj_mult_eq.center_x == obj_eq_final.center_x)
        self.objects["multiplication_eq"] = multiplication_eq
        
        # Solve layout
        layout.solve()
        
        # ========== PHASE 2: Animation Sequence ==========
        
        # Step 1
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Write(title))
        self.play(Create(star_prototype))
        animation_time = 2.0  # Estimate for Write + Create
        remaining = 5.616 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 2
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Write(group1_label))
        animation_time = 1.0
        remaining = 4.776 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 3
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(star_prototype, color=YELLOW))
        
        # Create copies for groups 2 and 3
        group2_copy = star_prototype.copy()
        group2_copy.move_to(group2.get_center())
        group3_copy = star_prototype.copy()
        group3_copy.move_to(group3.get_center())
        
        self.play(
            Transform(star_prototype.copy(), group2_copy),
            Transform(star_prototype.copy(), group3_copy)
        )
        # Replace the invisible placeholders with the actual copies
        self.remove(group2, group3)
        self.add(group2_copy, group3_copy)
        self.objects["group2"] = group2_copy
        self.objects["group3"] = group3_copy
        
        animation_time = 3.0
        remaining = 6.792 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 4
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(
            Write(group2_label),
            Write(group3_label)
        )
        animation_time = 2.0
        remaining = 6.336 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 5
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Circumscribe(all_groups, color=ORANGE, run_time=1))
        
        # Transform equation from "4" to "4 + 4"
        self.play(
            ReplacementTransform(equation_step1, equation_step2)
        )
        self.objects["equation_step1"] = equation_step2  # Update reference
        
        animation_time = 3.0
        remaining = 7.176 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 6
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        # Transform equation to "4 + 4 + 4"
        self.play(
            ReplacementTransform(equation_step2, equation_step3)
        )
        self.objects["equation_step2"] = equation_step3  # Update reference
        
        # Transform star groups into grid
        self.play(
            Transform(all_groups, final_grid)
        )
        self.remove(all_groups)
        self.add(final_grid)
        
        animation_time = 3.0
        remaining = 4.512 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 7
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(final_grid, color=YELLOW))
        
        # Transform equation to "4 + 4 + 4 = 12"
        self.play(
            ReplacementTransform(equation_step3, equation_final)
        )
        self.objects["equation_step3"] = equation_final  # Update reference
        
        animation_time = 3.0
        remaining = 5.544 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 8
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Circumscribe(equation_final, color=GREEN, run_time=1))
        
        self.play(Write(multiplication_eq))
        
        animation_time = 3.0
        remaining = 5.544 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Final pause
        self.wait(2)