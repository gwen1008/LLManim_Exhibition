from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for all objects
        self.objects = {}
        
        # Create Layout Engine
        layout = LayoutEngine()
        
        # Create objects from layout_plan
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title
        
        # Pizza Left (Circle)
        pizza_left = Circle(radius=2, color="#F4E4BA", fill_opacity=0.3, stroke_width=3)
        obj_pizza_left = LayoutObject(pizza_left, "pizza_left")
        layout.add(obj_pizza_left)
        layout.add_to_zone(obj_pizza_left, "CONTENT")
        # Position left: shift left from center
        layout.add_constraint(obj_pizza_left.center_x == -3)
        layout.add_constraint(obj_pizza_left.center_y == 0)
        self.objects["pizza_left"] = pizza_left
        
        # Pizza Right (Circle)
        pizza_right = Circle(radius=2, color="#F4E4BA", fill_opacity=0.3, stroke_width=3)
        obj_pizza_right = LayoutObject(pizza_right, "pizza_right")
        layout.add(obj_pizza_right)
        layout.add_to_zone(obj_pizza_right, "CONTENT")
        # Position right: shift right from center
        layout.add_constraint(obj_pizza_right.center_x == 3)
        layout.add_constraint(obj_pizza_right.center_y == 0)
        self.objects["pizza_right"] = pizza_right
        
        # Division Line Left (Vertical diameter)
        div_line_left = Line(DOWN*2, UP*2, color=WHITE, stroke_width=2)
        obj_div_line_left = LayoutObject(div_line_left, "div_line_left")
        layout.add(obj_div_line_left)
        layout.add_constraint(obj_div_line_left.center_x == obj_pizza_left.center_x)
        layout.add_constraint(obj_div_line_left.center_y == obj_pizza_left.center_y)
        self.objects["div_line_left"] = div_line_left
        
        # Division Lines Right (VGroup of vertical and horizontal diameters)
        div_line_right_v = Line(DOWN*2, UP*2, color=WHITE, stroke_width=2)
        div_line_right_h = Line(LEFT*2, RIGHT*2, color=WHITE, stroke_width=2)
        div_lines_right = VGroup(div_line_right_v, div_line_right_h)
        obj_div_lines_right = LayoutObject(div_lines_right, "div_lines_right")
        layout.add(obj_div_lines_right)
        layout.add_constraint(obj_div_lines_right.center_x == obj_pizza_right.center_x)
        layout.add_constraint(obj_div_lines_right.center_y == obj_pizza_right.center_y)
        self.objects["div_lines_right"] = div_lines_right
        
        # Sector Half (Right half of left pizza)
        # Note: Sector uses 'radius', not 'outer_radius'. Angle PI = 180 degrees, start_angle -PI/2 = -90 degrees (right half).
        sector_half = Sector(radius=2, angle=PI, start_angle=-PI/2, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        obj_sector_half = LayoutObject(sector_half, "sector_half")
        layout.add(obj_sector_half)
        layout.add_constraint(obj_sector_half.center_x == obj_pizza_left.center_x)
        layout.add_constraint(obj_sector_half.center_y == obj_pizza_left.center_y)
        self.objects["sector_half"] = sector_half
        
        # Sector Quarter 1 (Top right quarter of right pizza)
        sector_quarter_1 = Sector(radius=2, angle=PI/2, start_angle=0, color="#4ECDC4", fill_opacity=0.7, stroke_width=0)
        obj_sector_quarter_1 = LayoutObject(sector_quarter_1, "sector_quarter_1")
        layout.add(obj_sector_quarter_1)
        layout.add_constraint(obj_sector_quarter_1.center_x == obj_pizza_right.center_x)
        layout.add_constraint(obj_sector_quarter_1.center_y == obj_pizza_right.center_y)
        self.objects["sector_quarter_1"] = sector_quarter_1
        
        # Sector Quarter 2 (Bottom left quarter of right pizza)
        sector_quarter_2 = Sector(radius=2, angle=PI/2, start_angle=PI, color="#4ECDC4", fill_opacity=0.7, stroke_width=0)
        obj_sector_quarter_2 = LayoutObject(sector_quarter_2, "sector_quarter_2")
        layout.add(obj_sector_quarter_2)
        layout.add_constraint(obj_sector_quarter_2.center_x == obj_pizza_right.center_x)
        layout.add_constraint(obj_sector_quarter_2.center_y == obj_pizza_right.center_y)
        self.objects["sector_quarter_2"] = sector_quarter_2
        
        # Label Left (1/2)
        label_left = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        obj_label_left = LayoutObject(label_left, "label_left")
        layout.add(obj_label_left)
        # Position below left pizza
        layout.align_to(obj_label_left, obj_pizza_left, "BOTTOM", buff=0.8)
        layout.align_to(obj_label_left, obj_pizza_left, "CENTER_X")
        self.objects["label_left"] = label_left
        
        # Label Right (2/4)
        label_right = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        obj_label_right = LayoutObject(label_right, "label_right")
        layout.add(obj_label_right)
        # Position below right pizza
        layout.align_to(obj_label_right, obj_pizza_right, "BOTTOM", buff=0.8)
        layout.align_to(obj_label_right, obj_pizza_right, "CENTER_X")
        self.objects["label_right"] = label_right
        
        # Equality Sign (=)
        eq_sign = MathTex("=", color=YELLOW, font_size=48)
        obj_eq_sign = LayoutObject(eq_sign, "eq_sign")
        layout.add(obj_eq_sign)
        # Position at center, slightly up from origin (morph_anchor)
        layout.add_constraint(obj_eq_sign.center_x == 0)
        layout.add_constraint(obj_eq_sign.center_y == 0.5)
        self.objects["eq_sign"] = eq_sign
        
        # Explanation Text
        explanation_text = Text("The shaded area is the same: one half equals two quarters.", color=GRAY_B, font_size=28)
        obj_explanation_text = LayoutObject(explanation_text, "explanation_text")
        layout.add(obj_explanation_text)
        layout.add_to_zone(obj_explanation_text, "FOOTER")
        layout.add_constraint(obj_explanation_text.center_x == 0)
        self.objects["explanation_text"] = explanation_text
        
        # Solve all constraints
        layout.solve()
        
        # ========== PHASE 2: Animation Sequence ==========
        # Step 1: Let's start with two identical pizzas.
        step = {
            "step": 1,
            "duration": 3.072,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Create(self.objects["pizza_left"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))
        
        # Step 2: We divide the first pizza into 2 equal halves.
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "div_line_left", "color": "YELLOW"},
            "duration": 3.72,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Indicate(self.objects["div_line_left"], color=YELLOW))
        self.play(Create(self.objects["div_line_left"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 3: And we shade one of these halves to represent the fraction one-half.
        step = {
            "step": 3,
            "signal_action": {"type": "Indicate", "target": "sector_half", "color": "YELLOW"},
            "duration": 4.128,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Indicate(self.objects["sector_half"], color=YELLOW))
        self.play(Create(self.objects["sector_half"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 4: Now, let's look at the second pizza. We divide it into 4 equal quarters.
        step = {
            "step": 4,
            "duration": 5.904,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Create(self.objects["pizza_right"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))
        
        # Step 5: We shade two of these quarters, which are opposite each other, to represent two-quarters.
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "sector_quarter_1", "color": "YELLOW"},
            "duration": 5.616,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Indicate(self.objects["sector_quarter_1"], color=YELLOW))
        self.play(Create(self.objects["div_lines_right"]))
        self.play(Create(self.objects["sector_quarter_1"]), Create(self.objects["sector_quarter_2"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 3.0)))
        
        # Step 6: We label them: one-half, and two-quarters.
        step = {
            "step": 6,
            "duration": 3.672,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Write(self.objects["label_left"]), Write(self.objects["label_right"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))
        
        # Step 7: Now, the key insight: these two shaded areas are actually equal. Let's see why.
        step = {
            "step": 7,
            "signal_action": {"type": "Circumscribe", "target": "sector_half", "color": "YELLOW"},
            "duration": 6.792,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Circumscribe(self.objects["sector_half"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["explanation_text"]))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 8: Watch what happens if we take the shaded half and cut it right down the middle.
        step = {
            "step": 8,
            "signal_action": {"type": "Indicate", "target": "sector_half", "color": "RED"},
            "duration": 4.584,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Indicate(self.objects["sector_half"], color=RED))
        # Create two temporary sectors that match the right pizza's quarters but at the left pizza's position
        # These will be the target of the transformation.
        sector_half_copy = self.objects["sector_half"].copy()
        # We'll transform into a VGroup of two quarters (matching the right pizza's shaded quarters in position)
        # For simplicity, we'll transform into the existing sector_quarter_1 and sector_quarter_2 but move them to the center for the morph.
        # Create a VGroup of two sectors at the morph anchor (center) for the transformation.
        target_sector1 = Sector(radius=2, angle=PI/2, start_angle=0, color="#4ECDC4", fill_opacity=0.7, stroke_width=0)
        target_sector2 = Sector(radius=2, angle=PI/2, start_angle=PI, color="#4ECDC4", fill_opacity=0.7, stroke_width=0)
        target_group = VGroup(target_sector1, target_sector2)
        target_group.move_to(self.objects["eq_sign"].get_center())
        self.play(Transform(self.objects["sector_half"], target_group))
        self.wait(max(0.1, max(0.1, step["duration"] - 2.0)))
        
        # Step 9: We get exactly the two shaded quarters from the second pizza. Therefore, one-half must equal two-quarters.
        step = {
            "step": 9,
            "signal_action": {"type": "Indicate", "target": "eq_sign", "color": "YELLOW"},
            "duration": 7.56,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Indicate(self.objects["eq_sign"], color=YELLOW))
        self.play(Write(self.objects["eq_sign"]))
        # Create new labels for the final equality: "1/2 = 2/4" horizontally at the center.
        label_left_new = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_right_new = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        # Position left of equals sign
        label_left_new.next_to(self.objects["eq_sign"], LEFT, buff=0.5)
        # Position right of equals sign
        label_right_new.next_to(self.objects["eq_sign"], RIGHT, buff=0.5)
        self.play(
            ReplacementTransform(self.objects["label_left"], label_left_new),
            ReplacementTransform(self.objects["label_right"], label_right_new)
        )
        # Update registry
        self.objects["label_left"] = label_left_new
        self.objects["label_right"] = label_right_new
        self.wait(max(0.1, max(0.1, step["duration"] - 3.0)))
        
        # Step 10: The shaded area is identical, proving the equivalence of the fractions.
        step = {
            "step": 10,
            "signal_action": {"type": "Circumscribe", "target": ["sector_quarter_1", "sector_quarter_2"], "color": "GREEN"},
            "duration": 4.872,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_09.mp3"
        }
        self.add_sound(step["audio_path"])
        self.play(Circumscribe(VGroup(self.objects["sector_quarter_1"], self.objects["sector_quarter_2"]), color=GREEN, run_time=1))
        self.wait(max(0.1, max(0.1, step["duration"] - 1.0)))