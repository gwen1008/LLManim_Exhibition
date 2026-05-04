# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示一個藍色 PiCreature 變成生病綠色，然後恢復原狀，最後顯示「1 in 1,000」標題和由許多 PiCreature 組成的網格，其中只有一個是生病的。



from manim import *
class OneInOneThousandHaveDisease(Scene):
    def construct(self):
        title = Tex("1 in 1{,}000")  # OldTexText -> Tex
        title.to_edge(UP)
        creature = PiCreature()
        all_creatures = VGroup(*[
            VGroup(*[
                creature.copy()
                for y in range(25)
            ]).arrange(DOWN, buff=SMALL_BUFF)
            for x in range(40)
        ]).arrange(RIGHT, buff=SMALL_BUFF)
        all_creatures.set_width(config.frame_width - 4)  # FRAME_WIDTH -> config.frame_width
        all_creatures.next_to(title, DOWN)
        randy = all_creatures[0][0]
        all_creatures[0].remove(randy)
        randy.change_mode("sick")
        randy.set_color(SICKLY_GREEN)
        randy.save_state()
        randy.set_height(3)
        randy.center()
        randy.change_mode("plain")
        randy.set_color(BLUE)

        self.add(randy)
        self.play(
            randy.animate.change_mode("sick"),  # 使用 .animate 語法
            randy.animate.set_color(SICKLY_GREEN)
        )
        self.play(Blink(randy))
        self.play(randy.animate.restore())  # 使用 .animate 語法
        self.play(
            Write(title),
            LaggedStartMap(FadeIn, all_creatures, run_time=3)
        )
        self.wait()
