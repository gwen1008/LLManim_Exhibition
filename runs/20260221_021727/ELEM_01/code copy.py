'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visual demonstration of fraction equivalence 1/2 = 2/4 by subdividing a whole (pizza) into halves and then quarters, showing the same shaded area.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for construction and final comparison
#    - Footer Region: [Bottom y=-3.5] for equivalence statement
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each pizza (circle + sectors + label) for easy movement and to prevent drift.
#    - During construction, objects overlap at center. During comparison, move VGroups left/right.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create blue pizza circle.
#    - Step 2: Shade half (yellow), create unshaded half (blue). Indicate shaded half.
#    - Step 3: Create orange pizza circle overlay. Write 1/2 label. Indicate blue pizza.
#    - Step 4: Subdivide: fade out halves, fade in quarters. Write 2/4 label. Circumscribe original shaded half.
#    - Step 5: Move pizzas side-by-side.
#    - Step 6: Show final equivalence statement. Circumscribe shaded half with green.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors (from layout_plan)
        title_anchor = 3.5 * UP
        pizza1_anchor = 3 * LEFT
        pizza2_anchor = 3 * RIGHT
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Pizza 1 (Blue) - Left
        pizza1_circle = Circle(radius=2.0, color="#1E90FF", stroke_width=4, fill_opacity=0.0)
        pizza1_circle.shift(pizza1_anchor)
        self.objects["pizza1_circle"] = pizza1_circle

        pizza1_half_shaded = Sector(radius=2.0, angle=PI, start_angle=0, color=YELLOW, fill_opacity=0.7, stroke_width=0)
        pizza1_half_shaded.shift(pizza1_anchor)
        self.objects["pizza1_half_shaded"] = pizza1_half_shaded

        pizza1_half_unshaded = Sector(radius=2.0, angle=PI, start_angle=PI, color="#1E90FF", fill_opacity=0.3, stroke_width=0)
        pizza1_half_unshaded.shift(pizza1_anchor)
        self.objects["pizza1_half_unshaded"] = pizza1_half_unshaded

        label_1half = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_1half.next_to(pizza1_circle, DOWN, buff=0.8)
        self.objects["label_1half"] = label_1half

        # Pizza 2 (Orange) - Right
        pizza2_circle = Circle(radius=2.0, color="#FF8C00", stroke_width=4, fill_opacity=0.0)
        pizza2_circle.shift(pizza2_anchor)
        self.objects["pizza2_circle"] = pizza2_circle

        # Quarter sectors for Pizza 2 (initially invisible)
        pizza2_quarter_shaded_1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color=YELLOW, fill_opacity=0.0, stroke_width=0)
        pizza2_quarter_shaded_1.shift(pizza2_anchor)
        self.objects["pizza2_quarter_shaded_1"] = pizza2_quarter_shaded_1

        pizza2_quarter_shaded_2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color=YELLOW, fill_opacity=0.0, stroke_width=0)
        pizza2_quarter_shaded_2.shift(pizza2_anchor)
        self.objects["pizza2_quarter_shaded_2"] = pizza2_quarter_shaded_2

        pizza2_quarter_unshaded_1 = Sector(radius=2.0, angle=PI/2, start_angle=PI, color="#FF8C00", fill_opacity=0.0, stroke_width=0)
        pizza2_quarter_unshaded_1.shift(pizza2_anchor)
        self.objects["pizza2_quarter_unshaded_1"] = pizza2_quarter_unshaded_1

        pizza2_quarter_unshaded_2 = Sector(radius=2.0, angle=PI/2, start_angle=3*PI/2, color="#FF8C00", fill_opacity=0.0, stroke_width=0)
        pizza2_quarter_unshaded_2.shift(pizza2_anchor)
        self.objects["pizza2_quarter_unshaded_2"] = pizza2_quarter_unshaded_2

        label_2quarters = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_2quarters.next_to(pizza2_circle, DOWN, buff=0.8)
        self.objects["label_2quarters"] = label_2quarters

        equivalence_statement = MathTex(r"\frac{1}{2} = \frac{2}{4}", color=GREEN, font_size=42)
        equivalence_statement.move_to(explanation_anchor)
        self.objects["equivalence_statement"] = equivalence_statement

        # Create VGroups for easy movement (as per hints)
        pizza1_group = VGroup(pizza1_circle, pizza1_half_shaded, pizza1_half_unshaded, label_1half)
        pizza2_group = VGroup(pizza2_circle, pizza2_quarter_shaded_1, pizza2_quarter_shaded_2,
                              pizza2_quarter_unshaded_1, pizza2_quarter_unshaded_2, label_2quarters)
        self.objects["pizza1_group"] = pizza1_group
        self.objects["pizza2_group"] = pizza2_group

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1
        step = {
            "step": 1,
            "duration": 5.52,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(pizza1_circle), Create(pizza2_circle))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Indicate", "target": "pizza1_half_shaded", "color": "YELLOW"},
            "duration": 3.936,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(FadeIn(pizza1_half_shaded))
        self.play(FadeIn(pizza1_half_unshaded))
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
            self.play(Indicate(target_obj, color=color))
        animation_time = 2.0 + 1.0  # FadeIn times + Indicate
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Indicate", "target": "pizza1_circle", "color": "ORANGE"},
            "duration": 7.44,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Note: pizza2_circle is already created in Step 1 now.
        self.play(Write(label_1half))
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = ORANGE if signal.get("color") == "ORANGE" else eval(signal.get("color"))
            self.play(Indicate(target_obj, color=color))
        animation_time = 1.0 + 1.0 + 1.0  # Create + Write + Indicate
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Circumscribe", "target": "pizza1_half_shaded", "color": "YELLOW"},
            "duration": 11.328,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            target_obj = self.objects[signal["target"]]
            color = YELLOW if signal.get("color") == "YELLOW" else eval(signal.get("color"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        # Subdivision animation: fade out halves, fade in quarters
        # Since pizza 2 (Orange) is explicitly separate, it should NOT affect pizza 1 (Blue).
        # We will directly fade in the pieces on the Right pizza.
        self.add(pizza2_quarter_shaded_1, pizza2_quarter_shaded_2, pizza2_quarter_unshaded_1, pizza2_quarter_unshaded_2)
        self.play(
            pizza2_quarter_shaded_1.animate.set_fill(opacity=0.7),
            pizza2_quarter_shaded_2.animate.set_fill(opacity=0.7),
            pizza2_quarter_unshaded_1.animate.set_fill(opacity=0.3),
            pizza2_quarter_unshaded_2.animate.set_fill(opacity=0.3),
            run_time=2.0
        )
        self.play(Write(label_2quarters))
        animation_time = 1.0 + 2.0 + 1.0  # Circumscribe + subdivision + Write
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5 - (Modified because layout changed, already moved. Skip move animation, just hold)
        step = {
            "step": 5,
            "duration": 8.904,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        
        animation_time = 0.0
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "signal_action": {"type": "Circumscribe", "target": "pizza1_half_shaded", "color": "GREEN"},
            "duration": 7.344,
            "audio_path": "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        }
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            # Target is specified as pizza1_half_shaded, but we should highlight the equivalent quarters in pizza2 since pizza1_half_shaded is invisible
            target_obj = VGroup(self.objects["pizza2_quarter_shaded_1"], self.objects["pizza2_quarter_shaded_2"])
            color = GREEN if signal.get("color") == "GREEN" else eval(signal.get("color"))
            self.play(Circumscribe(target_obj, color=color, run_time=1))
        self.play(Write(equivalence_statement))
        animation_time = 1.0 + 1.0  # Circumscribe + Write
        remaining = max(0.1, step["duration"] - animation_time + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 2))