from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # Title
        title = Text("Corresponding Interior Angles & Congruence", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # Parallel lines p and q
        line_p = Line(start=[-4, 1.5, 0], end=[4, 1.5, 0], color=BLUE, stroke_width=3)
        line_p.move_to(diagram_center + UP*1.5)
        self.objects["line_p"] = line_p
        
        line_q = Line(start=[-4, -1.5, 0], end=[4, -1.5, 0], color=BLUE, stroke_width=3)
        line_q.move_to(diagram_center + DOWN*1.5)
        self.objects["line_q"] = line_q
        
        # Transversal line t
        line_t = Line(start=[-4, 2.5, 0], end=[4, -2.5, 0], color=RED, stroke_width=3)
        line_t.move_to(diagram_center)
        self.objects["line_t"] = line_t
        
        # Labels for lines
        label_p = MathTex("p", color=BLUE)
        label_p.next_to(line_p, RIGHT, buff=0.2)
        self.objects["label_p"] = label_p
        
        label_q = MathTex("q", color=BLUE)
        label_q.next_to(line_q, RIGHT, buff=0.2)
        self.objects["label_q"] = label_q
        
        label_t = MathTex("t", color=RED)
        label_t.next_to(line_t.get_end(), RIGHT+UP, buff=0.1)
        self.objects["label_t"] = label_t
        
        # Intersection points P and Q
        point_P = Dot(point=[-2.4, 1.5, 0], color=WHITE, radius=0.06)
        self.objects["point_P"] = point_P
        
        point_Q = Dot(point=[2.4, -1.5, 0], color=WHITE, radius=0.06)
        self.objects["point_Q"] = point_Q
        
        # Labels for points
        label_P = MathTex("P", color=WHITE, font_size=24)
        label_P.next_to(point_P, UP+LEFT, buff=0.15)
        self.objects["label_P"] = label_P
        
        label_Q = MathTex("Q", color=WHITE, font_size=24)
        label_Q.next_to(point_Q, DOWN+RIGHT, buff=0.15)
        self.objects["label_Q"] = label_Q
        
        # Parallel symbols
        parallel_symbol_1 = MathTex(r"\parallel", color=YELLOW, font_size=30)
        parallel_symbol_1.next_to(line_p.get_center(), LEFT, buff=0.5)
        self.objects["parallel_symbol_1"] = parallel_symbol_1
        
        parallel_symbol_2 = MathTex(r"\parallel", color=YELLOW, font_size=30)
        parallel_symbol_2.next_to(line_q.get_center(), LEFT, buff=0.5)
        self.objects["parallel_symbol_2"] = parallel_symbol_2
        
        # Explanation text
        explanation_text = Text("If lines are parallel, corresponding angles are congruent.", font_size=28, color=YELLOW)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # Create angle arcs (will be positioned correctly later)
        # Angle at P between line_p and line_t
        angle_arc_1 = Angle(line1=line_p, line2=line_t, radius=0.4, other_angle=False, color=WHITE, stroke_width=2)
        # Move vertex to intersection point P
        angle_arc_1.move_to(point_P.get_center())
        self.objects["angle_arc_1"] = angle_arc_1
        
        # Angle at Q between line_t and line_q
        angle_arc_2 = Angle(line1=line_t, line2=line_q, radius=0.4, other_angle=False, color=WHITE, stroke_width=2)
        # Move vertex to intersection point Q
        angle_arc_2.move_to(point_Q.get_center())
        self.objects["angle_arc_2"] = angle_arc_2
        
        # Angle copy (will be positioned at P initially)
        angle_copy = Angle(line1=line_p, line2=line_t, radius=0.4, other_angle=False, color=GREEN, stroke_width=3)
        angle_copy.set_fill(color=GREEN, opacity=0.3)
        # Move vertex to intersection point P
        angle_copy.move_to(point_P.get_center())
        self.objects["angle_copy"] = angle_copy
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # Step 1
        audio_step1 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_p"]), run_time=1.5)
        remaining_1 = max(0.1, 6.84 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Step 2
        self.play(Create(self.objects["line_q"]), run_time=1.0)
        remaining_2 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Step 3
        self.play(Create(self.objects["line_t"]), run_time=1.0)
        remaining_3 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Step 4
        audio_step4 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Create labels and parallel symbols
        self.play(
            Write(self.objects["label_p"]),
            Write(self.objects["label_q"]),
            Write(self.objects["label_t"]),
            Write(self.objects["parallel_symbol_1"]),
            Write(self.objects["parallel_symbol_2"]),
            Create(self.objects["point_P"]),
            Create(self.objects["point_Q"]),
            Write(self.objects["label_P"]),
            Write(self.objects["label_Q"]),
            run_time=2.5
        )
        remaining_4 = max(0.1, 5.256 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Step 5
        audio_step5 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_P"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["angle_arc_1"]), run_time=2.0)
        remaining_5 = max(0.1, 12.96 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Step 6
        self.play(Indicate(self.objects["point_Q"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["angle_arc_2"]), run_time=1.0)
        remaining_6 = max(0.1, 2.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Step 7
        audio_step7 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        angle_arc_1_green = self.objects["angle_arc_1"].copy()
        angle_arc_1_green.set_color(GREEN)
        self.play(Transform(self.objects["angle_arc_1"], angle_arc_1_green), run_time=1.5)
        remaining_7 = max(0.1, 4.848 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # Step 8
        angle_arc_2_green = self.objects["angle_arc_2"].copy()
        angle_arc_2_green.set_color(GREEN)
        self.play(Transform(self.objects["angle_arc_2"], angle_arc_2_green), run_time=1.0)
        remaining_8 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # Step 9
        audio_step9 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["explanation_text"]), run_time=2.0)
        remaining_9 = max(0.1, 6.96 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Step 10
        audio_step10 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_arc_1"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["angle_copy"]), run_time=2.0)
        remaining_10 = max(0.1, 8.52 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # Step 11
        audio_step11 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_P"], color=ORANGE, run_time=1))
        # Translate angle_copy from P to Q
        angle_copy_at_Q = self.objects["angle_copy"].copy()
        # Position it at Q (maintaining same orientation relative to transversal)
        # We need to calculate the translation vector
        translation_vector = self.objects["point_Q"].get_center() - self.objects["point_P"].get_center()
        angle_copy_at_Q.shift(translation_vector)
        
        self.play(Transform(self.objects["angle_copy"], angle_copy_at_Q), run_time=2.0)
        remaining_11 = max(0.1, 5.616 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # Step 12
        audio_step12 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["angle_arc_2"], color=ORANGE, run_time=1))
        # Rotate angle_copy to match angle_arc_2
        # Create a version of angle_copy that matches angle_arc_2
        angle_copy_rotated = self.objects["angle_arc_2"].copy()
        angle_copy_rotated.set_color(GREEN)
        angle_copy_rotated.set_fill(color=GREEN, opacity=0.3)
        angle_copy_rotated.set_stroke(width=3)
        
        self.play(Transform(self.objects["angle_copy"], angle_copy_rotated), run_time=2.5)
        remaining_12 = max(0.1, 6.096 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_12))
        
        # Step 13
        audio_step13 = "media/audio/畫出平行線與一條截線_用綠色標示出內錯角_3027b6b499/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_copy"], color=YELLOW, run_time=1))
        self.play(FadeOut(self.objects["angle_copy"]), run_time=2.0)
        remaining_13 = max(0.1, 14.04 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_13))
        
        # Final pause
        self.wait(max(0.1, 2))