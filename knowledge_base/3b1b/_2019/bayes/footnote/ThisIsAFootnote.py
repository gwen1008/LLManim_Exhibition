# Source: 3b1b/_2019/bayes/footnote.py
# Description: [3b1b translated] 展示貝氏定理公式的視覺化推導過程，從縮圖圖像開始，逐步重排公式並加入註解，最後將完整方程式移動到畫面頂部。



from manim import *
class ThisIsAFootnote(TeacherStudentsScene):
    def construct(self):
        image = ImageMobject("bayes_thumbnail")
        image.set_height(2.5)
        rect = SurroundingRectangle(image, buff=0)
        rect.set_stroke(WHITE, 3)
        title = Tex("Bayes' theorem")
        title.match_width(image)
        title.next_to(image, UP)

        image_group = Group(rect, image, title)
        image_group.to_corner(UL)

        asterisk = Tex("*")
        asterisk.set_height(0.5)
        asterisk.set_stroke(BLACK, 3, background=True)
        asterisk.move_to(image.get_corner(UR), LEFT)

        formula = get_bayes_formula()
        formula.move_to(self.hold_up_spot, DOWN)

        pab = formula[:6]
        eq = formula[6]
        pa = formula[7:11]
        pba = formula[11:17]
        over = formula[17]
        pb = formula[18:23]

        # Show main video
        self.play(
            FadeIn(image_group, shift=DOWN),
            self.change_students(
                "pondering", "hooray", "tease",
                look_at=image
            )
        )
        self.play(
            Write(asterisk),
            self.teacher.animate.change("speaking"),
        )
        self.play(
            self.change_students(
                "thinking", "erm", "thinking"
            )
        )
        self.wait(3)
        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(formula, shift=DOWN),
            self.change_students(*3 * ["pondering"])
        )
        self.wait()

        # Rearrange
        parts = VGroup(
            pb, pab, eq, pa, pba,
        )
        parts.generate_target()
        parts.target.arrange(RIGHT, buff=SMALL_BUFF)
        parts.target.move_to(self.hold_up_spot)

        self.play(
            MoveToTarget(parts, path_arc=-30 * DEGREES),
            FadeOut(over),
            self.teacher.animate.change("pondering"),
        )
        self.wait()

        # Move to top
        p_both = MathTex(
            "P(A \\text{ and } B)",
            tex_to_color_map={"A": YELLOW, "B": BLUE},
        )
        eq2 = MathTex("=")
        full_equation = VGroup(
            pb, pab, eq, p_both, eq2, pa, pba
        )
        full_equation.generate_target()
        full_equation.target.arrange(RIGHT, buff=SMALL_BUFF)
        full_equation.target.set_width(FRAME_WIDTH - 1)
        full_equation.target.center()
        full_equation.target.to_edge(UP)

        p_both.set_opacity(0)
        p_both.scale(0.2)
        p_both.move_to(eq)
        eq2.move_to(eq)

        self.play(
            MoveToTarget(full_equation),
            FadeOut(image_group, shift=2 * LEFT),
            FadeOut(asterisk, shift=2 * LEFT),
            self.teacher.animate.look_at(4 * UP),
            self.change_students(
                "thinking", "erm", "confused",
                look_at=4 * UP
            )
        )
        self.wait(2)
