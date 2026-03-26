'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the construction of a tape diagram for a mixture ratio (milk:water = 2:5) and derive the ratio from the visual model.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title and Step Label
#    - Main Content: [Center y=0] for the tape diagram (7 squares) and ratio equation
#    - Footer Region: [Bottom y=-3.5] for explanatory footnote
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for the squares and labels to keep them together. Position the ratio equation to the right of the tape with sufficient buff.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/topic_folder/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Draw tape outline.
#    - Step 2: Divide into 7 squares.
#    - Step 3: Color and label milk squares (2 parts).
#    - Step 4: Color and label water squares (5 parts).
#    - Step 5: Show final ratio equation.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        self.add_sound("media/audio/Create_a_tape_diagra_95924de58c/final_narrative.mp3")  # [auto-injected: full narration]
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create a registry for all objects
        self.objects = {}

        # Define color constants from JSON
        MILK_COLOR = "#E6F2FF"
        WATER_COLOR = "#D4F1F9"

        # Create anchors based on layout_plan description
        title_anchor = 3.5 * UP
        diagram_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN

        # Create objects from layout_plan.objects
        # Title
        title = Text("Tape Diagram: Milk and Water Mixture", color=WHITE, font_size=36)
        title.move_to(title_anchor)
        self.objects["title"] = title

        # Step Label (initial content)
        step_label = Text("Step 1: Draw the tape.", color=YELLOW, font_size=28)
        step_label.next_to(title, DOWN, buff=0.5)
        self.objects["step_label"] = step_label

        # Tape Outline
        tape_outline = Rectangle(width=5.6, height=0.8, color=WHITE, fill_opacity=0.0, stroke_width=2)
        tape_outline.move_to(diagram_anchor)
        self.objects["tape_outline"] = tape_outline

        # Create the 7 squares
        # First square positioned relative to diagram_anchor
        square_1 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        # Align left edge to diagram_anchor + LEFT*2.8 (which is leftmost position)
        leftmost_pos = diagram_anchor + LEFT * 2.8
        square_1.align_to(leftmost_pos, LEFT)
        self.objects["square_1"] = square_1

        # Create remaining squares using next_to with buff=0
        square_2 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        square_2.next_to(square_1, RIGHT, buff=0.0)
        self.objects["square_2"] = square_2

        square_3 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        square_3.next_to(square_2, RIGHT, buff=0.0)
        self.objects["square_3"] = square_3

        square_4 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        square_4.next_to(square_3, RIGHT, buff=0.0)
        self.objects["square_4"] = square_4

        square_5 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        square_5.next_to(square_4, RIGHT, buff=0.0)
        self.objects["square_5"] = square_5

        square_6 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        square_6.next_to(square_5, RIGHT, buff=0.0)
        self.objects["square_6"] = square_6

        square_7 = Square(side_length=0.8, color=WHITE, fill_opacity=0.0, stroke_width=1)
        square_7.next_to(square_6, RIGHT, buff=0.0)
        self.objects["square_7"] = square_7

        # Create VGroups for milk and water squares for easier positioning
        milk_squares = VGroup(square_1, square_2)
        water_squares = VGroup(square_3, square_4, square_5, square_6, square_7)

        # Labels
        label_milk = Text("milk", color=MILK_COLOR, font_size=24)
        label_milk.next_to(milk_squares, DOWN, buff=0.3)
        self.objects["label_milk"] = label_milk

        label_water = Text("water", color=WATER_COLOR, font_size=24)
        label_water.next_to(water_squares, DOWN, buff=0.3)
        self.objects["label_water"] = label_water

        # Counts
        count_milk = MathTex("2", color=MILK_COLOR, font_size=32)
        count_milk.next_to(label_milk, DOWN, buff=0.2)
        self.objects["count_milk"] = count_milk

        count_water = MathTex("5", color=WATER_COLOR, font_size=32)
        count_water.next_to(label_water, DOWN, buff=0.2)
        self.objects["count_water"] = count_water

        # Ratio Equation
        ratio_eq = MathTex(r"\mathrm{milk}:\mathrm{water} = 2:5", color=WHITE, font_size=36)
        ratio_eq.next_to(tape_outline, RIGHT, buff=1.5)
        self.objects["ratio_eq"] = ratio_eq

        # Footnote
        footnote = Text("Each square represents one part of the mixture.", color=GRAY, font_size=24).set_opacity(0.8)
        footnote.move_to(explanation_anchor)
        self.objects["footnote"] = footnote

        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========

        # ========== Step 1 ==========
        audio_step1 = "media/audio/topic_folder/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))

        # Write title and step label
        self.play(Write(title), Write(step_label), run_time=1.5)
        # Create tape outline
        self.play(Create(tape_outline), run_time=1.0)
        remaining_1 = max(0.1, 2.5 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_1))

        # ========== Step 2 ==========
        audio_step2 = "media/audio/topic_folder/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))

        # Signal action: Circumscribe tape_outline
        self.play(Circumscribe(tape_outline, color=YELLOW, run_time=1))

        # Update step label
        step_label_2 = Text("Step 2: Divide into 7 equal parts.", color=YELLOW, font_size=28)
        step_label_2.next_to(title, DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_2))
        self.objects["step_label"] = step_label_2

        # Create all 7 squares
        squares_group = VGroup(square_1, square_2, square_3, square_4, square_5, square_6, square_7)
        self.play(Create(squares_group), run_time=2.0)
        remaining_2 = max(0.1, 3.5 - 1.0 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))

        # ========== Step 3 ==========
        audio_step3 = "media/audio/topic_folder/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))

        # Signal action: Indicate milk squares
        self.play(Indicate(milk_squares, color=MILK_COLOR, run_time=1))

        # Update step label
        step_label_3 = Text("Step 3: Identify milk parts.", color=YELLOW, font_size=28)
        step_label_3.next_to(title, DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_3))
        self.objects["step_label"] = step_label_3

        # Color milk squares
        self.play(
            square_1.animate.set_fill(MILK_COLOR, opacity=0.7),
            square_2.animate.set_fill(MILK_COLOR, opacity=0.7),
            run_time=1.0
        )
        # Write milk label and count
        self.play(Write(label_milk), Write(count_milk), run_time=1.5)
        remaining_3 = max(0.1, 4.0 - 1.0 - 1.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))

        # ========== Step 4 ==========
        audio_step4 = "media/audio/topic_folder/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))

        # Signal action: Indicate water squares
        self.play(Indicate(water_squares, color=WATER_COLOR, run_time=1))

        # Update step label
        step_label_4 = Text("Step 4: Identify water parts.", color=YELLOW, font_size=28)
        step_label_4.next_to(title, DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_4))
        self.objects["step_label"] = step_label_4

        # Color water squares
        self.play(
            square_3.animate.set_fill(WATER_COLOR, opacity=0.7),
            square_4.animate.set_fill(WATER_COLOR, opacity=0.7),
            square_5.animate.set_fill(WATER_COLOR, opacity=0.7),
            square_6.animate.set_fill(WATER_COLOR, opacity=0.7),
            square_7.animate.set_fill(WATER_COLOR, opacity=0.7),
            run_time=1.5
        )
        # Write water label and count
        self.play(Write(label_water), Write(count_water), run_time=1.5)
        remaining_4 = max(0.1, 4.0 - 1.0 - 1.5 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_4))

        # ========== Step 5 ==========
        audio_step5 = "media/audio/topic_folder/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))

        # Signal action: Indicate counts
        self.play(Indicate(VGroup(count_milk, count_water), color=YELLOW, run_time=1))

        # Update step label
        step_label_5 = Text("Step 5: State the ratio.", color=YELLOW, font_size=28)
        step_label_5.next_to(title, DOWN, buff=0.5)
        self.play(ReplacementTransform(self.objects["step_label"], step_label_5))
        self.objects["step_label"] = step_label_5

        # Write ratio equation
        self.play(Write(ratio_eq), run_time=2.0)
        # Write footnote
        self.play(Write(footnote), run_time=1.0)
        remaining_5 = max(0.1, 5.0 - 1.0 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))

        # Final hold
        self.wait(max(0.1, 2))