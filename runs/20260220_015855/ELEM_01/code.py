from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create all objects from layout_plan
        self.objects = {}
        
        # Create objects based on layout_plan.objects
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=40)
        self.objects["title"] = title
        
        # Pizza bases
        pizza1_base = Circle(radius=2.0, color="#333333", fill_opacity=0.7, stroke_width=3)
        self.objects["pizza1_base"] = pizza1_base
        
        pizza2_base = Circle(radius=2.0, color="#333333", fill_opacity=0.7, stroke_width=3)
        self.objects["pizza2_base"] = pizza2_base
        
        # Division lines
        pizza1_div_line = Line(UP*2, DOWN*2, color=WHITE, stroke_width=3)
        self.objects["pizza1_div_line"] = pizza1_div_line
        
        pizza2_div_line1 = Line(UP*2, DOWN*2, color=WHITE, stroke_width=3)
        self.objects["pizza2_div_line1"] = pizza2_div_line1
        
        pizza2_div_line2 = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=3)
        self.objects["pizza2_div_line2"] = pizza2_div_line2
        
        # Shaded sectors
        # Note: Sector API uses 'radius', not 'outer_radius'
        pizza1_shaded_sector = Sector(
            radius=2.0, 
            angle=PI, 
            color="#1E90FF", 
            fill_opacity=0.8, 
            stroke_width=0
        )
        self.objects["pizza1_shaded_sector"] = pizza1_shaded_sector
        
        pizza2_shaded_sector1 = Sector(
            radius=2.0, 
            angle=PI/2, 
            color="#1E90FF", 
            fill_opacity=0.8, 
            stroke_width=0
        )
        self.objects["pizza2_shaded_sector1"] = pizza2_shaded_sector1
        
        pizza2_shaded_sector2 = Sector(
            radius=2.0, 
            angle=PI/2, 
            start_angle=PI/2,
            color="#1E90FF", 
            fill_opacity=0.8, 
            stroke_width=0
        )
        self.objects["pizza2_shaded_sector2"] = pizza2_shaded_sector2
        
        # Fraction labels
        label_1over2 = MathTex(r"\frac{1}{2}", color=YELLOW, font_size=36)
        self.objects["label_1over2"] = label_1over2
        
        label_2over4 = MathTex(r"\frac{2}{4}", color=YELLOW, font_size=36)
        self.objects["label_2over4"] = label_2over4
        
        # Explanation text
        explanation_text = Text("Same area shaded → Fractions are equivalent", color=GREEN, font_size=28)
        self.objects["explanation_text"] = explanation_text
        
        # Initialize Layout Engine
        layout = LayoutEngine()
        
        # Register objects as LayoutObjects
        obj_title = LayoutObject(title, "title")
        obj_pizza1_base = LayoutObject(pizza1_base, "pizza1_base")
        obj_pizza2_base = LayoutObject(pizza2_base, "pizza2_base")
        obj_pizza1_div_line = LayoutObject(pizza1_div_line, "pizza1_div_line")
        obj_pizza2_div_line1 = LayoutObject(pizza2_div_line1, "pizza2_div_line1")
        obj_pizza2_div_line2 = LayoutObject(pizza2_div_line2, "pizza2_div_line2")
        obj_pizza1_shaded_sector = LayoutObject(pizza1_shaded_sector, "pizza1_shaded_sector")
        obj_pizza2_shaded_sector1 = LayoutObject(pizza2_shaded_sector1, "pizza2_shaded_sector1")
        obj_pizza2_shaded_sector2 = LayoutObject(pizza2_shaded_sector2, "pizza2_shaded_sector2")
        obj_label_1over2 = LayoutObject(label_1over2, "label_1over2")
        obj_label_2over4 = LayoutObject(label_2over4, "label_2over4")
        obj_explanation_text = LayoutObject(explanation_text, "explanation_text")
        
        # Add objects to layout
        layout.add(obj_title)
        layout.add(obj_pizza1_base)
        layout.add(obj_pizza2_base)
        layout.add(obj_pizza1_div_line)
        layout.add(obj_pizza2_div_line1)
        layout.add(obj_pizza2_div_line2)
        layout.add(obj_pizza1_shaded_sector)
        layout.add(obj_pizza2_shaded_sector1)
        layout.add(obj_pizza2_shaded_sector2)
        layout.add(obj_label_1over2)
        layout.add(obj_label_2over4)
        layout.add(obj_explanation_text)
        
        # Assign to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_pizza1_base, "CONTENT")
        layout.add_to_zone(obj_pizza2_base, "CONTENT")
        layout.add_to_zone(obj_pizza1_div_line, "CONTENT")
        layout.add_to_zone(obj_pizza2_div_line1, "CONTENT")
        layout.add_to_zone(obj_pizza2_div_line2, "CONTENT")
        layout.add_to_zone(obj_pizza1_shaded_sector, "CONTENT")
        layout.add_to_zone(obj_pizza2_shaded_sector1, "CONTENT")
        layout.add_to_zone(obj_pizza2_shaded_sector2, "CONTENT")
        layout.add_to_zone(obj_label_1over2, "CONTENT")
        layout.add_to_zone(obj_label_2over4, "CONTENT")
        layout.add_to_zone(obj_explanation_text, "FOOTER")
        
        # Position pizzas side-by-side
        layout.align_to(obj_pizza1_base, obj_title, "BOTTOM", buff=1.5)
        layout.align_to(obj_pizza2_base, obj_title, "BOTTOM", buff=1.5)
        layout.add_constraint(obj_pizza1_base.center_x == -3)
        layout.add_constraint(obj_pizza2_base.center_x == 3)
        
        # Align division lines to their respective pizza centers
        layout.align_to(obj_pizza1_div_line, obj_pizza1_base, "CENTER")
        layout.align_to(obj_pizza2_div_line1, obj_pizza2_base, "CENTER")
        layout.align_to(obj_pizza2_div_line2, obj_pizza2_base, "CENTER")
        
        # Align shaded sectors to their respective pizza centers
        layout.align_to(obj_pizza1_shaded_sector, obj_pizza1_base, "CENTER")
        layout.align_to(obj_pizza2_shaded_sector1, obj_pizza2_base, "CENTER")
        layout.align_to(obj_pizza2_shaded_sector2, obj_pizza2_base, "CENTER")
        
        # Position labels below pizzas
        layout.align_to(obj_label_1over2, obj_pizza1_base, "BOTTOM", buff=0.5)
        layout.align_to(obj_label_2over4, obj_pizza2_base, "BOTTOM", buff=0.5)
        layout.add_constraint(obj_label_1over2.center_x == obj_pizza1_base.center_x)
        layout.add_constraint(obj_label_2over4.center_x == obj_pizza2_base.center_x)
        
        # Center explanation text
        layout.add_constraint(obj_explanation_text.center_x == 0)
        
        # Solve layout
        layout.solve()
        
        # Apply positions to all objects
        # Note: Objects are not added to scene yet, just positioned
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Create(pizza1_base))
        animation_time = 1.0
        remaining = 4.68 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 2
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Create(pizza2_base))
        animation_time = 1.0
        remaining = 3.768 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 3
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(pizza1_div_line, color=WHITE))
        self.play(Create(pizza1_div_line))
        animation_time = 2.0  # Indicate + Create
        remaining = 4.968 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 4
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(pizza1_shaded_sector, color=BLUE))
        self.play(FadeIn(pizza1_shaded_sector))
        animation_time = 2.0  # Indicate + FadeIn
        remaining = 4.32 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 5
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Circumscribe(label_1over2, color=YELLOW, run_time=1))
        self.play(Write(label_1over2))
        animation_time = 2.0  # Circumscribe + Write
        remaining = 2.88 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 6
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(pizza2_div_line1, color=WHITE))
        self.play(Create(pizza2_div_line1), Create(pizza2_div_line2))
        animation_time = 2.0  # Indicate + Create both
        remaining = 6.528 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 7
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(pizza2_shaded_sector1, color=BLUE))
        self.play(FadeIn(pizza2_shaded_sector1), FadeIn(pizza2_shaded_sector2))
        animation_time = 2.0  # Indicate + FadeIn both
        remaining = 4.584 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 8
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Circumscribe(label_2over4, color=YELLOW, run_time=1))
        self.play(Write(label_2over4))
        animation_time = 2.0  # Circumscribe + Write
        remaining = 2.448 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Step 9
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Indicate(pizza1_shaded_sector, color=BLUE))
        # Create a copy of pizza1_shaded_sector to transform
        shaded_copy = pizza1_shaded_sector.copy()
        # Create a target VGroup combining both shaded sectors of pizza2
        target_shaded = VGroup(pizza2_shaded_sector1.copy(), pizza2_shaded_sector2.copy())
        # Position target at pizza2 center
        target_shaded.move_to(pizza2_base.get_center())
        
        self.play(ReplacementTransform(shaded_copy, target_shaded))
        animation_time = 3.0  # Indicate + ReplacementTransform
        remaining = 6.096 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Clean up the transformed copy
        self.remove(shaded_copy, target_shaded)
        
        # Step 10
        audio_file = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_09.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        self.play(Circumscribe(explanation_text, color=GREEN, run_time=1))
        self.play(Write(explanation_text))
        animation_time = 2.0  # Circumscribe + Write
        remaining = 6.24 - animation_time + 0.5
        if remaining > 0:
            self.wait(remaining)
        
        # Final pause
        self.wait(2)