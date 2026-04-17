# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示常微分方程（ODE）與偏微分方程（PDE）的對比，分別在兩個動態邊框的矩形框中呈現，並用箭頭標示其輸入變量。



from manim import *
class ODEvsPDEinFrames(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = GREY_E

    def construct(self):
        frames = VGroup(*[
            ScreenRectangle(
                height=3.5,
                fill_opacity=1,
                fill_color=BLACK,
                stroke_width=0,
            )
            for x in range(2)
        ])
        frames.arrange(RIGHT, buff=LARGE_BUFF)
        frames.shift(0.5 * DOWN)

        # 在 ManimCE 中，AnimatedBoundary 已不存在，使用 SurroundingRectangle 配合動畫模擬
        # 我們將在播放動畫時創建邊框並更新其顏色
        animated_frames = VGroup()
        for frame in frames:
            # 創建一個初始的邊框，稍後用動畫更新
            rect = SurroundingRectangle(frame, color=WHITE, stroke_width=1)
            animated_frames.add(rect)

        titles = VGroup(
            # MathTex("ODEs"),
            # MathTex("PDEs"),
            Text("Ordinary", "Differential", "Equations"),
            Text("Partial", "Differential", "Equations"),
        )
        for title, frame in zip(titles, frames):
            title.arrange(
                DOWN,
                buff=MED_SMALL_BUFF,
                aligned_edge=LEFT
            )
            title.next_to(frame, UP, MED_LARGE_BUFF)
            title.initials = VGroup(*[
                part[0] for part in title
            ])
        titles[0][1].shift(0.05 * UP)

        # ODE content
        ode = self.get_ode()  # 假設 get_ode() 是自定義函數，返回一個 MathTex 物件
        ode.set_width(frames[0].get_width() - MED_LARGE_BUFF)
        ode.next_to(frames[0].get_top(), DOWN)
        ts = ode.get_parts_by_tex("{t}")
        one_input = Text("One input")
        one_input.next_to(frames[0].get_bottom(), UP)
        o_arrows = VGroup(*[
            Arrow(
                one_input.get_top(),
                t.get_bottom(),
                buff=0.2,
                color=WHITE,
                max_tip_length_to_length_ratio=0.075,
                path_arc=pa
            )
            for t, pa in zip(ts, [-0.7, 0, 0.7])
        ])
        o_arrows.set_stroke(width=3)
        frames[0].add(ode, one_input, o_arrows)

        # PDE content
        pde = MathTex(
            r"""
            \frac{\partial T}{\partial t}
            {(x, y, t)} =
            \frac{\partial^2 T}{\partial x^2}
            {(x, y, t)} +
            \frac{\partial^2 T}{\partial y^2}
            {(x, y, t)}
            """,
            tex_to_color_map={"{(x, y, t)}": WHITE}
        )
        pde.set_width(frames[1].get_width() - MED_LARGE_BUFF)
        pde.next_to(frames[1].get_top(), DOWN)
        inputs = pde.get_parts_by_tex("{(x, y, t)}")
        multi_input = Text("Multiple inputs")
        multi_input.next_to(frames[1].get_bottom(), UP)
        p_arrows = VGroup(*[
            Arrow(
                multi_input.get_top(),
                mob.get_bottom(),
                buff=0.2,
                color=WHITE,
                max_tip_length_to_length_ratio=0.075,
                path_arc=pa
            )
            for mob, pa in zip(inputs, [-0.7, 0, 0.7])
        ])
        p_arrows.set_stroke(width=3)
        frames[1].add(pde, multi_input, p_arrows)

        self.add(
            frames[0],
            animated_frames[0],
            titles[0]
        )
        self.play(
            Write(one_input),
            Create(o_arrows, lag_ratio=0.5)
        )
        self.wait(2)
        self.play(titles[0].initials.animate.set_color(BLUE))
        self.wait(7)

        # Transition
        self.play(
            TransformFromCopy(titles[0], titles[1]),
            TransformFromCopy(frames[0], frames[1]),
        )
        # 模擬 AnimatedBoundary 效果：讓邊框顏色循環變化
        # 由於 AnimatedBoundary 不存在，我們用一個簡單的顏色循環動畫代替
        self.play(
            animated_frames[1].animate.set_color(BLUE).set_stroke_width(3),
            run_time=0.5
        )
        self.play(
            animated_frames[1].animate.set_color(WHITE).set_stroke_width(1),
            run_time=0.5
        )
        self.wait()
        self.play(titles[1].initials.animate.set_color(YELLOW))
        self.wait(30)

    # 假設的 get_ode 函數，因為原始代碼未提供，這裡創建一個簡單的 ODE 公式
    def get_ode(self):
        return MathTex(
            r"\frac{d^2 x}{dt^2} + \gamma \frac{dx}{dt} + \omega_0^2 x = 0",
            tex_to_color_map={"{t}": WHITE}
        )
