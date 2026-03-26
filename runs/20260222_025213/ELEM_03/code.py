from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan
        title_anchor = 3.5 * UP
        construction_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Area and Perimeter of a 4x3 Rectangle", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # start_point (Dot)
        start_point = Dot(radius=0.08, color=YELLOW)
        start_point.move_to(construction_anchor + 2 * LEFT + 1.5 * DOWN)
        self.objects["start_point"] = start_point
        
        # rect_outline (Polygon) - vertices from geometry_def
        # Note: geometry_def is a string list, we parse it.
        # "[(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]"
        # We'll create the polygon but keep it invisible initially.
        rect_vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0)]
        rect_outline = Polygon(*rect_vertices, color=BLUE, stroke_width=3, fill_opacity=0.0)
        rect_outline.move_to(construction_anchor)
        self.objects["rect_outline"] = rect_outline
        
        # grid_lines (VGroup) - vertical lines at x=-1,0,1 and horizontal lines at y=-0.5,0.5,1.5
        # within rectangle bounds: x from -2 to 2, y from -1.5 to 1.5
        grid_lines = VGroup()
        # vertical lines
        for x in [-1, 0, 1]:
            line = Line(start=(x, -1.5, 0), end=(x, 1.5, 0), color="#888888", stroke_width=1)
            grid_lines.add(line)
        # horizontal lines
        for y in [-0.5, 0.5, 1.5]:
            line = Line(start=(-2, y, 0), end=(2, y, 0), color="#888888", stroke_width=1)
            grid_lines.add(line)
        grid_lines.move_to(construction_anchor)
        self.objects["grid_lines"] = grid_lines
        
        # tracer_dot (Dot)
        tracer_dot = Dot(radius=0.1, color=RED)
        tracer_dot.move_to(self.objects["start_point"].get_center())
        tracer_dot.set_z_index(5)
        self.objects["tracer_dot"] = tracer_dot
        
        # step_explanation (Text) - initial content from layout_plan
        step_explanation = Text("Step 1: Start at a point.", color=WHITE, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "duration": 5.832,
            "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_00.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        self.play(Indicate(self.objects["start_point"], color=YELLOW))
        # Visual Action
        self.play(Create(self.objects["start_point"]))
        # Update explanation text (we'll create a new one and transform)
        new_explanation = Text("Step 1: Start at a point.", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Wait for remaining audio
        animation_time = 2.0  # Approximate for Indicate + Create + Transform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        step = {
            "step": 2,
            "duration": 7.992,
            "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_01.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # No signal action
        # Visual Action: Transform the dot into the bottom edge line.
        # We'll create the bottom edge line and replace the dot.
        bottom_edge = Line(start=(-2, -1.5, 0), end=(2, -1.5, 0), color=BLUE, stroke_width=3)
        bottom_edge.move_to(construction_anchor)
        self.play(Transform(self.objects["start_point"], bottom_edge))
        self.objects["start_point"] = bottom_edge  # update reference
        # Update explanation
        new_explanation = Text("Step 2: Draw bottom edge (4 units right).", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Wait
        animation_time = 2.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        step = {
            "step": 3,
            "duration": 9.168,
            "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_02.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # No signal action
        # Visual Action: Create the remaining three sides.
        # We already have the bottom edge. We'll create the other three sides as a group.
        right_side = Line(start=(2, -1.5, 0), end=(2, 1.5, 0), color=BLUE, stroke_width=3)
        top_edge = Line(start=(2, 1.5, 0), end=(-2, 1.5, 0), color=BLUE, stroke_width=3)
        left_side = Line(start=(-2, 1.5, 0), end=(-2, -1.5, 0), color=BLUE, stroke_width=3)
        remaining_sides = VGroup(right_side, top_edge, left_side)
        remaining_sides.move_to(construction_anchor)
        self.play(Create(remaining_sides))
        # Now we have the complete rectangle outline. Let's group them.
        complete_outline = VGroup(self.objects["start_point"], remaining_sides)
        self.objects["rect_outline"] = complete_outline  # update reference
        # Update explanation
        new_explanation = Text("Step 3: Draw remaining sides to close rectangle.", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Wait
        animation_time = 3.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        step = {
            "step": 4,
            "duration": 11.544,
            "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_03.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # Signal Action
        self.play(Circumscribe(self.objects["rect_outline"], color=YELLOW, run_time=1))
        # Visual Action
        self.play(Create(self.objects["grid_lines"]))
        # Update explanation
        new_explanation = Text("Step 4: Add grid to visualize area (12 squares).", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Wait
        animation_time = 3.0
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        step = {
            "step": 5,
            "duration": 8.568,
            "audio_path": "media/audio/畫一個_4x3_的長方形_用填充小方格來_dc1af9b532/step_04.mp3"
        }
        # Audio
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # No signal action
        # Visual Action: Move tracer dot along the rectangle outline.
        # We need to create a path that is the rectangle perimeter.
        # Since rect_outline is a VGroup of lines, we can use a custom path.
        # Let's create a Path that goes through the vertices in order.
        path = VMobject()
        vertices = [(-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0), (-2, -1.5, 0)]
        path.set_points_smoothly([*[np.array(v) for v in vertices]])
        path.move_to(construction_anchor)
        self.add(self.objects["tracer_dot"])
        self.play(MoveAlongPath(self.objects["tracer_dot"], path, rate_func=linear, run_time=4))
        # Update explanation
        new_explanation = Text("Step 5: Trace perimeter (total distance around).", color=WHITE, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        # Wait
        animation_time = 5.0  # 4 for move + 1 for transform
        remaining = step["duration"] - animation_time + 0.5
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))