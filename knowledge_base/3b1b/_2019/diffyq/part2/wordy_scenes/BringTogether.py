# Source: 3b1b/_2019/diffyq/part2/wordy_scenes.py
# Description: [3b1b translated] 展示兩個箭頭從兩側向中間靠攏，同時文字從模糊分散狀態恢復到正常位置的動畫。



from manim import *
class BringTogether(Scene):
    def construct(self):
        arrows = VGroup(Vector(2 * RIGHT), Vector(2 * LEFT))
        arrows.arrange(RIGHT, buff=2)
        words = Text("Bring together")
        words.next_to(arrows, DOWN)
        words.save_state()
        # 在 ManimCE 中沒有 space_out_submobjects，用 stretch 模擬類似效果
        words.stretch(1.2, dim=0)  # 水平拉伸模擬分散效果

        self.play(
            FadeIn(words, shift=UP * 0.5),  # VFadeIn 用 FadeIn 替代
            Restore(words),
            arrows.animate.arrange(RIGHT, buff=SMALL_BUFF),  # 改為 .animate 語法
            FadeIn(arrows, shift=DOWN * 0.5),  # VFadeIn 用 FadeIn 替代
        )
        self.play(FadeOut(words), FadeOut(arrows))
