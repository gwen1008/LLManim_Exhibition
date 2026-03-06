'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Prove that alternate interior angles (∠3 and ∠7) are equal when two parallel lines are cut by a transversal.
# 2. Layout Strategy: Left-Right split with zones.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] Left for diagram, Right for proof equations.
#    - Footer Region: [Bottom y=-3.5] for explanatory text.
# 3. Anti-Overlap Check: Use LayoutEngine to place Title (HEADER), Diagram & Proof (CONTENT), and Explanation (FOOTER) in separate zones to prevent collision.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_XX.mp3"
# 5. Animation Flow: Draw diagram → Highlight green angles → Show properties → Derive equality → Visual congruence animation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}  # Registry for all objects

        # Create objects from layout_plan.objects
        # Title
        title = Text("Parallel Lines & Transversal: Angle Equality", color=WHITE, font_size=40)
        self.objects["title"] = title

        # Diagram Lines
        line_l1 = Line(start=[-4, 1.5, 0], end=[4, 1.5, 0], color=BLUE, stroke_width=3)
        self.objects["line_l1"] = line_l1
        line_l2 = Line(start=[-4, -1.5, 0], end=[4, -1.5, 0], color=BLUE, stroke_width=3)
        self.objects["line_l2"] = line_l2
        line_t = Line(start=[-3, 2.5, 0], end=[3, -2.5, 0], color=YELLOW, stroke_width=3)
        self.objects["line_t"] = line_t

        # Angle Arcs (will be positioned after lines are added to scene)
        # We'll create them later in step 1 after lines are created.

        # Labels for angles (will be positioned after arcs)
        label_1 = MathTex("1", color=WHITE, font_size=24)
        self.objects["label_1"] = label_1
        label_3 = MathTex("3", color=GREEN, font_size=24)
        self.objects["label_3"] = label_3
        label_5 = MathTex("5", color=WHITE, font_size=24)
        self.objects["label_5"] = label_5
        label_7 = MathTex("7", color=GREEN, font_size=24)
        self.objects["label_7"] = label_7

        # Proof Text and Equations
        prop1_text = Text("Corresponding angles are equal:", color=GRAY_B, font_size=28)
        self.objects["prop1_text"] = prop1_text
        prop1_eq = MathTex(r"\angle 1 = \angle 5", color=BLUE, font_size=36)
        self.objects["prop1_eq"] = prop1_eq
        prop2_text = Text("Interior angles on same side are supplementary:", color=GRAY_B, font_size=28)
        self.objects["prop2_text"] = prop2_text
        prop2_eq = MathTex(r"\angle 3 + \angle 5 = 180^\circ", color=ORANGE, font_size=36)
        self.objects["prop2_eq"] = prop2_eq
        proof_step1 = MathTex(r"\angle 3 + \angle 5 = 180^\circ", color=ORANGE, font_size=36)
        self.objects["proof_step1"] = proof_step1
        proof_step2 = MathTex(r"\angle 5 + \angle 7 = 180^\circ", color=PINK, font_size=36)
        self.objects["proof_step2"] = proof_step2
        proof_step3 = MathTex(r"\angle 3 = \angle 7", color=GREEN, font_size=42)
        self.objects["proof_step3"] = proof_step3
        explanation_text = Text("Since both ∠3 and ∠7 are supplementary to ∠5, they must be equal.", color=GRAY_B, font_size=30)
        self.objects["explanation_text"] = explanation_text

        # ========== LAYOUT ENGINE ==========
        from utils.layout_engine import LayoutEngine, LayoutObject
        layout = LayoutEngine()

        # Register objects with layout
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        # Diagram group (left side)
        diagram_group = VGroup(line_l1, line_l2, line_t)
        obj_diagram = LayoutObject(diagram_group, "diagram")
        layout.add(obj_diagram)
        layout.add_to_zone(obj_diagram, "CONTENT")
        layout.add_constraint(obj_diagram.center_x == -3)  # Left of center
        layout.add_constraint(obj_diagram.center_y == 0)

        # Proof group (right side)
        proof_group = VGroup(prop1_text, prop1_eq, prop2_text, prop2_eq, proof_step1, proof_step2, proof_step3)
        proof_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        # Adjust buff for specific elements
        prop1_eq.next_to(prop1_text, DOWN, buff=0.3)
        prop2_text.next_to(prop1_eq, DOWN, buff=0.8)
        prop2_eq.next_to(prop2_text, DOWN, buff=0.3)
        proof_step1.next_to(prop2_eq, DOWN, buff=1.0)
        proof_step2.next_to(proof_step1, DOWN, buff=0.3)
        proof_step3.next_to(proof_step2, DOWN, buff=0.3)

        obj_proof = LayoutObject(proof_group, "proof")
        layout.add(obj_proof)
        layout.add_to_zone(obj_proof, "CONTENT")
        layout.add_constraint(obj_proof.center_x == 3)  # Right of center
        layout.add_constraint(obj_proof.center_y == 0)

        # Explanation
        obj_explanation = LayoutObject(explanation_text, "explanation")
        layout.add(obj_explanation)
        layout.add_to_zone(obj_explanation, "FOOTER")
        layout.add_constraint(obj_explanation.center_x == 0)

        # Solve layout
        layout.solve()

        # Apply positions from layout
        title.move_to(obj_title.get_center())
        diagram_group.move_to(obj_diagram.get_center())
        proof_group.move_to(obj_proof.get_center())
        explanation_text.move_to(obj_explanation.get_center())

        # Angle arcs depend on lines, create them after layout
        # Intersection points (approximate from line definitions)
        # line_t intersects line_l1 at A, line_l2 at B
        # We'll calculate intersections manually for simplicity
        # line_l1: y = 1.5, line_t: from (-3,2.5) to (3,-2.5) slope = -5/6
        # Solve for intersection A: y = 1.5, x such that point lies on line_t
        # Parametric: x = -3 + t*6, y = 2.5 - t*5, set y=1.5 => t = (2.5-1.5)/5 = 0.2
        # x_A = -3 + 0.2*6 = -1.8, y_A = 1.5
        A = np.array([-1.8, 1.5, 0])
        # Intersection B: line_l2: y = -1.5
        # t = (2.5 - (-1.5))/5 = 4/5 = 0.8
        # x_B = -3 + 0.8*6 = 1.8, y_B = -1.5
        B = np.array([1.8, -1.5, 0])

        # Create angle arcs using Angle class (requires lines as Mobjects)
        # We'll create temporary lines from intersection points for Angle to use
        # For angle at A between line_t and line_l1
        # line_t direction at A: from A to B direction? Actually line_t direction vector
        t_vec = line_t.get_end() - line_t.get_start()  # (6, -5, 0)
        t_vec = t_vec / np.linalg.norm(t_vec)
        l1_vec = line_l1.get_end() - line_l1.get_start()  # (8, 0, 0)
        l1_vec = l1_vec / np.linalg.norm(l1_vec)

        # Create line segments at intersection A for Angle class
        line_t_at_A = Line(A, A + t_vec, color=YELLOW, stroke_width=3)
        line_l1_at_A = Line(A, A + l1_vec, color=BLUE, stroke_width=3)
        angle_1 = Angle(line_t_at_A, line_l1_at_A, radius=0.4, color=WHITE, stroke_width=2)
        self.objects["angle_1"] = angle_1
        angle_3 = Angle(line_l1_at_A, line_t_at_A, radius=0.4, other_angle=True, color=WHITE, stroke_width=2)  # will be colored green later
        self.objects["angle_3"] = angle_3

        # For angle at B between line_t and line_l2
        l2_vec = line_l2.get_end() - line_l2.get_start()  # (8, 0, 0)
        l2_vec = l2_vec / np.linalg.norm(l2_vec)
        line_t_at_B = Line(B, B + t_vec, color=YELLOW, stroke_width=3)
        line_l2_at_B = Line(B, B + l2_vec, color=BLUE, stroke_width=3)
        angle_5 = Angle(line_t_at_B, line_l2_at_B, radius=0.4, color=WHITE, stroke_width=2)
        self.objects["angle_5"] = angle_5
        angle_7 = Angle(line_l2_at_B, line_t_at_B, radius=0.4, other_angle=True, color=WHITE, stroke_width=2)  # will be colored green later
        self.objects["angle_7"] = angle_7

        # Position labels relative to arcs (approximate)
        label_1.next_to(angle_1, UP, buff=0.1)
        label_3.next_to(angle_3, LEFT, buff=0.1)
        label_5.next_to(angle_5, UP, buff=0.1)
        label_7.next_to(angle_7, LEFT, buff=0.1)

        # Initially hide proof and explanation elements
        for obj in [prop1_text, prop1_eq, prop2_text, prop2_eq, proof_step1, proof_step2, proof_step3, explanation_text]:
            obj.set_opacity(0)

        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        step = {
            "step": 1,
            "duration": 6.96,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Create(line_l1), Create(line_l2), Create(line_t), run_time=2)
        self.play(Create(angle_1), Create(angle_3), Create(angle_5), Create(angle_7), run_time=2)
        self.play(Write(label_1), Write(label_3), Write(label_5), Write(label_7), run_time=1.5)
        remaining = step["duration"] - (2 + 2 + 1.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 2
        step = {
            "step": 2,
            "signal_action": {"type": "Circumscribe", "target": "angle_3", "color": "GREEN"},
            "duration": 7.92,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_01.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action"):
            self.play(Circumscribe(self.objects["angle_3"], color=GREEN, run_time=1))
        # Change angle_3 and angle_7 to green
        self.play(
            self.objects["angle_3"].animate.set_color(GREEN).set_stroke(width=4),
            self.objects["angle_7"].animate.set_color(GREEN).set_stroke(width=4),
            run_time=1.5
        )
        # Write property labels and equations (fade in)
        self.play(
            FadeIn(self.objects["prop1_text"], shift=UP*0.5),
            FadeIn(self.objects["prop2_text"], shift=UP*0.5),
            run_time=1.5
        )
        remaining = step["duration"] - (1 + 1.5 + 1.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 3
        step = {
            "step": 3,
            "signal_action": {"type": "Indicate", "target": "prop1_eq", "color": "YELLOW"},
            "duration": 8.448,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_02.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Write prop1_eq
        self.play(Write(self.objects["prop1_eq"]), run_time=1.5)
        if step.get("signal_action"):
            self.play(Indicate(self.objects["prop1_eq"], color=YELLOW), run_time=1.5)
        # Highlight angles 1 and 5 temporarily
        angle1_copy = self.objects["angle_1"].copy().set_color(YELLOW).set_stroke(width=6)
        angle5_copy = self.objects["angle_5"].copy().set_color(YELLOW).set_stroke(width=6)
        self.play(FadeIn(angle1_copy, scale=0.5), FadeIn(angle5_copy, scale=0.5), run_time=1)
        self.wait(max(0.1, 0.5))
        self.play(FadeOut(angle1_copy), FadeOut(angle5_copy), run_time=0.5)
        remaining = step["duration"] - (1.5 + 1.5 + 1 + 0.5 + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 4
        step = {
            "step": 4,
            "signal_action": {"type": "Indicate", "target": "prop2_eq", "color": "YELLOW"},
            "duration": 9.336,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Write prop2_eq
        self.play(Write(self.objects["prop2_eq"]), run_time=1.5)
        if step.get("signal_action"):
            self.play(Indicate(self.objects["prop2_eq"], color=YELLOW), run_time=1.5)
        # Highlight angles 3 and 5 temporarily
        angle3_copy = self.objects["angle_3"].copy().set_color(ORANGE).set_stroke(width=6)
        angle5_copy = self.objects["angle_5"].copy().set_color(ORANGE).set_stroke(width=6)
        self.play(FadeIn(angle3_copy, scale=0.5), FadeIn(angle5_copy, scale=0.5), run_time=1)
        self.wait(max(0.1, 1))
        self.play(FadeOut(angle3_copy), FadeOut(angle5_copy), run_time=0.5)
        remaining = step["duration"] - (1.5 + 1.5 + 1 + 1 + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 5
        step = {
            "step": 5,
            "signal_action": {"type": "Indicate", "target": "proof_step2", "color": "YELLOW"},
            "duration": 7.944,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_04.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Write proof_step1 and proof_step2
        self.play(FadeIn(self.objects["proof_step1"], shift=UP*0.5), run_time=1)
        self.play(FadeIn(self.objects["proof_step2"], shift=UP*0.5), run_time=1)
        if step.get("signal_action"):
            self.play(Indicate(self.objects["proof_step2"], color=YELLOW), run_time=1.5)
        # Highlight angles 5 and 7 temporarily
        angle5_copy = self.objects["angle_5"].copy().set_color(PINK).set_stroke(width=6)
        angle7_copy = self.objects["angle_7"].copy().set_color(PINK).set_stroke(width=6)
        self.play(FadeIn(angle5_copy, scale=0.5), FadeIn(angle7_copy, scale=0.5), run_time=1)
        self.wait(max(0.1, 0.5))
        self.play(FadeOut(angle5_copy), FadeOut(angle7_copy), run_time=0.5)
        remaining = step["duration"] - (1 + 1 + 1.5 + 1 + 0.5 + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 6
        step = {
            "step": 6,
            "signal_action": {"type": "TransformMatchingTex", "target": "proof_step1", "details": "Morph equations"},
            "duration": 7.296,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_05.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Morph proof_step1 and proof_step2 into proof_step3 using TransformMatchingTex
        # We'll create a copy of proof_step1 and proof_step2, transform them to proof_step3
        proof1 = self.objects["proof_step1"]
        proof2 = self.objects["proof_step2"]
        proof3 = self.objects["proof_step3"]
        proof3.set_opacity(1)
        # Use TransformMatchingTex on proof1 to proof3, then fade out proof2
        self.play(TransformMatchingTex(proof1.copy(), proof3, path_arc=90*DEGREES), run_time=2)
        self.play(FadeOut(proof2), run_time=0.5)
        # Write explanation text
        self.play(FadeIn(self.objects["explanation_text"], shift=UP*0.5), run_time=1.5)
        remaining = step["duration"] - (2 + 0.5 + 1.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Step 7
        step = {
            "step": 7,
            "signal_action": {"type": "Indicate", "target": "angle_3", "color": "GREEN"},
            "duration": 5.328,
            "audio_path": "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_06.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action"):
            self.play(Indicate(self.objects["angle_3"], color=GREEN), run_time=1)
        # Create copy of angle_3 and animate it to angle_7
        angle3_copy = self.objects["angle_3"].copy().set_z_index(1)
        angle7_target = self.objects["angle_7"]
        self.play(
            Rotate(angle3_copy, angle=PI, about_point=angle3_copy.get_center()),  # Rotate 180 degrees
            angle3_copy.animate.move_to(angle7_target.get_center()).set_color(GREEN),
            run_time=2
        )
        self.play(FadeOut(angle3_copy), run_time=0.5)
        remaining = step["duration"] - (1 + 2 + 0.5)
        if remaining > 0:
            self.wait(max(0.1, remaining))

        # Final wait
        self.wait(max(0.1, 2))