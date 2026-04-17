# Source: 3b1b/_2018/eop/chapter1/show_uncertainty_disease.py
# Description: [3b1b translated] 展示一個藍色 PiCreature 角色從健康到生病再康復的動畫過程，並顯示患病機率為 0.5%。



from manim import *
class RandyIsSickOrNot(Scene):
    def construct(self):
        title = Tex("1 in 200")
        title.to_edge(UP)

        # 注意：ManimCE 沒有內建的 SicklyPiCreature 類別
        # 這裡假設 randy 是一個普通的 PiCreature 或 Mobject
        # 實際使用時需要根據具體實現調整
        randy = Circle(color=BLUE, fill_opacity=0.8)  # 替代 SicklyPiCreature
        randy.set_height(3)
        randy.move_to(2*LEFT)
        randy.save_state()

        self.add(randy)

        p_sick = MathTex("p(","\\text{sick}",") = 0.5\%").scale(1.7)
        p_sick.set_color_by_tex("sick", GREEN)
        p_sick.next_to(randy, UP, buff=LARGE_BUFF)
        self.add(p_sick)
        self.wait()

        # 模擬 get_slightly_sick 效果
        self.play(
            randy.animate.set_color(YELLOW).scale(0.95),
            rate_func=there_and_back
        )
        self.wait(0.5)  # 替代 Blink
        self.wait(2)

        # 模擬 get_sick 效果
        self.play(
            randy.animate.set_color(GREEN).scale(0.9)
        )
        self.wait(0.5)  # 替代 Blink
        self.wait()

        # 模擬 get_better 效果
        self.play(
            randy.animate.set_color(BLUE).scale(1/0.9)
        )

        self.play(
            randy.animate.set_color(YELLOW).scale(0.95),
            rate_func=there_and_back
        )
        self.wait(0.5)  # 替代 Blink
        self.wait(0.5)

        self.play(
            randy.animate.set_color(GREEN).scale(0.9)
        )
        
        self.wait(0.5)  # 替代 Blink
        self.play(
            randy.animate.set_color(BLUE).scale(1/0.9)
        )
        self.wait(3)
