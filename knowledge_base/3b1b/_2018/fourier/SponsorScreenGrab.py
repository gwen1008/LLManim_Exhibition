# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個 PiCreature 指向一個螢幕矩形，螢幕上方顯示網址，PiCreature 的表情隨時間變化。



from manim import *
class SponsorScreenGrab(PiCreatureScene):
    def construct(self):
        morty = self.pi_creature
        screen = ScreenRectangle(height=5)
        screen.to_corner(UP + LEFT)
        screen.shift(MED_LARGE_BUFF * DOWN)
        url = Text("janestreet.com/3b1b")
        url.next_to(screen, UP)

        self.play(
            morty.animate.change("raise_right_hand"),
            Create(screen)
        )
        self.play(Write(url))
        self.wait(2)
        for mode in ["happy", "thinking", "pondering", "thinking"]:
            self.play(morty.animate.change(mode, screen))
            self.wait(4)
