# Source: 3b1b/_2019/bayes/part1.py
# Description: [3b1b translated] 展示貝葉斯公式的逐步建構過程，先標註假設與證據變數，再依序呈現先驗機率、似然函數和證據項，最後將公式縮小並置於畫面上方。



from manim import *
class IntroduceFormula(Scene):
    def construct(self):
        formula = get_bayes_formula()
        formula.save_state()
        formula.set_width(config.frame_width - 1)

        def get_formula_slice(*indices):
            return VGroup(*[formula[i] for i in indices])

        H_label = formula.get_part_by_tex("{H}")
        E_label = formula.get_part_by_tex("{E}")

        hyp_label = Text("Hypothesis")
        hyp_label.set_color(HYPOTHESIS_COLOR)
        hyp_label.next_to(H_label, UP, buff=LARGE_BUFF)

        evid_label = Text("Evidence")
        evid_label.set_color(EVIDENCE_COLOR1)
        evid_label.next_to(E_label, DOWN, buff=LARGE_BUFF)

        hyp_arrow = Arrow(hyp_label.get_bottom(), H_label.get_top(), buff=SMALL_BUFF)
        evid_arrow = Arrow(evid_label.get_top(), E_label.get_bottom(), buff=SMALL_BUFF)

        self.add(formula[:6])
        # self.add(get_submobject_index_labels(formula))
        # return
        self.play(
            FadeIn(hyp_label, shift=DOWN),
            GrowArrow(hyp_arrow),
            FadeIn(evid_label, shift=UP),
            GrowArrow(evid_arrow),
        )
        self.wait()

        # Prior
        self.play(
            Create(formula.get_part_by_tex("=")),
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
            Swap(lhs_copy[2], lhs_copy[4]),
            run_time=run_time,
        )
        self.play(
            lhs_copy.animate.move_to(likelihood),
            run_time=run_time,
        )

        # Evidence
        self.play(
            Create(formula.get_part_by_tex("\\over")),
            TransformFromCopy(
                get_formula_slice(0, 1, 4, 5),
                get_formula_slice(19, 20, 21, 22),
            ),
        )
        self.wait()

        self.clear()
        self.play(
            formula.animate.restore(),
            formula.animate.scale(1.5),
            formula.animate.to_edge(UP),
            FadeOut(VGroup(
                hyp_arrow, hyp_label,
                evid_arrow, evid_label,
            ))
        )
