# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示兩個角色（Randolph 和數學家）之間的對話動畫，其中一個角色指向屏幕上的內容，另一個角色則回應數學相關的評論。



from manim import *
class LocalMathematician(PiCreatureScene):
    def construct(self):
        randy, mathy = self.pi_creatures
        screen = ScreenRectangle(height=2)
        screen.to_corner(UL)
        screen.set_opacity(0)  # 原 fade(1) 表示完全透明

        mathy_name = Text("Local\nmathematician", font_size=24)
        mathy_name.next_to(mathy, LEFT, buff=LARGE_BUFF)
        arrow = Arrow(mathy_name.get_right(), mathy.get_left())

        self.play(
            Animation(screen),
            mathy.animate.change("pondering"),
            PiCreatureSays(
                randy, "Check these\nout!",
                target_mode="surprised",
                bubble_config={"height": 3, "width": 4},
                look_at_arg=screen,
            ),
        )
        self.play(
            Animation(screen),
            RemovePiCreatureBubble(
                randy,
                target_mode="raise_right_hand",
                look_at_arg=screen,
            )
        )
        self.wait(2)
        self.play(
            PiCreatureSays(
                mathy, "Ah yes, consider\n$x^n - 1$ over $\\mathds{C}$...",
                look_at_arg=randy.eyes
            ),
            randy.animate.change("happy", mathy.eyes)
        )
        self.wait(3)

    def create_pi_creatures(self):
        randy = Randolph().flip()
        mathy = Mathematician()
        randy.scale(0.9)
        randy.to_edge(DOWN).shift(4 * RIGHT)
        mathy.to_edge(DOWN).shift(4 * LEFT)
        return randy, mathy
