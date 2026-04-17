# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示兩個並排的黑色矩形框，上方分別對應物理微分方程和愛情方程，邊框有動態效果。



from manim import *
class FramesComparingPhysicsToLove(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        ode = get_ode()
        ode.to_edge(UP)

        love = VGroup(
            get_love_equation1(),
            get_love_equation2(),
        )
        love.scale(0.5)
        love.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        frames = VGroup(*[
            ScreenRectangle(
                height=3.5,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            )
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)
        frames.shift(DOWN)

        animated_frames = AnimatedBoundary(frames)

        ode.next_to(frames[0], UP)
        love.next_to(frames[1], UP)

        self.add(frames, animated_frames)
        self.add(ode, love)

        self.wait(15)
