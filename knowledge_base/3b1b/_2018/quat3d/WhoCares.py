# Source: 3b1b/_2018/quat3d.py
# Description: [3b1b translated] 展示教師與學生場景中，學生提出質疑後，教師展示社群媒體對四元數的討論截圖，並聚焦於 Twitter 回應的動畫過程。



from manim import *
class WhoCares(TeacherStudentsScene):
    def construct(self):
        quotes = Group(*[
            ImageMobject(
                f"CoderQuaternionResponse_{d}",
                height=2
            )
            for d in range(4)
        ])
        logos = Group(*[
            ImageMobject(name, height=0.5)
            for name in [
                "TwitterLogo",
                "HackerNewsLogo",
                "RedditLogo",
                "YouTubeLogo",
            ]
        ])
        for quote, logo in zip(quotes, logos):
            logo.move_to(quote.get_corner(UR))
            quote.add(logo)

        quotes.arrange_in_grid()
        quotes.set_height(4)
        quotes.to_corner(UL)

        self.student_says(
            "Um...who cares?",
            target_mode="sassy",
            added_anims=[self.teacher.change, "guilty"]
        )
        self.play_student_changes("angry", "sassy", "sad")
        self.wait(2)
        self.play(
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand"
        )
        # 註解部分已移除，因原代碼已註解掉
        # 僅保留未註解的 Twitter 部分

        # Show Twitter
        t_quote = quotes[0]
        # 原註解代碼已移除
        t_quote.set_opacity(0)  # 使用 set_opacity 替代 fade(1)
        t_quote.to_corner(UL)
        self.play(
            self.change_students(*3 * ["pondering"], look_at=quotes),
            t_quote.animate.set_opacity(1).scale(2).to_corner(UL),
        )
        self.wait(2)
        self.play_student_changes(
            "pondering", "happy", "tease",
            look_at=t_quote
        )
        self.wait(2)
        self.play(FadeOut(t_quote))
        self.wait(5)
