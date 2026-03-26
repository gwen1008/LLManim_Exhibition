'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Solve the equation 2x = 6 using a concrete balance scale model to visualize dividing both sides by 2.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for balance scale and equation
#    - Footer Region: [Bottom y=-3.5] for step-by-step explanation text
# 3. Anti-Overlap Check:
#    - The scale is centered at ORIGIN. Pans and items are positioned relative to the beam.
#    - Equation is placed above the scale, explanation below. Use VGroups for collective items.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/solving_2x_equals_6/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Show title.
#    - Step 2: Build the scale with items and show equation.
#    - Step 3: Highlight equation, update explanation.
#    - Step 4: Show large division symbol.
#    - Step 5: Fade out half the items (one box, three circles).
#    - Step 6: Transform equation to x=3, indicate balanced beam, update explanation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_visualize_the_equ_030c3c0724/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        scale_center = ORIGIN
        equation_anchor = 2.5 * UP  # Above the scale
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Solving 2x = 6 with a Balance Scale", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # balance_beam
        balance_beam = Line(start=LEFT*4, end=RIGHT*4, color=GRAY_C, stroke_width=8)
        balance_beam.move_to(scale_center)
        self.objects["balance_beam"] = balance_beam
        
        # fulcrum (Triangle)
        fulcrum = Polygon([0,0.2,0], [-0.2,-0.2,0], [0.2,-0.2,0], color=GRAY, fill_opacity=1.0)
        fulcrum.move_to(scale_center + DOWN*0.2)
        self.objects["fulcrum"] = fulcrum
        
        # left_string and right_string depend on balance_beam endpoints
        left_string = Line(start=balance_beam.get_start(), end=balance_beam.get_start() + DOWN*2, color=GRAY_C, stroke_width=3)
        self.objects["left_string"] = left_string
        right_string = Line(start=balance_beam.get_end(), end=balance_beam.get_end() + DOWN*2, color=GRAY_C, stroke_width=3)
        self.objects["right_string"] = right_string
        
        # left_pan and right_pan
        left_pan = Rectangle(width=2.0, height=0.2, color=GOLD, fill_opacity=0.8, stroke_width=2)
        left_pan.move_to(left_string.get_end() + DOWN*0.1)
        self.objects["left_pan"] = left_pan
        right_pan = Rectangle(width=2.0, height=0.2, color=GOLD, fill_opacity=0.8, stroke_width=2)
        right_pan.move_to(right_string.get_end() + DOWN*0.1)
        self.objects["right_pan"] = right_pan
        
        # boxes and labels
        box1 = Square(side_length=1.0, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box1.move_to(left_pan.get_center() + LEFT*0.3 + UP*0.1)
        self.objects["box1"] = box1
        box2 = Square(side_length=1.0, color=BLUE, fill_opacity=0.7, stroke_width=2)
        box2.move_to(left_pan.get_center() + RIGHT*0.3 + UP*0.1)
        self.objects["box2"] = box2
        
        label_x1 = MathTex("x", color=WHITE, font_size=30)
        label_x1.move_to(box1.get_center())
        self.objects["label_x1"] = label_x1
        label_x2 = MathTex("x", color=WHITE, font_size=30)
        label_x2.move_to(box2.get_center())
        self.objects["label_x2"] = label_x2
        
        # circles
        circle1 = Circle(radius=0.4, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle1.move_to(right_pan.get_center() + LEFT*0.8 + UP*0.5)
        self.objects["circle1"] = circle1
        circle2 = Circle(radius=0.4, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle2.move_to(right_pan.get_center() + UP*0.5)
        self.objects["circle2"] = circle2
        circle3 = Circle(radius=0.4, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle3.move_to(right_pan.get_center() + RIGHT*0.8 + UP*0.5)
        self.objects["circle3"] = circle3
        circle4 = Circle(radius=0.4, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle4.move_to(right_pan.get_center() + LEFT*0.8 + DOWN*0.5)
        self.objects["circle4"] = circle4
        circle5 = Circle(radius=0.4, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle5.move_to(right_pan.get_center() + DOWN*0.5)
        self.objects["circle5"] = circle5
        circle6 = Circle(radius=0.4, color=GREEN, fill_opacity=0.7, stroke_width=2)
        circle6.move_to(right_pan.get_center() + RIGHT*0.8 + DOWN*0.5)
        self.objects["circle6"] = circle6
        
        # equation_initial
        equation_initial = MathTex("2x = 6", color=YELLOW, font_size=48)
        equation_initial.move_to(equation_anchor)
        self.objects["equation_initial"] = equation_initial
        
        # divider
        divider = MathTex(r"\div\,2", color=RED, font_size=72)
        divider.move_to(scale_center)
        divider.set_opacity(0)
        self.objects["divider"] = divider
        
        # step_explanation
        step_explanation = Text("", color=GRAY_C, font_size=24)
        step_explanation.move_to(explanation_anchor)
        self.objects["step_explanation"] = step_explanation
        
        # Create VGroups for collective handling (implementation_hints)
        left_pan_items = VGroup(box1, box2, label_x1, label_x2)
        right_pan_items = VGroup(circle1, circle2, circle3, circle4, circle5, circle6)
        scale_structure = VGroup(balance_beam, fulcrum, left_string, right_string, left_pan, right_pan)
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/solving_2x_equals_6/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/solving_2x_equals_6/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        # Build scale structure
        self.play(Create(scale_structure), run_time=2.0)
        self.wait(max(0.1, 0.5))
        # Add left items
        self.play(FadeIn(self.objects["box1"]), FadeIn(self.objects["box2"]), run_time=1.0)
        self.play(Write(self.objects["label_x1"]), Write(self.objects["label_x2"]), run_time=1.0)
        # Add right items
        self.play(FadeIn(self.objects["circle1"]), FadeIn(self.objects["circle2"]), FadeIn(self.objects["circle3"]),
                  FadeIn(self.objects["circle4"]), FadeIn(self.objects["circle5"]), FadeIn(self.objects["circle6"]), run_time=1.5)
        # Show equation
        self.play(Write(self.objects["equation_initial"]), run_time=1.0)
        remaining_2 = max(0.1, 5.0 - (2.0+0.5+1.0+1.0+1.5+1.0) + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/solving_2x_equals_6/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        # Signal action: Circumscribe equation
        self.play(Circumscribe(self.objects["equation_initial"], color=YELLOW, run_time=1))
        # Update explanation text
        new_explanation = Text("The equation is balanced: 2x = 6", color=GRAY_C, font_size=24)
        new_explanation.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation), run_time=1.5)
        self.objects["step_explanation"] = new_explanation
        remaining_3 = max(0.1, 4.0 - (1+1.5) + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/solving_2x_equals_6/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Make divider appear and pulse
        self.play(self.objects["divider"].animate.set_opacity(1).scale(1.2), run_time=1.0)
        self.play(self.objects["divider"].animate.scale(1/1.2), run_time=0.5)
        remaining_4 = max(0.1, 2.5 - (1.0+0.5) + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/solving_2x_equals_6/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Signal action: Indicate divider
        self.play(Indicate(self.objects["divider"], color=RED, run_time=1))
        # Update explanation text
        new_explanation2 = Text("Divide both sides by 2: Remove half from each side.", color=GRAY_C, font_size=24)
        new_explanation2.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation2), run_time=1.0)
        self.objects["step_explanation"] = new_explanation2
        # Fade out half the items
        self.play(FadeOut(self.objects["box2"]), FadeOut(self.objects["label_x2"]),
                  FadeOut(self.objects["circle4"]), FadeOut(self.objects["circle5"]), FadeOut(self.objects["circle6"]), run_time=1.5)
        remaining_5 = max(0.1, 3.0 - (1+1.0+1.5) + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/solving_2x_equals_6/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        # Signal action: Indicate balance_beam
        self.play(Indicate(self.objects["balance_beam"], color=GREEN, run_time=1))
        # Fade out divider
        self.play(FadeOut(self.objects["divider"]), run_time=0.5)
        # Transform equation
        equation_final = MathTex("x = 3", color=YELLOW, font_size=48)
        equation_final.move_to(equation_anchor)
        self.play(ReplacementTransform(self.objects["equation_initial"], equation_final), run_time=1.5)
        self.objects["equation_initial"] = equation_final
        # Update explanation text
        new_explanation3 = Text("The scale is still balanced: x = 3", color=GRAY_C, font_size=24)
        new_explanation3.move_to(explanation_anchor)
        self.play(ReplacementTransform(self.objects["step_explanation"], new_explanation3), run_time=1.5)
        self.objects["step_explanation"] = new_explanation3
        remaining_6 = max(0.1, 4.0 - (1+0.5+1.5+1.5) + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # Final hold
        self.wait(max(0.1, 2))