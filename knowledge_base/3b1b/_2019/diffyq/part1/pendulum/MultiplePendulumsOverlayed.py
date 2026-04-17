# Source: 3b1b/_2019/diffyq/part1/pendulum.py
# Description: [3b1b translated] 展示五個不同初始角度的鐘擺同時擺動，並在左上角繪製它們的角度隨時間變化的圖形，右下角有一個角色注視著鐘擺。



from manim import *
class MultiplePendulumsOverlayed(Scene):
    def __init__(
        self,
        initial_thetas=[
            150 * DEGREES,
            90 * DEGREES,
            60 * DEGREES,
            30 * DEGREES,
            10 * DEGREES,
        ],
        weight_colors=[
            PINK, RED, GREEN, BLUE, GREY,
        ],
        pendulum_config={
            "top_point": ORIGIN,
            "length": 3,
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.initial_thetas = initial_thetas
        self.weight_colors = weight_colors
        self.pendulum_config = pendulum_config

    def construct(self):
        # 創建多個鐘擺
        pendulums = VGroup(*[
            Pendulum(
                initial_theta=theta,
                weight_style={
                    "fill_color": wc,
                    "fill_opacity": 0.5,
                },
                **self.pendulum_config,
            )
            for theta, wc in zip(
                self.initial_thetas,
                self.weight_colors,
            )
        ])
        
        # 啟動鐘擺擺動並移除角度標籤
        for pendulum in pendulums:
            pendulum.start_swinging()
            pendulum.remove(pendulum.theta_label)

        # 創建角色並設置更新器
        randy = Randolph(color=BLUE_C)
        randy.to_corner(DL)
        randy.add_updater(lambda r: r.look_at(pendulums[0].weight))

        # 創建坐標軸（需要自定義 ThetaVsTAxes 類）
        axes = ThetaVsTAxes(
            x_max=20,
            y_axis_config={
                "unit_size": 0.5,
                "tip_length": 0.3,
            },
        )
        axes.to_corner(UL)
        
        # 創建實時繪製的圖形
        graphs = VGroup(*[
            axes.get_live_drawn_graph(
                pendulum,
                stroke_color=pendulum.weight.get_color(),
                stroke_width=1,
            )
            for pendulum in pendulums
        ])

        # 添加物件到場景
        self.add(pendulums)
        self.add(axes, *graphs)
        
        # 動畫序列
        self.play(randy.animate.change("sassy"))
        self.wait(2)
        self.play(Blink(randy))
        self.wait(5)
        self.play(randy.animate.change("angry"))
        self.play(Blink(randy))
        self.wait(10)
