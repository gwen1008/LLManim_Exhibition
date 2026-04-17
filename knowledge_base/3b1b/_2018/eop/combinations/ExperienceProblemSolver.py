# Source: 3b1b/_2018/eop/combinations.py
# Description: [3b1b translated] 展示兩個角色討論數學公式，其中一個角色快速給出答案，另一個角色感到困惑，最後角色思考帕斯卡三角形圖案。



from manim import *
class ExperienceProblemSolver(PiCreatureScene):
    def construct(self):
        self.add_equation()
        self.jenny_solves()
        self.no_genius()
        self.think_about_patterns()

    def add_equation(self):
        equation = MathTex(
            "\\frac{x^3 + y^3}{(x+y)^2} + \\frac{3xy}{x+y}"
        )
        equation.to_edge(UP)

        self.play(Write(equation))
        self.wait()

        self.equation = equation

    def jenny_solves(self):
        randy, jenny = self.randy, self.jenny
        jenny_words = TexText("It's just $x+y$")
        randy_words = TexText("...wait...")
        randy_words.next_to(randy.get_corner(UP+RIGHT), RIGHT)

        self.pi_creature_says(
            jenny, jenny_words, 
            target_mode = "hooray",
            bubble_config = {"height" : 2, "width" : 3}
        )
        self.wait()
        self.play(
            randy.animate.change("confused", self.equation),
            Write(randy_words)
        )
        self.play(randy.animate.look_at(self.equation.get_left()))
        self.play(randy.animate.look_at(jenny.eyes))
        self.play(jenny.animate.change("happy"))
        self.play(randy.animate.change("tired"))
        self.wait()
        self.play(*[FadeOut(mob) for mob in [
            jenny.bubble, jenny_words, randy_words
        ]])

    def no_genius(self):
        randy, jenny = self.randy, self.jenny

        lightbulb = Lightbulb()
        lightbulb.next_to(jenny, UP)
        cross = Cross(lightbulb)
        cross.set_stroke(RED, 8)

        self.play(LaggedStartMap(Create, lightbulb))
        self.play(
            Create(cross),
            jenny.animate.change("sassy", cross),
            randy.animate.change("happy")
        )
        self.wait(2)

        self.to_fade = VGroup(lightbulb, cross)

    def think_about_patterns(self):
        randy, jenny = self.randy, self.jenny
        
        # 創建帕斯卡三角形
        rows = VGroup()
        for n in range(6):
            row = VGroup()
            for k in range(n+1):
                # 計算組合數 C(n, k)
                from math import comb
                value = comb(n, k)
                num = Text(str(value), font_size=24)
                row.add(num)
            row.arrange(RIGHT, buff=0.6*0.8)
            rows.add(row)
        
        # 排列行
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3*0.8)
        rows.scale(0.8)
        
        # 根據數值設置顏色
        for row in rows:
            for num in row:
                n = float(num.tex_string)
                color = interpolate_color(BLUE, YELLOW, n/10.0)
                num.set_color(color)

        self.pi_creature_thinks(
            jenny, "",
            bubble_config = {"width" : 5, "height" : 4.2},
            added_anims = [
                FadeOut(self.to_fade),
                FadeOut(self.equation),
                randy.animate.change("plain")
            ]
        )
        
        # 計算氣泡中心位置
        bubble_center = jenny.bubble.get_bubble_center()
        rows.move_to(
            bubble_center + MED_SMALL_BUFF*(UP+LEFT)
        )
        
        self.play(FadeIn(rows[0]))
        for i in range(len(rows)-1):
            last_row = rows[i]
            curr_row = rows[i+1]
            
            # 創建兩個變換動畫
            anims = []
            
            # 從上一行複製到當前行的右側部分
            if len(last_row) > 0:
                copy1 = last_row.copy()
                target1 = VGroup(*curr_row[1:]) if len(curr_row) > 1 else VGroup()
                anims.append(Transform(copy1, target1, remover=True))
            
            # 從上一行複製到當前行的左側部分
            if len(last_row) > 0:
                copy2 = last_row.copy()
                target2 = VGroup(*curr_row[:-1]) if len(curr_row) > 0 else VGroup()
                anims.append(Transform(copy2, target2, remover=True))
            
            if anims:
                self.play(*anims)
            self.add(curr_row)
        
        self.wait(3)

    def create_pi_creatures(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        randy.shift(4*LEFT)
        
        # 使用PiCreature類創建Jenny
        jenny = PiCreature(color=BLUE_C)
        jenny.flip()
        jenny.to_edge(DOWN)
        jenny.shift(4*RIGHT)
        
        self.randy, self.jenny = randy, jenny
        return VGroup(randy, jenny)
