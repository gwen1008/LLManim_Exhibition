'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as combining equal groups. Three groups of four stars combine into a 3x4 array, showing 3 × 4 = 12.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Groups and Multiplication"
#    - Main Content: [Center y=0] for star groups and final array.
#    - Footer Region: [Bottom y=-3.5] for equation.
# 3. Anti-Overlap Check:
#    - Strategy: Initial groups placed in a triangle around center (LEFT*3+UP*1, RIGHT*3+UP*1, DOWN*2). Final array at center. Equation at bottom. No overlap.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? Yes, for each step.
# 5. Animation Flow:
#    - Step 1: Create first blue star group.
#    - Step 2: Indicate blue group, then create green and red groups.
#    - Step 3: Indicate red group, then transform all three groups into a central yellow 3x4 array.
#    - Step 4: Circumscribe final array, write "3" below.
#    - Step 5: Indicate final array, morph "3" into "3 × 4 = 12".
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create Objects from layout_plan.objects
        # Title
        title = Text("Groups and Multiplication", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Helper function to create a 2x2 grid of stars
        def create_star_grid(n_stars=4, star_radius=0.4, grid_buff=0.2, color=WHITE):
            stars = VGroup()
            for i in range(2):
                for j in range(2):
                    star = Star(n=5, outer_radius=star_radius, color=color, fill_opacity=0.8, stroke_width=2)
                    star.move_to([j * (star_radius*2 + grid_buff), -i * (star_radius*2 + grid_buff), 0])
                    stars.add(star)
            return stars

        # Group 1 (Blue)
        group1 = create_star_grid(star_radius=0.4, grid_buff=0.2, color="#1E90FF")
        group1.move_to(content_center + LEFT*3 + UP*1)
        self.objects["group1"] = group1

        # Group 2 (Green)
        group2 = create_star_grid(star_radius=0.4, grid_buff=0.2, color="#32CD32")
        group2.move_to(content_center + RIGHT*3 + UP*1)
        self.objects["group2"] = group2

        # Group 3 (Red)
        group3 = create_star_grid(star_radius=0.4, grid_buff=0.2, color="#FF6347")
        group3.move_to(content_center + DOWN*2)
        self.objects["group3"] = group3

        # Final 3x4 star array (Yellow)
        final_star_array = VGroup()
        star_radius_final = 0.3
        grid_buff_final = 0.15
        for row in range(3):
            row_group = VGroup()
            for col in range(4):
                star = Star(n=5, outer_radius=star_radius_final, color=YELLOW, fill_opacity=0.8, stroke_width=2)
                star.move_to([col * (star_radius_final*2 + grid_buff_final), -row * (star_radius_final*2 + grid_buff_final), 0])
                row_group.add(star)
            final_star_array.add(row_group)
        final_star_array.move_to(content_center)
        self.objects["final_star_array"] = final_star_array

        # Equations
        eq_3 = MathTex("3", color=WHITE, font_size=48)
        eq_3.move_to(explanation_anchor + LEFT*2)
        self.objects["eq_3"] = eq_3

        eq_3x4 = MathTex("3 \\times 4", color=WHITE, font_size=48)
        eq_3x4.move_to(explanation_anchor)
        self.objects["eq_3x4"] = eq_3x4  # Not directly animated but used as intermediate reference

        eq_3x4_12 = MathTex("3 \\times 4 = 12", color=WHITE, font_size=48)
        eq_3x4_12.move_to(explanation_anchor)
        self.objects["eq_3x4_12"] = eq_3x4_12

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/The_animation_should_fc8c0205c1/step_00.mp3")  # [auto-injected] duration=2.69s
        _audio_dur_0 = 2.69  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.0)
        self.play(Create(self.objects["group1"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/The_animation_should_fc8c0205c1/step_01.mp3")  # [auto-injected] duration=3.24s
        _audio_dur_1 = 3.24  # [audio-sync] actual TTS duration
        # Step 2
        self.play(Indicate(self.objects["group1"], color="#1E90FF", scale_factor=1.2), run_time=1.0)
        self.play(Create(self.objects["group2"]), run_time=1.0)
        self.play(Create(self.objects["group3"]), run_time=1.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/The_animation_should_fc8c0205c1/step_02.mp3")  # [auto-injected] duration=4.32s
        _audio_dur_2 = 4.32  # [audio-sync] actual TTS duration
        # Step 3
        self.play(Indicate(self.objects["group3"], color="#FF6347", scale_factor=1.2), run_time=1.0)
        self.play(
            Transform(self.objects["group1"], self.objects["final_star_array"]),
            Transform(self.objects["group2"], self.objects["final_star_array"]),
            Transform(self.objects["group3"], self.objects["final_star_array"]),
            run_time=2.0
        )
        # Clean up duplicates - keep only one final array
        self.remove(self.objects["group1"], self.objects["group2"], self.objects["group3"])
        self.add(self.objects["final_star_array"])
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/The_animation_should_fc8c0205c1/step_03.mp3")  # [auto-injected] duration=3.84s
        _audio_dur_3 = 3.84  # [audio-sync] actual TTS duration
        # Step 4
        self.play(Circumscribe(self.objects["final_star_array"], color=YELLOW, run_time=1.0))
        self.play(Write(self.objects["eq_3"]), run_time=1.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/The_animation_should_fc8c0205c1/step_04.mp3")  # [auto-injected] duration=5.02s
        _audio_dur_4 = 5.02  # [audio-sync] actual TTS duration
        # Step 5
        self.play(Indicate(self.objects["final_star_array"], color=YELLOW, scale_factor=1.2), run_time=1.0)
        self.play(TransformMatchingTex(self.objects["eq_3"], self.objects["eq_3x4_12"], path_arc=90), run_time=2.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))