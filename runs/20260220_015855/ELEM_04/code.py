from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create Layout Engine
        layout = LayoutEngine()
        
        # Create objects from layout_plan
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=40)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        
        # Pizza 1 Circle
        pizza1_circle = Circle(radius=2.0, color=WHITE, stroke_width=3)
        obj_pizza1_circle = LayoutObject(pizza1_circle, "pizza1_circle")
        layout.add(obj_pizza1_circle)
        layout.add_to_zone(obj_pizza1_circle, "CONTENT")
        layout.add_constraint(obj_pizza1_circle.center_x == -3.5)
        layout.add_constraint(obj_pizza1_circle.center_y == 0)
        
        # Pizza 2 Circle
        pizza2_circle = Circle(radius=2.0, color=WHITE, stroke_width=3)
        obj_pizza2_circle = LayoutObject(pizza2_circle, "pizza2_circle")
        layout.add(obj_pizza2_circle)
        layout.add_to_zone(obj_pizza2_circle, "CONTENT")
        layout.add_constraint(obj_pizza2_circle.center_x == 3.5)
        layout.add_constraint(obj_pizza2_circle.center_y == 0)
        
        # Pizza 1 Division Line
        pizza1_div_line = Line(start=ORIGIN, end=UP*2.0, color=WHITE, stroke_width=2)
        pizza1_div_line.move_to(pizza1_circle.get_center())
        
        # Pizza 1 Shaded Sector (1/2)
        pizza1_shaded_sector = Sector(
            radius=2.0,
            angle=PI,
            start_angle=0,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        pizza1_shaded_sector.move_to(pizza1_circle.get_center())
        
        # Pizza 2 Division Lines
        pizza2_div_line1 = Line(start=ORIGIN, end=UP*2.0, color=WHITE, stroke_width=2)
        pizza2_div_line1.move_to(pizza2_circle.get_center())
        
        pizza2_div_line2 = Line(start=ORIGIN, end=RIGHT*2.0, color=WHITE, stroke_width=2)
        pizza2_div_line2.move_to(pizza2_circle.get_center())
        
        pizza2_div_line3 = Line(start=ORIGIN, end=DOWN*2.0, color=WHITE, stroke_width=2)
        pizza2_div_line3.move_to(pizza2_circle.get_center())
        
        # Pizza 2 Shaded Sectors (2/4)
        pizza2_shaded_sector1 = Sector(
            radius=2.0,
            angle=PI/2,
            start_angle=0,
            color="#1E90FF",
            fill_opacity=0.7,
            stroke_width=0
        )
        pizza2_shaded_sector1.move_to(pizza2_circle.get_center())
        
        pizza2_shaded_sector2 = Sector(
            radius=2.0,
            angle=PI/2,
            start_angle=3*PI/2,
            color="#87CEEB",
            fill_opacity=0.7,
            stroke_width=0
        )
        pizza2_shaded_sector2.move_to(pizza2_circle.get_center())
        
        # Fraction Labels
        label_pizza1 = MathTex(r"\frac{1}{2}", color="#1E90FF", font_size=36)
        label_pizza1.next_to(pizza1_circle, DOWN, buff=0.8)
        
        label_pizza2 = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_pizza2.next_to(pizza2_circle, DOWN, buff=0.8)
        
        # Final Equivalence Equation
        equivalence_eq = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=YELLOW, font_size=40)
        obj_equivalence_eq = LayoutObject(equivalence_eq, "equivalence_eq")
        layout.add(obj_equivalence_eq)
        layout.add_to_zone(obj_equivalence_eq, "FOOTER")
        layout.add_constraint(obj_equivalence_eq.center_x == 0)
        
        # Solve layout constraints
        layout.solve()
        
        # Create VGroups for each pizza (for transformation)
        pizza1_group = VGroup(pizza1_circle, pizza1_div_line, pizza1_shaded_sector, label_pizza1)
        pizza2_group = VGroup(pizza2_circle, pizza2_div_line1, pizza2_div_line2, pizza2_div_line3,
                             pizza2_shaded_sector1, pizza2_shaded_sector2, label_pizza2)
        
        # Store objects in registry for reference
        self.objects = {
            "title": title,
            "pizza1_circle": pizza1_circle,
            "pizza2_circle": pizza2_circle,
            "pizza1_div_line": pizza1_div_line,
            "pizza1_shaded_sector": pizza1_shaded_sector,
            "pizza2_div_line1": pizza2_div_line1,
            "pizza2_div_line2": pizza2_div_line2,
            "pizza2_div_line3": pizza2_div_line3,
            "pizza2_shaded_sector1": pizza2_shaded_sector1,
            "pizza2_shaded_sector2": pizza2_shaded_sector2,
            "label_pizza1": label_pizza1,
            "label_pizza2": label_pizza2,
            "equivalence_eq": equivalence_eq,
            "pizza1_group": pizza1_group,
            "pizza2_group": pizza2_group
        }
        
        # ========== PHASE 2: Animation Sequence ==========
        
        # Step 1
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3")
        self.play(Write(title))
        self.play(Create(pizza1_circle), Create(pizza2_circle))
        remaining = 3.264 - 2.0  # Approx animation time for Write + 2xCreate
        if remaining > 0:
            self.wait(remaining)
        
        # Step 2
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3")
        self.play(Indicate(pizza1_circle, color=YELLOW))
        self.play(Create(pizza1_div_line))
        remaining = 3.72 - 2.0  # Indicate + Create
        if remaining > 0:
            self.wait(remaining)
        
        # Step 3
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3")
        self.play(Indicate(pizza1_div_line, color=YELLOW))
        self.play(FadeIn(pizza1_shaded_sector))
        remaining = 3.648 - 2.0  # Indicate + FadeIn
        if remaining > 0:
            self.wait(remaining)
        
        # Step 4
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3")
        self.play(Indicate(pizza2_circle, color=YELLOW))
        self.play(
            Create(pizza2_div_line1),
            Create(pizza2_div_line2),
            Create(pizza2_div_line3)
        )
        remaining = 4.368 - 3.0  # Indicate + 3xCreate
        if remaining > 0:
            self.wait(remaining)
        
        # Step 5
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3")
        self.play(
            FadeIn(pizza2_shaded_sector1),
            FadeIn(pizza2_shaded_sector2)
        )
        remaining = 4.32 - 1.5  # 2x FadeIn
        if remaining > 0:
            self.wait(remaining)
        
        # Step 6
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3")
        self.play(
            Write(label_pizza1),
            Write(label_pizza2)
        )
        remaining = 3.072 - 1.5  # 2x Write
        if remaining > 0:
            self.wait(remaining)
        
        # Step 7
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3")
        self.play(Circumscribe(pizza2_circle, color=YELLOW, run_time=1))
        self.play(
            pizza2_group.animate.move_to(pizza1_group.get_center()),
            run_time=2
        )
        remaining = 6.672 - 3.0  # Circumscribe + move
        if remaining > 0:
            self.wait(remaining)
        
        # Step 8
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3")
        self.play(Indicate(pizza1_shaded_sector, color=YELLOW))
        
        # Create new 1/2 label for transformation
        label_pizza2_new = MathTex(r"\frac{1}{2}", color="#1E90FF", font_size=36)
        label_pizza2_new.move_to(label_pizza2.get_center())
        
        self.play(ReplacementTransform(label_pizza2, label_pizza2_new))
        self.objects["label_pizza2"] = label_pizza2_new
        
        remaining = 8.16 - 3.0  # Indicate + ReplacementTransform
        if remaining > 0:
            self.wait(remaining)
        
        # Step 9
        self.add_sound("media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3")
        self.play(Write(equivalence_eq))
        remaining = 4.584 - 1.5  # Write
        if remaining > 0:
            self.wait(remaining)
        
        # Final pause
        self.wait(2)