from manim import *


class GeneratedScene(Scene):
    def construct(self):
        # 座標設定 BC = 3
        B = np.array([-1.5, -1.2, 0])
        C = np.array([1.5, -1.2, 0])
        A = np.array([0.30, 1.37, 0])  # 2.57 - 1.2
        r = 3.0

        # 標題
        title = Text("三角形與兩圓的位置關係", font="STSong").scale(0.7).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 三角形
        tri = Polygon(A, B, C, color=WHITE)
        a_dot = Dot(A, color=YELLOW)
        b_dot = Dot(B, color=BLUE)
        c_dot = Dot(C, color=GREEN)
        a_lbl = Text("A", color=YELLOW).scale(0.5).next_to(A, UP)
        b_lbl = Text("B", color=BLUE).scale(0.5).next_to(B, DL)
        c_lbl = Text("C", color=GREEN).scale(0.5).next_to(C, DR)

        self.play(Create(tri))
        self.play(*[FadeIn(d) for d in (a_dot, b_dot, c_dot)],
                  *[Write(l) for l in (a_lbl, b_lbl, c_lbl)])
        self.wait(0.3)

        # 角度標示
        angB = Text("∠B = 55°").scale(0.45).set_color(BLUE)
        angC = Text("∠C = 65°").scale(0.45).set_color(GREEN)
        angA = Text("∠A = 60°").scale(0.45).set_color(YELLOW)
        info = VGroup(angB, angC, angA).arrange(DOWN, aligned_edge=LEFT).to_corner(UL).shift(DOWN*0.8)
        self.play(Write(angB), Write(angC))
        self.wait(0.3)
        self.play(Write(angA))
        self.wait(0.5)

        # 圓 B
        circB = Circle(radius=r, color=BLUE).move_to(B)
        radB = Line(B, C, color=BLUE_E)
        self.play(Create(radB))
        self.play(Create(circB))
        self.wait(0.3)

        # 圓 C
        circC = Circle(radius=r, color=GREEN).move_to(C)
        radC = Line(C, B, color=GREEN_E)
        self.play(Create(circC))
        self.wait(0.5)

        # 判斷 BA 與 BC
        ba = Line(B, A, color=YELLOW)
        self.play(Create(ba))
        cmp1 = Text("BA 對 ∠C(65°) > BC 對 ∠A(60°)", font="STSong").scale(0.4).to_edge(DOWN)
        cmp1b = Text("⇒ BA > BC ⇒ A 在圓 B 外部", font="STSong").scale(0.45).set_color(RED).next_to(cmp1, UP)
        self.play(Write(cmp1))
        self.play(Write(cmp1b))
        self.play(Indicate(a_dot), circB.animate.set_stroke(width=6))
        self.wait(0.8)
        self.play(FadeOut(cmp1), FadeOut(cmp1b), FadeOut(ba))

        # 判斷 CA 與 BC
        ca = Line(C, A, color=YELLOW)
        self.play(Create(ca))
        cmp2 = Text("CA 對 ∠B(55°) < BC 對 ∠A(60°)", font="STSong").scale(0.4).to_edge(DOWN)
        cmp2b = Text("⇒ CA < BC ⇒ A 在圓 C 內部", font="STSong").scale(0.45).set_color(RED).next_to(cmp2, UP)
        self.play(Write(cmp2))
        self.play(Write(cmp2b))
        self.play(Indicate(a_dot), circC.animate.set_stroke(width=6))
        self.wait(0.8)
        self.play(FadeOut(cmp2), FadeOut(cmp2b), FadeOut(ca))

        # 結論
        ans = Text("(D) 在圓 B 內部，在圓 C 外部 ✗", font="STSong").scale(0.5).set_color(GREY)
        ans_correct = Text("(A) 在圓 B 外部，在圓 C 內部", font="STSong").scale(0.55).set_color(YELLOW)
        ans_correct.to_edge(DOWN)
        box = SurroundingRectangle(ans_correct, color=YELLOW, buff=0.2)
        self.play(Write(ans_correct))
        self.play(Create(box))
        self.wait(2)