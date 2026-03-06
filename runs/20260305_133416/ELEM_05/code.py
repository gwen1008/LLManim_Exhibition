'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the rule for rounding decimals to the nearest whole number using a number line, midpoint, and decision zones.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, points, zones
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for composite objects (e.g., number line with ticks). Place zones behind the line (z_index=-1). Position labels above/below points with buff.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5` for each step?
# 5. Animation Flow:
#    - Step 1: Introduce number line and endpoints.
#    - Step 2: Mark the number 3.7.
#    - Step 3: Introduce the midpoint 3.5 and the two decision zones.
#    - Step 4: Highlight the 'round up' zone where 3.7 lies.
#    - Step 5: Animate the point moving to 4, update its label, and highlight the result.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_number_line_d5882e5d2a/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Define Anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan
        # title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole Number", font_size=36, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # number_line
        number_line = NumberLine(x_range=[3, 4, 0.1], length=6, include_numbers=True, color=GRAY_B)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line

        # endpoint_3
        endpoint_3 = MathTex("3", color=WHITE)
        endpoint_3.next_to(number_line.n2p(3), DOWN, buff=0.2)
        self.objects["endpoint_3"] = endpoint_3

        # endpoint_4
        endpoint_4 = MathTex("4", color=WHITE)
        endpoint_4.next_to(number_line.n2p(4), DOWN, buff=0.2)
        self.objects["endpoint_4"] = endpoint_4

        # point_3_7_dot
        point_3_7_dot = Dot(radius=0.08, color=YELLOW)
        point_3_7_dot.move_to(number_line.n2p(3.7))
        self.objects["point_3_7_dot"] = point_3_7_dot

        # point_3_7_label
        point_3_7_label = MathTex("3.7", color=YELLOW)
        point_3_7_label.next_to(point_3_7_dot, UP, buff=0.15)
        self.objects["point_3_7_label"] = point_3_7_label

        # midpoint_3_5_dot
        midpoint_3_5_dot = Dot(radius=0.06, color=RED)
        midpoint_3_5_dot.move_to(number_line.n2p(3.5))
        self.objects["midpoint_3_5_dot"] = midpoint_3_5_dot

        # midpoint_3_5_label
        midpoint_3_5_label = MathTex("3.5", color=RED)
        midpoint_3_5_label.next_to(midpoint_3_5_dot, UP, buff=0.15)
        self.objects["midpoint_3_5_label"] = midpoint_3_5_label

        # zone_round_down
        zone_round_down = Rectangle(width=3, height=0.8, color=BLUE, fill_opacity=0.2, stroke_opacity=0)
        zone_round_down.move_to(number_line.n2p(3.25))
        zone_round_down.set_z_index(-1)
        self.objects["zone_round_down"] = zone_round_down

        # zone_round_up
        zone_round_up = Rectangle(width=3, height=0.8, color=ORANGE, fill_opacity=0.2, stroke_opacity=0)
        zone_round_up.move_to(number_line.n2p(3.75))
        zone_round_up.set_z_index(-1)
        self.objects["zone_round_up"] = zone_round_up

        # explanation_text
        explanation_text = Text("We will round 3.7 to the nearest whole number.", font_size=24, color=GRAY_B)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # result_4_highlight
        result_4_highlight = Rectangle(width=0.8, height=0.8, color=GREEN, fill_opacity=0, stroke_width=4)
        result_4_highlight.move_to(number_line.n2p(4))
        self.objects["result_4_highlight"] = result_4_highlight

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # Narrative: Let's look at a number line from 3 to 4. Our task is to round the number 3.7 to the nearest whole number.
        # signal_action: null
        # visual_action: Create number_line, then write endpoint labels.
        self.play(Write(self.objects["title"]), run_time=1.5)
        self.play(Create(self.objects["number_line"]), run_time=1.5)
        self.play(Write(self.objects["endpoint_3"]), Write(self.objects["endpoint_4"]), run_time=1.0)
        remaining_1 = max(0.1, 3.0 - (1.5 + 1.5 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # Narrative: First, we mark the number in question: three point seven.
        # signal_action: Indicate point_3_7_dot with YELLOW
        # visual_action: Create point_3_7_dot, then write its label.
        self.play(Indicate(self.objects["point_3_7_dot"], color=YELLOW, run_time=1))
        self.play(GrowFromCenter(self.objects["point_3_7_dot"]), run_time=0.8)
        self.play(Write(self.objects["point_3_7_label"]), run_time=0.7)
        remaining_2 = max(0.1, 2.5 - (1 + 0.8 + 0.7) + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # Narrative: The key to rounding is the midpoint between the two whole numbers. For 3 and 4, the midpoint is three point five.
        # signal_action: Circumscribe midpoint_3_5_dot with RED
        # visual_action: Create midpoint_3_5_dot and its label. Then, create the two decision zones.
        self.play(Circumscribe(self.objects["midpoint_3_5_dot"], color=RED, run_time=1))
        self.play(GrowFromCenter(self.objects["midpoint_3_5_dot"]), run_time=0.8)
        self.play(Write(self.objects["midpoint_3_5_label"]), run_time=0.7)
        self.play(FadeIn(self.objects["zone_round_down"]), FadeIn(self.objects["zone_round_up"]), run_time=1.5)
        remaining_3 = max(0.1, 4.0 - (1 + 0.8 + 0.7 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # Narrative: Here is the rule: numbers below the midpoint round down to 3. Numbers at or above the midpoint round up to 4. Since 3.7 is greater than 3.5, it lies in the 'round up' zone.
        # signal_action: Indicate zone_round_up with ORANGE
        # visual_action: Fade in the orange 'round up' zone. Then, briefly flash the blue 'round down' zone for contrast.
        self.play(Indicate(self.objects["zone_round_up"], color=ORANGE, run_time=1))
        self.play(self.objects["zone_round_down"].animate.set_fill(opacity=0.4), run_time=0.5)
        self.play(self.objects["zone_round_down"].animate.set_fill(opacity=0.2), run_time=0.5)
        remaining_4 = max(0.1, 5.0 - (1 + 0.5 + 0.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # Narrative: Therefore, 3.7 rounds up to 4.
        # signal_action: Indicate result_4_highlight with GREEN
        # visual_action: Succession: Move dot, transform label, draw highlight box.
        self.play(Indicate(self.objects["result_4_highlight"], color=GREEN, run_time=1))
        # Move the dot
        self.play(self.objects["point_3_7_dot"].animate.move_to(self.objects["number_line"].n2p(4)), run_time=1.5)
        # Transform the label
        label_4 = MathTex("4", color=YELLOW)
        label_4.next_to(self.objects["point_3_7_dot"], UP, buff=0.15)
        self.play(ReplacementTransform(self.objects["point_3_7_label"], label_4), run_time=0.8)
        self.objects["point_3_7_label"] = label_4  # Update registry
        # Draw the highlight box
        self.play(Create(self.objects["result_4_highlight"]), run_time=1.0)
        remaining_5 = max(0.1, 4.0 - (1 + 1.5 + 0.8 + 1.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))