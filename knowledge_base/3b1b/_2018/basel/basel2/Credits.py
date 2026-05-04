# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示製作人員名單以淡入動畫逐行出現，最後將 Patreon 標誌繪製並置於頂部。



from manim import *
class Credits(Scene):
    def construct(self):
        credits = VGroup(*[
            VGroup(*list(map(Text, pair)))
            for pair in [
                ("Primary writer and animator:", "Ben Hambrecht"),
                ("Editing, advising, narrating:", "Grant Sanderson"),
                ("Based on a paper originally by:", "Johan Wästlund"),
            ]
        ])
        for credit, color in zip(credits, [MAROON_D, BLUE_D, WHITE]):
            credit[1].set_color(color)
            credit.arrange(DOWN, buff=SMALL_BUFF)

        credits.arrange(DOWN, buff=LARGE_BUFF)
        credits.center()

        patreon_logo = PatreonLogo()
        patreon_logo.to_edge(UP)

        for credit in credits:
            self.play(LaggedStartMap(FadeIn, credit[0]))
            self.play(FadeIn(credit[1]))
        self.wait()
        self.play(
            credits.animate.next_to(patreon_logo.get_bottom(), DOWN, buff=MED_LARGE_BUFF),
            DrawBorderThenFill(patreon_logo)
        )
        self.wait()
