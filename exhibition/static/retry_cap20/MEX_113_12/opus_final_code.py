from manim import *


class GeneratedScene(Scene):
    def construct(self):
        title = Text("二次函數的最大最小值", font="STSong").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Two functions
        eqA = MathTex("y = (x+20)^2 + 60", color=BLUE).scale(0.8)
        eqB = MathTex("y = -(x-30)^2 + 60", color=RED).scale(0.8)
        labelA = Text("甲", font="STSong", color=BLUE).scale(0.7)
        labelB = Text("乙", font="STSong", color=RED).scale(0.7)

        groupA = VGroup(labelA, eqA).arrange(RIGHT, buff=0.3)
        groupB = VGroup(labelB, eqB).arrange(RIGHT, buff=0.3)
        eqs = VGroup(groupA, groupB).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(groupA, shift=RIGHT))
        self.play(FadeIn(groupB, shift=RIGHT))
        self.wait(0.5)

        # Axes for visual
        axes = Axes(
            x_range=[-40, 40, 20],
            y_range=[-40, 80, 40],
            x_length=6,
            y_length=3.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).to_edge(DOWN, buff=0.5)

        parabA = axes.plot(lambda x: 0.02 * (x + 20) ** 2 + 60 * 0.02, color=BLUE, x_range=[-40, 5])
        parabB = axes.plot(lambda x: -0.02 * (x - 30) ** 2 + 60 * 0.02, color=RED, x_range=[5, 40])

        # vertices in scaled coords
        vertexA = Dot(axes.c2p(-20, 60 * 0.02), color=BLUE)
        vertexB = Dot(axes.c2p(30, 60 * 0.02), color=RED)

        self.play(Create(axes))
        self.play(Create(parabA), Create(parabB))
        self.play(FadeIn(vertexA), FadeIn(vertexB))
        self.wait(0.5)

        # Analysis A
        noteA = VGroup(
            Text("甲：係數 +1 > 0，開口向上", font="STSong", color=BLUE).scale(0.5),
            Text("⇒ 有最小值", font="STSong", color=BLUE).scale(0.5),
            Text("頂點 x=-20, y_min=60", font="STSong", color=BLUE).scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        noteA.to_edge(LEFT, buff=0.3).shift(DOWN * 0.5)

        self.play(Write(noteA))
        self.wait(1)

        # Analysis B
        noteB = VGroup(
            Text("乙：係數 -1 < 0，開口向下", font="STSong", color=RED).scale(0.5),
            Text("⇒ 有最大值", font="STSong", color=RED).scale(0.5),
            Text("頂點 x=30, y_max=60", font="STSong", color=RED).scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        noteB.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

        self.play(Write(noteB))
        self.wait(1)

        # Evaluate options
        self.play(FadeOut(noteA), FadeOut(noteB), FadeOut(axes),
                  FadeOut(parabA), FadeOut(parabB),
                  FadeOut(vertexA), FadeOut(vertexB))

        optC = Text("(C) 乙有最大值，且其值為 x=30 時的 y 值 → 正確",
                    font="STSong", color=GREEN).scale(0.55)
        optC.next_to(eqs, DOWN, buff=0.8)

        check = MathTex(r"y_{max} = -(30-30)^2 + 60 = 60", color=GREEN).scale(0.7)
        check.next_to(optC, DOWN, buff=0.4)

        box = SurroundingRectangle(optC, color=GREEN, buff=0.15)

        self.play(Write(optC))
        self.play(Create(box))
        self.play(Write(check))
        self.wait(2)

        ans = Text("答案：(C)", font="STSong", color=YELLOW).scale(0.9)
        ans.next_to(check, DOWN, buff=0.5)
        self.play(FadeIn(ans, scale=1.2))
        self.wait(2)