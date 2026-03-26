from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create objects from layout_plan
        # Title
        title = Text("Area and Perimeter of a 4x3 Rectangle", color=WHITE, font_size=36)
        self.objects["title"] = title
        
        # Vertices (dots)
        vertex_v1 = Dot(point=np.array([-2, -1.5, 0]), color=GREEN, radius=0.08)
        self.objects["vertex_v1"] = vertex_v1
        
        vertex_v2 = Dot(point=np.array([2, -1.5, 0]), color=GREEN, radius=0.08)
        self.objects["vertex_v2"] = vertex_v2
        
        vertex_v3 = Dot(point=np.array([2, 1.5, 0]), color=GREEN, radius=0.08)
        self.objects["vertex_v3"] = vertex_v3
        
        vertex_v4 = Dot(point=np.array([-2, 1.5, 0]), color=GREEN, radius=0.08)
        self.objects["vertex_v4"] = vertex_v4
        
        # Rectangle (Polygon)
        rect_vertices = [
            np.array([-2, -1.5, 0]),
            np.array([2, -1.5, 0]),
            np.array([2, 1.5, 0]),
            np.array([-2, 1.5, 0])
        ]
        rectangle = Polygon(*rect_vertices, color=BLUE, stroke_width=4, fill_opacity=0.0)
        self.objects["rectangle"] = rectangle
        
        # Area Grid (VGroup of 12 squares)
        area_grid = VGroup()
        for col in range(4):
            for row in range(3):
                sq = Square(side_length=1, color="#66BB6A", fill_opacity=0.3, stroke_width=1, stroke_color="#388E3C")
                sq.move_to(np.array([-1.5 + col, -1 + row, 0]))
                area_grid.add(sq)
        self.objects["area_grid"] = area_grid
        
        # Perimeter Line (initially invisible)
        perimeter_line = Polygon(*rect_vertices, color=YELLOW, stroke_width=6, stroke_opacity=0.0)
        self.objects["perimeter_line"] = perimeter_line
        
        # Tracing Dot
        tracing_dot = Dot(point=np.array([-2, -1.5, 0]), color=YELLOW, radius=0.1)
        self.objects["tracing_dot"] = tracing_dot
        
        # Step Explanation (initial text)
        step_explanation = Text("Step 1: Define the rectangle's vertices.", color=GRAY_B, font_size=28)
        self.objects["step_explanation"] = step_explanation
        
        # Setup Layout Engine
        layout = LayoutEngine()
        
        # Register objects as LayoutObjects
        obj_title = LayoutObject(title, "title")
        obj_vertex_v1 = LayoutObject(vertex_v1, "vertex_v1")
        obj_vertex_v2 = LayoutObject(vertex_v2, "vertex_v2")
        obj_vertex_v3 = LayoutObject(vertex_v3, "vertex_v3")
        obj_vertex_v4 = LayoutObject(vertex_v4, "vertex_v4")
        obj_rectangle = LayoutObject(rectangle, "rectangle")
        obj_area_grid = LayoutObject(area_grid, "area_grid")
        obj_perimeter_line = LayoutObject(perimeter_line, "perimeter_line")
        obj_tracing_dot = LayoutObject(tracing_dot, "tracing_dot")
        obj_step_explanation = LayoutObject(step_explanation, "step_explanation")
        
        # Add objects to layout one by one
        layout.add(obj_title)
        layout.add(obj_vertex_v1)
        layout.add(obj_vertex_v2)
        layout.add(obj_vertex_v3)
        layout.add(obj_vertex_v4)
        layout.add(obj_rectangle)
        layout.add(obj_area_grid)
        layout.add(obj_perimeter_line)
        layout.add(obj_tracing_dot)
        layout.add(obj_step_explanation)
        
        # Assign to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_vertex_v1, "CONTENT")
        layout.add_to_zone(obj_vertex_v2, "CONTENT")
        layout.add_to_zone(obj_vertex_v3, "CONTENT")
        layout.add_to_zone(obj_vertex_v4, "CONTENT")
        layout.add_to_zone(obj_rectangle, "CONTENT")
        layout.add_to_zone(obj_area_grid, "CONTENT")
        layout.add_to_zone(obj_perimeter_line, "CONTENT")
        layout.add_to_zone(obj_tracing_dot, "CONTENT")
        layout.add_to_zone(obj_step_explanation, "FOOTER")
        
        # Center content horizontally
        layout.add_constraint(obj_title.center_x == 0)
        layout.add_constraint(obj_step_explanation.center_x == 0)
        
        # Solve layout
        layout.solve()
        
        # Apply positions to mobjects
        title.move_to(obj_title.get_center())
        vertex_v1.move_to(obj_vertex_v1.get_center())
        vertex_v2.move_to(obj_vertex_v2.get_center())
        vertex_v3.move_to(obj_vertex_v3.get_center())
        vertex_v4.move_to(obj_vertex_v4.get_center())
        rectangle.move_to(obj_rectangle.get_center())
        area_grid.move_to(obj_area_grid.get_center())
        perimeter_line.move_to(obj_perimeter_line.get_center())
        tracing_dot.move_to(obj_tracing_dot.get_center())
        step_explanation.move_to(obj_step_explanation.get_center())
        
        # ========== PHASE 2: Animation Sequence ==========
        sequence = [
            {
                "step": 1,
                "narrative": "We start by defining the corners, or vertices, of our rectangle. It has a width of 4 units and a height of 3 units.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "title", "details": "Fade in the title."},
                "duration": 8.568,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
            },
            {
                "step": 2,
                "narrative": "Let's place the four vertices. We'll position them so the rectangle is centered.",
                "signal_action": None,
                "visual_action": {"type": "Create", "target_id": "vertex_v1", "details": "Create the four vertex dots one after the other."},
                "duration": 5.808,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
            },
            {
                "step": 3,
                "narrative": "Now, we connect these vertices to form the edges of the rectangle.",
                "signal_action": {"type": "Indicate", "target": "vertex_v1", "color": "ORANGE"},
                "visual_action": {"type": "Create", "target_id": "rectangle", "details": "Draw the blue rectangle by creating its edges."},
                "duration": 4.536,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
            },
            {
                "step": 4,
                "narrative": "The area inside is 4 times 3, which equals 12 square units. We can visualize this area by filling the rectangle with a grid of unit squares.",
                "signal_action": {"type": "Circumscribe", "target": "rectangle", "color": "PINK"},
                "visual_action": {"type": "Create", "target_id": "area_grid", "details": "Fade in all 12 unit squares simultaneously to represent area."},
                "duration": 10.248,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
            },
            {
                "step": 5,
                "narrative": "The perimeter is the total distance around the boundary. Let's highlight the rectangle's edges to emphasize this path.",
                "signal_action": {"type": "Indicate", "target": "rectangle", "color": "YELLOW"},
                "visual_action": {"type": "Create", "target_id": "tracing_dot", "details": "Place the yellow tracing dot at the starting vertex (bottom-left)."},
                "duration": 7.752,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
            },
            {
                "step": 6,
                "narrative": "Now, watch as we trace the entire perimeter. The dot will travel along the edges, and we'll draw the path behind it.",
                "signal_action": None,
                "visual_action": {"type": "AnimationGroup", "target_id": "perimeter_trace_animation", "details": "Animate the tracing_dot moving along the rectangle's path (MoveAlongPath). Simultaneously, animate the perimeter_line's stroke_opacity from 0 to 1 over the same duration to simulate it being drawn. Use a linear rate function for constant speed. Total path length is 14 units (4+3+4+3). A speed of ~2 units/sec gives a 7-second animation."},
                "duration": 8.16,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_05.mp3"
            },
            {
                "step": 7,
                "narrative": "And there we have it. The area is filled with 12 squares, and the perimeter is this continuous yellow path around the outside.",
                "signal_action": {"type": "Circumscribe", "target": "area_grid", "color": "GREEN"},
                "visual_action": {"type": "Wait", "target_id": None, "details": "Hold the final frame for a moment."},
                "duration": 8.688,
                "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_06.mp3"
            }
        ]
        
        # Process each step
        for step in sequence:
            step_num = step["step"]
            audio_file = step.get("audio_path")
            
            # Add audio if file exists
            if audio_file and os.path.exists(audio_file):
                self.add_sound(audio_file)
            
            # Signal action
            signal = step.get("signal_action")
            if signal is not None:
                target_id = signal["target"]
                target_obj = self.objects[target_id]
                color_str = signal.get("color", "YELLOW")
                color_map = {
                    "YELLOW": YELLOW,
                    "ORANGE": ORANGE,
                    "PINK": PINK,
                    "GREEN": GREEN,
                    "RED": RED,
                    "BLUE": BLUE
                }
                color = color_map.get(color_str, YELLOW)
                
                if signal["type"] == "Circumscribe":
                    self.play(Circumscribe(target_obj, color=color, run_time=1))
                elif signal["type"] == "Indicate":
                    self.play(Indicate(target_obj, color=color))
            
            # Visual action
            visual = step["visual_action"]
            action_type = visual["type"]
            target_id = visual.get("target_id")
            
            if action_type == "Create":
                if target_id == "title":
                    self.play(Write(self.objects["title"]))
                    # Update explanation text for step 1
                    new_explanation = Text("Step 1: Define the rectangle's vertices.", color=GRAY_B, font_size=28)
                    new_explanation.move_to(self.objects["step_explanation"].get_center())
                    self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                    self.objects["step_explanation"] = new_explanation
                    animation_time = 1.0
                elif target_id == "vertex_v1":
                    # Create all four vertices in sequence
                    self.play(Create(self.objects["vertex_v1"]))
                    self.play(Create(self.objects["vertex_v2"]))
                    self.play(Create(self.objects["vertex_v3"]))
                    self.play(Create(self.objects["vertex_v4"]))
                    # Update explanation text for step 2
                    new_explanation = Text("Step 2: Place the four vertices.", color=GRAY_B, font_size=28)
                    new_explanation.move_to(self.objects["step_explanation"].get_center())
                    self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                    self.objects["step_explanation"] = new_explanation
                    animation_time = 4 * 0.5  # 4 vertices, 0.5s each
                elif target_id == "rectangle":
                    self.play(Create(self.objects["rectangle"]))
                    # Update explanation text for step 3
                    new_explanation = Text("Step 3: Connect vertices to form edges.", color=GRAY_B, font_size=28)
                    new_explanation.move_to(self.objects["step_explanation"].get_center())
                    self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                    self.objects["step_explanation"] = new_explanation
                    animation_time = 2.0
                elif target_id == "area_grid":
                    self.play(Create(self.objects["area_grid"], run_time=2))
                    # Update explanation text for step 4
                    new_explanation = Text("Step 4: Fill with unit squares (Area = 12).", color=GRAY_B, font_size=28)
                    new_explanation.move_to(self.objects["step_explanation"].get_center())
                    self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                    self.objects["step_explanation"] = new_explanation
                    animation_time = 2.0
                elif target_id == "tracing_dot":
                    self.play(Create(self.objects["tracing_dot"]))
                    # Update explanation text for step 5
                    new_explanation = Text("Step 5: Perimeter is the boundary path.", color=GRAY_B, font_size=28)
                    new_explanation.move_to(self.objects["step_explanation"].get_center())
                    self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                    self.objects["step_explanation"] = new_explanation
                    animation_time = 1.0
            elif action_type == "AnimationGroup" and target_id == "perimeter_trace_animation":
                # Create the perimeter path (same as rectangle vertices, closed)
                path = Polygon(*rect_vertices, color=YELLOW, stroke_width=6, stroke_opacity=0.0)
                path.move_to(self.objects["perimeter_line"].get_center())
                
                # Animate dot moving along path and line appearing
                trace_time = 7.0  # As per hint: 14 units at ~2 units/sec
                dot_anim = MoveAlongPath(self.objects["tracing_dot"], path, run_time=trace_time, rate_func=linear)
                line_anim = self.objects["perimeter_line"].animate.set_stroke(opacity=1.0).set_run_time(trace_time)
                
                self.play(AnimationGroup(dot_anim, line_anim, lag_ratio=0))
                # Update explanation text for step 6
                new_explanation = Text("Step 6: Trace the perimeter path.", color=GRAY_B, font_size=28)
                new_explanation.move_to(self.objects["step_explanation"].get_center())
                self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                self.objects["step_explanation"] = new_explanation
                animation_time = trace_time
            elif action_type == "Wait":
                # Just hold the frame
                animation_time = 0
                # Update explanation text for final step
                new_explanation = Text("Step 7: Area (squares) and Perimeter (path).", color=GRAY_B, font_size=28)
                new_explanation.move_to(self.objects["step_explanation"].get_center())
                self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation))
                self.objects["step_explanation"] = new_explanation
            
            # Wait for remaining audio duration
            remaining = step["duration"] - animation_time + 0.5
            if remaining > 0:
                self.wait(max(0.1, max(0.1, remaining)))
        
        # Final hold
        self.wait(max(0.1, 2))