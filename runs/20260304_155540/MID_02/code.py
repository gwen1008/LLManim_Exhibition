'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the ratio 2:5 (milk to water) using a tape diagram, building understanding of part-to-whole relationships and proportions.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for ratio summary text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Use VGroups for the 7 segments to manage them collectively. Position title at top, tape at center, summary at bottom with clear spacing.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow: [Brief sequence of events]
#    - Step 1: Show empty tape outline.
#    - Step 2: Divide tape into 7 equal segment outlines.
#    - Step 3: Fill and label the 2 milk segments, add brace.
#    - Step 4: Fill and label the 5 water segments, add brace.
#    - Step 5: Display final ratio and proportion summary.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors based on zones
        title_anchor = 3.5 * UP
        tape_center_anchor = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan
        # Title
        title = Text("Tape Diagram: Milk to Water Ratio 2:5", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Tape Outline
        tape_outline = Rectangle(width=7.0, height=1.0, color=WHITE, stroke_width=3, fill_opacity=0.0)
        tape_outline.move_to(tape_center_anchor)
        self.objects["tape_outline"] = tape_outline

        # Create the 7 segment polygons
        # Define vertices for a unit square centered at origin, width=1, height=1
        # We will position them using move_to with offsets
        base_vertices = [
            (-0.5, 0.5, 0),
            (-0.5, -0.5, 0),
            (0.5, -0.5, 0),
            (0.5, 0.5, 0)
        ]
        segment_colors = ["#66B3FF", "#66B3FF", "#CCE5FF", "#CCE5FF", "#CCE5FF", "#CCE5FF", "#CCE5FF"]
        segment_positions = [
            tape_center_anchor + 3.0 * LEFT,
            tape_center_anchor + 2.0 * LEFT,
            tape_center_anchor + 1.0 * LEFT,
            tape_center_anchor,
            tape_center_anchor + 1.0 * RIGHT,
            tape_center_anchor + 2.0 * RIGHT,
            tape_center_anchor + 3.0 * RIGHT
        ]

        for i in range(7):
            seg = Polygon(*base_vertices, color=segment_colors[i], fill_opacity=0.0, stroke_width=0)
            seg.move_to(segment_positions[i])
            self.objects[f"segment_{i}"] = seg

        # Labels
        label_milk = Text("Milk", color="#66B3FF", font_size=28)
        label_milk.move_to(tape_center_anchor + 2.5 * LEFT + 0.8 * UP)
        self.objects["label_milk"] = label_milk

        label_water = Text("Water", color="#CCE5FF", font_size=28)
        label_water.move_to(tape_center_anchor + 1.5 * RIGHT + 0.8 * UP)
        self.objects["label_water"] = label_water

        # Braces
        milk_line = Line(tape_center_anchor + 3.5 * LEFT, tape_center_anchor + 1.5 * LEFT, color="#66B3FF")
        brace_milk = Brace(milk_line, direction=UP, color="#66B3FF")
        brace_milk.move_to(tape_center_anchor + 2.5 * LEFT + 0.5 * UP)
        self.objects["brace_milk"] = brace_milk

        water_line = Line(tape_center_anchor + 2.5 * LEFT, tape_center_anchor + 3.5 * RIGHT, color="#CCE5FF")
        brace_water = Brace(water_line, direction=UP, color="#CCE5FF")
        brace_water.move_to(tape_center_anchor + 1.5 * RIGHT + 0.5 * UP)
        self.objects["brace_water"] = brace_water

        # Ratio Summary (using Tex for mixed text and math)
        ratio_summary = Tex(r"Milk $= \frac{2}{7}$\quad Water $= \frac{5}{7}$\quad Ratio $= 2:5$", color=WHITE, font_size=32)
        ratio_summary.move_to(footer_anchor)
        self.objects["ratio_summary"] = ratio_summary

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_labeled_tap_cf3cd1a5f7/step_00.mp3")  # [auto-injected] duration=4.13s
        _audio_dur_0 = 4.13  # [audio-sync] actual TTS duration
        # Step 1: Show blank tape outline
        self.play(Write(self.objects["title"]), run_time=1.5)
        self.wait(max(0.1, 0.5)) # Small pause after title
        self.play(Create(self.objects["tape_outline"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_labeled_tap_cf3cd1a5f7/step_01.mp3")  # [auto-injected] duration=3.58s
        _audio_dur_1 = 3.58  # [audio-sync] actual TTS duration
        # Step 2: Divide into 7 equal parts
        # Signal action: Indicate tape outline
        self.play(Indicate(self.objects["tape_outline"], color=YELLOW, run_time=1))
        # Create all segment outlines as a group
        segment_creation_anims = [Create(self.objects[f"segment_{i}"]) for i in range(7)]
        self.play(AnimationGroup(*segment_creation_anims, lag_ratio=0.1), run_time=2.5)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_labeled_tap_cf3cd1a5f7/step_02.mp3")  # [auto-injected] duration=3.91s
        _audio_dur_2 = 3.91  # [audio-sync] actual TTS duration
        # Step 3: Color and label the two milk parts
        # Signal action: Circumscribe first milk segment
        self.play(Circumscribe(self.objects["segment_0"], color=YELLOW, run_time=1))
        # Fill the two milk segments
        self.play(
            self.objects["segment_0"].animate.set_fill(opacity=0.5),
            self.objects["segment_1"].animate.set_fill(opacity=0.5),
            run_time=1.0
        )
        # Write label and create brace
        self.play(Write(self.objects["label_milk"]), run_time=0.8)
        self.play(Create(self.objects["brace_milk"]), run_time=0.7)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_labeled_tap_cf3cd1a5f7/step_03.mp3")  # [auto-injected] duration=2.28s
        _audio_dur_3 = 2.28  # [audio-sync] actual TTS duration
        # Step 4: Color and label the five water parts
        # Signal action: Indicate first water segment
        self.play(Indicate(self.objects["segment_2"], color=YELLOW, run_time=1))
        # Fill the five water segments
        fill_anims = [self.objects[f"segment_{i}"].animate.set_fill(opacity=0.5) for i in range(2, 7)]
        self.play(AnimationGroup(*fill_anims, lag_ratio=0.05), run_time=1.5)
        # Write label and create brace
        self.play(Write(self.objects["label_water"]), run_time=0.8)
        self.play(Create(self.objects["brace_water"]), run_time=0.7)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_labeled_tap_cf3cd1a5f7/step_04.mp3")  # [auto-injected] duration=9.02s
        _audio_dur_4 = 9.02  # [audio-sync] actual TTS duration
        # Step 5: Show final ratio summary
        # Signal action: Indicate milk brace
        self.play(Indicate(self.objects["brace_milk"], color=WHITE, run_time=1))
        self.play(Write(self.objects["ratio_summary"]), run_time=2.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))