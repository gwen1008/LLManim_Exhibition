'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate vector addition via the head-to-tail method and its equivalence to component-wise addition, including magnitude calculation.
# 2. Layout Strategy: Use LayoutEngine to manage zones.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for coordinate plane and vectors
#    - Footer Region: [Bottom y=-3.5] for magnitude calculations
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep title, content, and footer separated. Use relative positioning for vector labels.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_XX.mp3"
# 5. Animation Flow: Show coordinate grid, draw vector A, label it, draw vector B head-to-tail, show its component form, draw resultant C, transform A+B group into C, then show magnitude calculations.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create Layout Engine
        layout = LayoutEngine()
        
        # Create objects from layout_plan
        # Title
        title = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=36)
        obj_title = LayoutObject(title, "title")
        layout.add(obj_title)
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_constraint(obj_title.center_x == 0)
        self.objects["title"] = title
        
        # Axes (NumberPlane)
        axes = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            stroke_opacity=0.5
        )
        obj_axes = LayoutObject(axes, "axes")
        layout.add(obj_axes)
        layout.add_to_zone(obj_axes, "CONTENT")
        layout.add_constraint(obj_axes.center_x == 0)
        layout.add_constraint(obj_axes.center_y == 0)
        self.objects["axes"] = axes
        
        # Vector A
        vector_a = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color=BLUE,
            stroke_width=6,
            buff=0
        )
        obj_vector_a = LayoutObject(vector_a, "vector_a")
        layout.add(obj_vector_a)
        # Position relative to axes center (which is at origin)
        layout.align_to(obj_vector_a, obj_axes, "CENTER")
        self.objects["vector_a"] = vector_a
        
        # Label A
        label_a = MathTex(r"\vec{A} = (3,1)", color=BLUE, font_size=28)
        # Position will be set relative to vector_a after layout solve
        self.objects["label_a"] = label_a
        
        # Vector B (head-to-tail)
        vector_b_tail = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color=GREEN,
            stroke_width=6,
            buff=0
        )
        obj_vector_b_tail = LayoutObject(vector_b_tail, "vector_b_tail")
        layout.add(obj_vector_b_tail)
        layout.align_to(obj_vector_b_tail, obj_axes, "CENTER")
        self.objects["vector_b_tail"] = vector_b_tail
        
        # Label B (head-to-tail)
        label_b_tail = MathTex(r"\vec{B} = (1,2)", color=GREEN, font_size=28)
        self.objects["label_b_tail"] = label_b_tail
        
        # Vector B (component form at origin)
        vector_b_components = Arrow(
            start=[0, 0, 0],
            end=[1, 2, 0],
            color=GREEN,
            stroke_width=4,
            stroke_opacity=0.5,
            buff=0
        )
        obj_vector_b_components = LayoutObject(vector_b_components, "vector_b_components")
        layout.add(obj_vector_b_components)
        layout.align_to(obj_vector_b_components, obj_axes, "CENTER")
        self.objects["vector_b_components"] = vector_b_components
        
        # Label B (components)
        label_b_components = MathTex(r"(1,2)", color=GREEN, font_size=24, opacity=0.7)
        self.objects["label_b_components"] = label_b_components
        
        # Vector C (resultant)
        vector_c = Arrow(
            start=[0, 0, 0],
            end=[4, 3, 0],
            color=ORANGE,
            stroke_width=8,
            buff=0
        )
        obj_vector_c = LayoutObject(vector_c, "vector_c")
        layout.add(obj_vector_c)
        layout.align_to(obj_vector_c, obj_axes, "CENTER")
        self.objects["vector_c"] = vector_c
        
        # Label C
        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4,3)", color=ORANGE, font_size=32)
        self.objects["label_c"] = label_c
        
        # Calculation Title
        calc_title = Text("Magnitudes (Pythagorean Theorem):", color=WHITE, font_size=24)
        obj_calc_title = LayoutObject(calc_title, "calc_title")
        layout.add(obj_calc_title)
        layout.add_to_zone(obj_calc_title, "FOOTER")
        layout.align_to(obj_calc_title, obj_axes, "LEFT")
        self.objects["calc_title"] = calc_title
        
        # Calculation A
        calc_a = MathTex(r"|\vec{A}| = \sqrt{3^2 + 1^2} = \sqrt{10} \approx 3.16", color=BLUE, font_size=24)
        obj_calc_a = LayoutObject(calc_a, "calc_a")
        layout.add(obj_calc_a)
        layout.add_to_zone(obj_calc_a, "FOOTER")
        layout.align_to(obj_calc_a, obj_calc_title, "LEFT")
        layout.align_to(obj_calc_a, obj_calc_title, "BOTTOM", buff=-0.3)
        self.objects["calc_a"] = calc_a
        
        # Calculation B
        calc_b = MathTex(r"|\vec{B}| = \sqrt{1^2 + 2^2} = \sqrt{5} \approx 2.24", color=GREEN, font_size=24)
        obj_calc_b = LayoutObject(calc_b, "calc_b")
        layout.add(obj_calc_b)
        layout.add_to_zone(obj_calc_b, "FOOTER")
        layout.align_to(obj_calc_b, obj_calc_a, "LEFT")
        layout.align_to(obj_calc_b, obj_calc_a, "BOTTOM", buff=-0.2)
        self.objects["calc_b"] = calc_b
        
        # Calculation C
        calc_c = MathTex(r"|\vec{C}| = \sqrt{4^2 + 3^2} = \sqrt{25} = 5", color=ORANGE, font_size=24)
        obj_calc_c = LayoutObject(calc_c, "calc_c")
        layout.add(obj_calc_c)
        layout.add_to_zone(obj_calc_c, "FOOTER")
        layout.align_to(obj_calc_c, obj_calc_b, "LEFT")
        layout.align_to(obj_calc_c, obj_calc_b, "BOTTOM", buff=-0.2)
        self.objects["calc_c"] = calc_c
        
        # Solve layout
        layout.solve()
        
        # Now position labels relative to their vectors (using solved positions)
        label_a.next_to(vector_a.get_end(), RIGHT+UP, buff=0.2)
        label_b_tail.next_to(vector_b_tail.get_end(), RIGHT+UP, buff=0.2)
        label_b_components.next_to(vector_b_components.get_end(), LEFT+DOWN, buff=0.2)
        label_c.next_to(vector_c.get_end(), LEFT+UP, buff=0.3)
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We begin with a 2D coordinate system. Vector A starts at the origin and ends at the point (3,1).",
                "signal_action": None,
                "visual_action": {
                    "type": "Create",
                    "target_id": "axes",
                    "details": "Fade in coordinate grid"
                },
                "duration": 7.848,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Draw vector A, representing the displacement (3,1).",
                "signal_action": {
                    "type": "Indicate",
                    "target": "vector_a",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "vector_a",
                    "details": "Draw blue arrow from (0,0) to (3,1)"
                },
                "duration": 4.536,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Label it. Vector A equals (3,1).",
                "signal_action": None,
                "visual_action": {
                    "type": "Write",
                    "target_id": "label_a",
                    "details": "Write label next to arrowhead"
                },
                "duration": 4.56,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "Now, vector B has components (1,2). We can place its tail at the head of vector A. This is the head-to-tail method.",
                "signal_action": {
                    "type": "Circumscribe",
                    "target": "vector_a.get_end()",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "vector_b_tail",
                    "details": "Draw green arrow from (3,1) to (4,3)"
                },
                "duration": 8.544,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "Label this vector B. Notice it's the same as the vector (1,2) from the origin.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "vector_b_components",
                    "color": "YELLOW"
                },
                "visual_action": [
                    {
                        "type": "Write",
                        "target_id": "label_b_tail",
                        "details": "Write label for B at its head"
                    },
                    {
                        "type": "Create",
                        "target_id": "vector_b_components",
                        "details": "Fade in translucent copy of B at origin for reference"
                    },
                    {
                        "type": "Write",
                        "target_id": "label_b_components",
                        "details": "Write its component label"
                    }
                ],
                "duration": 5.76,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "The sum, or resultant vector C, goes from the tail of A to the head of B. This is vector addition.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "vector_c",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Create",
                    "target_id": "vector_c",
                    "details": "Draw orange dashed arrow from (0,0) to (4,3)"
                },
                "duration": 6.264,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "Now, watch as vectors A and B transform into their sum, vector C, at the origin. This shows the equivalence: (3,1) + (1,2) = (4,3).",
                "signal_action": None,
                "visual_action": {
                    "type": "Transform",
                    "target_id": ["vector_a", "vector_b_tail"],
                    "details": "Morph the group of vectors A and B (in head-to-tail position) into the single vector C at the origin. Use VGroup for the source.",
                    "into_id": "vector_c"
                },
                "duration": 13.2,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_06.mp3"
            },
            {
                "step": 8,
                "narrative": "Finally, we calculate the magnitudes using the Pythagorean theorem on their components.",
                "signal_action": None,
                "visual_action": {
                    "type": "Write",
                    "target_id": "calc_title",
                    "details": "Write the calculation section title"
                },
                "duration": 5.712,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_07.mp3"
            },
            {
                "step": 9,
                "narrative": "For vector A: the square root of 3 squared plus 1 squared.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "calc_a",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "calc_a",
                    "details": "Write calculation for |A|"
                },
                "duration": 4.584,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_08.mp3"
            },
            {
                "step": 10,
                "narrative": "For vector B: the square root of 1 squared plus 2 squared.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "calc_b",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "calc_b",
                    "details": "Write calculation for |B|"
                },
                "duration": 4.464,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_09.mp3"
            },
            {
                "step": 11,
                "narrative": "For the resultant C: the square root of 4 squared plus 3 squared equals 5.",
                "signal_action": {
                    "type": "Indicate",
                    "target": "calc_c",
                    "color": "YELLOW"
                },
                "visual_action": {
                    "type": "Write",
                    "target_id": "calc_c",
                    "details": "Write calculation for |C|"
                },
                "duration": 5.256,
                "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_10.mp3"
            }
        ]
        
        # Process each step
        for step in sequence:
            # Add audio
            audio_file = step.get("audio_path")
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Handle signal action
            signal_action = step.get("signal_action")
            if signal_action is not None:
                signal_type = signal_action["type"]
                target_ref = signal_action["target"]
                color_str = signal_action.get("color", "YELLOW")
                color = eval(color_str)
                
                # Get target object
                if target_ref == "vector_a.get_end()":
                    # Special case: need to create a dot at the endpoint for circumscribe
                    target_point = vector_a.get_end()
                    dot = Dot(target_point, radius=0.1, color=color)
                    self.add(dot)
                    if signal_type == "Circumscribe":
                        self.play(Circumscribe(dot, color=color, run_time=1))
                    self.remove(dot)
                else:
                    target_obj = self.objects.get(target_ref)
                    if target_obj:
                        if signal_type == "Circumscribe":
                            self.play(Circumscribe(target_obj, color=color, run_time=1))
                        elif signal_type == "Indicate":
                            self.play(Indicate(target_obj, color=color))
            
            # Handle visual action
            visual_action = step["visual_action"]
            animation_time = 0
            
            if isinstance(visual_action, list):
                # Multiple visual actions in one step
                for action in visual_action:
                    action_type = action["type"]
                    target_id = action["target_id"]
                    target_obj = self.objects[target_id]
                    
                    if action_type == "Create":
                        self.play(Create(target_obj))
                        animation_time += 1
                    elif action_type == "Write":
                        self.play(Write(target_obj))
                        animation_time += 1
            else:
                # Single visual action
                action_type = visual_action["type"]
                target_id = visual_action.get("target_id")
                
                if action_type == "Create":
                    target_obj = self.objects[target_id]
                    self.play(Create(target_obj))
                    animation_time += 1
                elif action_type == "Write":
                    target_obj = self.objects[target_id]
                    self.play(Write(target_obj))
                    animation_time += 1
                elif action_type == "Transform":
                    # Special case: transform VGroup of A and B into C
                    source_ids = visual_action["target_id"]
                    into_id = visual_action["into_id"]
                    
                    # Create VGroup of source vectors
                    source_objs = [self.objects[vid] for vid in source_ids]
                    source_group = VGroup(*source_objs)
                    
                    target_obj = self.objects[into_id]
                    
                    # First make sure target_obj is not visible yet
                    target_obj.set_opacity(0)
                    self.add(target_obj)
                    
                    # Transform source group into target
                    self.play(Transform(source_group, target_obj))
                    animation_time += 2
                    
                    # Clean up source group
                    self.remove(source_group)
                    target_obj.set_opacity(1)
            
            # Wait for remaining audio duration
            remaining = max(0.1, step["duration"] - animation_time + 0.5)
            if remaining > 0:
                self.wait(max(0.1, remaining))
        
        # Final wait
        self.wait(max(0.1, 2))