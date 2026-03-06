from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors based on layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        left_pizza_pos = 3.5 * LEFT
        right_pizza_pos = 3.5 * RIGHT
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Fraction Equivalence: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Pizza 1 objects
        pizza1_circle = Circle(radius=2.0, color="#FFD700", fill_opacity=0.2, stroke_width=3)
        pizza1_circle.move_to(content_center)
        self.objects["pizza1_circle"] = pizza1_circle
        
        pizza1_shaded_sector = Sector(radius=2.0, angle=PI, start_angle=0, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        pizza1_shaded_sector.move_to(content_center)
        self.objects["pizza1_shaded_sector"] = pizza1_shaded_sector
        
        pizza1_line = Line(start=[-2,0,0], end=[2,0,0], color=WHITE, stroke_width=2)
        pizza1_line.move_to(content_center)
        self.objects["pizza1_line"] = pizza1_line
        
        label_1over2 = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_1over2.next_to(pizza1_circle, DOWN, buff=0.5)
        self.objects["label_1over2"] = label_1over2
        
        # Pizza 2 objects
        pizza2_circle = Circle(radius=2.0, color="#FFD700", fill_opacity=0.2, stroke_width=3)
        pizza2_circle.move_to(content_center)
        self.objects["pizza2_circle"] = pizza2_circle
        
        pizza2_sector1 = Sector(radius=2.0, angle=PI/2, start_angle=0, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        pizza2_sector1.move_to(content_center)
        self.objects["pizza2_sector1"] = pizza2_sector1
        
        pizza2_sector2 = Sector(radius=2.0, angle=PI/2, start_angle=PI/2, color="#FF6B6B", fill_opacity=0.7, stroke_width=0)
        pizza2_sector2.move_to(content_center)
        self.objects["pizza2_sector2"] = pizza2_sector2
        
        line1 = Line(start=[0,-2,0], end=[0,2,0], color=WHITE, stroke_width=2)
        line2 = Line(start=[-2,0,0], end=[2,0,0], color=WHITE, stroke_width=2)
        pizza2_lines = VGroup(line1, line2)
        pizza2_lines.move_to(content_center)
        self.objects["pizza2_lines"] = pizza2_lines
        
        label_2over4 = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_2over4.next_to(pizza2_circle, DOWN, buff=0.5)
        self.objects["label_2over4"] = label_2over4
        
        # Explanation text
        explanation_text = Text("The shaded area is the same: one half equals two quarters.", color=GRAY_B, font_size=28)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Create VGroups for each pizza to move them together later
        pizza1_group = VGroup(pizza1_circle, pizza1_shaded_sector, pizza1_line, label_1over2)
        pizza2_group = VGroup(pizza2_circle, pizza2_sector1, pizza2_sector2, pizza2_lines, label_2over4)
        self.objects["pizza1_group"] = pizza1_group
        self.objects["pizza2_group"] = pizza2_group
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["pizza1_circle"]), run_time=2.0)
        remaining_1 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["pizza1_line"]), run_time=2.0)
        remaining_2 = max(0.1, 3.84 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza1_shaded_sector"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["pizza1_shaded_sector"]), run_time=1.5)
        remaining_3 = max(0.1, 3.36 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_1over2"]), run_time=1.5)
        remaining_4 = max(0.1, 2.424 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["pizza2_circle"]), run_time=2.0)
        self.play(Create(self.objects["pizza2_lines"]), run_time=1.5)
        remaining_5 = max(0.1, 4.92 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza2_sector1"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["pizza2_sector1"]), run_time=1.2)
        self.play(Create(self.objects["pizza2_sector2"]), run_time=1.2)
        remaining_6 = max(0.1, 4.848 - 3.4 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_2over4"]), run_time=1.5)
        remaining_7 = max(0.1, 2.424 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(
            self.objects["pizza1_group"].animate.move_to(left_pizza_pos),
            self.objects["pizza2_group"].animate.move_to(right_pizza_pos),
            run_time=3.0
        )
        remaining_8 = max(0.1, 4.2 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = "media/audio/用兩個一樣的披薩圖形_示範為什麼_1_2_3f651bb561/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        shaded_group = VGroup(
            self.objects["pizza1_shaded_sector"],
            self.objects["pizza2_sector1"],
            self.objects["pizza2_sector2"]
        )
        self.play(Circumscribe(shaded_group, color=GREEN, run_time=1.5))
        self.play(Write(self.objects["explanation_text"]), run_time=2.0)
        remaining_9 = max(0.1, 6.168 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Final pause
        self.wait(max(0.1, 2))