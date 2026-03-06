'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize multiplication as repeated addition (3×4) using abstract groups.
# 2. Layout Strategy: [Define the screen zones]
#    - Header Region: [y=3.5] for Title (equation)
#    - Main Content: [Center y=0] for three circles and final star grid
#    - Footer Region: [Bottom y=-3.5] for step narration text
# 3. Anti-Overlap Check: [How will you prevent collision?]
#    - Strategy: Position circles horizontally spaced (LEFT*3, ORIGIN, RIGHT*3). Stars inside circles use relative offsets. Final grid uses VGroup.arrange_in_grid.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/multiplication_3x4/step_XX.mp3"
# 5. Animation Flow: [Brief sequence of events]
#    - Show equation.
#    - Show three empty circles with labels.
#    - Fill each circle with 4 stars sequentially.
#    - Transform all stars into a 3x4 grid, fade out circles.
#    - Morph equation to show answer (12).
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/To_illustrate_the_co_ddb86074a8/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN

        # Object registry
        self.objects = {}

        # Create objects from layout_plan.objects
        # title_equation
        title_equation = MathTex(r"3 \times 4 = ?", color=YELLOW, font_size=48)
        title_equation.move_to(title_anchor)
        self.objects["title_equation"] = title_equation

        # group1_circle
        group1_circle = Circle(radius=0.8, color=BLUE, stroke_width=3)
        group1_circle.move_to(content_center + 3 * LEFT)
        self.objects["group1_circle"] = group1_circle

        # group2_circle
        group2_circle = Circle(radius=0.8, color=GREEN, stroke_width=3)
        group2_circle.move_to(content_center)
        self.objects["group2_circle"] = group2_circle

        # group3_circle
        group3_circle = Circle(radius=0.8, color=RED, stroke_width=3)
        group3_circle.move_to(content_center + 3 * RIGHT)
        self.objects["group3_circle"] = group3_circle

        # label_group1
        label_group1 = Text("Group 1", color=BLUE, font_size=24)
        label_group1.next_to(self.objects["group1_circle"], DOWN, buff=0.3)
        self.objects["label_group1"] = label_group1

        # label_group2
        label_group2 = Text("Group 2", color=GREEN, font_size=24)
        label_group2.next_to(self.objects["group2_circle"], DOWN, buff=0.3)
        self.objects["label_group2"] = label_group2

        # label_group3
        label_group3 = Text("Group 3", color=RED, font_size=24)
        label_group3.next_to(self.objects["group3_circle"], DOWN, buff=0.3)
        self.objects["label_group3"] = label_group3

        # footer_text (initial content)
        footer_text = Text("We have 3 empty groups.", color=GRAY_C, font_size=28)
        footer_text.move_to(footer_anchor)
        self.objects["footer_text"] = footer_text

        # Create star groups (not added yet, stored for later steps)
        # Relative positions for 4 stars inside a circle
        star_offsets = [(-0.4, 0.2, 0), (0.4, 0.2, 0), (-0.4, -0.2, 0), (0.4, -0.2, 0)]

        # stars_group1
        stars1 = VGroup()
        for offset in star_offsets:
            star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=1).scale(0.4)
            star.move_to(self.objects["group1_circle"].get_center() + np.array(offset))
            stars1.add(star)
        self.objects["stars_group1"] = stars1

        # stars_group2
        stars2 = VGroup()
        for offset in star_offsets:
            star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=1).scale(0.4)
            star.move_to(self.objects["group2_circle"].get_center() + np.array(offset))
            stars2.add(star)
        self.objects["stars_group2"] = stars2

        # stars_group3
        stars3 = VGroup()
        for offset in star_offsets:
            star = Star(n=5, outer_radius=0.2, color=YELLOW, fill_opacity=1).scale(0.4)
            star.move_to(self.objects["group3_circle"].get_center() + np.array(offset))
            stars3.add(star)
        self.objects["stars_group3"] = stars3

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/multiplication_3x4/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # visual_action: Create title_equation
        self.play(Write(self.objects["title_equation"]), run_time=1.5)
        # Update footer text
        new_footer = Text("Let's explore what three times four means. We start with three groups.", color=GRAY_C, font_size=28)
        new_footer.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer))
        self.objects["footer_text"] = new_footer

        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/multiplication_3x4/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # signal_action: Indicate group1_circle
        self.play(Indicate(self.objects["group1_circle"], color=YELLOW, run_time=1))

        # visual_action: Create circles and labels
        self.play(
            Create(self.objects["group1_circle"]),
            Create(self.objects["group2_circle"]),
            Create(self.objects["group3_circle"]),
            Write(self.objects["label_group1"]),
            Write(self.objects["label_group2"]),
            Write(self.objects["label_group3"]),
            run_time=2.0
        )
        # Update footer text
        new_footer2 = Text("First, we establish our three empty groups.", color=GRAY_C, font_size=28)
        new_footer2.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer2))
        self.objects["footer_text"] = new_footer2

        remaining_2 = max(0.1, 3.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/multiplication_3x4/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # signal_action: Circumscribe group1_circle
        self.play(Circumscribe(self.objects["group1_circle"], color=YELLOW, run_time=1))

        # visual_action: Create stars_group1
        self.play(Create(self.objects["stars_group1"]), run_time=1.5)
        # Update footer text
        new_footer3 = Text("Now, we put four stars into the first group.", color=GRAY_C, font_size=28)
        new_footer3.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer3))
        self.objects["footer_text"] = new_footer3

        remaining_3 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/multiplication_3x4/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # signal_action: Indicate group2_circle
        self.play(Indicate(self.objects["group2_circle"], color=YELLOW, run_time=1))

        # visual_action: Create stars_group2
        self.play(Create(self.objects["stars_group2"]), run_time=1.0)
        # Update footer text
        new_footer4 = Text("We do the same for the second group, and then the third group. Each group contains four stars.", color=GRAY_C, font_size=28)
        new_footer4.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer4))
        self.objects["footer_text"] = new_footer4

        remaining_4 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/multiplication_3x4/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # signal_action: Indicate group3_circle
        self.play(Indicate(self.objects["group3_circle"], color=YELLOW, run_time=1))

        # visual_action: Create stars_group3
        self.play(Create(self.objects["stars_group3"]), run_time=1.0)
        # Update footer text
        new_footer5 = Text("And finally, the third group. Now we have three groups of four.", color=GRAY_C, font_size=28)
        new_footer5.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer5))
        self.objects["footer_text"] = new_footer5

        remaining_5 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # ========== Step 6 ==========
        audio_step6 = "media/audio/multiplication_3x4/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        # Prepare final grid: 3 rows, 4 columns of stars centered at content_center
        all_stars = VGroup(self.objects["stars_group1"], self.objects["stars_group2"], self.objects["stars_group3"])
        # Flatten to get 12 individual stars
        star_list = []
        for group in [self.objects["stars_group1"], self.objects["stars_group2"], self.objects["stars_group3"]]:
            for star in group:
                star_list.append(star)
        stars_vgroup = VGroup(*star_list)
        # Arrange in grid: 3 rows, 4 columns
        stars_vgroup.arrange_in_grid(rows=3, cols=4, buff=0.3)
        stars_vgroup.move_to(content_center)

        # visual_action: Transform stars to grid, fade out circles and labels
        self.play(
            Transform(all_stars, stars_vgroup),
            FadeOut(self.objects["group1_circle"]),
            FadeOut(self.objects["group2_circle"]),
            FadeOut(self.objects["group3_circle"]),
            FadeOut(self.objects["label_group1"]),
            FadeOut(self.objects["label_group2"]),
            FadeOut(self.objects["label_group3"]),
            run_time=3.0
        )
        # Update footer text
        new_footer6 = Text("To find the total, we combine all the stars. Three groups of four makes twelve stars in total.", color=GRAY_C, font_size=28)
        new_footer6.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer6))
        self.objects["footer_text"] = new_footer6

        remaining_6 = max(0.1, 4.0 - 3.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        # ========== Step 7 ==========
        audio_step7 = "media/audio/multiplication_3x4/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        # signal_action: Circumscribe title_equation
        self.play(Circumscribe(self.objects["title_equation"], color=GREEN, run_time=1))

        # visual_action: TransformMatchingTex title_equation
        new_equation = MathTex(r"3 \times 4 = 12", color=YELLOW, font_size=48)
        new_equation.move_to(title_anchor)
        self.play(TransformMatchingTex(self.objects["title_equation"], new_equation), run_time=1.5)
        self.objects["title_equation"] = new_equation

        # Update footer text
        new_footer7 = Text("Therefore, three times four equals twelve.", color=GRAY_C, font_size=28)
        new_footer7.move_to(footer_anchor)
        self.play(Transform(self.objects["footer_text"], new_footer7))
        self.objects["footer_text"] = new_footer7

        remaining_7 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_7))

        # Final hold
        self.wait(max(0.1, 2))