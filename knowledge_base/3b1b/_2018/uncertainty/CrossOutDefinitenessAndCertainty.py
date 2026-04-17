# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 老師在課堂上劃掉「明確性」和「確定性」兩個詞，學生們露出困惑表情。



from manim import *
class CrossOutDefinitenessAndCertainty(TeacherStudentsScene):
    def construct(self):
        words = VGroup(
            Text("Definiteness"),
            Text("Certainty"),
        )
        words.arrange(DOWN)
        words.next_to(self.teacher, UP+LEFT)
        crosses = VGroup(*[Cross(word) for word in words])

        self.add(words)
        self.play(
            self.teacher.animate.change("sassy"),
            Create(crosses[0])
        )
        self.play(
            self.change_students(*3*["erm"]),
            Create(crosses[1])
        )
        self.wait(2)
