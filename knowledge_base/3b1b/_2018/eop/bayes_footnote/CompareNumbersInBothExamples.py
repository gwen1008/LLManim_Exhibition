# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示疾病與心靈感應兩個貝葉斯範例的機率公式對比，包含標題、分隔線和著色的數學公式。



from manim import *
class CompareNumbersInBothExamples(Scene):
    def construct(self):
        v_line = Line(UP, DOWN).scale(FRAME_HEIGHT / 2)
        v_line.shift(MED_LARGE_BUFF * LEFT)
        h_line = Line(LEFT, RIGHT).scale(FRAME_WIDTH / 2)
        h_line.to_edge(UP, buff=1.25 * LARGE_BUFF)
        
        titles = VGroup()
        for word, vect in ("Disease", LEFT), ("Telepathy", RIGHT):
            title = Text("%s example" % word, font_size=36)
            title.shift(vect * FRAME_WIDTH / 4.0)
            title.to_edge(UP)
            titles.add(title)
        
        priors = VGroup(*[
            MathTex(
                "P(", "\\text{%s}" % s, ")", "= 1/1{,}000}"
            )
            for s in ("Sick", "Powers")
        ])
        
        likelihoods = VGroup(*[
            MathTex(
                "P(", "\\text{%s}" % s1, "|", 
                "\\text{Not }", "\\text{%s}" % s2, ")",
                "=", "1/100"
            )
            for s1, s2 in [("+", "Sick"), ("Correct", "Powers")]
        ])
        
        priors.next_to(likelihoods, UP, LARGE_BUFF)
        
        for group in priors, likelihoods:
            for mob, vect in zip(group, [LEFT, RIGHT]):
                # 使用 set_color_by_tex 的替代方法
                if "Sick" in mob.get_tex_string():
                    mob.set_color_by_tex("Sick", BLUE)
                if "Powers" in mob.get_tex_string():
                    mob.set_color_by_tex("Powers", BLUE)
                if "+" in mob.get_tex_string():
                    mob.set_color_by_tex("+", GREEN)
                if "Correct" in mob.get_tex_string():
                    mob.set_color_by_tex("Correct", GREEN)
                mob.scale(0.8)
                mob.shift(vect * FRAME_WIDTH / 4)

        self.play(
            LaggedStartMap(FadeIn, titles, lag_ratio=0.7),
            Create(h_line),
            Create(v_line)
        )
        self.wait()
        self.play(FadeIn(priors))
        self.wait()
        self.play(FadeIn(likelihoods))
        self.wait(3)
