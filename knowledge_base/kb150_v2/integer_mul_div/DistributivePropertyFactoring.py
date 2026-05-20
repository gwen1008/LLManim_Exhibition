# [VISUAL REASONING]
# Implements reverse distributive law: factor out -17, simplify bracket to 100, multiply to -1700.
# Vertical layout: title (top), step label (upper), equation (center), explanation (bottom).

from manim import *

class DistributivePropertyFactoring(Scene):
    def construct(self):
        # Step 1
        title = Text("Reverse Distributive Law", color=WHITE, font_size=38).to_edge(UP, buff=0.5)
        step_label = Text("Step 1: Original Expression", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq1 = MathTex(r"(-17) \times 35 - (-17) \times (-65)", color=WHITE).move_to(ORIGIN)
        
        anim_time_1 = 3.0
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(step_label), Write(eq1), run_time=1.8)
        self.wait(5.23)

        # Step 2
        explain1 = Text("Both terms share the common factor (-17)", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        anim_time_2 = 3.0
        self.play(Write(explain1), run_time=1.5)
        self.play(Circumscribe(eq1, color=YELLOW), run_time=1.5)
        self.wait(2.04)

        # Step 3
        step_label_2 = Text("Step 2: Factor Out (-17)", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq2 = MathTex(r"(-17) \times \left[ 35 - (-65) \right]", color=WHITE).move_to(ORIGIN)
        explain2 = Text("Factor out (-17) using reverse distributive law", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        
        anim_time_3 = 2.5
        self.play(FadeOut(explain1), FadeOut(step_label), run_time=0.5)
        self.play(ReplacementTransform(eq1, eq2), FadeIn(step_label_2), FadeIn(explain2), run_time=2.0)
        self.wait(3.16)

        # Step 4
        step_label_3 = Text("Step 3: Simplify the Bracket", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq3 = MathTex(r"(-17) \times 100", color=WHITE).move_to(ORIGIN)
        explain3 = Text("Compute 35 - (-65) = 35 + 65 = 100", color=WHITE, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        
        anim_time_4 = 3.0
        self.play(Indicate(eq2, color=RED), run_time=1.0)
        self.play(FadeOut(explain2), FadeOut(step_label_2), run_time=0.3)
        self.play(ReplacementTransform(eq2, eq3), FadeIn(step_label_3), FadeIn(explain3), run_time=1.7)
        self.wait(3.04)

        # Step 5
        step_label_4 = Text("Step 4: Final Multiplication", color=YELLOW, font_size=28).move_to(ORIGIN + np.array([0, 1.8, 0]))
        eq4 = MathTex(r"-1700", color=GREEN).move_to(ORIGIN)
        explain4 = Text("Multiply: (-17) x 100 = -1700", color=GREEN, font_size=26).move_to(ORIGIN + np.array([0, -2.3, 0]))
        
        anim_time_5 = 3.0
        self.play(FadeOut(explain3), FadeOut(step_label_3), run_time=0.5)
        self.play(ReplacementTransform(eq3, eq4), FadeIn(step_label_4), FadeIn(explain4), run_time=1.5)
        answer_box = SurroundingRectangle(eq4, color=GREEN, buff=0.3)
        self.play(Create(answer_box), run_time=1.0)
        self.wait(3.79)
