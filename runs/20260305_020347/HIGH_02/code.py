'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the transformation of the parent parabola y=x² into y=(x-2)²-3, showing horizontal and vertical shifts, and identifying key features (vertex, axis of symmetry).
# 2. Layout Strategy: High-Low Split
#    - Header Region: [y=3.5] for Title and Step Indicator
#    - Main Content: [Center y=0] for Axes and Parabola graphs
#    - Footer Region: [Bottom y=-3.5] for Explanation Text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for vertex dot+label. Use ReplacementTransform for step indicator and explanation text to update in place, preventing clutter.
#    - Equations are placed at a fixed anchor (UP*2.0 + LEFT*3.5) and morphed in place.
# 4. Audio Check (CRITICAL) - We do NOT add `self.add_sound()`. The system will auto-inject it.
#    - [x] Have I assigned `remaining_N = max(0.1, json_duration - anim_time + 0.5)` for each step?
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Write parent equation and draw parent graph.
#    - Step 3: Transform parent graph to horizontally shifted graph, update step/exp text, and morph equation.
#    - Step 4: Transform horizontally shifted graph to final graph, update step/exp text, and morph equation.
#    - Step 5: Draw axis of symmetry line.
#    - Step 6: Create vertex dot, labels, and axis label; update step/exp text to final state.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create Layout Engine and define zones
        layout = LayoutEngine()
        # We'll create objects first, then register them with layout.

        # Create Anchors (as per layout_plan)
        title_anchor = 3.5 * UP
        content_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-5, 5, 1],
            axis_config={'include_numbers': True},
            color=GRAY_B  # GRAY_C -> GRAY_B
        ).move_to(content_anchor).scale(0.9)
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))

        # Title
        title = Text("Graphing a Parabola: Transformations", color=WHITE, font_size=36).move_to(title_anchor + UP*0.3)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_constraint(layout.get("title").center_x == 0)

        # Step Indicator (initial state)
        step_indicator = Text("Step 1: Parent Function y = x²", color=YELLOW, font_size=28).next_to(title, DOWN, buff=0.3)
        self.objects["step_indicator"] = step_indicator
        layout.add(LayoutObject(step_indicator, "step_indicator"))
        layout.add_to_zone(layout.get("step_indicator"), "HEADER")
        layout.align_to(layout.get("step_indicator"), layout.get("title"), 'CENTER_X')

        # Explanation Text (initial state)
        exp_text = Paragraph(
            "We start with the basic parabola, symmetric about the y-axis.",
            color=GRAY_B, font_size=24, alignment="center", line_spacing=0.5
        ).move_to(explanation_anchor)
        exp_text.width = 12  # Set width as per properties
        self.objects["exp_text"] = exp_text
        layout.add(LayoutObject(exp_text, "exp_text"))
        layout.add_to_zone(layout.get("exp_text"), "FOOTER")
        layout.add_constraint(layout.get("exp_text").center_x == 0)

        # Parent Graph y = x²
        graph_parent = axes.plot(lambda x: x**2, color=GRAY_D)  # #666666 -> GRAY_D
        graph_parent.set_stroke(width=3)
        self.objects["graph_parent"] = graph_parent

        # Horizontally Shifted Graph y = (x-2)²
        graph_shifted_h = axes.plot(lambda x: (x-2)**2, color=GRAY_C)  # #AAAAAA -> GRAY_C
        graph_shifted_h.set_stroke(width=3)
        self.objects["graph_shifted_h"] = graph_shifted_h

        # Final Graph y = (x-2)² - 3
        graph_final = axes.plot(lambda x: (x-2)**2 - 3, color=BLUE)
        graph_final.set_stroke(width=5)
        self.objects["graph_final"] = graph_final

        # Axis of Symmetry Line (x=2)
        axis_line = DashedLine(
            start=axes.c2p(2, axes.y_range[0]),
            end=axes.c2p(2, axes.y_range[1]),
            color=TEAL,
            stroke_width=4,
            dash_length=0.1
        )
        self.objects["axis_line"] = axis_line

        # Axis Label
        axis_label = MathTex(r"x = 2", color=TEAL, font_size=32).next_to(axes.c2p(2, axes.y_range[1]), UP, buff=0.2)
        self.objects["axis_label"] = axis_label

        # Vertex Dot
        vertex_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0).move_to(axes.c2p(2, -3))
        self.objects["vertex_dot"] = vertex_dot

        # Vertex Label
        vertex_label = MathTex(r"(2,\,-3)", color=RED, font_size=32).next_to(vertex_dot, UP+RIGHT, buff=0.15)
        self.objects["vertex_label"] = vertex_label

        # Equations (placed at fixed anchor)
        eq_anchor = content_anchor + UP*2.0 + LEFT*3.5
        eq_parent = MathTex(r"y = x^2", color=GRAY_D, font_size=40).move_to(eq_anchor)
        self.objects["eq_parent"] = eq_parent
        eq_shifted_h = MathTex(r"y = (x-2)^2", color=GRAY_C, font_size=40).move_to(eq_anchor)
        self.objects["eq_shifted_h"] = eq_shifted_h
        eq_final = MathTex(r"y = (x-2)^2 - 3", color=BLUE, font_size=40).move_to(eq_anchor)
        self.objects["eq_final"] = eq_final

        # Solve layout constraints
        layout.solve()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/Create_a_Manim_anima_d5e26a2713/step_00.mp3")  # [auto-injected] duration=7.25s
        _audio_dur_0 = 7.25  # [audio-sync] actual TTS duration
        # Step 1: Create axes
        self.play(Create(axes), run_time=2.0)
        remaining_1 = _audio_dur_0  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/Create_a_Manim_anima_d5e26a2713/step_01.mp3")  # [auto-injected] duration=6.10s
        _audio_dur_1 = 6.10  # [audio-sync] actual TTS duration
        # Step 2: Write parent equation and draw parent graph
        self.play(Write(eq_parent), run_time=1.0)
        self.play(Create(graph_parent), run_time=2.0)
        remaining_2 = _audio_dur_1  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/Create_a_Manim_anima_d5e26a2713/step_02.mp3")  # [auto-injected] duration=9.34s
        _audio_dur_2 = 9.34  # [audio-sync] actual TTS duration
        # Step 3: Transform to horizontal shift
        # Update step indicator
        step_indicator_2 = Text("Step 2: Horizontal Shift", color=YELLOW, font_size=28).move_to(step_indicator.get_center())
        # Update explanation text
        exp_text_2 = Paragraph(
            "The (x-2)² shifts the graph right 2 units. The axis of symmetry moves to x=2.",
            color=GRAY_B, font_size=24, alignment="center", line_spacing=0.5
        ).move_to(exp_text.get_center())
        exp_text_2.width = 12

        # Signal: Circumscribe eq_shifted_h
        self.play(Circumscribe(eq_shifted_h, color=YELLOW, run_time=1))
        # Visual actions: Transform graph, update texts, transform equation
        self.play(
            Transform(graph_parent, graph_shifted_h),
            ReplacementTransform(step_indicator, step_indicator_2),
            ReplacementTransform(exp_text, exp_text_2),
            ReplacementTransform(eq_parent, eq_shifted_h),
            run_time=3.0
        )
        # Update registry
        self.objects["step_indicator"] = step_indicator_2
        self.objects["exp_text"] = exp_text_2
        remaining_3 = _audio_dur_2  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/Create_a_Manim_anima_d5e26a2713/step_03.mp3")  # [auto-injected] duration=8.81s
        _audio_dur_3 = 8.81  # [audio-sync] actual TTS duration
        # Step 4: Transform to final graph
        # Update step indicator
        step_indicator_3 = Text("Step 3: Vertical Shift", color=YELLOW, font_size=28).move_to(step_indicator_2.get_center())
        # Update explanation text
        exp_text_3 = Paragraph(
            "The -3 shifts the graph down 3 units. The vertex is now at (2, -3).",
            color=GRAY_B, font_size=24, alignment="center", line_spacing=0.5
        ).move_to(exp_text_2.get_center())
        exp_text_3.width = 12

        # Signal: Circumscribe eq_final
        self.play(Circumscribe(eq_final, color=YELLOW, run_time=1))
        # Visual actions: Transform graph, update texts, transform equation
        self.play(
            Transform(graph_parent, graph_final),  # graph_parent now holds graph_shifted_h
            ReplacementTransform(step_indicator_2, step_indicator_3),
            ReplacementTransform(exp_text_2, exp_text_3),
            ReplacementTransform(eq_shifted_h, eq_final),
            run_time=3.0
        )
        # Update registry
        self.objects["step_indicator"] = step_indicator_3
        self.objects["exp_text"] = exp_text_3
        remaining_4 = _audio_dur_3  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/Create_a_Manim_anima_d5e26a2713/step_04.mp3")  # [auto-injected] duration=7.56s
        _audio_dur_4 = 7.56  # [audio-sync] actual TTS duration
        # Step 5: Draw axis of symmetry line
        self.play(Create(axis_line), run_time=2.0)
        remaining_5 = _audio_dur_4  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/Create_a_Manim_anima_d5e26a2713/step_05.mp3")  # [auto-injected] duration=6.91s
        _audio_dur_5 = 6.91  # [audio-sync] actual TTS duration
        # Step 6: Create vertex dot, labels, and axis label; update step/exp text
        # Update step indicator
        step_indicator_final = Text("Complete", color=GREEN, font_size=28).move_to(step_indicator_3.get_center())
        # Update explanation text
        exp_text_final = Paragraph(
            "Graph of y=(x-2)²-3 with vertex (2,-3) and axis x=2.",
            color=GRAY_B, font_size=24, alignment="center", line_spacing=0.5
        ).move_to(exp_text_3.get_center())
        exp_text_final.width = 12

        # Signal: Indicate vertex_dot (will appear with creation)
        # We'll create the dot first, then indicate it.
        self.play(
            Create(vertex_dot),
            Write(vertex_label),
            Write(axis_label),
            ReplacementTransform(step_indicator_3, step_indicator_final),
            ReplacementTransform(exp_text_3, exp_text_final),
            run_time=2.0
        )
        # Now indicate the vertex dot
        self.play(Indicate(vertex_dot, color=RED, run_time=1))
        remaining_6 = _audio_dur_5  # [audio-sync] use actual TTS duration
        self.wait(max(0.1, remaining_6))

        # Final hold
        self.wait(max(0.1, 2))