'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize displacement on a number line, showing a jump from -2 to +3 is a movement of 5 units.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, points, and arrow
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups to keep labels with their points. Position number line centrally, title at top, explanation at bottom.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Show title.
#    - Draw number line and label ticks.
#    - Mark start point (-2) and end point (+3).
#    - Animate an arrow growing from -2 to +3.
#    - Label the displacement as "5 units".
#    - Show the arithmetic relationship: 3 - (-2) = 5.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Title
        title = Text("位移：從 -2 到 +3", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.objects["title"] = title

        # Number Line
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=10,
            include_numbers=True,
            numbers_with_elongated_ticks=[-5, 0, 5],
            font_size=30
        )
        number_line.move_to(ORIGIN)
        self.objects["number_line"] = number_line

        # Start Point (-2)
        start_point = Dot(number_line.n2p(-2), color=BLUE)
        start_label = MathTex("-2", color=BLUE, font_size=30)
        start_label.next_to(start_point, DOWN, buff=0.2)
        start_group = VGroup(start_point, start_label)
        self.objects["start_group"] = start_group

        # End Point (+3)
        end_point = Dot(number_line.n2p(3), color=GREEN)
        end_label = MathTex("+3", color=GREEN, font_size=30)
        end_label.next_to(end_point, UP, buff=0.2)
        end_group = VGroup(end_point, end_label)
        self.objects["end_group"] = end_group

        # Displacement Arrow (will be animated)
        arrow = Arrow(
            start=number_line.n2p(-2),
            end=number_line.n2p(-2),  # Initially zero length
            buff=0,
            color=YELLOW,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["arrow"] = arrow

        # Displacement Label
        displacement_label = Text("位移 = 5 單位", color=YELLOW, font_size=36)
        displacement_label.next_to(arrow, UP, buff=0.5)
        self.objects["displacement_label"] = displacement_label

        # Arithmetic Explanation
        explanation = MathTex(r"3 - (-2) = 5", color=WHITE, font_size=40)
        explanation.to_edge(DOWN, buff=0.8)
        self.objects["explanation"] = explanation

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # Step 1: Show Title
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # Step 2: Draw Number Line
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_2 = max(0.1, 4.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # Step 3: Mark Start Point (-2)
        self.play(
            Create(self.objects["start_group"][0]),
            Write(self.objects["start_group"][1]),
            run_time=1.5
        )
        remaining_3 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # Step 4: Mark End Point (+3)
        self.play(
            Create(self.objects["end_group"][0]),
            Write(self.objects["end_group"][1]),
            run_time=1.5
        )
        remaining_4 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # Step 5: Animate Arrow Growing from -2 to +3
        # Signal Action: Focus on the start point before the arrow grows
        self.play(FocusOn(self.objects["start_group"][0]))
        self.wait(max(0.1, 0.5))

        arrow_target = Arrow(
            start=number_line.n2p(-2),
            end=number_line.n2p(3),
            buff=0,
            color=YELLOW,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        self.play(Transform(self.objects["arrow"], arrow_target), run_time=2.5)
        remaining_5 = max(0.1, 5.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Step 6: Show Displacement Label
        self.play(Write(self.objects["displacement_label"]), run_time=1.5)
        remaining_6 = max(0.1, 4.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))

        # Step 7: Show Arithmetic Explanation
        self.play(Write(self.objects["explanation"]), run_time=2.0)
        remaining_7 = max(0.1, 5.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Final hold
        self.wait(max(0.1, 2))