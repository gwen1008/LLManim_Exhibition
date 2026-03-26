from manim import *
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        
        # Create anchors
        title_anchor = 3.5 * UP
        axes_anchor = ORIGIN
        explanation_anchor = 3.5 * DOWN
        
        # Create objects from layout_plan
        # title
        title = Text("Graphing a Parabola: Transformations", color=WHITE, font_size=40)
        title.move_to(title_anchor)
        self.objects["title"] = title
        
        # axes
        axes = Axes(
            x_range=[-3, 7, 1],
            y_range=[-5, 5, 1],
            x_length=12,
            y_length=8,
            axis_config={"include_numbers": True}
        )
        axes.move_to(axes_anchor)
        self.objects["axes"] = axes
        
        # parent_graph (will be created on axes)
        parent_graph = axes.plot(lambda x: x**2, x_range=[-3, 5])
        parent_graph.set_color(BLUE)
        parent_graph.set_stroke(width=3)
        self.objects["parent_graph"] = parent_graph
        
        # parent_eq_label
        parent_eq_label = MathTex(r"y = x^2", color=BLUE)
        parent_eq_label.next_to(axes, UP, buff=0.2).to_edge(LEFT, buff=1)
        self.objects["parent_eq_label"] = parent_eq_label
        
        # final_graph (initially invisible)
        final_graph = axes.plot(lambda x: (x-2)**2 - 3, x_range=[-1, 5])
        final_graph.set_color(GREEN)
        final_graph.set_stroke(width=5)
        final_graph.move_to(axes.c2p(2, -3))
        self.objects["final_graph"] = final_graph
        
        # final_eq_label
        final_eq_label = MathTex(r"y = (x-2)^2 - 3", color=GREEN)
        final_eq_label.next_to(axes, UP, buff=0.2).to_edge(RIGHT, buff=1)
        self.objects["final_eq_label"] = final_eq_label
        
        # vertex_dot
        vertex_dot = Dot(radius=0.08, color=RED, fill_opacity=1.0)
        vertex_dot.move_to(axes.c2p(2, -3))
        self.objects["vertex_dot"] = vertex_dot
        
        # vertex_label
        vertex_label = MathTex(r"(2,\,-3)", color=RED)
        vertex_label.next_to(vertex_dot, UP+RIGHT, buff=0.2).shift(LEFT * 1.5)
        self.objects["vertex_label"] = vertex_label
        
        # axis_line
        axis_line = DashedLine(
            start=axes.c2p(2, -5),
            end=axes.c2p(2, 5),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.1
        )
        self.objects["axis_line"] = axis_line
        
        # axis_label
        axis_label = MathTex(r"x = 2", color=YELLOW)
        axis_label.next_to(axis_line, UP, buff=0.1).to_edge(UP, buff=1.0)
        self.objects["axis_label"] = axis_label
        
        # step_explanation
        step_explanation = Text("We start with the basic parabola, y = x^2.", color=LIGHT_GRAY, font_size=28)
        step_explanation.move_to(explanation_anchor)
        step_explanation.scale(0.8)
        self.objects["step_explanation"] = step_explanation
        
        # ========== PHASE 2: Animation Sequence (UNROLLED) ==========
        
        # ========== Step 1 ==========
        audio_step1 = "media/audio/Draw_the_parabola_re_a55f895d06/step_00.mp3"
        if os.path.exists(audio_step1):
            self.add_sound(audio_step1)
        elif os.path.exists(audio_step1.replace(".mp3", ".wav")):
            self.add_sound(audio_step1.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["parent_eq_label"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["axes"]), run_time=1.5)
        remaining_1 = max(0.1, 5.664 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_1))
        
        # ========== Step 2 ==========
        audio_step2 = "media/audio/Draw_the_parabola_re_a55f895d06/step_01.mp3"
        if os.path.exists(audio_step2):
            self.add_sound(audio_step2)
        elif os.path.exists(audio_step2.replace(".mp3", ".wav")):
            self.add_sound(audio_step2.replace(".mp3", ".wav"))
        
        self.play(Create(self.objects["parent_graph"]), run_time=2.0)
        remaining_2 = max(0.1, 4.704 - 2.0 + 0.5)
        self.wait(max(0.1, remaining_2))
        
        # ========== Step 3 ==========
        audio_step3 = "media/audio/Draw_the_parabola_re_a55f895d06/step_02.mp3"
        if os.path.exists(audio_step3):
            self.add_sound(audio_step3)
        elif os.path.exists(audio_step3.replace(".mp3", ".wav")):
            self.add_sound(audio_step3.replace(".mp3", ".wav"))
        
        self.play(Write(self.objects["final_eq_label"]), run_time=1.5)
        remaining_3 = max(0.1, 8.064 - 1.5 + 0.5)
        self.wait(max(0.1, remaining_3))
        
        # ========== Step 4 ==========
        audio_step4 = "media/audio/Draw_the_parabola_re_a55f895d06/step_03.mp3"
        if os.path.exists(audio_step4):
            self.add_sound(audio_step4)
        elif os.path.exists(audio_step4.replace(".mp3", ".wav")):
            self.add_sound(audio_step4.replace(".mp3", ".wav"))
        
        # Indicate part of final_eq_label (x-2)
        self.play(Indicate(self.objects["final_eq_label"][0][4:6], color=ORANGE, run_time=1))
        self.play(Transform(self.objects["parent_graph"], self.objects["final_graph"]), run_time=3.0)
        remaining_4 = max(0.1, 8.4 - 3.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_4))
        
        # ========== Step 5 ==========
        audio_step5 = "media/audio/Draw_the_parabola_re_a55f895d06/step_04.mp3"
        if os.path.exists(audio_step5):
            self.add_sound(audio_step5)
        elif os.path.exists(audio_step5.replace(".mp3", ".wav")):
            self.add_sound(audio_step5.replace(".mp3", ".wav"))
        
        # Indicate part of final_eq_label (-3)
        self.play(Indicate(self.objects["final_eq_label"][0][8:10], color=PINK, run_time=1))
        self.play(Create(self.objects["vertex_dot"]), run_time=1.5)
        remaining_5 = max(0.1, 10.368 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_5))
        
        # ========== Step 6 ==========
        audio_step6 = "media/audio/Draw_the_parabola_re_a55f895d06/step_05.mp3"
        if os.path.exists(audio_step6):
            self.add_sound(audio_step6)
        elif os.path.exists(audio_step6.replace(".mp3", ".wav")):
            self.add_sound(audio_step6.replace(".mp3", ".wav"))
        
        self.play(Indicate(self.objects["vertex_dot"], color=RED, run_time=1))
        self.play(
            Write(self.objects["vertex_label"]),
            Create(self.objects["axis_line"]),
            run_time=2.0
        )
        remaining_6 = max(0.1, 9.384 - 2.0 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_6))
        
        # ========== Step 7 ==========
        audio_step7 = "media/audio/Draw_the_parabola_re_a55f895d06/step_06.mp3"
        if os.path.exists(audio_step7):
            self.add_sound(audio_step7)
        elif os.path.exists(audio_step7.replace(".mp3", ".wav")):
            self.add_sound(audio_step7.replace(".mp3", ".wav"))
        
        self.play(Circumscribe(self.objects["axis_line"], color=YELLOW, run_time=1))
        self.play(Write(self.objects["axis_label"]), run_time=1.5)
        remaining_7 = max(0.1, 7.32 - 1.5 - 1.0 + 0.5)
        self.wait(max(0.1, remaining_7))