'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Graph the quadratic function y = (x-2)² - 3 by transforming the parent function y = x², showing the horizontal shift (right 2) and vertical shift (down 3), and identifying the vertex (2, -3) and axis of symmetry (x=2).
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Graphing y = (x-2)² - 3"
#    - Main Content: [Center y=0] for axes and graphs
#    - Footer Region: [Bottom y=-3.5] for step explanation text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for function labels and position them to the left of the axes. Keep graphs centered. Use dynamic step explanation that updates.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = json_duration - anim_time + 0.5`?
# 5. Animation Flow:
#    - Show title and axes.
#    - Plot parent function y=x² (gray).
#    - Transform it horizontally to y=(x-2)² (yellow).
#    - Transform it vertically to y=(x-2)²-3 (blue).
#    - Mark vertex (2,-3) with red dot.
#    - Draw axis of symmetry (green dashed line).
#    - Label vertex and axis.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Graphing y = (x-2)² - 3", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_constraint(layout.get("title").center_x == 0)

        # axes
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=8,
            axis_config={"color": GRAY_C}
        )
        axes.move_to(content_center)
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))
        layout.add_to_zone(layout.get("axes"), "CONTENT")
        layout.add_constraint(layout.get("axes").center_x == 0)
        layout.add_constraint(layout.get("axes").center_y == 0)

        # parent_graph (y = x^2)
        parent_graph = axes.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=GRAY, stroke_width=3)
        self.objects["parent_graph"] = parent_graph
        layout.add(LayoutObject(parent_graph, "parent_graph"))
        layout.add_to_zone(layout.get("parent_graph"), "CONTENT")
        layout.align_to(layout.get("parent_graph"), layout.get("axes"), 'CENTER')

        # parent_label
        parent_label = MathTex(r"y = x^2", color=GRAY, font_size=28)
        self.objects["parent_label"] = parent_label
        layout.add(LayoutObject(parent_label, "parent_label"))
        layout.add_to_zone(layout.get("parent_label"), "CONTENT")
        # Position will be set relative to axes after solve

        # shifted_graph (y = (x-2)^2)
        shifted_graph = axes.plot(lambda x: (x-2)**2, x_range=[-0.5, 4.5], color=YELLOW, stroke_width=3)
        self.objects["shifted_graph"] = shifted_graph
        layout.add(LayoutObject(shifted_graph, "shifted_graph"))
        layout.add_to_zone(layout.get("shifted_graph"), "CONTENT")
        layout.align_to(layout.get("shifted_graph"), layout.get("axes"), 'CENTER')

        # shifted_label
        shifted_label = MathTex(r"y = (x-2)^2", color=YELLOW, font_size=28)
        self.objects["shifted_label"] = shifted_label
        layout.add(LayoutObject(shifted_label, "shifted_label"))
        layout.add_to_zone(layout.get("shifted_label"), "CONTENT")

        # final_graph (y = (x-2)^2 - 3)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-0.5, 4.5], color=BLUE, stroke_width=4)
        self.objects["final_graph"] = final_graph
        layout.add(LayoutObject(final_graph, "final_graph"))
        layout.add_to_zone(layout.get("final_graph"), "CONTENT")
        layout.align_to(layout.get("final_graph"), layout.get("axes"), 'CENTER')

        # final_label
        final_label = MathTex(r"y = (x-2)^2 - 3", color=BLUE, font_size=28)
        self.objects["final_label"] = final_label
        layout.add(LayoutObject(final_label, "final_label"))
        layout.add_to_zone(layout.get("final_label"), "CONTENT")

        # vertex_point
        vertex_point = Dot(axes.coords_to_point(2, -3), color=RED, radius=0.08, fill_opacity=1.0)
        self.objects["vertex_point"] = vertex_point
        layout.add(LayoutObject(vertex_point, "vertex_point"))
        layout.add_to_zone(layout.get("vertex_point"), "CONTENT")

        # vertex_label
        vertex_label = MathTex(r"(2, -3)", color=RED, font_size=24)
        self.objects["vertex_label"] = vertex_label
        layout.add(LayoutObject(vertex_label, "vertex_label"))
        layout.add_to_zone(layout.get("vertex_label"), "CONTENT")

        # axis_symmetry (dashed line at x=2)
        axis_symmetry = DashedLine(
            start=axes.coords_to_point(2, 3),
            end=axes.coords_to_point(2, -3),
            color=GREEN,
            stroke_width=3,
            dash_length=0.1
        )
        self.objects["axis_symmetry"] = axis_symmetry
        layout.add(LayoutObject(axis_symmetry, "axis_symmetry"))
        layout.add_to_zone(layout.get("axis_symmetry"), "CONTENT")

        # axis_label
        axis_label = MathTex(r"x = 2", color=GREEN, font_size=24)
        self.objects["axis_label"] = axis_label
        layout.add(LayoutObject(axis_label, "axis_label"))
        layout.add_to_zone(layout.get("axis_label"), "CONTENT")

        # step_explanation (dynamic text)
        step_explanation = Text("Starting with the parent function y = x²", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        layout.add(LayoutObject(step_explanation, "step_explanation"))
        layout.add_to_zone(layout.get("step_explanation"), "FOOTER")
        layout.add_constraint(layout.get("step_explanation").center_x == 0)

        # Solve layout constraints
        layout.solve()

        # Apply solved positions to mobjects
        title.move_to(layout.get("title").get_center())
        axes.move_to(layout.get("axes").get_center())
        parent_graph.move_to(layout.get("parent_graph").get_center())
        parent_label.move_to(layout.get("parent_label").get_center())
        shifted_graph.move_to(layout.get("shifted_graph").get_center())
        shifted_label.move_to(layout.get("shifted_label").get_center())
        final_graph.move_to(layout.get("final_graph").get_center())
        final_label.move_to(layout.get("final_label").get_center())
        vertex_point.move_to(layout.get("vertex_point").get_center())
        vertex_label.move_to(layout.get("vertex_label").get_center())
        axis_symmetry.move_to(layout.get("axis_symmetry").get_center())
        axis_label.move_to(layout.get("axis_label").get_center())
        step_explanation.move_to(layout.get("step_explanation").get_center())

        # Position labels to the left of axes (manual relative positioning after solve)
        label_x = axes.get_left()[0] - 2.0
        parent_label.move_to([label_x, axes.get_top()[1] - 0.5, 0])
        shifted_label.next_to(parent_label, DOWN, buff=0.5, aligned_edge=LEFT)
        final_label.next_to(shifted_label, DOWN, buff=0.5, aligned_edge=LEFT)
        vertex_label.next_to(vertex_point, UP+RIGHT, buff=0.2)
        axis_label.next_to(axis_symmetry, UP, buff=0.2)

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_00.mp3")  # [auto-injected] duration=10.49s
        _audio_dur_0 = 10.49  # [audio-sync] actual TTS duration
        # Step 1: Title
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_01.mp3")  # [auto-injected] duration=9.98s
        _audio_dur_1 = 9.98  # [audio-sync] actual TTS duration
        # Step 2: Axes
        self.play(Create(self.objects["axes"]), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_02.mp3")  # [auto-injected] duration=5.83s
        _audio_dur_2 = 5.83  # [audio-sync] actual TTS duration
        # Step 3: Parent function y = x^2
        # Update explanation text
        new_explanation_1 = Text("Plot the parent function y = x²", color=GRAY_C, font_size=24)
        new_explanation_1.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_1))
        self.objects["step_explanation"] = new_explanation_1
        self.play(Indicate(self.objects["parent_label"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["parent_graph"]), run_time=2.0)
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration  # total 3.0, signal 1.0, graph 2.0
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_03.mp3")  # [auto-injected] duration=12.05s
        _audio_dur_3 = 12.05  # [audio-sync] actual TTS duration
        # Step 4: Horizontal shift to y = (x-2)^2
        new_explanation_2 = Text("Horizontal shift: move right 2 units", color=GRAY_C, font_size=24)
        new_explanation_2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_2))
        self.objects["step_explanation"] = new_explanation_2
        self.play(Indicate(self.objects["parent_graph"], color=YELLOW, run_time=1))
        self.play(Transform(self.objects["parent_graph"], self.objects["shifted_graph"]), run_time=2.5)
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_04.mp3")  # [auto-injected] duration=9.48s
        _audio_dur_4 = 9.48  # [audio-sync] actual TTS duration
        # Step 5: Vertical shift to y = (x-2)^2 - 3
        new_explanation_3 = Text("Vertical shift: move down 3 units", color=GRAY_C, font_size=24)
        new_explanation_3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_3))
        self.objects["step_explanation"] = new_explanation_3
        self.play(Indicate(self.objects["shifted_graph"], color=BLUE, run_time=1))
        self.play(Transform(self.objects["shifted_graph"], self.objects["final_graph"]), run_time=2.5)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_05.mp3")  # [auto-injected] duration=7.99s
        _audio_dur_5 = 7.99  # [audio-sync] actual TTS duration
        # Step 6: Vertex point
        new_explanation_4 = Text("Vertex at (2, -3) is the lowest point", color=GRAY_C, font_size=24)
        new_explanation_4.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_4))
        self.objects["step_explanation"] = new_explanation_4
        self.play(Circumscribe(self.objects["vertex_point"], color=RED, run_time=1))
        self.play(Create(self.objects["vertex_point"]), run_time=1.5)
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_06.mp3")  # [auto-injected] duration=7.06s
        _audio_dur_6 = 7.06  # [audio-sync] actual TTS duration
        # Step 7: Axis of symmetry
        new_explanation_5 = Text("Axis of symmetry: x = 2", color=GRAY_C, font_size=24)
        new_explanation_5.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_5))
        self.objects["step_explanation"] = new_explanation_5
        self.play(Indicate(self.objects["axis_symmetry"], color=GREEN, run_time=1))
        self.play(Create(self.objects["axis_symmetry"]), run_time=1.5)
        remaining_7 = _audio_dur_6  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/Create_a_Manim_anima_2bc8d31391/step_07.mp3")  # [auto-injected] duration=14.52s
        _audio_dur_7 = 14.52  # [audio-sync] actual TTS duration
        # Step 8: Labels
        new_explanation_6 = Text("Graph complete: y = (x-2)² - 3", color=GRAY_C, font_size=24)
        new_explanation_6.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation_6))
        self.objects["step_explanation"] = new_explanation_6
        self.play(Write(self.objects["vertex_label"]), Write(self.objects["axis_label"]), run_time=2.0)
        remaining_8 = _audio_dur_7  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_8))

        # Final hold
        self.wait(max(0.1, 2))