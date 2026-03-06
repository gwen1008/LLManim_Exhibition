from manim import *
from utils.layout_engine import LayoutEngine, LayoutObject
import os

class GeneratedScene(Scene):
    def construct(self):
        # ========== PHASE 1: Layout & Object Creation ==========
        self.objects = {}
        layout = LayoutEngine()

        # Create objects from layout_plan
        # 1. Title
        title = Text("Graphing y = 2x - 1", color=WHITE, font_size=40)
        self.objects["title"] = title
        layout.add(LayoutObject(title, "title"))

        # 2. Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True},
            color=GREY
        )
        self.objects["axes"] = axes
        layout.add(LayoutObject(axes, "axes"))

        # 3. Equation display
        eq_display = MathTex("y = 2x - 1", color=YELLOW, font_size=36)
        self.objects["eq_display"] = eq_display
        layout.add(LayoutObject(eq_display, "eq_display"))

        # 4. Intercept point and label
        point_intercept = Dot(radius=0.08, color=GREEN).move_to(axes.c2p(0, -1))
        self.objects["point_intercept"] = point_intercept
        layout.add(LayoutObject(point_intercept, "point_intercept"))

        label_intercept = MathTex("(0, -1)", color=GREEN, font_size=24).next_to(point_intercept, LEFT+UP, buff=0.2)
        self.objects["label_intercept"] = label_intercept
        layout.add(LayoutObject(label_intercept, "label_intercept"))

        # 5. Run arrow and label
        arrow_run = Arrow(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, -1),
            color=BLUE,
            stroke_width=6,
            buff=0
        )
        self.objects["arrow_run"] = arrow_run
        layout.add(LayoutObject(arrow_run, "arrow_run"))

        label_run = MathTex("\\text{run}=1", color=BLUE, font_size=24).next_to(arrow_run, DOWN, buff=0.1)
        self.objects["label_run"] = label_run
        layout.add(LayoutObject(label_run, "label_run"))

        # 6. Rise arrow and label
        arrow_rise = Arrow(
            start=axes.c2p(1, -1),
            end=axes.c2p(1, 1),
            color=RED,
            stroke_width=6,
            buff=0
        )
        self.objects["arrow_rise"] = arrow_rise
        layout.add(LayoutObject(arrow_rise, "arrow_rise"))

        label_rise = MathTex("\\text{rise}=2", color=RED, font_size=24).next_to(arrow_rise, RIGHT, buff=0.1)
        self.objects["label_rise"] = label_rise
        layout.add(LayoutObject(label_rise, "label_rise"))

        # 7. Second point and label
        point_second = Dot(radius=0.08, color=GREEN).move_to(axes.c2p(1, 1))
        self.objects["point_second"] = point_second
        layout.add(LayoutObject(point_second, "point_second"))

        label_second = MathTex("(1, 1)", color=GREEN, font_size=24).next_to(point_second, RIGHT+UP, buff=0.2)
        self.objects["label_second"] = label_second
        layout.add(LayoutObject(label_second, "label_second"))

        # 8. Line segment (function segment)
        line_function = Line(
            start=axes.c2p(0, -1),
            end=axes.c2p(1, 1),
            color=YELLOW,
            stroke_width=6
        )
        self.objects["line_function"] = line_function
        layout.add(LayoutObject(line_function, "line_function"))

        # 9. Full line
        line_full = Line(
            start=axes.c2p(-2, -5),
            end=axes.c2p(3, 5),
            color=YELLOW,
            stroke_width=4
        )
        self.objects["line_full"] = line_full
        layout.add(LayoutObject(line_full, "line_full"))

        # 10. Explanation text (initial content)
        explanation_text = Text(
            "Step 1: Set up the coordinate plane and the equation.",
            color=LIGHT_GREY,
            font_size=28
        )
        self.objects["explanation_text"] = explanation_text
        layout.add(LayoutObject(explanation_text, "explanation_text"))

        # Apply layout zones
        layout.add_to_zone(layout.get("title"), "HEADER")
        layout.add_to_zone(layout.get("eq_display"), "HEADER")
        layout.add_to_zone(layout.get("axes"), "CONTENT")
        layout.add_to_zone(layout.get("point_intercept"), "CONTENT")
        layout.add_to_zone(layout.get("label_intercept"), "CONTENT")
        layout.add_to_zone(layout.get("arrow_run"), "CONTENT")
        layout.add_to_zone(layout.get("label_run"), "CONTENT")
        layout.add_to_zone(layout.get("arrow_rise"), "CONTENT")
        layout.add_to_zone(layout.get("label_rise"), "CONTENT")
        layout.add_to_zone(layout.get("point_second"), "CONTENT")
        layout.add_to_zone(layout.get("label_second"), "CONTENT")
        layout.add_to_zone(layout.get("line_function"), "CONTENT")
        layout.add_to_zone(layout.get("line_full"), "CONTENT")
        layout.add_to_zone(layout.get("explanation_text"), "FOOTER")

        # Center axes in content zone
        layout.add_constraint(layout.get("axes").center_x == 0)
        layout.add_constraint(layout.get("axes").center_y == 0)

        # Align equation below title
        layout.align_to(layout.get("eq_display"), layout.get("title"), "BOTTOM", buff=0.5)
        layout.add_constraint(layout.get("eq_display").center_x == 0)

        # Solve layout
        layout.solve()

        # ========== PHASE 2: Animation Sequence ==========
        # Step 1
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_00.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Write(self.objects["title"]))
        self.play(Create(self.objects["axes"]))
        self.wait(4.608 - 2)  # Approximate remaining time after animations

        # Step 2
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_01.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["eq_display"], color=YELLOW))
        self.play(
            LaggedStart(
                Write(self.objects["eq_display"]),
                Create(self.objects["point_intercept"]),
                Write(self.objects["label_intercept"]),
                lag_ratio=0.5
            )
        )
        self.wait(7.44 - 3)

        # Step 3
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_02.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Circumscribe(self.objects["point_intercept"], color=GREEN, run_time=1))
        self.play(GrowArrow(self.objects["arrow_run"]))
        self.wait(7.992 - 2)

        # Step 4
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_03.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(Indicate(self.objects["arrow_run"], color=BLUE))
        self.play(
            LaggedStart(
                GrowArrow(self.objects["arrow_rise"]),
                Create(self.objects["point_second"]),
                Write(self.objects["label_second"]),
                lag_ratio=0.5
            )
        )
        self.wait(6.552 - 3)

        # Step 5
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_04.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        arrow_group = VGroup(self.objects["arrow_run"], self.objects["arrow_rise"])
        self.play(Transform(arrow_group, self.objects["line_function"]))
        self.wait(9.672 - 1)

        # Step 6
        audio_file = "media/audio/畫出_y___2x___1_的函數圖形__6e74e04968/step_05.mp3"
        if os.path.exists(audio_file):
            self.add_sound(audio_file)
        self.play(
            LaggedStart(
                Write(self.objects["label_rise"]),
                Write(self.objects["label_run"]),
                Create(self.objects["line_full"]),
                lag_ratio=0.5
            )
        )
        self.wait(10.944 - 3)