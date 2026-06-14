from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("畢氏定理求斜邊長", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Right triangle vertices
        A = np.array([-3.5, -1.5, 0])  # right angle corner
        B = np.array([0.5, -1.5, 0])   # along base (8 cm)
        C = np.array([-3.5, 1.5, 0])   # up (6 cm)

        triangle = Polygon(A, B, C, color=BLUE)

        # Right angle mark
        ra_size = 0.3
        right_angle = Polygon(
            A,
            A + np.array([ra_size, 0, 0]),
            A + np.array([ra_size, ra_size, 0]),
            A + np.array([0, ra_size, 0]),
            color=WHITE,
        )

        self.play(Create(triangle), Create(right_angle))
        self.wait(0.5)

        # Label legs
        leg_a = Tex("6", font_size=36, color=YELLOW).next_to(
            (A + C) / 2, LEFT, buff=0.3
        )
        leg_b = Tex("8", font_size=36, color=YELLOW).next_to(
            (A + B) / 2, DOWN, buff=0.3
        )
        hyp = Tex("c", font_size=36, color=GREEN).next_to(
            (B + C) / 2, UR, buff=0.1
        )

        self.play(Write(leg_a), Write(leg_b))
        self.wait(0.5)
        self.play(Write(hyp))
        self.wait(0.5)

        # Pythagorean theorem steps
        steps = VGroup(
            MathTex("6^2 + 8^2 = c^2"),
            MathTex("36 + 64 = c^2"),
            MathTex("100 = c^2"),
            MathTex("c = \\sqrt{100} = 10"),
        ).arrange(DOWN, buff=0.4).scale(0.9)
        steps.to_edge(RIGHT, buff=0.8)

        self.play(Write(steps[0]))
        self.wait(0.6)
        self.play(TransformMatchingTex(steps[0].copy(), steps[1]))
        self.wait(0.6)
        self.play(Write(steps[2]))
        self.wait(0.6)
        self.play(Write(steps[3]))
        self.wait(0.6)

        # Highlight final answer
        box = SurroundingRectangle(steps[3], color=GREEN, buff=0.15)
        answer = Text("斜邊長 = 10 公分", font_size=36, color=GREEN)
        answer.next_to(box, DOWN, buff=0.4)

        self.play(Create(box))
        self.play(Write(answer))

        # Update hyp label with value
        hyp_val = Tex("10", font_size=36, color=GREEN).move_to(hyp)
        self.play(Transform(hyp, hyp_val))
        self.wait(2)