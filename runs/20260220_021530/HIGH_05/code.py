'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize vector addition using the head-to-tail method and connect it to the Pythagorean theorem for magnitude calculation.
# 2. Layout Strategy: Use LayoutEngine for a three-zone layout.
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for coordinate axes, vectors, and triangles
#    - Footer Region: [Bottom y=-3.5] for vector equations and magnitude calculations
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep Header, Content, and Footer separate. Use VGroups for vector+label pairs.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_XX.mp3"
# 5. Animation Flow: Draw axes -> Vector A and its triangle -> Vector B -> Resultant Vector C -> Show vector equations -> Show magnitude calculations.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for all objects
        self.objects = {}

        # Initialize Layout Engine
        layout = LayoutEngine()

        # --- Create Objects from layout_plan ---
        # 1. Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"stroke_opacity": 0.7},
            background_line_style={"stroke_opacity": 0.4}
        )
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))

        # 2. Vector A and its components
        vector_a = Arrow(start=[0, 0, 0], end=[3, 1, 0], color=BLUE, stroke_width=6, buff=0)
        self.objects["vector_a"] = vector_a
        layout.add(LayoutObject(vector_a, "vector_a"))

        label_a = MathTex(r"\vec{A} = (3, 1)", color=BLUE, font_size=36)
        self.objects["label_a"] = label_a
        layout.add(LayoutObject(label_a, "label_a"))

        # Polygon for triangle_a: vertices must be passed as separate arguments
        tri_a_verts = [
            np.array([0, 0, 0]),
            np.array([3, 0, 0]),
            np.array([3, 1, 0])
        ]
        triangle_a = Polygon(*tri_a_verts, color=BLUE, fill_opacity=0.2, stroke_width=2)
        self.objects["triangle_a"] = triangle_a
        layout.add(LayoutObject(triangle_a, "triangle_a"))

        # 3. Vector B and its components
        vector_b = Arrow(start=[3, 1, 0], end=[4, 3, 0], color=GREEN, stroke_width=6, buff=0)
        self.objects["vector_b"] = vector_b
        layout.add(LayoutObject(vector_b, "vector_b"))

        label_b = MathTex(r"\vec{B} = (1, 2)", color=GREEN, font_size=36)
        self.objects["label_b"] = label_b
        layout.add(LayoutObject(label_b, "label_b"))

        tri_b_verts = [
            np.array([3, 1, 0]),
            np.array([4, 1, 0]),
            np.array([4, 3, 0])
        ]
        triangle_b = Polygon(*tri_b_verts, color=GREEN, fill_opacity=0.2, stroke_width=2)
        self.objects["triangle_b"] = triangle_b
        layout.add(LayoutObject(triangle_b, "triangle_b"))

        # 4. Resultant Vector C and its components
        vector_c = Arrow(start=[0, 0, 0], end=[4, 3, 0], color=RED, stroke_width=8, buff=0)
        self.objects["vector_c"] = vector_c
        layout.add(LayoutObject(vector_c, "vector_c"))

        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color=RED, font_size=36)
        self.objects["label_c"] = label_c
        layout.add(LayoutObject(label_c, "label_c"))

        tri_c_verts = [
            np.array([0, 0, 0]),
            np.array([4, 0, 0]),
            np.array([4, 3, 0])
        ]
        triangle_c = Polygon(*tri_c_verts, color=RED, fill_opacity=0.2, stroke_width=2)
        self.objects["triangle_c"] = triangle_c
        layout.add(LayoutObject(triangle_c, "triangle_c"))

        # 5. Title and Step Label (Header Zone)
        title = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=48)
        self.objects["title"] = title
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)

        step_label = Text("Step 1: Draw vector A", color=YELLOW, font_size=32)
        self.objects["step_label"] = step_label
        obj_step = LayoutObject(step_label, "step_label")
        layout.add(obj_step)
        layout.add_to_zone(obj_step, "HEADER")
        layout.align_to(obj_step, obj_title, "BOTTOM", buff=0.5)
        layout.add_constraint(obj_step.center_x == 0)

        # 6. Footer Equations
        footer_eq1 = MathTex(
            r"\vec{A} = (3, 1),\quad \vec{B} = (1, 2),\quad \vec{C} = \vec{A} + \vec{B} = (4, 3)",
            color=WHITE,
            font_size=32
        )
        self.objects["footer_eq1"] = footer_eq1
        obj_footer_eq1 = LayoutObject(footer_eq1, "footer_eq1")
        layout.add(obj_footer_eq1)
        layout.add_to_zone(obj_footer_eq1, "FOOTER")
        layout.add_constraint(obj_footer_eq1.center_x == 0)

        footer_mag = MathTex(
            r"|\vec{A}| = \sqrt{3^2 + 1^2} = \sqrt{10},\quad |\vec{B}| = \sqrt{1^2 + 2^2} = \sqrt{5},\quad |\vec{C}| = \sqrt{4^2 + 3^2} = 5",
            color=WHITE,
            font_size=32
        )
        self.objects["footer_mag"] = footer_mag
        obj_footer_mag = LayoutObject(footer_mag, "footer_mag")
        layout.add(obj_footer_mag)
        layout.add_to_zone(obj_footer_mag, "FOOTER")
        layout.align_to(obj_footer_mag, obj_footer_eq1, "BOTTOM", buff=0.5)
        layout.add_constraint(obj_footer_mag.center_x == 0)

        # Solve the layout constraints
        layout.solve()

        # Apply positions to objects that need relative positioning (labels next to vectors)
        # These are not handled by the layout engine because they depend on other mobjects' positions after layout.
        # We'll position them after the main layout is solved and before animations start.
        # For now, store the intended relationships; we'll apply them just before the respective animation step.

        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        step = {
            "step": 1,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3",
            "duration": 7.656,
            "visual_action": {"type": "Create", "target_id": "axes"}
        }
        if os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Create(axes))
        self.wait(step["duration"] - 1.0)  # Approximate animation runtime

        # Step 2
        step = {
            "step": 2,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3",
            "duration": 5.256,
            "signal_action": {"type": "Circumscribe", "target": "triangle_a", "color": "YELLOW"},
            "visual_action": {"type": "Create", "target_id": "triangle_a"}
        }
        if os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Position label_a relative to vector_a (tip) before animating
        label_a.next_to(vector_a.get_end(), UP+RIGHT, buff=0.2)
        self.play(Create(vector_a), Write(label_a))
        self.play(Create(triangle_a))
        self.play(Circumscribe(triangle_a, color=YELLOW, run_time=1))
        self.wait(step["duration"] - 3.0)  # Approx runtime for creates + circumscribe

        # Step 3
        step = {
            "step": 3,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3",
            "duration": 8.88,
            "signal_action": {"type": "Indicate", "target": "vector_b", "color": "GREEN"},
            "visual_action": {"type": "Create", "target_id": "vector_b"}
        }
        if os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update step label
        new_step_label = Text("Step 2: Draw vector B", color=YELLOW, font_size=32)
        new_step_label.move_to(self.objects["step_label"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label
        # Position label_b
        label_b.next_to(vector_b.get_end(), UP+RIGHT, buff=0.2)
        self.play(Create(vector_b), Write(label_b))
        self.play(Indicate(vector_b, color=GREEN))
        self.wait(step["duration"] - 3.0)

        # Step 4
        step = {
            "step": 4,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3",
            "duration": 7.176,
            "signal_action": {"type": "Indicate", "target": "vector_c", "color": "RED"},
            "visual_action": {"type": "Create", "target_id": "vector_c"}
        }
        if os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update step label
        new_step_label = Text("Step 3: Resultant vector C", color=YELLOW, font_size=32)
        new_step_label.move_to(self.objects["step_label"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label
        # Position label_c
        label_c.next_to(vector_c.get_end(), LEFT+UP, buff=0.3)
        self.play(Create(vector_c), Write(label_c))
        self.play(Indicate(vector_c, color=RED))
        self.wait(step["duration"] - 3.0)

        # Step 5
        step = {
            "step": 5,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3",
            "duration": 12.384,
            "signal_action": {"type": "Circumscribe", "target": "footer_eq1", "color": "YELLOW"},
            "visual_action": {"type": "Write", "target_id": "footer_eq1"}
        }
        if os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update step label
        new_step_label = Text("Step 4: Vector addition", color=YELLOW, font_size=32)
        new_step_label.move_to(self.objects["step_label"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label
        self.play(Write(footer_eq1))
        self.play(Circumscribe(footer_eq1, color=YELLOW, run_time=1))
        self.wait(step["duration"] - 3.0)

        # Step 6
        step = {
            "step": 6,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3",
            "duration": 12.768,
            "signal_action": {"type": "Indicate", "target": "footer_mag", "color": "RED"},
            "visual_action": {"type": "Write", "target_id": "footer_mag"}
        }
        if os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Update step label
        new_step_label = Text("Step 5: Magnitude calculation", color=YELLOW, font_size=32)
        new_step_label.move_to(self.objects["step_label"].get_center())
        self.play(ReplacementTransform(self.objects["step_label"], new_step_label))
        self.objects["step_label"] = new_step_label
        self.play(Write(footer_mag))
        self.play(Indicate(footer_mag, color=RED))
        self.wait(step["duration"] - 3.0)

        # Final pause
        self.wait(2)