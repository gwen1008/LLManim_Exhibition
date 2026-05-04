# Source: 3b1b/_2019/bayes/footnote.py
# Description: [3b1b translated] 展示貝葉斯公式的視覺化推導，用一個生病的小人圖示和顏色標記來解釋條件機率中各項的意義。



from manim import *
class DiseaseBayes(Scene):
    def construct(self):
        formula = MathTex(
            "P(D | +) = {P(D) P(+ | D) \\over P(+)}",
            tex_to_color_map={
                "D": YELLOW,
                "+": BLUE,
            },
            isolate=list("P(|)=")
        )
        formula.scale(2.5)

        Ds = formula.get_parts_by_tex("D")
        for D in Ds:
            index = formula.index_of_part(D)
            pi = Randolph()
            pi.change("sick")
            pi.set_color(SICKLY_GREEN)
            pi.replace(D)
            formula.submobjects[index] = pi
            # 在 ManimCE 中，get_tex 不是標準屬性，我們改用自定義屬性
            pi.original_tex = "D"

        lhs = formula[:6]
        lhs.save_state()
        lhs.center()

        sicky = lhs[2]

        sick_words = TexText(
            "You are sick",
            tex_to_color_map={
                "sick": SICKLY_GREEN,
            },
        )
        sick_words.scale(1.5)
        sick_words.next_to(sicky, UP, 2 * LARGE_BUFF)
        positive_words = TexText("Positive test result")
        positive_words.scale(1.5)
        positive_words.set_color(BLUE)
        positive_words.next_to(lhs[4], DOWN, 2 * LARGE_BUFF)

        sick_arrow = Arrow(sicky.get_top(), sick_words.get_bottom())
        positive_arrow = Arrow(lhs[4].get_bottom(), positive_words.get_top())

        arrow_groups = VGroup(
            sick_words, sick_arrow,
            positive_words, positive_arrow,
        )

        sicky.save_state()
        sicky.change("happy")
        sicky.set_color(BLUE)

        self.play(FadeIn(lhs, shift=DOWN))
        self.play(
            Restore(sicky),
            GrowArrow(sick_arrow),
            FadeIn(sick_words, shift=DOWN),
        )
        self.play(
            GrowArrow(positive_arrow),
            FadeIn(positive_words, shift=UP),
        )
        self.wait(2)
        self.play(
            Restore(lhs),
            arrow_groups.animate.move_to(arrow_groups.get_center()),  # 保持相對位置
            FadeIn(formula[6]),
        )

        # Prior
        def get_formula_slice(*indices):
            return VGroup(*[formula[i] for i in indices])

        self.play(
            TransformFromCopy(
                get_formula_slice(0, 1, 2, 5),
                get_formula_slice(8, 9, 10, 11),
            ),
        )

        # Likelihood
        lhs_copy = formula[:6].copy()
        likelihood = formula[12:18]
        run_time = 1
        self.play(
            lhs_copy.animate.next_to(likelihood, UP),
            run_time=run_time,
        )
        self.play(
            lhs_copy[2].animate.move_to(lhs_copy[4].get_center()),
            lhs_copy[4].animate.move_to(lhs_copy[2].get_center()),
            run_time=run_time,
        )
        self.play(
            lhs_copy.animate.move_to(likelihood.get_center()),
            run_time=run_time,
        )

        # Evidence
        self.play(
            Create(formula.get_part_by_tex("\\over")),
            TransformFromCopy(
                get_formula_slice(12, 13, 14, 17),
                get_formula_slice(19, 20, 21, 22),
            ),
        )
        self.wait()
