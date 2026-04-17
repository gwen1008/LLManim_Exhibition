# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個謎題陳述場景，包含 AoPS 標誌、網址和問題文字，文字以漸入方式逐行顯示。



from manim import *
class PuzzleStatement(Scene):
    def construct(self):
        aops_logo = AoPSLogo()
        url = Text("AoPS.com/3b1b")
        url.next_to(aops_logo, UP)
        group = VGroup(aops_logo, url)
        group.to_edge(UP)
        self.add(group)

        words = Text("""
            AoPS must choose one of 20 people to send to a 
            tug-of-war tournament.  We don't care who we send, 
            as long as we don't send our weakest person. \\ \\ 

            Each person has a different strength, but we don't know 
            those strengths.  We get 10 intramural 10-on-10 matches 
            to determine who we send.  Can we make sure we don't send
             the weakest person?
        """, alignment="")
        words.set_width(config.frame_width - 2)
        words.next_to(group, DOWN, buff=LARGE_BUFF)
        self.play(LaggedStart(*[FadeIn(word) for word in words], run_time=5, lag_ratio=0.2))
        self.wait(2)
