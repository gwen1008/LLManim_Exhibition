'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize rounding 3.7 to the nearest whole number using a color-coded number line.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for number line, zones, dot, and labels
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanations
# 3. Anti-Overlap Check:
#    - Strategy: Place number line at center. Zones behind line (z_index=-1). Labels positioned with next_to.
#    - Use VGroup for number line components. Ensure footer text is scaled.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/rounding_number_line/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create number line.
#    - Step 2: Indicate and create dot at 3.7 with label.
#    - Step 3: Circumscribe midpoint label 3.5, create colored zones.
#    - Step 4: Indicate green zone.
#    - Step 5: Indicate dot, animate dot and label to 4.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # title
        title = Text("Rounding on a Number Line: 3.7 to the Nearest Whole Number", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # number_line
        # Note: NumberLine in Manim v0.19.2 uses x_range and length. include_numbers is True by default for integers in range.
        number_line = NumberLine(x_range=[3, 4, 0.5], length=6, include_numbers=True, color=GRAY_B)
        number_line.move_to(content_center)
        self.objects["number_line"] = number_line
        
        # zone_round_down
        zone_round_down = Rectangle(width=3, height=0.4, color=RED, fill_opacity=0.2, stroke_opacity=0)
        zone_round_down.move_to(content_center + LEFT * 1.5)
        zone_round_down.set_z_index(-1)
        self.objects["zone_round_down"] = zone_round_down
        
        # zone_round_up
        zone_round_up = Rectangle(width=3, height=0.4, color=GREEN, fill_opacity=0.2, stroke_opacity=0)
        zone_round_up.move_to(content_center + RIGHT * 1.5)
        zone_round_up.set_z_index(-1)
        self.objects["zone_round_up"] = zone_round_up
        
        # point_dot
        point_dot = Dot(radius=0.08, color=YELLOW)
        point_dot.move_to(number_line.n2p(3.7))
        self.objects["point_dot"] = point_dot
        
        # point_label
        point_label = MathTex("3.7", color=YELLOW)
        point_label.next_to(point_dot, UP, buff=0.2)
        self.objects["point_label"] = point_label
        
        # midpoint_label
        midpoint_label = MathTex("3.5", color=WHITE, font_size=30)
        midpoint_label.next_to(number_line.n2p(3.5), DOWN, buff=0.3)
        self.objects["midpoint_label"] = midpoint_label
        
        # footer_text
        footer_text = Text("Let's begin by drawing our number line.", color=GRAY_B, font_size=24)
        footer_text.move_to(explanation_anchor)
        self.objects["footer_text"] = footer_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Create_a_Manim_anima_729d124bd9/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/rounding_number_line/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=0.5)
        self.play(Create(self.objects["number_line"]), run_time=2.0)
        remaining_1 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # Update footer text for step 2
        footer_text_step2 = Text("Now, let's plot our number, three point seven, on this line.", color=GRAY_B, font_size=24)
        footer_text_step2.move_to(explanation_anchor)
        self.play(Transform(self.objects["footer_text"], footer_text_step2))
        self.objects["footer_text"] = footer_text_step2
        
        self.add_sound("media/audio/Create_a_Manim_anima_729d124bd9/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/rounding_number_line/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_dot"], color=YELLOW, run_time=1))
        self.play(FadeIn(self.objects["point_dot"]), run_time=0.5)
        self.play(Write(self.objects["point_label"]), run_time=0.5)
        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # Update footer text for step 3
        footer_text_step3 = Text("To round, we need the midpoint 3.5. Numbers at or above it round up; below round down.", color=GRAY_B, font_size=24)
        footer_text_step3.move_to(explanation_anchor)
        self.play(Transform(self.objects["footer_text"], footer_text_step3))
        self.objects["footer_text"] = footer_text_step3
        
        self.add_sound("media/audio/Create_a_Manim_anima_729d124bd9/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/rounding_number_line/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["midpoint_label"], color=WHITE, run_time=1))
        self.play(Write(self.objects["midpoint_label"]), run_time=0.5)
        self.play(FadeIn(self.objects["zone_round_down"]), FadeIn(self.objects["zone_round_up"]), run_time=1.5)
        remaining_3 = max(0.1, 5.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # Update footer text for step 4
        footer_text_step4 = Text("Look where 3.7 lies. It's in the green zone, beyond the midpoint, closer to 4.", color=GRAY_B, font_size=24)
        footer_text_step4.move_to(explanation_anchor)
        self.play(Transform(self.objects["footer_text"], footer_text_step4))
        self.objects["footer_text"] = footer_text_step4
        
        self.add_sound("media/audio/Create_a_Manim_anima_729d124bd9/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/rounding_number_line/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["zone_round_up"], color=GREEN, run_time=1))
        remaining_4 = max(0.1, 4.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # Update footer text for step 5
        footer_text_step5 = Text("Therefore, three point seven rounds up to four.", color=GRAY_B, font_size=24)
        footer_text_step5.move_to(explanation_anchor)
        self.play(Transform(self.objects["footer_text"], footer_text_step5))
        self.objects["footer_text"] = footer_text_step5
        
        self.add_sound("media/audio/Create_a_Manim_anima_729d124bd9/step_04.mp3")  # [auto-injected]
        # Step 5
        audio_step5 = "media/audio/rounding_number_line/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["point_dot"], color=YELLOW, run_time=1))
        
        # Create target dot at 4 and label
        target_dot = Dot(radius=0.08, color=YELLOW)
        target_dot.move_to(self.objects["number_line"].n2p(4))
        target_label = MathTex("4", color=YELLOW)
        target_label.next_to(target_dot, UP, buff=0.2)
        
        # Animate dot along an arc
        arc_path = ArcBetweenPoints(
            self.objects["point_dot"].get_center(),
            target_dot.get_center(),
            angle=PI/4,
            stroke_opacity=0
        )
        self.play(MoveAlongPath(self.objects["point_dot"], arc_path), run_time=1.5)
        self.play(Transform(self.objects["point_label"], target_label), run_time=0.5)
        remaining_5 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # Final hold
        self.wait(max(0.1, 2))