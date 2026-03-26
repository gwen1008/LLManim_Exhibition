'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the supplementary relationship (α + β = 180°) between co-interior angles formed by a transversal cutting two parallel lines.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title "Parallel Lines and a Transversal"
#    - Main Content: [Center y=0] for the diagram (parallel lines, transversal, angle arcs)
#    - Footer Region: [Bottom y=-3.5] for explanatory text/equation
# 3. Anti-Overlap Check:
#    - Strategy: Use LayoutEngine zones to keep title, diagram, and footer separated.
#    - Angle arcs and labels are positioned relative to line intersections, ensuring they don't overlap.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/{topic_safe_name}/step_XX.mp3" - will use step number to construct path.
# 5. Animation Flow:
#    - Create parallel lines and transversal.
#    - Add parallel symbols.
#    - Show initial explanation text.
#    - Highlight and label the two co-interior angles (α and β).
#    - Transform explanation into the supplementary equation α + β = 180°.
#    - Final emphasis on the equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}  # Registry for all objects

        # Create Layout Engine
        from utils.layout_engine import LayoutEngine, LayoutObject
        layout = LayoutEngine()

        # Define Anchors (as per layout_plan)
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Object: title
        title = Text("Parallel Lines and a Transversal", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # Object: line_p1 (top parallel line)
        line_p1 = Line(start=[-5, 1, 0], end=[5, 1, 0], color=BLUE, stroke_width=4)
        line_p1.move_to(diagram_center + UP)
        self.objects["line_p1"] = line_p1
        obj_line_p1 = LayoutObject(line_p1, "line_p1")
        layout.add(obj_line_p1)
        layout.add_to_zone(obj_line_p1, "CONTENT")

        # Object: line_p2 (bottom parallel line)
        line_p2 = Line(start=[-5, -1, 0], end=[5, -1, 0], color=BLUE, stroke_width=4)
        line_p2.move_to(diagram_center + DOWN)
        self.objects["line_p2"] = line_p2
        obj_line_p2 = LayoutObject(line_p2, "line_p2")
        layout.add(obj_line_p2)
        layout.add_to_zone(obj_line_p2, "CONTENT")

        # Object: line_t (transversal)
        line_t = Line(start=[-4, -1.333, 0], end=[4, 1.333, 0], color=YELLOW, stroke_width=4)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t
        obj_line_t = LayoutObject(line_t, "line_t")
        layout.add(obj_line_t)
        layout.add_to_zone(obj_line_t, "CONTENT")

        # Object: parallel_symbol_1
        parallel_symbol_1 = MathTex(r"\|\|", color=GRAY, font_size=30)
        parallel_symbol_1.next_to(line_p1, RIGHT, buff=0.2)
        self.objects["parallel_symbol_1"] = parallel_symbol_1
        obj_ps1 = LayoutObject(parallel_symbol_1, "parallel_symbol_1")
        layout.add(obj_ps1)
        layout.add_to_zone(obj_ps1, "CONTENT")

        # Object: parallel_symbol_2
        parallel_symbol_2 = MathTex(r"\|\|", color=GRAY, font_size=30)
        parallel_symbol_2.next_to(line_p2, RIGHT, buff=0.2)
        self.objects["parallel_symbol_2"] = parallel_symbol_2
        obj_ps2 = LayoutObject(parallel_symbol_2, "parallel_symbol_2")
        layout.add(obj_ps2)
        layout.add_to_zone(obj_ps2, "CONTENT")

        # Object: angle_arc_alpha
        # Need intersection point of line_t and line_p1 for angle vertex
        # Approximate intersection: line_t goes from (-4, -1.333) to (4, 1.333), line_p1 is y=1.
        # Solve for intersection: param t for line_t: x = -4 + 8t, y = -1.333 + 2.666t. Set y=1 => t ≈ 0.875 => x ≈ 3.0
        # Vertex at approx (3.0, 1.0, 0)
        # We'll create the angle using the Angle class with the two lines.
        # Note: The geometry_def says line1=line_t, line2=line_p1, radius=0.4, other_angle=False.
        # We need to ensure the lines intersect. They do at the point where line_t crosses y=1.
        # Let's create a small segment of line_p1 and line_t near the intersection for the Angle.
        # For simplicity, we'll create the Angle using the full lines; Manim will find the intersection.
        angle_arc_alpha = Angle(line_t, line_p1, radius=0.4, other_angle=False, color=GREEN, stroke_width=6)
        self.objects["angle_arc_alpha"] = angle_arc_alpha
        obj_arc_alpha = LayoutObject(angle_arc_alpha, "angle_arc_alpha")
        layout.add(obj_arc_alpha)
        layout.add_to_zone(obj_arc_alpha, "CONTENT")

        # Object: angle_label_alpha
        angle_label_alpha = MathTex(r"\alpha", color=GREEN, font_size=30)
        # Position next to the arc's midpoint
        arc_mid_alpha = angle_arc_alpha.point_from_proportion(0.5)
        angle_label_alpha.next_to(arc_mid_alpha, UR, buff=0.15)
        self.objects["angle_label_alpha"] = angle_label_alpha
        obj_label_alpha = LayoutObject(angle_label_alpha, "angle_label_alpha")
        layout.add(obj_label_alpha)
        layout.add_to_zone(obj_label_alpha, "CONTENT")

        # Object: angle_arc_beta
        # geometry_def: line1=line_p2, line2=line_t, radius=0.4, other_angle=False
        angle_arc_beta = Angle(line_p2, line_t, radius=0.4, other_angle=False, color=GREEN, stroke_width=6)
        self.objects["angle_arc_beta"] = angle_arc_beta
        obj_arc_beta = LayoutObject(angle_arc_beta, "angle_arc_beta")
        layout.add(obj_arc_beta)
        layout.add_to_zone(obj_arc_beta, "CONTENT")

        # Object: angle_label_beta
        angle_label_beta = MathTex(r"\beta", color=GREEN, font_size=30)
        arc_mid_beta = angle_arc_beta.point_from_proportion(0.5)
        angle_label_beta.next_to(arc_mid_beta, UL, buff=0.15)
        self.objects["angle_label_beta"] = angle_label_beta
        obj_label_beta = LayoutObject(angle_label_beta, "angle_label_beta")
        layout.add(obj_label_beta)
        layout.add_to_zone(obj_label_beta, "CONTENT")

        # Object: eq_initial
        eq_initial = MathTex(r"\alpha,\ \beta = \text{Interior angles on the same side}", color=WHITE, font_size=30)
        eq_initial.move_to(explanation_anchor)
        self.objects["eq_initial"] = eq_initial
        obj_eq_initial = LayoutObject(eq_initial, "eq_initial")
        layout.add(obj_eq_initial)
        layout.add_to_zone(obj_eq_initial, "FOOTER")
        layout.add_constraint(obj_eq_initial.center_x == 0)

        # Object: eq_supplementary
        eq_supplementary = MathTex(r"\alpha + \beta = 180^\circ", color=GREEN, font_size=36)
        eq_supplementary.move_to(explanation_anchor)
        self.objects["eq_supplementary"] = eq_supplementary
        obj_eq_supp = LayoutObject(eq_supplementary, "eq_supplementary")
        layout.add(obj_eq_supp)
        layout.add_to_zone(obj_eq_supp, "FOOTER")
        layout.add_constraint(obj_eq_supp.center_x == 0)

        # Solve layout constraints
        layout.solve()

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        # Step 1
        step = 1
        narrative = "Let's start with two parallel lines and a transversal cutting across them."
        # Audio
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Visual Action
        self.play(Create(self.objects["line_p1"]))
        animation_time = 1.5  # run_time for Create
        remaining = 1.5 - animation_time + 0.5  # duration - animation_time + buffer
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = 2
        narrative = ""
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        self.play(Create(self.objects["line_p2"]))
        animation_time = 1.5
        remaining = 1.5 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = 3
        narrative = "Now, we add a transversal, which is a line that intersects both parallel lines."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        self.play(Create(self.objects["line_t"]))
        animation_time = 2.0
        remaining = 2.0 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = 4
        narrative = "We mark the lines as parallel using the standard symbol."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Signal Action
        self.play(Indicate(self.objects["parallel_symbol_1"], color=GRAY))
        # Visual Action
        self.play(Write(self.objects["parallel_symbol_1"]))
        animation_time = 1.0 + 1.0  # Indicate run_time default 1, Write run_time default 1
        remaining = 1.5 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = 5
        narrative = ""
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        self.play(Write(self.objects["parallel_symbol_2"]))
        animation_time = 1.0
        remaining = 1.5 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = 6
        narrative = "We are interested in a specific pair: the interior angles on the same side of the transversal. Let's highlight them in green."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Signal Action
        self.play(Circumscribe(self.objects["eq_initial"], color=YELLOW, run_time=1))
        # Visual Action
        self.play(Write(self.objects["eq_initial"]))
        animation_time = 1.0 + 1.0  # Circumscribe run_time=1, Write default 1
        remaining = 3.0 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        step = 7
        narrative = "This angle, where the transversal meets the top line, we'll call alpha."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Signal Action
        self.play(Indicate(self.objects["angle_arc_alpha"], color=GREEN))
        # Visual Action
        self.play(Create(self.objects["angle_arc_alpha"]))
        animation_time = 1.0 + 1.0  # Indicate default 1, Create default 1
        remaining = 2.0 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 8
        step = 8
        narrative = ""
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        self.play(Write(self.objects["angle_label_alpha"]))
        animation_time = 1.0
        remaining = 1.5 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 9
        step = 9
        narrative = "And this angle, on the same side of the transversal but where it meets the bottom line, we'll call beta."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Signal Action
        self.play(Indicate(self.objects["angle_arc_beta"], color=GREEN))
        # Visual Action
        self.play(Create(self.objects["angle_arc_beta"]))
        animation_time = 1.0 + 1.0
        remaining = 2.0 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 10
        step = 10
        narrative = ""
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        self.play(Write(self.objects["angle_label_beta"]))
        animation_time = 1.0
        remaining = 1.5 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 11
        step = 11
        narrative = "For parallel lines cut by a transversal, these co-interior angles have a special relationship. They are not congruent, but supplementary."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Signal Action
        self.play(Indicate(self.objects["angle_label_alpha"], color=GREEN))
        # Visual Action: ReplacementTransform from eq_initial to eq_supplementary
        self.play(ReplacementTransform(self.objects["eq_initial"], self.objects["eq_supplementary"]))
        animation_time = 1.0 + 1.0  # Indicate default 1, ReplacementTransform default 1
        remaining = 4.0 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 12
        step = 12
        narrative = "Their measures add up to 180 degrees. This is a key property of parallel lines."
        audio_file = f"media/audio/step_{step-1:02d}.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        else:
            wav_file = f"media/audio/step_{step-1:02d}.wav"
            if os.path.exists(wav_file):
                self.add_sound(wav_file)
        # Signal Action
        self.play(Circumscribe(self.objects["eq_supplementary"], color=YELLOW, run_time=1))
        # Visual Action: Wait (no animation)
        animation_time = 1.0  # Circumscribe run_time=1
        remaining = 3.0 - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final hold
        self.wait(max(0.1, 1))