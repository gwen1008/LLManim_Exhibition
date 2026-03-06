'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize multiplication as repeated addition using three groups of four stars merging into a 3x4 grid.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for star groups and final grid
#    - Footer Region: [Bottom y=-3.5] for step labels and final equation
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for each cluster. Position groups horizontally with spacing, then shift left to center. Final grid at ORIGIN.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/multiplication_as_repeated_addition/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create first blue group (center), indicate it.
#    - Step 2: Create second green group (right), indicate, shift both left to center.
#    - Step 3: Create third red group (right), indicate, shift all left to center.
#    - Step 4: Circumscribe first group, transform three groups into final 3x4 grid.
#    - Step 5: Indicate and write final equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/The_animation_should_917e8a90ce/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create title
        title = Text("Multiplication as Repeated Addition", color=WHITE, font_size=36)
        title.move_to(3.5 * UP)
        self.objects["title"] = title
        
        # Create star template (not added to scene yet)
        star_template = Star(outer_radius=0.3, inner_radius=0.15, n=5, 
                             color=YELLOW, fill_opacity=0.8, stroke_width=2)
        self.objects["star_template"] = star_template
        
        # Create group1: 4 stars in 2x2 grid
        stars1 = VGroup(*[star_template.copy().set_color(BLUE_C) for _ in range(4)])
        stars1.arrange_in_grid(rows=2, cols=2, buff=0.4)
        stars1.move_to(ORIGIN)
        self.objects["group1"] = stars1
        
        # Create group2: 4 stars in 2x2 grid
        stars2 = VGroup(*[star_template.copy().set_color(GREEN_C) for _ in range(4)])
        stars2.arrange_in_grid(rows=2, cols=2, buff=0.4)
        stars2.move_to(ORIGIN + 3.0 * RIGHT)
        self.objects["group2"] = stars2
        
        # Create group3: 4 stars in 2x2 grid
        stars3 = VGroup(*[star_template.copy().set_color(RED_C) for _ in range(4)])
        stars3.arrange_in_grid(rows=2, cols=2, buff=0.4)
        stars3.move_to(ORIGIN + 6.0 * RIGHT)
        self.objects["group3"] = stars3
        
        # Create final_grid: 12 stars in 3x4 grid
        stars_final = VGroup(*[star_template.copy().set_color(YELLOW) for _ in range(12)])
        stars_final.arrange_in_grid(rows=3, cols=4, buff=0.5)
        stars_final.move_to(ORIGIN)
        self.objects["final_grid"] = stars_final
        
        # Create labels
        label_step1 = Text("1 group of 4", color=BLUE_C, font_size=30)
        label_step1.move_to(3.5 * DOWN)
        self.objects["label_step1"] = label_step1
        
        label_step2 = Text("1 group of 4  +  1 group of 4", color=WHITE, font_size=30)
        label_step2.move_to(3.5 * DOWN)
        self.objects["label_step2"] = label_step2
        
        label_step3 = Text("1 group of 4  +  1 group of 4  +  1 group of 4", color=WHITE, font_size=28)
        label_step3.move_to(3.5 * DOWN)
        self.objects["label_step3"] = label_step3
        
        equation = MathTex(r"3 \times 4 = 12", color=GREEN, font_size=40)
        equation.move_to(3.5 * DOWN)
        self.objects["equation"] = equation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/multiplication_as_repeated_addition/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Indicate(self.objects["group1"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["group1"]), run_time=1.5)
        self.play(Write(self.objects["label_step1"]), run_time=1.0)
        remaining_1 = max(0.1, 3.0 - (1.0 + 1 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/multiplication_as_repeated_addition/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["group2"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["group2"]), run_time=1.5)
        self.play(
            self.objects["group1"].animate.shift(1.5 * LEFT),
            self.objects["group2"].animate.shift(1.5 * LEFT),
            run_time=1.0
        )
        self.play(
            ReplacementTransform(self.objects["label_step1"], self.objects["label_step2"]),
            run_time=1.0
        )
        remaining_2 = max(0.1, 3.5 - (1 + 1.5 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/multiplication_as_repeated_addition/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["group3"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["group3"]), run_time=1.5)
        self.play(
            self.objects["group1"].animate.shift(1.5 * LEFT),
            self.objects["group2"].animate.shift(1.5 * LEFT),
            self.objects["group3"].animate.shift(3.0 * LEFT),
            run_time=1.0
        )
        self.play(
            ReplacementTransform(self.objects["label_step2"], self.objects["label_step3"]),
            run_time=1.0
        )
        remaining_3 = max(0.1, 4.0 - (1 + 1.5 + 1.0 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/multiplication_as_repeated_addition/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["group1"], color=BLUE, run_time=1))
        # Transform three groups into final grid
        self.play(
            Transform(self.objects["group1"], self.objects["final_grid"][0:4].set_color(BLUE_C)),
            Transform(self.objects["group2"], self.objects["final_grid"][4:8].set_color(GREEN_C)),
            Transform(self.objects["group3"], self.objects["final_grid"][8:12].set_color(RED_C)),
            run_time=2.0
        )
        # Fade out the transformed groups and show the unified final grid
        self.remove(self.objects["group1"], self.objects["group2"], self.objects["group3"])
        self.add(self.objects["final_grid"])
        self.play(FadeOut(self.objects["label_step3"]), run_time=0.5)
        remaining_4 = max(0.1, 4.0 - (1 + 2.0 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/multiplication_as_repeated_addition/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["equation"], color=GREEN, run_time=1))
        self.play(Write(self.objects["equation"]), run_time=1.5)
        remaining_5 = max(0.1, 3.5 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_5))