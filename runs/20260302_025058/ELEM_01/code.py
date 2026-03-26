'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualizing the equivalence of fractions 1/2 and 2/4 using a pizza analogy.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for two pizzas side-by-side
#    - Footer Region: [Bottom y=-3.5] for explanation text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Position pizzas at LEFT*3 and RIGHT*3 from origin, leaving center space for arrow.
#    - Use VGroups for each pizza's components to manage positioning.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/Create_two_identical_15b2e54233/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Show two whole pizzas.
#    - Cut left pizza into halves, color one half, label 1/2.
#    - Cut right pizza into quarters, color two quarters, label 2/4.
#    - Show explanation, highlight equivalence, draw connecting arrow.
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
        
        # Create objects from layout_plan.objects
        # title
        title = Text("Equivalent Fractions: 1/2 = 2/4", color=WHITE, font_size=48)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # pizza_left_circle
        pizza_left_circle = Circle(radius=2, color=WHITE, stroke_width=4, fill_opacity=0)
        pizza_left_circle.move_to(content_center + 3 * LEFT)
        self.objects["pizza_left_circle"] = pizza_left_circle
        
        # pizza_right_circle
        pizza_right_circle = Circle(radius=2, color=WHITE, stroke_width=4, fill_opacity=0)
        pizza_right_circle.move_to(content_center + 3 * RIGHT)
        self.objects["pizza_right_circle"] = pizza_right_circle
        
        # cut_left
        cut_left = Line(UP * 2, DOWN * 2, color=WHITE, stroke_width=3)
        cut_left.move_to(pizza_left_circle.get_center())
        self.objects["cut_left"] = cut_left
        
        # cut_right_vertical
        cut_right_vertical = Line(UP * 2, DOWN * 2, color=WHITE, stroke_width=3)
        cut_right_vertical.move_to(pizza_right_circle.get_center())
        self.objects["cut_right_vertical"] = cut_right_vertical
        
        # cut_right_horizontal
        cut_right_horizontal = Line(LEFT * 2, RIGHT * 2, color=WHITE, stroke_width=3)
        cut_right_horizontal.move_to(pizza_right_circle.get_center())
        self.objects["cut_right_horizontal"] = cut_right_horizontal
        
        # sector_left
        sector_left = Sector(radius=2, angle=PI, start_angle=-PI/2, color="#1E90FF", fill_opacity=0.8, stroke_width=0)
        sector_left.move_to(pizza_left_circle.get_center())
        self.objects["sector_left"] = sector_left
        
        # sector_right_top
        sector_right_top = Sector(radius=2, angle=PI/2, start_angle=0, color="#1E90FF", fill_opacity=0.8, stroke_width=0)
        sector_right_top.move_to(pizza_right_circle.get_center())
        self.objects["sector_right_top"] = sector_right_top
        
        # sector_right_bottom
        sector_right_bottom = Sector(radius=2, angle=PI/2, start_angle=PI/2, color="#1E90FF", fill_opacity=0.8, stroke_width=0)
        sector_right_bottom.move_to(pizza_right_circle.get_center())
        self.objects["sector_right_bottom"] = sector_right_bottom
        
        # label_left
        label_left = MathTex(r"\frac{1}{2}", color=WHITE, font_size=36)
        label_left.next_to(pizza_left_circle, DOWN, buff=0.8)
        self.objects["label_left"] = label_left
        
        # label_right
        label_right = MathTex(r"\frac{2}{4}", color=WHITE, font_size=36)
        label_right.next_to(pizza_right_circle, DOWN, buff=0.8)
        self.objects["label_right"] = label_right
        
        # explanation_text
        explanation_text = Text("The colored area is the same!", color=YELLOW, font_size=32)
        explanation_text.move_to(explanation_anchor)
        self.objects["explanation_text"] = explanation_text
        
        # equivalence_arrow
        equivalence_arrow = DoubleArrow(LEFT, RIGHT, color=GREEN, stroke_width=6, tip_length=0.2)
        equivalence_arrow.move_to(content_center)
        self.objects["equivalence_arrow"] = equivalence_arrow
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Create_two_identical_15b2e54233/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["pizza_left_circle"]), run_time=1.5)
        remaining_1 = max(0.1, 3.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Create_two_identical_15b2e54233/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["pizza_right_circle"]), run_time=1.5)
        remaining_2 = max(0.1, 2.472 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Create_two_identical_15b2e54233/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza_left_circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_left"]), run_time=1.5)
        remaining_3 = max(0.1, 3.96 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Create_two_identical_15b2e54233/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["cut_left"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["sector_left"]), run_time=1.5)
        remaining_4 = max(0.1, 4.512 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Create_two_identical_15b2e54233/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["sector_left"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["label_left"]), run_time=1.0)
        remaining_5 = max(0.1, 2.76 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/Create_two_identical_15b2e54233/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["pizza_right_circle"], color=YELLOW, run_time=1))
        self.play(Create(self.objects["cut_right_vertical"]), run_time=1.5)
        remaining_6 = max(0.1, 4.848 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/Create_two_identical_15b2e54233/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["cut_right_horizontal"]), run_time=1.5)
        remaining_7 = max(0.1, 2.112 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        # ========== Step 8 ==========
        audio_step8 = "media/audio/Create_two_identical_15b2e54233/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["cut_right_vertical"], color=YELLOW, run_time=0.5),
                  Indicate(self.objects["cut_right_horizontal"], color=YELLOW, run_time=0.5))
        self.play(Create(self.objects["sector_right_top"]), run_time=1.5)
        remaining_8 = max(0.1, 5.76 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        # ========== Step 9 ==========
        audio_step9 = "media/audio/Create_two_identical_15b2e54233/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["sector_right_bottom"]), run_time=1.5)
        remaining_9 = max(0.1, 1.8 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # ========== Step 10 ==========
        audio_step10 = "media/audio/Create_two_identical_15b2e54233/step_09.mp3"
        if os.path.exists(audio_step10):
            self.add_sound(audio_step10)
        elif os.path.exists(audio_step10.replace(".mp3", ".wav")):
            self.add_sound(audio_step10.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["sector_right_top"], color=YELLOW, run_time=0.5),
                  Circumscribe(self.objects["sector_right_bottom"], color=YELLOW, run_time=0.5))
        self.play(Write(self.objects["label_right"]), run_time=1.0)
        remaining_10 = max(0.1, 3.048 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_10))
        
        # ========== Step 11 ==========
        audio_step11 = "media/audio/Create_two_identical_15b2e54233/step_10.mp3"
        if os.path.exists(audio_step11):
            self.add_sound(audio_step11)
        elif os.path.exists(audio_step11.replace(".mp3", ".wav")):
            self.add_sound(audio_step11.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["sector_left"], color=RED, run_time=1))
        self.play(FadeIn(self.objects["explanation_text"]), run_time=1.0)
        remaining_11 = max(0.1, 5.328 - 1.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_11))
        
        # ========== Step 12 ==========
        audio_step12 = "media/audio/Create_two_identical_15b2e54233/step_11.mp3"
        if os.path.exists(audio_step12):
            self.add_sound(audio_step12)
        elif os.path.exists(audio_step12.replace(".mp3", ".wav")):
            self.add_sound(audio_step12.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["sector_right_top"], color=RED, run_time=0.5),
                  Indicate(self.objects["sector_right_bottom"], color=RED, run_time=0.5))
        remaining_12 = max(0.1, 4.872 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_12))
        
        # ========== Step 13 ==========
        audio_step13 = "media/audio/Create_two_identical_15b2e54233/step_12.mp3"
        if os.path.exists(audio_step13):
            self.add_sound(audio_step13)
        elif os.path.exists(audio_step13.replace(".mp3", ".wav")):
            self.add_sound(audio_step13.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["label_left"], color=GREEN, run_time=0.5),
                  Circumscribe(self.objects["label_right"], color=GREEN, run_time=0.5))
        self.play(Create(self.objects["equivalence_arrow"]), run_time=1.5)
        remaining_13 = max(0.1, 3.552 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_13))
        
        # Final hold
        self.wait(max(0.1, 2))