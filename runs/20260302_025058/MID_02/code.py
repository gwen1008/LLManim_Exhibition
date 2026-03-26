from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        tape_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # title
        title = Text("Tape Diagram: Milk and Water Mixture", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # tape_outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(tape_anchor)
        self.objects["tape_outline"] = tape_outline
        
        # division lines (positions relative to tape_anchor)
        div_line_1 = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_1.move_to(tape_anchor + LEFT*2.5)
        self.objects["div_line_1"] = div_line_1
        
        div_line_2 = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_2.move_to(tape_anchor + LEFT*1.5)
        self.objects["div_line_2"] = div_line_2
        
        div_line_3 = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_3.move_to(tape_anchor + LEFT*0.5)
        self.objects["div_line_3"] = div_line_3
        
        div_line_4 = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_4.move_to(tape_anchor + RIGHT*0.5)
        self.objects["div_line_4"] = div_line_4
        
        div_line_5 = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_5.move_to(tape_anchor + RIGHT*1.5)
        self.objects["div_line_5"] = div_line_5
        
        div_line_6 = Line(start=UP*0.5, end=DOWN*0.5, color=WHITE, stroke_width=2)
        div_line_6.move_to(tape_anchor + RIGHT*2.5)
        self.objects["div_line_6"] = div_line_6
        
        # milk_label
        milk_label = Text("Milk", color="#ADD8E6", font_size=28)
        milk_label.next_to(tape_outline, UP, buff=0.5)
        milk_label.align_to(tape_anchor + LEFT*2.0, LEFT)
        self.objects["milk_label"] = milk_label
        
        # water_label
        water_label = Text("Water", color="#87CEEB", font_size=28)
        water_label.next_to(tape_outline, UP, buff=0.5)
        water_label.align_to(tape_anchor + RIGHT*1.0, RIGHT)
        self.objects["water_label"] = water_label
        
        # milk_fraction
        milk_fraction = MathTex(r"\frac{2}{7}", color="#ADD8E6")
        milk_fraction.next_to(tape_outline, DOWN, buff=0.3)
        milk_fraction.align_to(tape_anchor + LEFT*2.0, LEFT)
        self.objects["milk_fraction"] = milk_fraction
        
        # water_fraction
        water_fraction = MathTex(r"\frac{5}{7}", color="#87CEEB")
        water_fraction.next_to(tape_outline, DOWN, buff=0.3)
        water_fraction.align_to(tape_anchor + RIGHT*1.0, RIGHT)
        self.objects["water_fraction"] = water_fraction
        
        # ratio_summary
        ratio_summary = MathTex(r"\mathrm{Ratio of Milk to Water} = 2 : 5", color=YELLOW, font_size=32)
        ratio_summary.move_to(footer_anchor)
        self.objects["ratio_summary"] = ratio_summary
        
        # Create milk sections (rectangles for fill)
        milk_section1 = Rectangle(width=1.0, height=1.0, fill_color="#ADD8E6", fill_opacity=0.0, stroke_opacity=0.0)
        milk_section1.move_to(tape_anchor + LEFT*3.0)
        self.objects["milk_section1"] = milk_section1
        
        milk_section2 = Rectangle(width=1.0, height=1.0, fill_color="#ADD8E6", fill_opacity=0.0, stroke_opacity=0.0)
        milk_section2.move_to(tape_anchor + LEFT*2.0)
        self.objects["milk_section2"] = milk_section2
        
        # Create water sections (rectangles for fill)
        water_section3 = Rectangle(width=1.0, height=1.0, fill_color="#87CEEB", fill_opacity=0.0, stroke_opacity=0.0)
        water_section3.move_to(tape_anchor + LEFT*1.0)
        self.objects["water_section3"] = water_section3
        
        water_section4 = Rectangle(width=1.0, height=1.0, fill_color="#87CEEB", fill_opacity=0.0, stroke_opacity=0.0)
        water_section4.move_to(tape_anchor)
        self.objects["water_section4"] = water_section4
        
        water_section5 = Rectangle(width=1.0, height=1.0, fill_color="#87CEEB", fill_opacity=0.0, stroke_opacity=0.0)
        water_section5.move_to(tape_anchor + RIGHT*1.0)
        self.objects["water_section5"] = water_section5
        
        water_section6 = Rectangle(width=1.0, height=1.0, fill_color="#87CEEB", fill_opacity=0.0, stroke_opacity=0.0)
        water_section6.move_to(tape_anchor + RIGHT*2.0)
        self.objects["water_section6"] = water_section6
        
        water_section7 = Rectangle(width=1.0, height=1.0, fill_color="#87CEEB", fill_opacity=0.0, stroke_opacity=0.0)
        water_section7.move_to(tape_anchor + RIGHT*3.0)
        self.objects["water_section7"] = water_section7
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_a_tape_diagra_2abe4d0442/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["tape_outline"]), run_time=1.5)
        remaining_1 = max(0.1, 5.544 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_a_tape_diagra_2abe4d0442/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(
            LaggedStart(
                Create(self.objects["div_line_1"]),
                Create(self.objects["div_line_2"]),
                Create(self.objects["div_line_3"]),
                Create(self.objects["div_line_4"]),
                Create(self.objects["div_line_5"]),
                Create(self.objects["div_line_6"]),
                lag_ratio=0.2
            ),
            run_time=2.5
        )
        remaining_2 = max(0.1, 3.864 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_a_tape_diagra_2abe4d0442/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Indicate div_line_2
        self.play(Indicate(self.objects["div_line_2"], color=YELLOW, run_time=1))
        
        # Visual action: Fill milk sections, write milk label and fraction
        self.play(
            AnimationGroup(
                self.objects["milk_section1"].animate.set_fill(opacity=0.3),
                self.objects["milk_section2"].animate.set_fill(opacity=0.3),
                Write(self.objects["milk_label"]),
                Write(self.objects["milk_fraction"]),
                lag_ratio=0.0
            ),
            run_time=2.0
        )
        remaining_3 = max(0.1, 5.472 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_a_tape_diagra_2abe4d0442/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Signal action: Indicate div_line_6
        self.play(Indicate(self.objects["div_line_6"], color=YELLOW, run_time=1))
        
        # Visual action: Fill water sections, write water label and fraction
        self.play(
            AnimationGroup(
                self.objects["water_section3"].animate.set_fill(opacity=0.3),
                self.objects["water_section4"].animate.set_fill(opacity=0.3),
                self.objects["water_section5"].animate.set_fill(opacity=0.3),
                self.objects["water_section6"].animate.set_fill(opacity=0.3),
                self.objects["water_section7"].animate.set_fill(opacity=0.3),
                Write(self.objects["water_label"]),
                Write(self.objects["water_fraction"]),
                lag_ratio=0.0
            ),
            run_time=2.5
        )
        remaining_4 = max(0.1, 5.76 - 1.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_a_tape_diagra_2abe4d0442/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe ratio_summary
        self.play(Circumscribe(self.objects["ratio_summary"], color=YELLOW, run_time=1))
        
        # Visual action: Write ratio_summary
        self.play(Write(self.objects["ratio_summary"]), run_time=1.5)
        remaining_5 = max(0.1, 9.528 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))