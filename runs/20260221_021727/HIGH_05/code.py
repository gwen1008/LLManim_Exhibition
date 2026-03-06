from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors based on layout_plan
        title_anchor = 3.5 * UP
        axes_center = ORIGIN  # Slightly above origin is handled by moving the plane
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # Title
        title = Text("Vector Addition: Head-to-Tail Method", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Coordinate System (NumberPlane)
        # Parse geometry_def: "x_range=[-1, 5, 1], y_range=[-1, 4, 1], x_length=10, y_length=8"
        # We'll create a NumberPlane with these parameters
        coordinate_system = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=10,
            y_length=8,
            axis_config={"stroke_opacity": 0.7},
            background_line_style={"stroke_opacity": 0.4}
        )
        coordinate_system.move_to(axes_center)
        self.objects["coordinate_system"] = coordinate_system
        
        # Vector A: start=[0, 0, 0], end=[3, 1, 0]
        vector_a = Arrow(
            start=[0, 0, 0],
            end=[3, 1, 0],
            color=BLUE,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        vector_a.move_to(axes_center)  # The start point is at axes_center
        self.objects["vector_a"] = vector_a
        
        # Label A: "\\vec{A} = (3, 1)"
        label_a = MathTex(r"\vec{A} = (3, 1)", color=BLUE, font_size=28)
        # Position will be set relative to vector_a later (after vector_a is created)
        self.objects["label_a"] = label_a
        
        # Vector B: start=[3, 1, 0], end=[4, 3, 0]
        vector_b = Arrow(
            start=[3, 1, 0],
            end=[4, 3, 0],
            color=GREEN,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        vector_b.move_to(axes_center)  # The start point is offset, but we move the whole arrow to origin then shift?
        # Actually, Arrow start/end are absolute. We'll create it at origin then shift.
        # Let's create it with correct start/end relative to axes_center.
        vector_b_start = axes_center + np.array([3, 1, 0])
        vector_b_end = axes_center + np.array([4, 3, 0])
        vector_b = Arrow(
            start=vector_b_start,
            end=vector_b_end,
            color=GREEN,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["vector_b"] = vector_b
        
        # Label B: "\\vec{B} = (1, 2)"
        label_b = MathTex(r"\vec{B} = (1, 2)", color=GREEN, font_size=28)
        self.objects["label_b"] = label_b
        
        # Vector C: start=[0, 0, 0], end=[4, 3, 0]
        vector_c_start = axes_center + np.array([0, 0, 0])
        vector_c_end = axes_center + np.array([4, 3, 0])
        vector_c = Arrow(
            start=vector_c_start,
            end=vector_c_end,
            color=YELLOW,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.15
        )
        self.objects["vector_c"] = vector_c
        
        # Label C: "\\vec{C} = \\vec{A} + \\vec{B} = (4, 3)"
        label_c = MathTex(r"\vec{C} = \vec{A} + \vec{B} = (4, 3)", color=YELLOW, font_size=32)
        self.objects["label_c"] = label_c
        
        # Component display in footer
        component_display = MathTex(r"\vec{A} + \vec{B} = (3,1) + (1,2) = (3+1, 1+2)", color=WHITE, font_size=32)
        component_display.move_to(footer_anchor)
        self.objects["component_display"] = component_display
        
        # Result display below component
        result_display = MathTex(r"= (4, 3)", color=YELLOW, font_size=32)
        result_display.next_to(component_display, DOWN, buff=0.3)
        self.objects["result_display"] = result_display
        
        # Now set positions that depend on other objects
        label_a.next_to(vector_a.get_center(), UP + LEFT, buff=0.2)
        label_b.next_to(vector_b.get_center(), RIGHT, buff=0.2)
        label_c.next_to(vector_c.get_center(), DOWN + RIGHT, buff=0.3)
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        step = {
            "step": 1,
            "duration": 7.2,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_00.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(FadeIn(self.objects["title"]))
        animation_time = 1.0  # Approximate run_time for FadeIn
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 2
        step = {
            "step": 2,
            "duration": 5.976,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_01.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Create(self.objects["coordinate_system"]))
        animation_time = 2.0
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 3
        step = {
            "step": 3,
            "duration": 4.008,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_02.mp3",
            "signal_action": {"type": "Indicate", "target": "vector_a", "color": "BLUE"}
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(GrowArrow(self.objects["vector_a"]))
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            if signal["type"] == "Indicate":
                self.play(Indicate(self.objects["vector_a"], color=BLUE))
        animation_time = 1.5 + 1.0  # GrowArrow + Indicate
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 4
        step = {
            "step": 4,
            "duration": 6.24,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_03.mp3",
            "signal_action": {"type": "Circumscribe", "target": "vector_a.get_end()", "color": "WHITE"}
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        # For Circumscribe target "vector_a.get_end()", we need a Dot at that point
        tip_dot = Dot(self.objects["vector_a"].get_end(), radius=0.05, color=WHITE)
        self.add(tip_dot)  # Add it temporarily for circumscription
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            if signal["type"] == "Circumscribe":
                self.play(Circumscribe(tip_dot, color=WHITE, run_time=1))
        self.play(Write(self.objects["label_a"]))
        self.remove(tip_dot)  # Remove the dot after circumscription
        animation_time = 1.0 + 1.0  # Circumscribe + Write
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 5
        step = {
            "step": 5,
            "duration": 7.536,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_04.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(GrowArrow(self.objects["vector_b"]))
        animation_time = 1.5
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 6
        step = {
            "step": 6,
            "duration": 8.424,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_05.mp3",
            "signal_action": {"type": "Indicate", "target": "label_b", "color": "GREEN"}
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Write(self.objects["label_b"]))
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            if signal["type"] == "Indicate":
                self.play(Indicate(self.objects["label_b"], color=GREEN))
        animation_time = 1.0 + 1.0  # Write + Indicate
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 7
        step = {
            "step": 7,
            "duration": 5.952,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_06.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Write(self.objects["component_display"]))
        animation_time = 1.5
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 8
        step = {
            "step": 8,
            "duration": 5.064,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_07.mp3"
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Write(self.objects["result_display"]))
        animation_time = 1.0
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 9
        step = {
            "step": 9,
            "duration": 7.488,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_08.mp3",
            "signal_action": {"type": "Indicate", "target": "vector_a", "color": "BLUE"}
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            if signal["type"] == "Indicate":
                self.play(Indicate(self.objects["vector_a"], color=BLUE))
        # Create a VGroup of A and B to transform into C
        vectors_ab = VGroup(self.objects["vector_a"], self.objects["vector_b"])
        self.play(ReplacementTransform(vectors_ab, self.objects["vector_c"]))
        # Also fade out labels A and B
        self.play(FadeOut(self.objects["label_a"]), FadeOut(self.objects["label_b"]))
        animation_time = 1.0 + 2.0 + 1.0  # Indicate + Transform + FadeOut
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Step 10
        step = {
            "step": 10,
            "duration": 5.448,
            "audio_path": "media/audio/畫出向量_A__3__1__與_B__1_b0d97556b3/step_09.mp3",
            "signal_action": {"type": "Circumscribe", "target": "vector_c", "color": "YELLOW"}
        }
        if step.get("audio_path") and os.path.exists(step["audio_path"]):
            self.add_sound(step["audio_path"])
        self.play(Write(self.objects["label_c"]))
        if step.get("signal_action") is not None:
            signal = step["signal_action"]
            if signal["type"] == "Circumscribe":
                self.play(Circumscribe(self.objects["vector_c"], color=YELLOW, run_time=1))
        animation_time = 1.0 + 1.0  # Write + Circumscribe
        remaining = max(0.1, step["duration"] - animation_time)
        if remaining > 0:
            self.wait(max(0.1, remaining))
        
        # Final hold
        self.wait(max(0.1, 2))