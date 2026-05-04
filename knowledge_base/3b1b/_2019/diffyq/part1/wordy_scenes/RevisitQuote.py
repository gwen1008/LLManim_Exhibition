# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示一段引言中的語言部分被替換為新文字，同時 Pi 角色從出現到淡出的過程。



from manim import *
class RevisitQuote(Scene):  # 注意：PiCreatureScene 在 ManimCE 中需另外實現或替換
    def construct(self):
        # 假設 quote 是已定義的 VGroup，包含 law_part 和 language_part
        quote = self.get_quote()  # 需自行實現 get_quote 方法
        quote.law_part.set_color(YELLOW)
        quote.language_part.set_color(BLUE)
        quote.set_stroke(BLACK, 6, background=True)
        quote.scale(0.8, about_edge=UL)

        new_language_part = Text(
            "Language of differential equations",
            font_size=36
        )
        new_language_part.to_edge(UP)
        new_language_part.match_style(quote.language_part)

        # 假設 randy 是 PiCreature 物件，需自行實現或替換為其他角色
        randy = self.pi_creature

        self.play(
            FadeIn(quote[:-1], shift=DOWN),
            FadeIn(quote[-1:], shift=LEFT),
            randy.animate.change("raise_right_hand"),  # 假設 change 方法存在
        )
        self.play(Blink(randy))  # 假設 Blink 動畫已定義
        self.play(randy.animate.change("angry"))
        self.play(
            Blink(randy),
            FadeOut(randy, run_time=3)  # 用 FadeOut 替代 VFadeOut
        )
        mover = VGroup(quote.language_part)
        self.add(quote, mover)
        self.play(
            ReplacementTransform(
                mover, new_language_part,
            ),
            *[
                FadeOut(part)
                for part in quote
                if part is not quote.language_part
            ],
            run_time=2,
        )
        self.wait()
