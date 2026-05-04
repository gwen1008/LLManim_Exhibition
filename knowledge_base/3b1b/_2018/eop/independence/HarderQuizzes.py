# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示兩組困難的數學問題並在每個的第一個問題上打叉。



from manim import *
class HarderQuizzes(Scene):
    def construct(self):
        quizzes = VGroup(
            get_quiz(
                "Find all primes $p$ \\\\ where $p+2$ is prime.",
                "Find all primes $p$ \\\\ where $2^{p}-1$ is prime.",
                "Solve $\\zeta(s) = 0$",
            ),
            get_quiz(
                "Find $S$ such that \\\\ $\\#\\mathds{N} < \\#S < \\#\\mathcal{P}(\\mathds{N})$",
                "Describe ``forcing''",
                "Prove from ZFC that $S \\notin S$.",
            ),
        )
        quizzes.arrange(RIGHT)
        quizzes.to_edge(DOWN)
        crosses = VGroup(*[
            Cross(quiz.questions[0])
            for quiz in quizzes
        ])

        for quiz in quizzes:
            self.play(FadeIn(quiz))
        self.wait()
        for cross in crosses:
            self.play(Create(cross))
        self.wait()
