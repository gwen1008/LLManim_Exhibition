from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Multiplication: 3 × 4 = 12", color=WHITE, font_size=36)
        self.objects["title"] = title
        
        # Create stars for rows
        star_positions_row1 = [(-1.2, 0.6, 0), (-0.4, 0.6, 0), (0.4, 0.6, 0), (1.2, 0.6, 0)]
        stars_row1 = VGroup(*[Star(n=5, color=YELLOW, outer_radius=0.15, fill_opacity=1).move_to(pos) for pos in star_positions_row1])
        self.objects["row1"] = stars_row1
        
        star_positions_row2 = [(-1.2, 0, 0), (-0.4, 0, 0), (0.4, 0, 0), (1.2, 0, 0)]
        stars_row2 = VGroup(*[Star(n=5, color=YELLOW, outer_radius=0.15, fill_opacity=1).move_to(pos) for pos in star_positions_row2])
        self.objects["row2"] = stars_row2
        
        star_positions_row3 = [(-1.2, -0.6, 0), (-0.4, -0.6, 0), (0.4, -0.6, 0), (1.2, -0.6, 0)]
        stars_row3 = VGroup(*[Star(n=5, color=YELLOW, outer_radius=0.15, fill_opacity=1).move_to(pos) for pos in star_positions_row3])
        self.objects["row3"] = stars_row3
        
        # Labels for groups
        label_group1 = MathTex("4", color=BLUE, font_size=30)
        self.objects["label_group1"] = label_group1
        
        label_group2 = MathTex("4", color=BLUE, font_size=30)
        self.objects["label_group2"] = label_group2
        
        label_group3 = MathTex("4", color=BLUE, font_size=30)
        self.objects["label_group3"] = label_group3
        
        # Equation
        equation = MathTex("3 \\times 4 = 12", color=GREEN, font_size=32)
        self.objects["equation"] = equation
        
        # Total stars cluster (initially not created, will be created during transformation)
        # We'll create it later in step 5.
        
        # Total label
        total_label = MathTex("12", color=RED, font_size=36)
        self.objects["total_label"] = total_label
        
        # Initialize Layout Engine
        layout = LayoutEngine()
        
        # Register objects as LayoutObjects
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        
        # For grid rows, we'll position them relative to each other manually as per geometry_def
        # They are already placed at specific coordinates, so we won't use layout for them.
        # But we need to position the labels next to rows.
        # We'll position labels after rows are added to scene.
        
        # Equation goes to FOOTER zone
        obj_equation = LayoutObject(equation, "equation")
        layout.add(obj_equation)
        layout.add_to_zone(obj_equation, "FOOTER")
        layout.add_constraint(obj_equation.center_x == 0)
        
        # Total label will be positioned later relative to cluster.
        
        # Solve layout for title and equation
        layout.solve()
        
        # Apply solved positions
        title.move_to(obj_title.get_center())
        equation.move_to(obj_equation.get_center())
        
        # Position rows at grid_center (ORIGIN) with offsets as per geometry_def
        # They are already at correct relative positions, just move the group center to ORIGIN.
        grid_group = VGroup(stars_row1, stars_row2, stars_row3)
        grid_group.move_to(ORIGIN)
        
        # Position labels next to rows (using relative positioning)
        label_group1.next_to(stars_row1, RIGHT, buff=0.8)
        label_group2.next_to(stars_row2, RIGHT, buff=0.8)
        label_group3.next_to(stars_row3, RIGHT, buff=0.8)
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(title))
        self.wait(7.392 - 1.0 + 0.5)
        
        # Step 2
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(stars_row1, color=YELLOW))
        self.play(Create(stars_row1))
        self.wait(3.576 - 2.0 + 0.5)
        
        # Step 3
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(stars_row2, color=YELLOW))
        self.play(Create(stars_row2), Create(stars_row3))
        self.wait(5.016 - 2.0 + 0.5)
        
        # Step 4
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(label_group1, color=BLUE, run_time=1))
        self.play(Write(label_group1), Write(label_group2), Write(label_group3))
        self.wait(6.72 - 2.0 + 0.5)
        
        # Step 5
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(equation, color=GREEN))
        
        # Create circular cluster - FIXED: Use arrange_in_grid instead of arrange_in_circle
        all_stars = VGroup(stars_row1, stars_row2, stars_row3)
        star_list = []
        for row in [stars_row1, stars_row2, stars_row3]:
            for star in row:
                star_list.append(star)
        cluster_stars = VGroup(*star_list)
        
        # Arrange stars in a circular pattern manually
        radius = 1.5
        for i, star in enumerate(cluster_stars):
            angle = i * 2 * PI / len(cluster_stars)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            star.move_to([x, y, 0])
        
        cluster_stars.move_to(ORIGIN)
        self.objects["total_stars"] = cluster_stars
        
        self.play(Write(equation), ReplacementTransform(all_stars, cluster_stars))
        self.wait(7.752 - 3.0 + 0.5)
        
        # Step 6
        audio_file = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3"
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        total_label.next_to(cluster_stars, DOWN, buff=0.5)
        self.play(Circumscribe(total_label, color=RED, run_time=1))
        self.play(Write(total_label))
        self.wait(8.208 - 2.0 + 0.5)
        
        # Final wait
        self.wait(2)