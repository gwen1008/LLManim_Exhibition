# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 將兩個關於相流收斂、發散和循環的問題以淡入動畫顯示在右上角。



from manim import *
class PhaseFlowQuestions(Scene):
    def construct(self):
        questions = VGroup(
            Text(
                "Which points does the flow\n" +
                "converge to?  Diverge away from?",
            ),
            Text("Where are there cycles?"),
        )
        questions.arrange(DOWN, buff=LARGE_BUFF)
        questions.to_corner(UR)
        for question in questions:
            self.play(FadeIn(question, shift=DOWN))
            self.wait(2)
