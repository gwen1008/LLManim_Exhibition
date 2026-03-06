'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Demonstrate how to use a protractor to measure a 60° angle.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for angle and protractor
#    - Footer Region: [Bottom y=-3.5] for step explanations
# 3. Anti-Overlap Check:
#    - Protractor starts offset (UP*2+RIGHT*2) to avoid overlap with angle.
#    - Step explanation text is at bottom, clear of main content.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/measuring_angle_with_protractor/step_XX.mp3"
# 5. Animation Flow:
#    - Draw angle (rays + arc).
#    - Build protractor components piece-by-piece.
#    - Animate protractor into alignment.
#    - Show measurement line and label.
#    - Fade out protractor, leaving clean angle.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_Manim_anima_7e116f4879/final_narrative.mp3")  # [auto-injected: full narration]
        self.camera.background_color = "#1e1e1e"
        
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors
        title_anchor = 3.5 * UP
        vertex_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        protractor_start_anchor = 2 * UP + 2 * RIGHT
        
        # Object registry
        self.objects = {}
        
        # Create title
        title = Text("Measuring a 60° Angle with a Protractor", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Create ray OA (horizontal)
        ray_oa = Line(start=ORIGIN, end=4 * RIGHT, color=BLUE, stroke_width=4)
        ray_oa.move_to(vertex_anchor, aligned_edge=LEFT)
        self.objects["ray_oa"] = ray_oa
        
        # Create ray OB (60 degrees)
        angle_rad = 60 * DEGREES
        ray_ob_end = np.array([2.0 * np.cos(angle_rad), 2.0 * np.sin(angle_rad), 0])
        ray_ob = Line(start=ORIGIN, end=ray_ob_end, color=BLUE, stroke_width=4)
        ray_ob.move_to(vertex_anchor, aligned_edge=LEFT)
        self.objects["ray_ob"] = ray_ob
        
        # Create angle arc
        angle_arc = Arc(radius=1.5, start_angle=0, angle=angle_rad, color=YELLOW, stroke_width=3)
        angle_arc.move_arc_center_to(vertex_anchor)
        self.objects["angle_arc"] = angle_arc
        
        # Create protractor components
        protractor_radius = 3.5
        protractor_semicircle = Arc(radius=protractor_radius, start_angle=0, angle=180 * DEGREES, color=GRAY_B, stroke_width=2)
        protractor_semicircle.move_to(protractor_start_anchor)
        self.objects["protractor_semicircle"] = protractor_semicircle
        
        protractor_center_dot = Dot(radius=0.05, color=RED, fill_opacity=1.0)
        protractor_center_dot.move_to(protractor_start_anchor)
        self.objects["protractor_center_dot"] = protractor_center_dot
        
        protractor_baseline = Line(start=0.5 * LEFT, end=1.0 * RIGHT, color=RED, stroke_width=2)
        protractor_baseline.move_to(protractor_start_anchor)
        self.objects["protractor_baseline"] = protractor_baseline
        
        # Create protractor scale ticks and labels
        major_ticks = VGroup()
        minor_ticks = VGroup()
        scale_labels = VGroup()
        
        for deg in range(0, 181, 10):
            rad = deg * DEGREES
            start_pt = protractor_radius * np.array([np.cos(rad), np.sin(rad), 0])
            if deg % 10 == 0:
                # Major tick (10°)
                end_pt = (protractor_radius - 0.3) * np.array([np.cos(rad), np.sin(rad), 0])
                tick = Line(start=start_pt, end=end_pt, color=WHITE, stroke_width=1.5)
                major_ticks.add(tick)
                # Label every 10 degrees
                if deg % 30 == 0 or deg == 60 or deg == 90 or deg == 120 or deg == 150:
                    label_pos = (protractor_radius - 0.6) * np.array([np.cos(rad), np.sin(rad), 0])
                    label = Text(str(deg), color=WHITE, font_size=18)
                    label.move_to(label_pos)
                    scale_labels.add(label)
            else:
                # Minor tick (5°)
                end_pt = (protractor_radius - 0.15) * np.array([np.cos(rad), np.sin(rad), 0])
                tick = Line(start=start_pt, end=end_pt, color=WHITE, stroke_width=1)
                minor_ticks.add(tick)
        
        # Group all scale components
        protractor_scale = VGroup(major_ticks, minor_ticks, scale_labels)
        protractor_scale.move_to(protractor_start_anchor)
        self.objects["protractor_scale"] = protractor_scale
        
        # Create protractor VGroup (all components)
        protractor_vgroup = VGroup(protractor_semicircle, protractor_center_dot, protractor_baseline, protractor_scale)
        protractor_vgroup.move_to(protractor_start_anchor)
        self.objects["protractor_vgroup"] = protractor_vgroup
        
        # Create measurement line (dashed)
        measurement_line_end = protractor_radius * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        measurement_line = DashedLine(start=ORIGIN, end=measurement_line_end, color=GREEN, stroke_width=2, dash_length=0.05)
        measurement_line.move_to(vertex_anchor, aligned_edge=LEFT)
        self.objects["measurement_line"] = measurement_line
        
        # Create measurement label
        measurement_label = MathTex("60^\\circ", color=GREEN, font_size=32)
        measurement_label.next_to(measurement_line_end, UR, buff=0.1)
        self.objects["measurement_label"] = measurement_label
        
        # Create step explanation text
        step_explanation = Text("Step 1: Draw the angle.", color=GRAY_B, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        topic_safe_name = "measuring_angle_with_protractor"
        
        # ========== Step 1 ==========
        audio_step1 = f"media/audio/{topic_safe_name}/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), Write(self.objects["step_explanation"]), Create(self.objects["ray_oa"]), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = f"media/audio/{topic_safe_name}/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["ray_oa"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["ray_ob"]), run_time=1.5)
        remaining_2 = max(0.1, 2.5 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = f"media/audio/{topic_safe_name}/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["angle_arc"]), run_time=1.5)
        remaining_3 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = f"media/audio/{topic_safe_name}/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_arc"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["protractor_semicircle"]), run_time=1.5)
        remaining_4 = max(0.1, 2.0 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = f"media/audio/{topic_safe_name}/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Create a dot at vertex for indication
        vertex_dot = Dot(radius=0.05, color=RED, fill_opacity=1.0)
        vertex_dot.move_to(vertex_anchor)
        self.add(vertex_dot)
        self.play(Indicate(vertex_dot, color=RED, run_time=1))
        self.remove(vertex_dot)
        
        self.play(Create(self.objects["protractor_center_dot"]), run_time=1.0)
        remaining_5 = max(0.1, 1.5 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = f"media/audio/{topic_safe_name}/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["ray_oa"], color=RED, run_time=1))
        self.play(Create(self.objects["protractor_baseline"]), run_time=1.0)
        remaining_6 = max(0.1, 1.5 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Add scale to protractor before grouping animation
        self.play(Create(self.objects["protractor_scale"]), run_time=1.0)
        self.wait(max(0.1, 0.5))
        
        # ========== Step 7 ==========
        audio_step7 = f"media/audio/{topic_safe_name}/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        # Update step explanation
        new_explanation = Text("Step 7: Align the protractor.", color=GRAY_B, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], new_explanation))
        self.objects["step_explanation"] = new_explanation
        
        # Create aligned protractor (target position)
        aligned_protractor = self.objects["protractor_vgroup"].copy()
        aligned_protractor.move_to(vertex_anchor)
        # Rotate baseline to match ray OA (which is horizontal)
        # Since baseline is already horizontal in the group, just ensure center is at vertex
        self.play(Transform(self.objects["protractor_vgroup"], aligned_protractor), run_time=2.5)
        remaining_7 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = f"media/audio/{topic_safe_name}/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["protractor_center_dot"], color=RED, run_time=1))
        self.play(Create(self.objects["measurement_line"]), run_time=2.0)
        remaining_8 = max(0.1, 3.0 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = f"media/audio/{topic_safe_name}/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["measurement_line"], color=GREEN, run_time=1))
        self.play(Write(self.objects["measurement_label"]), run_time=1.5)
        remaining_9 = max(0.1, 2.5 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # ========== Step 10 ==========
        audio_step10 = f"media/audio/{topic_safe_name}/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        # Update step explanation
        final_explanation = Text("Step 10: Remove the tool.", color=GRAY_B, font_size=24)
        final_explanation.move_to(explanation_anchor)
        self.play(Transform(self.objects["step_explanation"], final_explanation))
        self.objects["step_explanation"] = final_explanation
        
        self.play(FadeOut(self.objects["protractor_vgroup"]), run_time=1.5)
        remaining_10 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # Final hold
        self.wait(max(0.1, 2))