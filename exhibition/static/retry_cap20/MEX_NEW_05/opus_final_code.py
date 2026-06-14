from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("解一元二次方程式", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        eq = MathTex("x^2", "-", "5x", "+", "6", "=", "0", font_size=60)
        eq.next_to(title, DOWN, buff=0.8)
        self.play(Write(eq))
        self.wait(1)

        # Step 1: factorization
        step1 = Text("（1）因式分解", font_size=30, color=YELLOW)
        step1.next_to(eq, DOWN, buff=0.8).to_edge(LEFT, buff=1)
        self.play(FadeIn(step1))

        factored = MathTex("(x-2)", "(x-3)", "=", "0", font_size=60)
        factored.next_to(step1, DOWN, buff=0.6)
        self.play(TransformFromCopy(eq, factored))
        self.wait(1)

        # highlight the two factors
        box1 = SurroundingRectangle(factored[0], color=BLUE)
        box2 = SurroundingRectangle(factored[1], color=GREEN)
        self.play(Create(box1))
        self.play(Create(box2))
        self.wait(1)

        # Step 2: zero product property
        step2 = Text("（2）零積定理：令每個因式為零", font_size=28, color=YELLOW)
        step2.next_to(factored, DOWN, buff=0.8)
        self.play(FadeIn(step2))
        self.wait(0.5)

        # factor 1 -> equation
        eq1 = MathTex("x-2", "=", "0", font_size=50, color=BLUE)
        eq2 = MathTex("x-3", "=", "0", font_size=50, color=GREEN)
        eq1.next_to(step2, DOWN, buff=0.6).shift(LEFT * 2.5)
        eq2.next_to(step2, DOWN, buff=0.6).shift(RIGHT * 2.5)

        self.play(Indicate(box1, color=BLUE), TransformFromCopy(factored[0], eq1))
        self.wait(0.5)
        self.play(Indicate(box2, color=GREEN), TransformFromCopy(factored[1], eq2))
        self.wait(1)

        # Step 3: solutions
        step3 = Text("（3）解出答案", font_size=30, color=YELLOW)
        step3.next_to(eq1, DOWN, buff=0.9).shift(RIGHT * 2.5)
        self.play(FadeIn(step3))

        sol1 = MathTex("x=2", font_size=55, color=BLUE)
        sol2 = MathTex("x=3", font_size=55, color=GREEN)
        sol1.next_to(step3, DOWN, buff=0.5).shift(LEFT * 2.5)
        sol2.next_to(step3, DOWN, buff=0.5).shift(RIGHT * 2.5)

        self.play(TransformFromCopy(eq1, sol1))
        self.play(TransformFromCopy(eq2, sol2))
        self.wait(1)

        final_x2 = MathTex("x=2", font_size=60, color=BLUE)
        final_or = Text("或", font_size=48)
        final_x3 = MathTex("x=3", font_size=60, color=GREEN)
        final = VGroup(final_x2, final_or, final_x3).arrange(RIGHT, buff=0.5)
        final.to_edge(DOWN, buff=0.8)
        box_final = SurroundingRectangle(final, color=YELLOW, buff=0.3)
        self.play(Write(final), Create(box_final))
        self.wait(2)