# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示一個 PiCreature 動畫場景，其中包含 Udacity 贊助商標誌、URL 文字和螢幕矩形，PiCreature 做出各種手勢和表情變化。



from manim import *
class SponsorUnderlay(PiCreatureScene):
    def __init__(self, default_pi_creature_start_corner=DR, **kwargs):
        super().__init__(default_pi_creature_start_corner=default_pi_creature_start_corner, **kwargs)

    def construct(self):
        url = Text("https://udacity.com/3b1b/")
        url.to_corner(UL)

        rect = ScreenRectangle(height=5.5)
        rect.next_to(url, DOWN)
        rect.to_edge(LEFT)
        url.next_to(rect, UP)
        url.save_state()

        url.next_to(self.pi_creature.get_corner(UL), UP)

        logo = SVGMobject(file_name="udacity")
        logo.set_fill("#02b3e4")
        logo.to_corner(UR)

        self.add(logo)

        self.play(
            Write(url),
            self.pi_creature.change, "raise_right_hand"
        )
        self.play(
            url.restore,
            Create(rect),
            path_arc=90 * DEGREES,
        )
        self.wait(2)
        self.change_mode("thinking")
        self.wait()
        self.pi_creature.look_at(url)
        self.wait(10)
        self.change_mode("happy")
        self.wait(10)
        self.change_mode("raise_right_hand")
        self.wait(10)

        self.remove(rect)
        self.play(url.animate.next_to(self.pi_creature, UL))
        url_rect = SurroundingRectangle(url)
        self.play(Create(url_rect))
        self.play(FadeOut(url_rect))
        self.wait(3)
