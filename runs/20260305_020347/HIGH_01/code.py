'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the slope of the linear function y=2x-1 using a geometric slope triangle on a coordinate plane.
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title (function equation)
#    - Main Content: [Center y=0] for axes, graph, points, and slope triangle
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for labels and arrows (run, rise) to keep them together and positioned relative to their geometric elements.
#    - Ensure the slope triangle and labels do not obscure the axes numbers.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`? Yes, for each step.
# 5. Animation Flow:
#    - Step 1: Introduce the function title.
#    - Step 2: Create the coordinate axes.
#    - Step 3: Plot the line and highlight points A and B.
#    - Step 4: Show the horizontal run.
#    - Step 5: Show the vertical rise and complete the slope triangle.
#    - Step 6: Transform the title to show the slope calculation.
'''

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_an_animation__49ce5f4b80/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define Anchors
        title_anchor = 3.5 * UP
        graph_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Object Registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title_text
        title_text = MathTex(r"y = 2x - 1", color=BLUE).scale(1.2)
        title_text.move_to(title_anchor)
        self.objects["title_text"] = title_text

        # axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": True},
            color=WHITE
        )
        axes.move_to(graph_anchor)
        self.objects["axes"] = axes

        # graph_line
        graph_line = axes.plot(lambda x: 2*x - 1, color=BLUE, stroke_width=4)
        self.objects["graph_line"] = graph_line

        # dot_A
        dot_A = Dot(point=axes.c2p(0, -1), color=YELLOW, radius=0.08)
        self.objects["dot_A"] = dot_A

        # dot_B
        dot_B = Dot(point=axes.c2p(1, 1), color=YELLOW, radius=0.08)
        self.objects["dot_B"] = dot_B

        # label_A
        label_A = MathTex(r"A", color=YELLOW).scale(0.8)
        label_A.next_to(dot_A, LEFT+DOWN, buff=0.15)
        self.objects["label_A"] = label_A

        # label_B
        label_B = MathTex(r"B", color=YELLOW).scale(0.8)
        label_B.next_to(dot_B, RIGHT+UP, buff=0.15)
        self.objects["label_B"] = label_B

        # slope_triangle
        # geometry_def: "[axes.c2p(0, -1), axes.c2p(1, -1), axes.c2p(1, 1)]"
        # Polygon expects points as separate arguments, not a list.
        tri_vertices = [axes.c2p(0, -1), axes.c2p(1, -1), axes.c2p(1, 1)]
        slope_triangle = Polygon(*tri_vertices, color=GREEN, fill_opacity=0.3, stroke_width=3)
        self.objects["slope_triangle"] = slope_triangle

        # run_arrow
        run_arrow = Arrow(start=axes.c2p(0, -1), end=axes.c2p(1, -1), color=RED, stroke_width=4, buff=0)
        self.objects["run_arrow"] = run_arrow

        # rise_arrow
        rise_arrow = Arrow(start=axes.c2p(1, -1), end=axes.c2p(1, 1), color=RED, stroke_width=4, buff=0)
        self.objects["rise_arrow"] = rise_arrow

        # run_label
        run_label = Tex(r"Run $=1$", color=RED).scale(0.8)
        run_label.next_to(run_arrow, DOWN, buff=0.1)
        self.objects["run_label"] = run_label

        # rise_label
        rise_label = Tex(r"Rise $=2$", color=RED).scale(0.8)
        rise_label.next_to(rise_arrow, RIGHT, buff=0.1)
        self.objects["rise_label"] = rise_label

        # explanation_text
        explanation_text = Text("Let's visualize the function y = 2x - 1.", color=WHITE).scale(0.8)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        # signal_action: Circumscribe title_text
        self.play(Circumscribe(self.objects["title_text"], color=YELLOW, run_time=1))
        # visual_action: Write title_text
        self.play(Write(self.objects["title_text"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        # signal_action: null
        # visual_action: Create axes
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_2 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        # signal_action: null
        # visual_action: Create graph_line, dot_A, Write label_A, Create dot_B, Write label_B
        self.play(Create(self.objects["graph_line"]), run_time=2.0)
        self.play(
            Create(self.objects["dot_A"]),
            Write(self.objects["label_A"]),
            Create(self.objects["dot_B"]),
            Write(self.objects["label_B"]),
            run_time=3.0
        )
        remaining_3 = max(0.1, 5.0 - (2.0 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        # signal_action: Indicate run_arrow
        self.play(Indicate(self.objects["run_arrow"], color=RED, run_time=1))
        # visual_action: Create run_arrow, Write run_label
        self.play(
            Create(self.objects["run_arrow"]),
            Write(self.objects["run_label"]),
            run_time=2.5
        )
        remaining_4 = max(0.1, 3.5 - (1.0 + 2.5) + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        # signal_action: Indicate rise_arrow
        self.play(Indicate(self.objects["rise_arrow"], color=RED, run_time=1))
        # visual_action: Create rise_arrow, Write rise_label, Create slope_triangle
        self.play(
            Create(self.objects["rise_arrow"]),
            Write(self.objects["rise_label"]),
            Create(self.objects["slope_triangle"]),
            run_time=3.0
        )
        remaining_5 = max(0.1, 4.0 - (1.0 + 3.0) + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        # signal_action: Circumscribe title_text
        self.play(Circumscribe(self.objects["title_text"], color=GREEN, run_time=1))
        # visual_action: TransformMatchingTex title_text
        # Create the target Tex for the transformation.
        title_final = Tex(
            r"$y = 2x - 1$ \quad Slope $= \frac{Rise}{Run} = \frac{2}{1} = 2$",
            color=BLUE
        ).scale(1.2)
        title_final.move_to(title_anchor)
        self.play(
            TransformMatchingTex(self.objects["title_text"], title_final),
            run_time=4.0
        )
        self.objects["title_text"] = title_final  # Update registry
        remaining_6 = max(0.1, 5.0 - (1.0 + 4.0) + 0.5)
        self.wait(max(0.1, remaining_6))