'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the transformation of a parabola from the parent function y=x² to y=(x-2)²-3, showing horizontal and vertical shifts.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for axes and parabola
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep title, equation, axes, and explanation in separate vertical bands.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Create parent parabola y=x² and indicate its vertex.
#    - Step 3: Transform equation and parabola horizontally (shift right by 2).
#    - Step 4: Transform parabola vertically (shift down by 3) to final form.
#    - Step 5: Mark final vertex, label it, and draw axis of symmetry.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for objects
        self.objects = {}

        # Initialize Layout Engine
        layout = LayoutEngine()

        # 1. Create objects from layout_plan.objects
        # Axes
        axes = Axes(
            x_range=[-3, 7, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": LIGHT_GRAY}
        )
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))

        # Title
        title = Text("Graphing a Parabola: Transformational Approach", color=WHITE, font_size=36)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_constraint(layout.get("title").center_x == 0)

        # Equation Display (will be updated)
        eq_display = MathTex("y = x^2", color=BLUE, font_size=36)
        self.objects["eq_display"] = eq_display
        layout.add(LayoutObject(eq_display, "eq_display"))
        layout.add_to_zone(layout.get("eq_display"), "CONTENT")
        layout.add_constraint(layout.get("eq_display").center_x == 0)
        # Position equation above axes
        layout.align_to(layout.get("eq_display"), layout.get("axes"), "TOP", buff=1.0)

        # Parent Parabola (y = x^2)
        parent_parabola = axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE, stroke_width=3)
        self.objects["parent_parabola"] = parent_parabola
        # We'll add this to layout later after solving for axes position

        # Parent Vertex Dot
        parent_vertex = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.08, fill_opacity=1.0)
        self.objects["parent_vertex"] = parent_vertex

        # Transformed Parabola (y = (x-2)^2 - 3)
        transformed_parabola = axes.plot(lambda x: (x-2)**2 - 3, x_range=[0, 4], color=GREEN, stroke_width=3)
        self.objects["transformed_parabola"] = transformed_parabola

        # Final Vertex Dot
        final_vertex = Dot(axes.c2p(2, -3), color=RED, radius=0.1, fill_opacity=1.0)
        self.objects["final_vertex"] = final_vertex

        # Vertex Label
        vertex_label = MathTex("(2,-3)", color=RED, font_size=24)
        self.objects["vertex_label"] = vertex_label

        # Axis of Symmetry (dashed line at x=2)
        axis_symmetry = DashedLine(
            start=axes.c2p(2, -4),
            end=axes.c2p(2, 4),
            color=PURPLE,
            stroke_width=2,
            dash_length=0.05
        )
        self.objects["axis_symmetry"] = axis_symmetry

        # Explanation Text
        explanation_text = Text("Start with the parent function y = x²", color=LIGHT_GRAY, font_size=24)
        self.objects["explanation_text"] = explanation_text
        layout.add(LayoutObject(explanation_text, "explanation_text"))
        layout.add_to_zone(layout.get("explanation_text"), "FOOTER")
        layout.add_constraint(layout.get("explanation_text").center_x == 0)

        # Solve layout for title, equation, axes, and explanation
        layout.solve()

        # Now position objects that depend on axes coordinates (after layout.solve)
        # The axes center is at ORIGIN after layout.solve, but its coordinate system is internal.
        # We need to ensure parent_parabola, etc., are children of axes or positioned relative to it.
        # Since axes.plot already uses axes.c2p, they are correctly positioned relative to axes.
        # We just need to add them to the scene later.

        # Position vertex_label relative to final_vertex (which is at axes.c2p)
        # We'll position this after final_vertex is created.
        vertex_label.next_to(final_vertex, UP+RIGHT, buff=0.2)

        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We begin with the basic parabola, the parent function y equals x squared.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "axes", "details": "Draw coordinate axes"},
                "duration": 5.256,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Let's plot the parent function y = x². Notice its vertex is at the origin, (0,0).",
                "signal_action": {"type": "Indicate", "target": "parent_vertex", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "parent_parabola", "details": "Draw the blue parabola curve"},
                "duration": 7.752,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now we apply a horizontal shift. Replacing x with (x-2) moves the entire graph 2 units to the right.",
                "signal_action": {"type": "Circumscribe", "target": "eq_display", "color": "YELLOW"},
                "visual_action": {"type": "Transform", "target_id": "parent_parabola", "details": "Transform parent parabola to intermediate position (shifted right by 2)"},
                "duration": 8.376,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Next, we apply a vertical shift. Subtracting 3 moves the graph down by 3 units, giving us our final equation: y = (x-2)² - 3.",
                "signal_action": {"type": "Indicate", "target": "transformed_parabola", "color": "GREEN"},
                "visual_action": {"type": "Transform", "target_id": "parent_parabola", "details": "Transform to final parabola position (shifted down by 3)"},
                "duration": 12.144,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "The vertex of our transformed parabola is at (2, -3). Let's label it and draw the vertical axis of symmetry at x = 2.",
                "signal_action": {"type": "Indicate", "target": "final_vertex", "color": "RED"},
                "visual_action": {"type": "Create", "target_id": "final_vertex", "details": "Create red dot at vertex"},
                "duration": 9.672,
                "audio_path": "media/audio/畫出_y____x_2__2___3_的_95119814cf/step_04.mp3"
            }
        ]

        # We'll also need to update the equation display and explanation text during the sequence.
        # These are not explicitly in the sequence steps but implied by the narrative.
        # We'll handle them inline.

        # Step 1: Create axes
        step = sequence[0]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(title), Write(eq_display), Write(explanation_text))
        self.play(Create(axes))
        remaining = step["duration"] - 2.0  # Approximate animation time for Write and Create
        if remaining > 0:
            self.wait(remaining)

        # Step 2: Create parent parabola and indicate vertex
        step = sequence[1]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update explanation text
        new_explanation = Text("Plot the parent function y = x²", color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(explanation_text.get_center())
        self.play(ReplacementTransform(explanation_text, new_explanation))
        explanation_text = new_explanation
        self.objects["explanation_text"] = explanation_text
        # Create parent parabola
        self.play(Create(parent_parabola))
        # Add parent vertex dot (initially invisible, will be indicated)
        self.add(parent_vertex)
        # Signal action: Indicate parent vertex
        self.play(Indicate(parent_vertex, color=YELLOW))
        remaining = step["duration"] - 3.0  # Approx time for transform, create, indicate
        if remaining > 0:
            self.wait(remaining)

        # Step 3: Horizontal shift
        step = sequence[2]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update equation display to show horizontal shift
        eq_horizontal = MathTex("y = (x-2)^2", color=BLUE, font_size=36)
        eq_horizontal.move_to(eq_display.get_center())
        # Update explanation text
        new_explanation = Text("Horizontal shift: replace x with (x-2)", color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(explanation_text.get_center())
        self.play(
            ReplacementTransform(eq_display, eq_horizontal),
            ReplacementTransform(explanation_text, new_explanation)
        )
        eq_display = eq_horizontal
        explanation_text = new_explanation
        self.objects["eq_display"] = eq_display
        self.objects["explanation_text"] = explanation_text
        # Signal action: Circumscribe equation
        self.play(Circumscribe(eq_display, color=YELLOW, run_time=1))
        # Visual action: Transform parabola horizontally
        # We need an intermediate parabola (shifted right by 2, but not down)
        intermediate_parabola = axes.plot(lambda x: (x-2)**2, x_range=[0, 4], color=BLUE, stroke_width=3)
        self.play(ReplacementTransform(parent_parabola, intermediate_parabola))
        parent_parabola = intermediate_parabola
        self.objects["parent_parabola"] = parent_parabola
        remaining = step["duration"] - 5.0  # Approx time for transforms and circumscribe
        if remaining > 0:
            self.wait(remaining)

        # Step 4: Vertical shift
        step = sequence[3]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update equation display to final form
        eq_final = MathTex("y = (x-2)^2 - 3", color=GREEN, font_size=36)
        eq_final.move_to(eq_display.get_center())
        # Update explanation text
        new_explanation = Text("Vertical shift: subtract 3", color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(explanation_text.get_center())
        self.play(
            ReplacementTransform(eq_display, eq_final),
            ReplacementTransform(explanation_text, new_explanation)
        )
        eq_display = eq_final
        explanation_text = new_explanation
        self.objects["eq_display"] = eq_display
        self.objects["explanation_text"] = explanation_text
        # Signal action: Indicate transformed parabola (which we will create via transform)
        # We'll indicate the final parabola after transforming.
        # Visual action: Transform to final parabola
        self.play(ReplacementTransform(parent_parabola, transformed_parabola))
        parent_parabola = transformed_parabola
        self.objects["parent_parabola"] = parent_parabola
        # Now indicate the final parabola
        self.play(Indicate(transformed_parabola, color=GREEN))
        remaining = step["duration"] - 5.0  # Approx time for transforms and indicate
        if remaining > 0:
            self.wait(remaining)

        # Step 5: Mark vertex and draw axis
        step = sequence[4]
        audio_file = step["audio_path"]
        if audio_file and os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Update explanation text
        new_explanation = Text("Vertex at (2,-3), axis of symmetry x=2", color=LIGHT_GRAY, font_size=24)
        new_explanation.move_to(explanation_text.get_center())
        self.play(ReplacementTransform(explanation_text, new_explanation))
        explanation_text = new_explanation
        self.objects["explanation_text"] = explanation_text
        # Signal action: Indicate final vertex
        self.play(Indicate(final_vertex, color=RED))
        # Visual action: Create final vertex dot
        self.play(Create(final_vertex))
        # Also create vertex label and axis of symmetry (implied by narrative)
        self.play(Write(vertex_label), Create(axis_symmetry))
        remaining = step["duration"] - 5.0  # Approx time for indicate, create, write
        if remaining > 0:
            self.wait(remaining)

        # Final pause
        self.wait(2)