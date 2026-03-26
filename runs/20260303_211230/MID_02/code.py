'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the ratio 2:5 using a tape diagram divided into 7 equal parts, showing milk vs water mixture.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for ratio statement
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for sections and labels to keep them together. Position labels above tape with sufficient buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/topic_folder/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw tape outline.
#    - Step 2: Draw 6 division lines sequentially.
#    - Step 3: Highlight first two sections, add milk label and fill.
#    - Step 4: Highlight remaining five sections, add water label and fill.
#    - Step 5: Circumscribe labels, write ratio statement.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_tape_diagra_f73a3aafca/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        title_anchor = 3.5 * UP
        tape_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Tape Diagram: Milk and Water Mixture", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Tape outline
        tape_outline = Rectangle(width=10.5, height=1.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(tape_anchor)
        self.objects["tape_outline"] = tape_outline
        
        # Division lines
        div_line_1 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_1.move_to(tape_anchor + LEFT*4.5)
        self.objects["div_line_1"] = div_line_1
        
        div_line_2 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_2.move_to(tape_anchor + LEFT*3.0)
        self.objects["div_line_2"] = div_line_2
        
        div_line_3 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_3.move_to(tape_anchor + LEFT*1.5)
        self.objects["div_line_3"] = div_line_3
        
        div_line_4 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_4.move_to(tape_anchor)
        self.objects["div_line_4"] = div_line_4
        
        div_line_5 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_5.move_to(tape_anchor + RIGHT*1.5)
        self.objects["div_line_5"] = div_line_5
        
        div_line_6 = Line(UP*0.5, DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_6.move_to(tape_anchor + RIGHT*3.0)
        self.objects["div_line_6"] = div_line_6
        
        # Milk label
        milk_label = Text("Milk (2 parts)", color=BLUE_C, font_size=28)
        milk_label.move_to(tape_anchor + LEFT*3.75 + UP*1.2)
        self.objects["milk_label"] = milk_label
        
        # Water label
        water_label = Text("Water (5 parts)", color=GRAY_C, font_size=28)
        water_label.move_to(tape_anchor + RIGHT*2.25 + UP*1.2)
        self.objects["water_label"] = water_label
        
        # Ratio text
        ratio_tex = MathTex(r"\mathrm{Milk} : \mathrm{Water} = 2 : 5", color=YELLOW, font_size=36)
        ratio_tex.move_to(explanation_anchor)
        self.objects["ratio_tex"] = ratio_tex
        
        # Create section rectangles for filling (not in original objects, but needed for steps 3 & 4)
        section_width = 1.5
        section_height = 1.0
        section_rects = []
        for i in range(7):
            rect = Rectangle(width=section_width, height=section_height, fill_opacity=0.0, stroke_width=0)
            rect.move_to(tape_anchor + LEFT*(4.5 - i*1.5))
            section_rects.append(rect)
        self.objects["section_rects"] = VGroup(*section_rects)
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/topic_folder/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["tape_outline"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/topic_folder/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Create division lines sequentially
        div_lines = [
            self.objects["div_line_1"],
            self.objects["div_line_2"],
            self.objects["div_line_3"],
            self.objects["div_line_4"],
            self.objects["div_line_5"],
            self.objects["div_line_6"]
        ]
        anim_time_per_line = 0.5
        for line in div_lines:
            self.play(Create(line), run_time=anim_time_per_line)
        
        total_anim_time_2 = len(div_lines) * anim_time_per_line
        remaining_2 = max(0.1, 4.0 - total_anim_time_2 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/topic_folder/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate first two division lines
        self.play(
            Indicate(self.objects["div_line_1"], color=BLUE, run_time=0.5),
            Indicate(self.objects["div_line_2"], color=BLUE, run_time=0.5)
        )
        
        # Visual action: Add milk label and fill first two sections
        milk_fill_animations = []
        for i in range(2):
            rect_copy = self.objects["section_rects"][i].copy()
            rect_copy.set_fill(color=BLUE_C, opacity=0.5)
            rect_copy.set_stroke(width=0)
            milk_fill_animations.append(FadeIn(rect_copy))
        
        self.play(
            Write(self.objects["milk_label"]),
            *milk_fill_animations,
            run_time=1.5
        )
        
        remaining_3 = max(0.1, 3.0 - (0.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/topic_folder/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate remaining division lines and right edge
        indicate_targets = [
            self.objects["div_line_3"],
            self.objects["div_line_4"],
            self.objects["div_line_5"],
            self.objects["div_line_6"],
            self.objects["tape_outline"].get_right()
        ]
        indicate_anims = [Indicate(target, color=GRAY, run_time=0.5) for target in indicate_targets if isinstance(target, Mobject)]
        # Add a separate indication for the right edge point
        right_edge_dot = Dot(self.objects["tape_outline"].get_right(), radius=0.1, color=GRAY)
        right_edge_dot.set_opacity(0)
        self.add(right_edge_dot)
        indicate_anims.append(Indicate(right_edge_dot, color=GRAY, run_time=0.5))
        self.play(*indicate_anims)
        
        # Visual action: Add water label and fill remaining five sections
        water_fill_animations = []
        for i in range(2, 7):
            rect_copy = self.objects["section_rects"][i].copy()
            rect_copy.set_fill(color=GRAY_C, opacity=0.5)
            rect_copy.set_stroke(width=0)
            water_fill_animations.append(FadeIn(rect_copy))
        
        self.play(
            Write(self.objects["water_label"]),
            *water_fill_animations,
            run_time=1.5
        )
        
        remaining_4 = max(0.1, 3.0 - (0.5 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/topic_folder/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe labels
        self.play(
            Circumscribe(self.objects["milk_label"], color=YELLOW, run_time=1),
            Circumscribe(self.objects["water_label"], color=YELLOW, run_time=1)
        )
        
        # Visual action: Write ratio statement
        self.play(Write(self.objects["ratio_tex"]), run_time=1.5)
        
        remaining_5 = max(0.1, 4.0 - (1.0 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))