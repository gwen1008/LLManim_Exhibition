# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 展示微積分主題與其他相關數學分支的關聯圖，通過線條連接和文字動畫呈現。



from manim import *
class MoreTopics(Scene):
    def construct(self):
        calculus = Text("Calculus", color=YELLOW)
        calculus.to_edge(LEFT)
        calculus.add_background_rectangle()
        
        others = VGroup(
            Text("Multivariable calculus"),
            Text("Complex analysis"),
            Text("Differential geometry"),
            MathTex("\\vdots")
        )
        for word in others:
            word.add_background_rectangle()
        others.arrange(
            DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT,
        )
        others.to_edge(RIGHT)
        
        lines = VGroup(*[
            Line(calculus.get_right(), word.get_left(), buff=MED_SMALL_BUFF)
            for word in others
        ])

        rect = FullScreenFadeRectangle(fill_opacity=0.7)
        self.add(rect)

        self.add(calculus)
        self.play(
            LaggedStartMap(Create, lines),
            LaggedStartMap(Write, others),
        )
        self.wait()

        self.calculus = calculus
        self.lines = lines
        self.full_screen_rect = rect
        self.other_topics = others
