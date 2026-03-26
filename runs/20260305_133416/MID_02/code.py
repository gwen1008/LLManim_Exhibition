'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize a part-to-part ratio (2:5 milk to water) using a tape diagram (bar model) to show part-to-whole relationships.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for summary text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for tape components. Position labels above tape with buff. Keep summary at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Step 1: Draw tape outline.
#    - Step 2: Divide tape into 7 equal segments (create dividers and invisible segment rects).
#    - Step 3: Fill first two segments for milk, add label.
#    - Step 4: Fill remaining five segments for water, add label.
#    - Step 5: Show final ratio summary.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_labeled_tap_b182667086/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define anchors
        title_anchor = 3.5 * UP
        tape_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Tape Diagram: Milk to Water Ratio 2:5", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # tape_outline
        tape_outline = Rectangle(width=10, height=2, color=WHITE, fill_opacity=0.0, stroke_width=3)
        tape_outline.move_to(tape_anchor)
        self.objects["tape_outline"] = tape_outline

        # divider_lines (empty VGroup, will be populated in step 2)
        divider_lines = VGroup()
        divider_lines.move_to(tape_anchor)
        self.objects["divider_lines"] = divider_lines

        # segment_rects (empty VGroup, will be populated in step 2)
        segment_rects = VGroup()
        segment_rects.move_to(tape_anchor)
        self.objects["segment_rects"] = segment_rects

        # milk_color_fills (empty VGroup, will be populated in step 3)
        milk_color_fills = VGroup()
        milk_color_fills.move_to(tape_anchor)
        self.objects["milk_color_fills"] = milk_color_fills

        # water_color_fills (empty VGroup, will be populated in step 4)
        water_color_fills = VGroup()
        water_color_fills.move_to(tape_anchor)
        self.objects["water_color_fills"] = water_color_fills

        # label_milk (position calculated relative to tape_outline)
        label_milk = Text("Milk (2 parts)", color="#87CEEB", font_size=28)
        # Position: above tape, aligned left, shifted right by width of 1.5 segments (center of first two segments)
        # Each segment width = 10/7 ≈ 1.42857. Center of first two segments is at 1.5 * segment_width from left edge.
        segment_width = 10 / 7
        label_milk.next_to(tape_outline, UP, buff=0.5)
        label_milk.align_to(tape_outline.get_left(), LEFT)
        label_milk.shift(RIGHT * (segment_width * 1.5))
        self.objects["label_milk"] = label_milk

        # label_water (position calculated relative to tape_outline)
        label_water = Text("Water (5 parts)", color="#D2B48C", font_size=28)
        # Center of last five segments: start at segment 2, end at segment 6. Center is at segment 4.
        # Distance from left edge = segment_width * 4.5
        label_water.next_to(tape_outline, UP, buff=0.5)
        label_water.align_to(tape_outline.get_left(), LEFT)
        label_water.shift(RIGHT * (segment_width * 4.5))
        self.objects["label_water"] = label_water

        # ratio_summary
        ratio_summary = Tex(r"Ratio $= 2 : 5$ \quad Total Parts $= 7$", color=YELLOW, font_size=32)
        ratio_summary.move_to(explanation_anchor)
        self.objects["ratio_summary"] = ratio_summary

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # Narrative: Let's visualize a mixture with a ratio of two parts milk to five parts water. We start by drawing a tape diagram, which represents the total mixture.
        # signal_action: null
        # visual_action: Create tape_outline
        self.play(Create(tape_outline), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # Narrative: The total mixture is made of seven equal parts. We divide the tape into seven segments.
        # signal_action: Indicate tape_outline
        self.play(Indicate(tape_outline, color=YELLOW, run_time=1))
        # visual_action: Create divider_lines and segment_rects
        # Create 6 divider lines and 7 segment rectangles
        segment_width = 10 / 7
        tape_left = tape_outline.get_left()
        tape_top = tape_outline.get_top()
        tape_bottom = tape_outline.get_bottom()
        new_dividers = VGroup()
        new_segments = VGroup()
        for i in range(1, 7):  # 6 dividers
            x_pos = tape_left[0] + i * segment_width
            line = Line([x_pos, tape_top[1], 0], [x_pos, tape_bottom[1], 0], color=WHITE, stroke_width=2)
            new_dividers.add(line)
        for i in range(7):  # 7 segment rectangles (invisible, for filling later)
            left_x = tape_left[0] + i * segment_width
            right_x = left_x + segment_width
            rect = Rectangle(width=segment_width, height=2, color=WHITE, fill_opacity=0.0, stroke_opacity=0.0)
            rect.move_to([(left_x + right_x) / 2, tape_anchor[1], 0])
            new_segments.add(rect)
        # Update the VGroups in the registry
        self.objects["divider_lines"] = new_dividers
        self.objects["segment_rects"] = new_segments
        self.play(Create(new_dividers), run_time=2.0)
        remaining_2 = max(0.1, 3.5 - 2.0 - 1.0 + 0.5)  # total duration 3.5, anim: signal 1s + dividers 2s
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # Narrative: Two of these seven parts represent milk. Let's color them light blue and add a label.
        # signal_action: Circumscribe the first two segments
        # We'll create a temporary VGroup for the first two segments for circumscribing
        first_two_segments = VGroup(new_segments[0], new_segments[1])
        self.play(Circumscribe(first_two_segments, color="#87CEEB", run_time=1))
        # visual_action: Create milk_color_fills and label_milk
        milk_fills = VGroup()
        for i in range(2):
            fill_rect = Rectangle(width=segment_width, height=2, color="#87CEEB", fill_opacity=0.6, stroke_width=0)
            fill_rect.move_to(new_segments[i].get_center())
            milk_fills.add(fill_rect)
        self.objects["milk_color_fills"] = milk_fills
        self.play(Create(milk_fills), Write(label_milk), run_time=1.5)
        remaining_3 = max(0.1, 3.0 - 1.5 - 1.0 + 0.5)  # total 3.0, anim: signal 1s + fill+label 1.5s
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # Narrative: The remaining five parts represent water. We color them light brown and add its label.
        # signal_action: Circumscribe the last five segments
        last_five_segments = VGroup(*[new_segments[i] for i in range(2, 7)])
        self.play(Circumscribe(last_five_segments, color="#D2B48C", run_time=1))
        # visual_action: Create water_color_fills and label_water
        water_fills = VGroup()
        for i in range(2, 7):
            fill_rect = Rectangle(width=segment_width, height=2, color="#D2B48C", fill_opacity=0.6, stroke_width=0)
            fill_rect.move_to(new_segments[i].get_center())
            water_fills.add(fill_rect)
        self.objects["water_color_fills"] = water_fills
        self.play(Create(water_fills), Write(label_water), run_time=1.5)
        remaining_4 = max(0.1, 3.0 - 1.5 - 1.0 + 0.5)  # total 3.0, anim: signal 1s + fill+label 1.5s
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # Narrative: The completed tape diagram clearly shows the proportion: for every two parts of milk, there are five parts of water, making a total of seven parts in the mixture.
        # signal_action: Indicate ratio_summary
        self.play(Indicate(ratio_summary, color=YELLOW, run_time=1))
        # visual_action: Write ratio_summary
        self.play(Write(ratio_summary), run_time=1.5)
        remaining_5 = max(0.1, 4.0 - 1.5 - 1.0 + 0.5)  # total 4.0, anim: signal 1s + write 1.5s
        self.wait(max(0.1, remaining_5))