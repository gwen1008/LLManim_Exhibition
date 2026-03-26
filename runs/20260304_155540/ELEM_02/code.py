'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing multiplication as repeated addition and as a rectangular array. Show 3 groups of 4 combining into a total of 12.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for the three groups and the final array
#    - Footer Region: [Bottom y=-3.5] for the final equation
# 3. Anti-Overlap Check: Groups are placed horizontally with sufficient spacing. The final array is centered. Labels are placed directly below groups. The final equation is isolated at the bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] I will assign `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step.
# 5. Animation Flow: Title appears -> First group (blue) -> Label -> Second group (green) -> Label -> Third group (red) -> Label -> All groups transform into a 3x4 white grid -> Total count (12) highlighted -> Final equation appears.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        step_label_anchor = 3.0 * UP  # Will be positioned relative to title
        content_center = ORIGIN
        group_left_anchor = 3.5 * LEFT
        group_center_anchor = ORIGIN
        group_right_anchor = 3.5 * RIGHT
        footer_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Visualizing Multiplication: 3 × 4", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Step Label
        step_label = Text("Step 1: First Group", color=YELLOW, font_size=30)
        step_label.next_to(title, DOWN, buff=0.3)
        self.objects["step_label"] = step_label

        # Helper function to create a group of 4 stars in a 2x2 grid
        def create_star_group(color, position):
            stars = VGroup(*[Star(color=color, outer_radius=0.3, inner_radius=0.15) for _ in range(4)])
            stars.arrange_in_grid(rows=2, cols=2, buff=0.5)
            stars.move_to(position)
            for star in stars:
                star.set_fill(color=color, opacity=0.8)
                star.set_stroke(color=color, width=2)
            return stars

        # Group 1 (Blue)
        group1 = create_star_group(color="#1E90FF", position=group_left_anchor)
        self.objects["group1"] = group1
        count_label_1 = MathTex("4", color="#1E90FF", font_size=36)
        count_label_1.next_to(group1, DOWN, buff=0.5)
        self.objects["count_label_1"] = count_label_1

        # Group 2 (Green)
        group2 = create_star_group(color="#32CD32", position=group_center_anchor)
        self.objects["group2"] = group2
        count_label_2 = MathTex("4", color="#32CD32", font_size=36)
        count_label_2.next_to(group2, DOWN, buff=0.5)
        self.objects["count_label_2"] = count_label_2

        # Group 3 (Red)
        group3 = create_star_group(color="#FF6347", position=group_right_anchor)
        self.objects["group3"] = group3
        count_label_3 = MathTex("4", color="#FF6347", font_size=36)
        count_label_3.next_to(group3, DOWN, buff=0.5)
        self.objects["count_label_3"] = count_label_3

        # Total Stars Array (3x4 grid of white stars)
        all_stars = VGroup(*[Star(color=WHITE, outer_radius=0.25, inner_radius=0.125) for _ in range(12)])
        all_stars.arrange_in_grid(rows=3, cols=4, buff=0.4)
        all_stars.move_to(content_center)
        for star in all_stars:
            star.set_fill(color=WHITE, opacity=0.8)
            star.set_stroke(color=WHITE, width=2)
        self.objects["total_stars_array"] = all_stars

        # Total Count Circle and Label
        total_count_circle = Circle(radius=0.4, color=YELLOW, stroke_width=3, fill_opacity=0)
        total_count_circle.next_to(all_stars, RIGHT, buff=1.0)
        self.objects["total_count_circle"] = total_count_circle
        total_count_label = MathTex("12", color=YELLOW, font_size=36)
        total_count_label.move_to(total_count_circle.get_center())
        self.objects["total_count_label"] = total_count_label

        # Final Equation
        final_equation = MathTex(r"3 \times 4 = 12", color=WHITE, font_size=42)
        final_equation.move_to(footer_anchor)
        self.objects["final_equation"] = final_equation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_00.mp3")  # [auto-injected] duration=6.36s
        _audio_dur_0 = 6.36  # [audio-sync] actual TTS duration
        # Step 1
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_01.mp3")  # [auto-injected] duration=3.07s
        _audio_dur_1 = 3.07  # [audio-sync] actual TTS duration
        # Step 2
        # Signal Action: Indicate step_label
        self.play(Indicate(self.objects["step_label"], color=YELLOW, run_time=1))
        # Visual Action: Create group1
        self.play(Create(self.objects["group1"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_02.mp3")  # [auto-injected] duration=3.62s
        _audio_dur_2 = 3.62  # [audio-sync] actual TTS duration
        # Step 3
        # Signal Action: Circumscribe group1
        self.play(Circumscribe(self.objects["group1"], color="#1E90FF", run_time=1))
        # Visual Action: Write count_label_1
        self.play(Write(self.objects["count_label_1"]), run_time=1.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_03.mp3")  # [auto-injected] duration=4.75s
        _audio_dur_3 = 4.75  # [audio-sync] actual TTS duration
        # Step 4
        # Signal Action: ReplacementTransform for step_label
        step_label_2 = Text("Step 2: Second Group", color=YELLOW, font_size=30)
        step_label_2.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_2))
        self.objects["step_label"] = step_label_2
        # Visual Action: Create group2
        self.play(Create(self.objects["group2"]), run_time=2.0)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_04.mp3")  # [auto-injected] duration=2.81s
        _audio_dur_4 = 2.81  # [audio-sync] actual TTS duration
        # Step 5
        # Signal Action: Circumscribe group2
        self.play(Circumscribe(self.objects["group2"], color="#32CD32", run_time=1))
        # Visual Action: Write count_label_2
        self.play(Write(self.objects["count_label_2"]), run_time=1.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_05.mp3")  # [auto-injected] duration=4.58s
        _audio_dur_5 = 4.58  # [audio-sync] actual TTS duration
        # Step 6
        # Signal Action: ReplacementTransform for step_label
        step_label_3 = Text("Step 3: Third Group", color=YELLOW, font_size=30)
        step_label_3.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_3))
        self.objects["step_label"] = step_label_3
        # Visual Action: Create group3
        self.play(Create(self.objects["group3"]), run_time=2.0)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_06.mp3")  # [auto-injected] duration=4.44s
        _audio_dur_6 = 4.44  # [audio-sync] actual TTS duration
        # Step 7
        # Signal Action: Indicate count_label_3
        self.play(Indicate(self.objects["count_label_3"], color="#FF6347", run_time=1))
        # Visual Action: Write count_label_3
        self.play(Write(self.objects["count_label_3"]), run_time=1.5)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_07.mp3")  # [auto-injected] duration=7.03s
        _audio_dur_7 = 7.03  # [audio-sync] actual TTS duration
        # Step 8
        # Signal Action: ReplacementTransform for step_label
        step_label_combine = Text("Combining the Groups", color=YELLOW, font_size=30)
        step_label_combine.next_to(self.objects["title"], DOWN, buff=0.3)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_combine))
        self.objects["step_label"] = step_label_combine
        # Visual Action: Transform groups into the total array, fade out count labels
        self.play(
            Transform(self.objects["group1"], self.objects["total_stars_array"]),
            Transform(self.objects["group2"], self.objects["total_stars_array"]),
            Transform(self.objects["group3"], self.objects["total_stars_array"]),
            FadeOut(self.objects["count_label_1"]),
            FadeOut(self.objects["count_label_2"]),
            FadeOut(self.objects["count_label_3"]),
            run_time=3.0
        )
        # Ensure only one instance of the array is visible
        self.remove(self.objects["group1"], self.objects["group2"])
        self.add(self.objects["total_stars_array"])
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_08.mp3")  # [auto-injected] duration=6.19s
        _audio_dur_8 = 6.19  # [audio-sync] actual TTS duration
        # Step 9
        # Signal Action: Create total_count_circle
        self.play(Create(self.objects["total_count_circle"]), run_time=1.0)
        # Visual Action: Write total_count_label
        self.play(Write(self.objects["total_count_label"]), run_time=1.5)
        remaining_9 = _audio_dur_8  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_9))

        self.add_sound("media/audio/The_animation_should_1a066f4eed/step_09.mp3")  # [auto-injected] duration=6.74s
        _audio_dur_9 = 6.74  # [audio-sync] actual TTS duration
        # Step 10
        # Signal Action: FadeOut step_label
        self.play(FadeOut(self.objects["step_label"]), run_time=0.5)
        # Visual Action: Write final_equation
        self.play(Write(self.objects["final_equation"]), run_time=2.0)
        remaining_10 = _audio_dur_9  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_10))

        # Final hold
        self.wait(max(0.1, 2))