from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create all objects as defined in layout_plan
        self.objects = {}
        
        # Create title
        title = Text("Multiplication: 3 × 4 = 12", font_size=36, color=WHITE)
        self.objects["title"] = title
        
        # Create rows of stars (blue circles)
        star_radius = 0.2
        buff = 0.6
        
        # Row 1: 4 blue stars
        row1_stars = VGroup(*[Circle(radius=star_radius, color=BLUE, fill_opacity=0.7) for _ in range(4)])
        row1_stars.arrange(RIGHT, buff=buff)
        self.objects["row1"] = row1_stars
        
        # Row 2: 4 blue stars
        row2_stars = VGroup(*[Circle(radius=star_radius, color=BLUE, fill_opacity=0.7) for _ in range(4)])
        row2_stars.arrange(RIGHT, buff=buff)
        self.objects["row2"] = row2_stars
        
        # Row 3: 4 blue stars
        row3_stars = VGroup(*[Circle(radius=star_radius, color=BLUE, fill_opacity=0.7) for _ in range(4)])
        row3_stars.arrange(RIGHT, buff=buff)
        self.objects["row3"] = row3_stars
        
        # Row labels
        label_row1 = MathTex("4", color=BLUE)
        self.objects["label_row1"] = label_row1
        
        label_row2 = MathTex("4", color=BLUE)
        self.objects["label_row2"] = label_row2
        
        label_row3 = MathTex("4", color=BLUE)
        self.objects["label_row3"] = label_row3
        
        # Combined stars cluster (yellow, arranged in 3x4 grid)
        combined_stars = VGroup(*[Circle(radius=star_radius, color=YELLOW, fill_opacity=0.7) for _ in range(12)])
        combined_stars.arrange_in_grid(rows=3, cols=4, buff=buff)
        self.objects["combined_stars"] = combined_stars
        
        # Equations
        equation_initial = MathTex("3 \\times 4 = ?", font_size=36, color=WHITE)
        self.objects["equation_initial"] = equation_initial
        
        equation_final = MathTex("3 \\times 4 = 12", font_size=36, color=YELLOW)
        self.objects["equation_final"] = equation_final
        
        # Explanation text
        explanation_text = Text("Three groups of four combine to make twelve total", 
                               font_size=24, color=GRAY)
        self.objects["explanation_text"] = explanation_text
        
        # ========== LAYOUT ENGINE SETUP ==========
        layout = LayoutEngine()
        
        # Register all objects with layout engine
        obj_title = LayoutObject(title, "title")
        obj_row1 = LayoutObject(row1_stars, "row1")
        obj_row2 = LayoutObject(row2_stars, "row2")
        obj_row3 = LayoutObject(row3_stars, "row3")
        obj_label1 = LayoutObject(label_row1, "label_row1")
        obj_label2 = LayoutObject(label_row2, "label_row2")
        obj_label3 = LayoutObject(label_row3, "label_row3")
        obj_combined = LayoutObject(combined_stars, "combined_stars")
        obj_eq_init = LayoutObject(equation_initial, "equation_initial")
        obj_eq_final = LayoutObject(equation_final, "equation_final")
        obj_expl = LayoutObject(explanation_text, "explanation_text")
        
        # Add to layout
        layout.add(obj_title)
        layout.add(obj_row1)
        layout.add(obj_row2)
        layout.add(obj_row3)
        layout.add(obj_label1)
        layout.add(obj_label2)
        layout.add(obj_label3)
        layout.add(obj_combined)
        layout.add(obj_eq_init)
        layout.add(obj_eq_final)
        layout.add(obj_expl)
        
        # Assign to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_row1, "CONTENT")
        layout.add_to_zone(obj_row2, "CONTENT")
        layout.add_to_zone(obj_row3, "CONTENT")
        layout.add_to_zone(obj_label1, "CONTENT")
        layout.add_to_zone(obj_label2, "CONTENT")
        layout.add_to_zone(obj_label3, "CONTENT")
        layout.add_to_zone(obj_combined, "CONTENT")
        layout.add_to_zone(obj_eq_init, "CONTENT")
        layout.add_to_zone(obj_eq_final, "CONTENT")
        layout.add_to_zone(obj_expl, "FOOTER")
        
        # Constraints for vertical stack of rows
        layout.align_to(obj_row2, obj_row1, "BOTTOM", buff=1.0)
        layout.align_to(obj_row3, obj_row2, "BOTTOM", buff=1.0)
        layout.align_to(obj_row1, obj_title, "BOTTOM", buff=1.5)
        
        # Align labels to their rows
        layout.align_to(obj_label1, obj_row1, "RIGHT", buff=0.8)
        layout.align_to(obj_label2, obj_row2, "RIGHT", buff=0.8)
        layout.align_to(obj_label3, obj_row3, "RIGHT", buff=0.8)
        
        # Center equations horizontally
        layout.add_constraint(obj_eq_init.center_x == 0)
        layout.add_constraint(obj_eq_final.center_x == 0)
        
        # Position equations below rows
        layout.align_to(obj_eq_init, obj_row3, "BOTTOM", buff=1.0)
        
        # Center combined stars at same position as rows
        layout.align_to(obj_combined, obj_row2, "CENTER")
        
        # Solve layout
        layout.solve()
        
        # Hide combined stars initially (will be transformed into)
        combined_stars.set_opacity(0)
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3")
        self.play(Indicate(title, color=YELLOW), Write(title))
        self.wait(6.0 - 1)  # Signal animation takes ~1s
        
        # Step 2
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3")
        self.play(Create(row1_stars))
        self.wait(5.472 - 1)  # Create animation takes ~1s
        
        # Step 3
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3")
        self.play(Circumscribe(row1_stars, color=YELLOW, run_time=1))
        self.play(Write(label_row1))
        self.wait(2.856 - 2)  # Circumscribe + Write take ~2s
        
        # Step 4
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3")
        self.play(Create(row2_stars))
        self.wait(3.96 - 1)
        
        # Step 5
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3")
        self.play(Circumscribe(row2_stars, color=YELLOW, run_time=1))
        self.play(Write(label_row2))
        self.wait(3.096 - 2)
        
        # Step 6
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3")
        self.play(Create(row3_stars))
        self.wait(4.32 - 1)
        
        # Step 7
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_06.mp3")
        self.play(Circumscribe(row3_stars, color=YELLOW, run_time=1))
        self.play(Write(label_row3))
        self.wait(5.544 - 2)
        
        # Step 8
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_07.mp3")
        self.play(Write(equation_initial))
        self.wait(4.824 - 1)
        
        # Step 9
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_08.mp3")
        self.play(Indicate(row1_stars, color=ORANGE))
        # Prepare for transformation: fade out row1 and fade in corresponding part of combined
        row1_target = combined_stars[0:4].copy()
        row1_target.set_color(BLUE).set_opacity(0.7)
        row1_target.move_to(row1_stars.get_center())
        self.play(Transform(row1_stars, row1_target))
        self.wait(3.768 - 2)  # Indicate + Transform take ~2s
        
        # Step 10
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_09.mp3")
        self.play(Indicate(row2_stars, color=ORANGE))
        row2_target = combined_stars[4:8].copy()
        row2_target.set_color(BLUE).set_opacity(0.7)
        row2_target.move_to(row2_stars.get_center())
        self.play(Transform(row2_stars, row2_target))
        self.wait(3.84 - 2)
        
        # Step 11
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_10.mp3")
        self.play(Indicate(row3_stars, color=ORANGE))
        row3_target = combined_stars[8:12].copy()
        row3_target.set_color(BLUE).set_opacity(0.7)
        row3_target.move_to(row3_stars.get_center())
        self.play(Transform(row3_stars, row3_target))
        self.wait(2.928 - 2)
        
        # Now transform all to final yellow combined cluster
        self.play(
            row1_stars.animate.set_color(YELLOW),
            row2_stars.animate.set_color(YELLOW),
            row3_stars.animate.set_color(YELLOW),
            run_time=1
        )
        
        # Step 12
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_11.mp3")
        self.play(Circumscribe(VGroup(row1_stars, row2_stars, row3_stars), color=GREEN, run_time=1))
        self.play(ReplacementTransform(equation_initial, equation_final))
        self.wait(5.52 - 2)  # Circumscribe + ReplacementTransform take ~2s
        
        # Step 13
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_12.mp3")
        self.play(Indicate(equation_final, color=YELLOW))
        self.play(Write(explanation_text))
        self.wait(7.992 - 2)  # Indicate + Write take ~2s
        
        # Step 14
        self.add_sound("media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_13.mp3")
        self.play(Circumscribe(VGroup(row1_stars, row2_stars, row3_stars), color=YELLOW, run_time=1))
        self.play(FadeOut(label_row1), FadeOut(label_row2), FadeOut(label_row3))
        self.wait(3.744 - 2)  # Circumscribe + FadeOuts take ~2s
        
        # Final pause
        self.wait(2)