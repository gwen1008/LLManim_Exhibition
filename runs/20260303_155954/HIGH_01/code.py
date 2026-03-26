'''
# [VISUAL REASONING]
# 1. Pedagogical Goal: Visualize the linear function y=2x-1 by constructing it step-by-step from its y-intercept using the slope definition (rise/run). The staircase metaphor connects discrete steps to the continuous line.
# 2. Layout Strategy:
#    - Header Region: [y=3.5] for Title (equation)
#    - Main Content: [Center y=0] for coordinate plane and graphing
#    - Footer Region: [Bottom y=-3.5] for explanatory text
# 3. Anti-Overlap Check:
#    - Strategy: Use VGroups for step_path to keep staircase together. Position labels (rise, run) near segments. Keep footer text scaled.
# 4. Audio Check (CRITICAL):
#    - [x] Have I included self.add_sound() for EVERY step?
#    - [x] Files: "media/audio/slope_visualization/step_XX.mp3"
# 5. Animation Flow:
#    - Step 1: Create axes.
#    - Step 2: Write equation, signal with Indicate.
#    - Step 3: Plot y-intercept dot.
#    - Step 4: Update footer text, signal equation.
#    - Step 5: Add first horizontal step (run), label.
#    - Step 6: Add first vertical step (rise), label.
#    - Step 7: Build more steps, signal staircase.
#    - Step 8: Morph staircase into continuous line (key metaphor).
#    - Step 9: Highlight final line, update footer.
'''

