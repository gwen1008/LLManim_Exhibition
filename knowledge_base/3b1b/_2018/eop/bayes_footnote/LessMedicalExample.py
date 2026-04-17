# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示將「患病機率」替換為「心靈感應機率」的動畫過程，包含劃除舊文字和顯示新文字。



from manim import *
class LessMedicalExample(Scene):
    def construct(self):
        disease = MathTex("P(\\text{Having a disease})")
        telepathy = MathTex("P(\\text{Telepathy})")
        cross = Cross(disease)

        self.add(disease)
        self.wait()
        self.play(Create(cross))
        self.play(
            FadeIn(telepathy),
            VGroup(disease, cross).animate.shift(2*UP)
        )
        self.wait()
