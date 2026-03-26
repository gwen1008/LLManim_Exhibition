'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the part-to-part ratio 2:5 using a tape diagram (bar model).
# 2. Layout Strategy: Use high-low split.
#    - Header Region: [y=3.5] for Title
#    - Main Content: [Center y=0] for tape diagram
#    - Footer Region: [Bottom y=-3.5] for ratio text
# 3. Anti-Overlap Check: Use VGroups for milk/water sections and labels. Position labels above sections with buff. Keep diagram centered.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/ratio_2_5/step_XX.mp3"
# 5. Animation Flow: Title → Build milk sections → Label milk → Build water sections → Label water → Highlight milk → Highlight water → Show final ratio.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}

        # Create anchors
        title_anchor = 3.5 * UP
        diagram_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # title
        title = Text("Visualizing the Ratio 2:5 (Milk to Water)", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # section_template (positioned off-screen)
        section_template = Rectangle(width=0.8, height=2.0, stroke_width=2, stroke_color=WHITE)
        section_template.move_to(LEFT * 100)
        self.objects["section_template"] = section_template

        # milk_label (positioned off-screen initially)
        milk_label = Text("Milk (2 parts)", color="#D4A574", font_size=28)
        milk_label.move_to(LEFT * 100)
        self.objects["milk_label"] = milk_label

        # water_label (positioned off-screen initially)
        water_label = Text("Water (5 parts)", color="#89CFF0", font_size=28)
        water_label.move_to(LEFT * 100)
        self.objects["water_label"] = water_label

        # final_ratio_text
        final_ratio_text = MathTex(r"\mathrm{Ratio} = 2 : 5", color=YELLOW, font_size=32)
        final_ratio_text.move_to(explanation_anchor)
        self.objects["final_ratio_text"] = final_ratio_text

        # We'll create milk_sections and water_sections VGroups during animation
        self.objects["milk_sections"] = VGroup()
        self.objects["water_sections"] = VGroup()
        self.objects["final_tape_diagram"] = VGroup()  # Will combine milk and water sections

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/ratio_2_5/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        self.play(Write(self.objects["title"]), run_time=1.5)
        remaining_1 = max(0.1, 2.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_01.mp3")  # [auto-injected]
        # Step 2: Create milk sections
        audio_step2 = "media/audio/ratio_2_5/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        milk_color = "#D4A574"
        milk_sections = VGroup()
        start_x = -2.8
        for i in range(2):
            rect = self.objects["section_template"].copy()
            rect.set_fill(color=milk_color, opacity=0.7)
            rect.move_to([start_x + i * 0.8, 0, 0])
            milk_sections.add(rect)
        self.objects["milk_sections"] = milk_sections
        # Animate creation sequentially
        for rect in milk_sections:
            self.play(Create(rect), run_time=0.8)
        remaining_2 = max(0.1, 4.0 - (0.8 * 2) + 0.5)
        self.wait(max(0.1, remaining_2))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_02.mp3")  # [auto-injected]
        # Step 3: Indicate milk sections and write label
        audio_step3 = "media/audio/ratio_2_5/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["milk_sections"], color=YELLOW, run_time=1))
        milk_label = self.objects["milk_label"]
        milk_label.next_to(self.objects["milk_sections"], UP, buff=0.3)
        self.play(Write(milk_label), run_time=1.2)
        remaining_3 = max(0.1, 2.5 - (1 + 1.2) + 0.5)
        self.wait(max(0.1, remaining_3))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_03.mp3")  # [auto-injected]
        # Step 4: Create water sections
        audio_step4 = "media/audio/ratio_2_5/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        water_color = "#89CFF0"
        water_sections = VGroup()
        # Start after the last milk section (2 sections * width 0.8)
        start_x_water = -2.8 + 2 * 0.8
        for i in range(5):
            rect = self.objects["section_template"].copy()
            rect.set_fill(color=water_color, opacity=0.7)
            rect.move_to([start_x_water + i * 0.8, 0, 0])
            water_sections.add(rect)
        self.objects["water_sections"] = water_sections
        for rect in water_sections:
            self.play(Create(rect), run_time=0.8)
        remaining_4 = max(0.1, 4.0 - (0.8 * 5) + 0.5)
        self.wait(max(0.1, remaining_4))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_04.mp3")  # [auto-injected]
        # Step 5: Indicate water sections and write label
        audio_step5 = "media/audio/ratio_2_5/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        self.play(Indicate(self.objects["water_sections"], color=YELLOW, run_time=1))
        water_label = self.objects["water_label"]
        water_label.next_to(self.objects["water_sections"], UP, buff=0.3)
        self.play(Write(water_label), run_time=1.2)
        remaining_5 = max(0.1, 2.5 - (1 + 1.2) + 0.5)
        self.wait(max(0.1, remaining_5))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_05.mp3")  # [auto-injected]
        # Step 6: Highlight milk sections
        audio_step6 = "media/audio/ratio_2_5/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))

        milk_highlight = self.objects["milk_sections"].copy()
        milk_highlight.set_fill(opacity=1.0)
        self.play(Transform(self.objects["milk_sections"], milk_highlight), run_time=0.5)
        self.play(Transform(self.objects["milk_sections"], self.objects["milk_sections"].copy().set_fill(opacity=0.7)), run_time=0.5)
        remaining_6 = max(0.1, 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_06.mp3")  # [auto-injected]
        # Step 7: Highlight water sections
        audio_step7 = "media/audio/ratio_2_5/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))

        water_highlight = self.objects["water_sections"].copy()
        water_highlight.set_fill(opacity=1.0)
        self.play(Transform(self.objects["water_sections"], water_highlight), run_time=0.5)
        self.play(Transform(self.objects["water_sections"], self.objects["water_sections"].copy().set_fill(opacity=0.7)), run_time=0.5)
        remaining_7 = max(0.1, 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))

        self.add_sound("media/audio/To_visualize_the_2_5_a3571db48a/step_07.mp3")  # [auto-injected]
        # Step 8: Circumscribe final diagram and write ratio text
        audio_step8 = "media/audio/ratio_2_5/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))

        final_tape_diagram = VGroup(self.objects["milk_sections"], self.objects["water_sections"])
        self.objects["final_tape_diagram"] = final_tape_diagram
        self.play(Circumscribe(final_tape_diagram, color=GREEN, run_time=1))
        self.play(Write(self.objects["final_ratio_text"]), run_time=1.5)
        remaining_8 = max(0.1, 3.0 - (1 + 1.5) + 0.5)
        self.wait(max(0.1, remaining_8))