from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Define anchors from layout_plan
        title_anchor = 3.5 * UP
        content_center = ORIGIN
        footer_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan.objects
        # axes
        axes = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-5, 5, 1],
            x_length=14,
            y_length=10,
            background_line_style={"stroke_color": "#333333", "stroke_opacity": 0.5},
            axis_config={"color": "#333333"}
        ).move_to(content_center)
        self.objects["axes"] = axes
        
        # line_eq_label
        line_eq_label = MathTex(r"y = 2x - 1", color=YELLOW, font_size=48).move_to(title_anchor)
        self.objects["line_eq_label"] = line_eq_label
        
        # y_intercept_dot
        y_intercept_dot = Dot(radius=0.08, color=GREEN).move_to(axes.c2p(0, -1))
        self.objects["y_intercept_dot"] = y_intercept_dot
        
        # y_intercept_label
        y_intercept_label = MathTex(r"(0, -1)", color=GREEN, font_size=36).next_to(y_intercept_dot, UP+LEFT, buff=0.1)
        self.objects["y_intercept_label"] = y_intercept_label
        
        # step_path (initially empty VGroup)
        step_path = VGroup()
        step_path.set_color(BLUE)
        step_path.set_stroke(width=4)
        step_path.move_to(content_center)
        self.objects["step_path"] = step_path
        
        # final_line (created but not added yet)
        final_line = Line(
            start=axes.c2p(-6, -13),
            end=axes.c2p(6, 11),
            color=RED,
            stroke_width=6
        ).move_to(content_center)
        self.objects["final_line"] = final_line
        
        # rise_label
        rise_label = MathTex(r"\mathrm{rise}=2", color=TEAL, font_size=32).move_to(axes.c2p(0.5, 0))
        self.objects["rise_label"] = rise_label
        
        # run_label
        run_label = MathTex(r"\mathrm{run}=1", color=ORANGE, font_size=32).move_to(axes.c2p(0, -0.5))
        self.objects["run_label"] = run_label
        
        # footer_text
        footer_text = Text("We begin with the coordinate plane and the equation.", color=GRAY_C, font_size=28).move_to(footer_anchor)
        self.objects["footer_text"] = footer_text
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_00.mp3")  # [auto-injected]
        # Step 1
        audio_step1 = "media/audio/slope_visualization/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Create(axes), run_time=1.5)
        remaining_1 = max(0.1, 2.0 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_01.mp3")  # [auto-injected]
        # Step 2
        audio_step2 = "media/audio/slope_visualization/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Indicate(line_eq_label, color=YELLOW, run_time=1))
        self.play(Write(line_eq_label), run_time=1.5)
        remaining_2 = max(0.1, 3.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_02.mp3")  # [auto-injected]
        # Step 3
        audio_step3 = "media/audio/slope_visualization/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(GrowFromCenter(y_intercept_dot), run_time=1.0)
        self.play(Create(y_intercept_dot), run_time=1.0)
        remaining_3 = max(0.1, 2.5 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_03.mp3")  # [auto-injected]
        # Step 4
        audio_step4 = "media/audio/slope_visualization/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(line_eq_label, color=TEAL, run_time=1))
        new_footer_text = Text("Slope = rise/run = 2. For every 1 unit right, go up 2.", color=GRAY_C, font_size=28).move_to(footer_anchor)
        self.play(Transform(footer_text, new_footer_text), run_time=1.5)
        footer_text = new_footer_text
        self.objects["footer_text"] = footer_text
        remaining_4 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_04.mp3")  # [auto-injected]
        # Step 5: Add horizontal step (run)
        audio_step5 = "media/audio/slope_visualization/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Create horizontal line from (0,-1) to (1,-1)
        h_line = Line(axes.c2p(0, -1), axes.c2p(1, -1), color=BLUE, stroke_width=4)
        step_path.add(h_line)
        # Position run label
        run_label.move_to(axes.c2p(0.5, -1.5))
        self.play(Create(h_line), Write(run_label), run_time=1.0)
        remaining_5 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_05.mp3")  # [auto-injected]
        # Step 6: Add vertical step (rise)
        audio_step6 = "media/audio/slope_visualization/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        v_line = Line(axes.c2p(1, -1), axes.c2p(1, 1), color=BLUE, stroke_width=4)
        step_path.add(v_line)
        # Position rise label
        rise_label.move_to(axes.c2p(1.5, 0))
        self.play(Create(v_line), Write(rise_label), run_time=1.0)
        remaining_6 = max(0.1, 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_06.mp3")  # [auto-injected]
        # Step 7: Build more steps
        audio_step7 = "media/audio/slope_visualization/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Indicate(step_path, color=BLUE, run_time=1))
        
        # Define more points: (1,1) to (2,1) to (2,3); (2,3) to (3,3) to (3,5); also left/down: (0,-1) to (-1,-1) to (-1,-3)
        points = [(1,1), (2,1), (2,3), (3,3), (3,5), (-1,-1), (-1,-3)]
        prev_point = (1,1)
        new_lines = []
        for i in range(1, len(points)):
            line = Line(axes.c2p(*prev_point), axes.c2p(*points[i]), color=BLUE, stroke_width=4)
            step_path.add(line)
            new_lines.append(line)
            prev_point = points[i]
        
        self.play(*[Create(line) for line in new_lines], run_time=2.5)
        new_footer_text2 = Text("Repeating the slope recipe gives more points on the line.", color=GRAY_C, font_size=28).move_to(footer_anchor)
        self.play(Transform(footer_text, new_footer_text2), run_time=1.0)
        footer_text = new_footer_text2
        self.objects["footer_text"] = footer_text
        remaining_7 = max(0.1, 5.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_7))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_07.mp3")  # [auto-injected]
        # Step 8: Morph staircase into continuous line
        audio_step8 = "media/audio/slope_visualization/step_07.mp3"
        if os.path.exists(audio_step8):
            self.add_sound(audio_step8)
        elif os.path.exists(audio_step8.replace(".mp3", ".wav")):
            self.add_sound(audio_step8.replace(".mp3", ".wav"))
        
        # Fade out labels first
        self.play(FadeOut(rise_label), FadeOut(run_label), run_time=0.5)
        # Morph step_path into final_line
        self.play(ReplacementTransform(step_path, final_line), run_time=2.0)
        new_footer_text3 = Text("The staircase becomes the continuous line y=2x-1.", color=GRAY_C, font_size=28).move_to(footer_anchor)
        self.play(Transform(footer_text, new_footer_text3), run_time=1.0)
        footer_text = new_footer_text3
        self.objects["footer_text"] = footer_text
        remaining_8 = max(0.1, 3.0 - 3.5 + 0.5)
        self.wait(max(0.1, remaining_8))
        
        self.add_sound("media/audio/Create_an_animation__ce6c930079/step_08.mp3")  # [auto-injected]
        # Step 9: Highlight final line
        audio_step9 = "media/audio/slope_visualization/step_08.mp3"
        if os.path.exists(audio_step9):
            self.add_sound(audio_step9)
        elif os.path.exists(audio_step9.replace(".mp3", ".wav")):
            self.add_sound(audio_step9.replace(".mp3", ".wav"))
        
        self.play(Indicate(final_line, color=RED, run_time=1))
        self.play(Create(final_line), run_time=1.0)  # Ensure line is highlighted
        new_footer_text4 = Text("Graph of y=2x-1: slope 2, y-intercept -1.", color=GRAY_C, font_size=28).move_to(footer_anchor)
        self.play(Transform(footer_text, new_footer_text4), run_time=1.5)
        remaining_9 = max(0.1, 4.0 - 2.5 + 0.5)
        self.wait(max(0.1, remaining_9))
        
        # Final hold
        self.wait(max(0.1, 2))