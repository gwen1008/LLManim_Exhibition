# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 比較物理學中的微分方程與愛情方程，並用箭頭連接兩者，突出顯示關鍵符號。



from manim import *
class ComparePhysicsToLove(Scene):
    def construct(self):
        ode = get_ode()
        ode.to_edge(UP)
        thetas = ode.get_parts_by_tex("theta")

        love = VGroup(
            get_love_equation1(),
            get_love_equation2(),
        )
        love.scale(0.5)
        love.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        love.move_to(DOWN)
        hearts = VGroup(*filter(
            lambda sm: isinstance(sm, SuitSymbol),
            love.get_family()
        ))

        arrow = DoubleArrow(love.get_top(), ode.get_bottom())

        self.play(FadeIn(ode, shift=DOWN))
        self.play(FadeIn(love, shift=UP))
        self.wait()
        self.play(LaggedStartMap(
            CreateThenFadeAround,
            thetas,
        ))
        self.play(LaggedStartMap(
            CreateThenFadeAround,
            hearts,
        ))
        self.wait()
        self.play(Create(arrow))
        self.wait()
