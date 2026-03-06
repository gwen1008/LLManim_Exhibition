'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visually demonstrate the relationship between a circle's circumference and its diameter (C = πD) by unrolling the circle and measuring with the diameter.
# 2. Layout Strategy: Use LayoutEngine for zones.
#    - Header Region: [y=3.5] for Title
#    - Main Content: Left zone for circle, right zone for unrolled line.
#    - Footer Region: [Bottom y=-3.5] for final formula and explanation.
# 3. Anti-Overlap Check: Use LayoutEngine zones to keep header, content, and footer separate. Use VGroups for composite objects (circle+diameter).
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_XX.mp3"
# 5. Animation Flow: Create circle → show diameter → morph circle perimeter to line → show circumference line → measure with diameter copies → reveal π → show final formula.
'''

from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        # Create objects from layout_plan
        self.objects = {}

        # Title
        title = Text("Unrolling a Circle to Discover π", color=WHITE, font_size=36)
        self.objects["title"] = title

        # Circle with radius 1.2
        circle = Circle(radius=1.2, color=BLUE, stroke_width=4)
        self.objects["circle"] = circle

        # Diameter line (horizontal, length 2.4)
        diameter_line = Line(start=LEFT*1.2, end=RIGHT*1.2, color=YELLOW, stroke_width=6)
        self.objects["diameter_line"] = diameter_line

        # Label for diameter
        label_diameter = MathTex("D", color=YELLOW)
        self.objects["label_diameter"] = label_diameter

        # Circumference line (unrolled, length ~7.5398 ≈ 2π*1.2)
        circumference_length = 2 * PI * 1.2  # ~7.5398
        circumference_line = Line(start=LEFT*circumference_length/2, end=RIGHT*circumference_length/2, color=GREEN, stroke_width=4)
        self.objects["circumference_line"] = circumference_line

        # Label for circumference
        label_circumference = MathTex("C", color=GREEN)
        self.objects["label_circumference"] = label_circumference

        # Measuring diameter (vertical copy)
        measuring_diameter = Line(start=UP*1.2, end=DOWN*1.2, color=YELLOW, stroke_width=6)
        self.objects["measuring_diameter"] = measuring_diameter

        # Label for measuring diameter
        label_measuring_d = MathTex("D", color=YELLOW)
        self.objects["label_measuring_d"] = label_measuring_d

        # Pi symbol
        pi_symbol = MathTex(r"\pi \approx 3.14", color=PINK, font_size=36)
        self.objects["pi_symbol"] = pi_symbol

        # Footer formula
        footer_formula = MathTex(r"C = \pi D", color=WHITE, font_size=32)
        self.objects["footer_formula"] = footer_formula

        # Footer explanation
        footer_explanation = Text("The circumference is π times the diameter.", color=GRAY_B, font_size=24)
        self.objects["footer_explanation"] = footer_explanation

        # Initialize Layout Engine
        layout = LayoutEngine()

        # Register objects as LayoutObjects
        obj_title = LayoutObject(title, "title")
        obj_circle = LayoutObject(circle, "circle")
        obj_diameter_line = LayoutObject(diameter_line, "diameter_line")
        obj_label_diameter = LayoutObject(label_diameter, "label_diameter")
        obj_circumference_line = LayoutObject(circumference_line, "circumference_line")
        obj_label_circumference = LayoutObject(label_circumference, "label_circumference")
        obj_measuring_diameter = LayoutObject(measuring_diameter, "measuring_diameter")
        obj_label_measuring_d = LayoutObject(label_measuring_d, "label_measuring_d")
        obj_pi_symbol = LayoutObject(pi_symbol, "pi_symbol")
        obj_footer_formula = LayoutObject(footer_formula, "footer_formula")
        obj_footer_explanation = LayoutObject(footer_explanation, "footer_explanation")

        # Add objects to layout
        layout.add(obj_title)
        layout.add(obj_circle)
        layout.add(obj_diameter_line)
        layout.add(obj_label_diameter)
        layout.add(obj_circumference_line)
        layout.add(obj_label_circumference)
        layout.add(obj_measuring_diameter)
        layout.add(obj_label_measuring_d)
        layout.add(obj_pi_symbol)
        layout.add(obj_footer_formula)
        layout.add(obj_footer_explanation)

        # Assign to zones
        layout.add_to_zone(obj_title, "HEADER")
        layout.add_to_zone(obj_circle, "CONTENT")
        layout.add_to_zone(obj_diameter_line, "CONTENT")
        layout.add_to_zone(obj_label_diameter, "CONTENT")
        layout.add_to_zone(obj_circumference_line, "CONTENT")
        layout.add_to_zone(obj_label_circumference, "CONTENT")
        layout.add_to_zone(obj_measuring_diameter, "CONTENT")
        layout.add_to_zone(obj_label_measuring_d, "CONTENT")
        layout.add_to_zone(obj_pi_symbol, "CONTENT")
        layout.add_to_zone(obj_footer_formula, "FOOTER")
        layout.add_to_zone(obj_footer_explanation, "FOOTER")

        # Additional constraints for left-right split
        # Circle group to left side
        layout.add_constraint(obj_circle.center_x == -3.0)
        layout.add_constraint(obj_circle.center_y == 0)
        # Diameter line moves with circle
        layout.align_to(obj_diameter_line, obj_circle, 'CENTER')
        # Label diameter above the line
        layout.align_to(obj_label_diameter, obj_diameter_line, 'BOTTOM', buff=0.2)
        layout.add_constraint(obj_label_diameter.center_x == obj_diameter_line.center_x)

        # Circumference line to right side
        layout.add_constraint(obj_circumference_line.center_x == 3.0)
        layout.add_constraint(obj_circumference_line.center_y == 0)
        # Label circumference above the line
        layout.align_to(obj_label_circumference, obj_circumference_line, 'BOTTOM', buff=0.2)
        layout.add_constraint(obj_label_circumference.center_x == obj_circumference_line.center_x)

        # Measuring diameter starts at left end of circumference line
        layout.align_to(obj_measuring_diameter, obj_circumference_line, 'LEFT')
        layout.add_constraint(obj_measuring_diameter.center_y == obj_circumference_line.center_y - 1.5)
        # Label for measuring diameter
        layout.align_to(obj_label_measuring_d, obj_measuring_diameter, 'RIGHT', buff=0.2)
        layout.add_constraint(obj_label_measuring_d.center_y == obj_measuring_diameter.center_y)

        # Pi symbol above circumference line
        layout.align_to(obj_pi_symbol, obj_circumference_line, 'TOP', buff=0.5)
        layout.add_constraint(obj_pi_symbol.center_x == obj_circumference_line.center_x)

        # Center footer objects horizontally
        layout.add_constraint(obj_footer_formula.center_x == 0)
        layout.align_to(obj_footer_explanation, obj_footer_formula, 'BOTTOM', buff=0.3)
        layout.add_constraint(obj_footer_explanation.center_x == 0)

        # Solve layout
        layout.solve()

        # Apply positions to mobjects
        title.move_to(obj_title.get_center())
        circle.move_to(obj_circle.get_center())
        diameter_line.move_to(obj_diameter_line.get_center())
        label_diameter.move_to(obj_label_diameter.get_center())
        circumference_line.move_to(obj_circumference_line.get_center())
        label_circumference.move_to(obj_label_circumference.get_center())
        measuring_diameter.move_to(obj_measuring_diameter.get_center())
        label_measuring_d.move_to(obj_label_measuring_d.get_center())
        pi_symbol.move_to(obj_pi_symbol.get_center())
        footer_formula.move_to(obj_footer_formula.get_center())
        footer_explanation.move_to(obj_footer_explanation.get_center())

        # Initially hide objects that appear later
        circumference_line.set_opacity(0)
        label_circumference.set_opacity(0)
        measuring_diameter.set_opacity(0)
        label_measuring_d.set_opacity(0)
        pi_symbol.set_opacity(0)
        footer_formula.set_opacity(0)
        footer_explanation.set_opacity(0)

        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Create(circle))
        self.wait(max(0.1, max(0.1, 6.432 - 1.0)))  # Approx animation time 1s

        # Step 2
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Create diameter_line
        self.play(Create(diameter_line))
        # Visual action: Write label_diameter
        self.play(Write(label_diameter))
        self.wait(max(0.1, max(0.1, 2.448 - 2.0)))  # Approx animation time 2s

        # Step 3
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate circle
        self.play(Indicate(circle, color=WHITE))
        # Visual action: Transform circle perimeter to circumference line
        # We'll create a perimeter copy and morph it
        perimeter = circle.copy().set_color(GREEN).set_stroke(width=4)
        self.play(Create(perimeter))
        self.play(
            perimeter.animate.put_start_and_end_on(
                circumference_line.get_start(),
                circumference_line.get_end()
            ),
            FadeOut(circle),
            run_time=2
        )
        self.play(FadeOut(perimeter))
        circumference_line.set_opacity(1)
        self.play(Create(circumference_line))
        self.wait(max(0.1, max(0.1, 5.496 - 4.0)))  # Approx animation time 4s

        # Step 4
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Create circumference_line (already done, ensure visible)
        # Visual action: Write label_circumference
        label_circumference.set_opacity(1)
        self.play(Write(label_circumference))
        self.wait(max(0.1, max(0.1, 6.72 - 1.0)))  # Approx animation time 1s

        # Step 5
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Indicate measuring_diameter
        measuring_diameter.set_opacity(1)
        self.play(Indicate(measuring_diameter, color=YELLOW))
        # Visual action: Create measuring_diameter and animate copies along line
        self.play(Create(measuring_diameter))
        label_measuring_d.set_opacity(1)
        self.play(Write(label_measuring_d))

        # Create copies of diameter along the circumference line
        num_copies = 3
        diameter_copies = VGroup()
        for i in range(num_copies):
            copy = measuring_diameter.copy().set_opacity(0.5)
            copy.move_to(circumference_line.get_start() + RIGHT * (i * 2.4) + RIGHT*1.2)
            diameter_copies.add(copy)
        # Add a partial copy for the ~0.14 remainder
        partial_copy = measuring_diameter.copy().set_opacity(0.3).scale(0.14, about_point=measuring_diameter.get_start())
        partial_copy.move_to(circumference_line.get_start() + RIGHT * (3 * 2.4) + RIGHT*0.14*1.2)
        diameter_copies.add(partial_copy)

        self.play(LaggedStart(*[FadeIn(copy) for copy in diameter_copies], lag_ratio=0.3))
        self.wait(max(0.1, max(0.1, 7.152 - 4.0)))  # Approx animation time 4s

        # Step 6
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Write pi_symbol
        pi_symbol.set_opacity(1)
        self.play(Write(pi_symbol))
        # Visual action: FadeIn pi_symbol (already done via Write)
        self.wait(max(0.1, max(0.1, 8.328 - 1.0)))  # Approx animation time 1s

        # Step 7
        audio_file = "media/audio/呈現一個直徑為_D_的圓_將圓周_展開__6790d4e52a/step_06.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        # Signal action: Circumscribe footer_formula
        footer_formula.set_opacity(1)
        footer_explanation.set_opacity(1)
        self.play(Circumscribe(footer_formula, color=YELLOW, run_time=1))
        # Visual action: Write footer_formula and footer_explanation
        self.play(Write(footer_formula))
        self.play(Write(footer_explanation))
        self.wait(max(0.1, max(0.1, 4.704 - 2.0)))  # Approx animation time 2s

        # Final wait
        self.wait(max(0.1, 2))