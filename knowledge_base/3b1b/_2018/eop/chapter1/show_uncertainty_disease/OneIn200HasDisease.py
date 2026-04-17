# Source: 3b1b/_2018/eop/chapter1/show_uncertainty_disease.py
# Description: [3b1b translated] 展示一個藍色 PiCreature 變成生病狀態，然後恢復原狀，最後顯示「1 in 200」標題和 200 個 PiCreature 的網格，其中一個是生病的。



from manim import *
class OneIn200HasDisease(Scene):
    def construct(self):
        title = Text("1 in 200")
        title.to_edge(UP)
        creature = PiCreature()

        all_creatures = VGroup(*[
            VGroup(*[
                creature.copy()
                for y in range(20)
            ]).arrange(DOWN, SMALL_BUFF)
            for x in range(10)
        ]).arrange(RIGHT, SMALL_BUFF)
        all_creatures.set_height(config.frame_height * 0.8)
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

        #p_sick = MathTex("p(","\\text{sick}",") = 0.5\%")
        #p_sick.set_color_by_tex("sick", SICKLY_GREEN)
        #p_sick.next_to(randy, RIGHT+UP)
        #self.add(p_sick)
        self.wait()
        
        self.play(
            randy.animate.change_mode("sick"),
            randy.animate.set_color(SICKLY_GREEN)
        )
        self.play(Blink(randy))
        self.play(randy.animate.restore())
        self.wait()
        self.play(
            Write(title),
            LaggedStartMap(FadeIn, all_creatures, run_time = 3)
        )
        self.wait()
