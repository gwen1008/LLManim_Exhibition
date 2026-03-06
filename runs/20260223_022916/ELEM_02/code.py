from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors based on layout_plan zones
        header_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Create title_equation (initial)
        title_equation = MathTex(r"3 \times 4 = ?", color=YELLOW, font_size=48)
        title_equation.move_to(header_anchor)
        self.objects["title_equation"] = title_equation

        # Create row1_stars (4 blue stars)
        row1_positions = [(-1.2, 1.2, 0), (-0.4, 1.2, 0), (0.4, 1.2, 0), (1.2, 1.2, 0)]
        row1_stars = VGroup(*[Star(outer_radius=0.2, color=BLUE, fill_opacity=1).move_to(pos) for pos in row1_positions])
        self.objects["row1_stars"] = row1_stars

        # Create row2_stars (4 green stars)
        row2_positions = [(-1.2, 0, 0), (-0.4, 0, 0), (0.4, 0, 0), (1.2, 0, 0)]
        row2_stars = VGroup(*[Star(outer_radius=0.2, color=GREEN, fill_opacity=1).move_to(pos) for pos in row2_positions])
        self.objects["row2_stars"] = row2_stars

        # Create row3_stars (4 red stars)
        row3_positions = [(-1.2, -1.2, 0), (-0.4, -1.2, 0), (0.4, -1.2, 0), (1.2, -1.2, 0)]
        row3_stars = VGroup(*[Star(outer_radius=0.2, color=RED, fill_opacity=1).move_to(pos) for pos in row3_positions])
        self.objects["row3_stars"] = row3_stars

        # Create all_stars_cluster (target 4x3 grid)
        # First, collect all stars from rows into a single VGroup
        all_stars_list = []
        for star in row1_stars:
            all_stars_list.append(star.copy())
        for star in row2_stars:
            all_stars_list.append(star.copy())
        for star in row3_stars:
            all_stars_list.append(star.copy())
        all_stars_cluster = VGroup(*all_stars_list)
        # Arrange in a 4x3 grid (4 columns, 3 rows) centered at origin
        all_stars_cluster.arrange_in_grid(rows=3, cols=4, buff=0.5)
        all_stars_cluster.move_to(content_center)
        self.objects["all_stars_cluster"] = all_stars_cluster

        # Create addition_equation
        addition_equation = MathTex(r"4 + 4 + 4 = 12", color=WHITE, font_size=40)
        addition_equation.move_to(footer_anchor)
        self.objects["addition_equation"] = addition_equation

        # Create final_equation
        final_equation = MathTex(r"3 \times 4 = 12", color=GREEN, font_size=48)
        final_equation.move_to(header_anchor)
        self.objects["final_equation"] = final_equation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        self.play(Write(self.objects["title_equation"]), run_time=1.5)
        remaining_1 = max(0.1, 8.352 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["row1_stars"], color=BLUE, run_time=1))
        self.play(Create(self.objects["row1_stars"]), run_time=1.5)
        remaining_2 = max(0.1, 3.024 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["row2_stars"], color=GREEN, run_time=1))
        self.play(Create(self.objects["row2_stars"]), run_time=1.5)
        remaining_3 = max(0.1, 3.12 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["row3_stars"], color=RED, run_time=1))
        self.play(Create(self.objects["row3_stars"]), run_time=1.5)
        remaining_4 = max(0.1, 5.784 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["row1_stars"], color=YELLOW, run_time=1))
        
        # Get target positions from the pre-arranged cluster
        target_positions = []
        for i in range(12):
            target_positions.append(self.objects["all_stars_cluster"][i].get_center())
        
        # Animate each star to its target position
        animations = []
        for i, star in enumerate(self.objects["row1_stars"]):
            animations.append(star.animate.move_to(target_positions[i]))
        for i, star in enumerate(self.objects["row2_stars"]):
            animations.append(star.animate.move_to(target_positions[i+4]))
        for i, star in enumerate(self.objects["row3_stars"]):
            animations.append(star.animate.move_to(target_positions[i+8]))
        
        self.play(*animations, run_time=2.5)
        
        # Create the final cluster by grouping all stars
        final_cluster = VGroup(
            *self.objects["row1_stars"],
            *self.objects["row2_stars"], 
            *self.objects["row3_stars"]
        )
        self.objects["all_stars_cluster"] = final_cluster
        
        remaining_5 = max(0.1, 5.04 - 2.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        self.play(Write(self.objects["addition_equation"]), run_time=1.5)
        remaining_6 = max(0.1, 5.712 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/解釋_3___4_的意義_呈現_3_組各_377b3c2501/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        self.play(Circumscribe(self.objects["all_stars_cluster"], color=WHITE, run_time=1))
        self.play(TransformMatchingTex(self.objects["title_equation"], self.objects["final_equation"]), run_time=2.0)
        remaining_7 = max(0.1, 7.272 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))