from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        diagram_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Interior Angles & Parallel Lines", font_size=40, color=WHITE)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # line_parallel1
        line_parallel1 = Line(start=[-4, 1, 0], end=[4, 1, 0], color=BLUE, stroke_width=4)
        line_parallel1.move_to(diagram_center + UP)
        self.objects["line_parallel1"] = line_parallel1
        
        # line_parallel2
        line_parallel2 = Line(start=[-4, -1, 0], end=[4, -1, 0], color=BLUE, stroke_width=4)
        line_parallel2.move_to(diagram_center + DOWN)
        self.objects["line_parallel2"] = line_parallel2
        
        # line_transversal
        line_transversal = Line(start=[-4, -4/3, 0], end=[4, 4/3, 0], color=YELLOW, stroke_width=4)
        line_transversal.move_to(diagram_center)
        self.objects["line_transversal"] = line_transversal
        
        # label_parallel1
        label_parallel1 = MathTex("l", color=BLUE)
        label_parallel1.next_to(line_parallel1.get_end(), RIGHT, buff=0.2)
        self.objects["label_parallel1"] = label_parallel1
        
        # label_parallel2
        label_parallel2 = MathTex("m", color=BLUE)
        label_parallel2.next_to(line_parallel2.get_end(), RIGHT, buff=0.2)
        self.objects["label_parallel2"] = label_parallel2
        
        # label_transversal
        label_transversal = MathTex("t", color=YELLOW)
        label_transversal.next_to(line_transversal.get_end(), UR, buff=0.2)
        self.objects["label_transversal"] = label_transversal
        
        # point_A
        point_A = Dot(point=[3, 1, 0], color=WHITE, radius=0.05)
        self.objects["point_A"] = point_A
        
        # point_B
        point_B = Dot(point=[-3, -1, 0], color=WHITE, radius=0.05)
        self.objects["point_B"] = point_B
        
        # angle_arc_top (will be created after lines exist)
        # angle_arc_bottom (will be created after lines exist)
        # angle_label_top (positioned later)
        angle_label_top = MathTex(r"\angle 1", color=GREEN, font_size=24)
        self.objects["angle_label_top"] = angle_label_top
        
        # angle_label_bottom (positioned later)
        angle_label_bottom = MathTex(r"\angle 2", color=GREEN, font_size=24)
        self.objects["angle_label_bottom"] = angle_label_bottom
        
        # angle_arc_top will be created later in Step 8
        
        # explanation_text
        explanation_text = Text("Consecutive Interior Angles are supplementary. Corresponding Angles are equal.", font_size=28, color=GRAY_B)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # rotation_copy_arc and rotation_copy_label (will be created as copies later)
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_two_parallel_li_68991e7506/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["line_parallel1"]), run_time=1.5)
        remaining_1 = max(0.1, 6.768 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        self.play(Create(self.objects["line_parallel2"]), run_time=1.5)
        remaining_2 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        self.play(Create(self.objects["line_transversal"]), run_time=1.5)
        remaining_3 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_two_parallel_li_68991e7506/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["label_parallel1"]), run_time=1.0)
        remaining_4 = max(0.1, 2.424 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        self.play(Write(self.objects["label_parallel2"]), run_time=1.0)
        remaining_5 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        self.play(Write(self.objects["label_transversal"]), run_time=1.0)
        remaining_6 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/Draw_two_parallel_li_68991e7506/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_A"], color=WHITE, run_time=1))
        self.play(Create(self.objects["point_A"]), run_time=1.0)
        remaining_7 = max(0.1, 8.256 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        # Create angle_arc_top
        angle_arc_top = Angle(line_parallel1, line_transversal, radius=0.5, other_angle=False, color=GREEN, stroke_width=6)
        angle_arc_top.move_to(point_A.get_center())
        self.objects["angle_arc_top"] = angle_arc_top
        
        audio_step8 = "media/audio/Draw_two_parallel_li_68991e7506/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["angle_arc_top"]), run_time=1.5)
        remaining_8 = max(0.1, 2.256 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        # Position angle_label_top
        angle_label_top.next_to(angle_arc_top, UP, buff=0.1)
        
        audio_step9 = "media/audio/Draw_two_parallel_li_68991e7506/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["angle_label_top"]), run_time=1.0)
        remaining_9 = max(0.1, 1.896 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # ========== Step 10 ==========
        audio_step10 = "media/audio/Draw_two_parallel_li_68991e7506/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_B"], color=WHITE, run_time=1))
        self.play(Create(self.objects["point_B"]), run_time=1.0)
        remaining_10 = max(0.1, 8.184 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # ========== Step 11 ==========
        # Create angle_arc_bottom
        angle_arc_bottom = Angle(line_transversal, line_parallel2, radius=0.5, other_angle=False, color=GREEN, stroke_width=6)
        angle_arc_bottom.move_to(point_B.get_center())
        self.objects["angle_arc_bottom"] = angle_arc_bottom
        
        audio_step11 = "media/audio/Draw_two_parallel_li_68991e7506/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["angle_arc_bottom"]), run_time=1.5)
        remaining_11 = max(0.1, 2.424 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # ========== Step 12 ==========
        # Position angle_label_bottom
        angle_label_bottom.next_to(angle_arc_bottom, DOWN, buff=0.1)
        
        audio_step12 = "media/audio/Draw_two_parallel_li_68991e7506/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["angle_label_bottom"]), run_time=1.0)
        remaining_12 = max(0.1, 1.968 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_12))
        
        # ========== Step 13 ==========
        audio_step13 = "media/audio/Draw_two_parallel_li_68991e7506/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["angle_arc_top"], color=YELLOW, run_time=1))
        
        # Create rotation_copy_arc and rotation_copy_label as copies
        rotation_copy_arc = angle_arc_top.copy()
        rotation_copy_label = angle_label_top.copy()
        self.objects["rotation_copy_arc"] = rotation_copy_arc
        self.objects["rotation_copy_label"] = rotation_copy_label
        
        self.play(Create(rotation_copy_arc), Write(rotation_copy_label), run_time=1.5)
        remaining_13 = max(0.1, 9.336 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_13))
        
        # ========== Step 14 ==========
        audio_step14 = "media/audio/Draw_two_parallel_li_68991e7506/step_13.mp3"
        if os.path.exists(audio_step14):
            self.add_sound(audio_step14)
        elif os.path.exists(audio_step14.replace(".mp3", ".wav")):
            self.add_sound(audio_step14.replace(".mp3", ".wav"))
        
        # Calculate rotation and translation
        # Rotate 180 degrees around midpoint between the two intersection points
        midpoint = (point_A.get_center() + point_B.get_center()) / 2
        rotation_group = VGroup(rotation_copy_arc, rotation_copy_label)
        
        self.play(
            rotation_group.animate.rotate(angle=PI, about_point=midpoint).move_to(angle_arc_bottom.get_center()),
            run_time=3.0
        )
        remaining_14 = max(0.1, 7.632 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_14))
        
        # ========== Step 15 ==========
        audio_step15 = "media/audio/Draw_two_parallel_li_68991e7506/step_14.mp3"
        if os.path.exists(audio_step15):
            self.add_sound(audio_step15)
        elif os.path.exists(audio_step15.replace(".mp3", ".wav")):
            self.add_sound(audio_step15.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["angle_arc_bottom"], color=GREEN, run_time=1))
        self.play(FadeOut(rotation_copy_arc), FadeOut(rotation_copy_label), run_time=1.5)
        remaining_15 = max(0.1, 8.568 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_15))
        
        # ========== Step 16 ==========
        audio_step16 = "media/audio/Draw_two_parallel_li_68991e7506/step_15.mp3"
        if os.path.exists(audio_step16):
            self.add_sound(audio_step16)
        elif os.path.exists(audio_step16.replace(".mp3", ".wav")):
            self.add_sound(audio_step16.replace(".mp3", ".wav"))
        
        # Adjust explanation text position to avoid overflow
        explanation_text.move_to([0, -3.5, 0])
        self.play(Write(self.objects["explanation_text"]), run_time=2.0)
        remaining_16 = max(0.1, 12.888 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_16))