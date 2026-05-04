# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個圓形湖泊周圍有16個光源，上方顯示一個無窮級數公式和問號的縮圖場景。



from manim import *
class ThumbnailScene(Scene):
    def construct(self):
        # 使用 MathTex 替代 OldTex
        equation = MathTex("1+{1\\over 4}+{1\\over 9}+{1\\over 16}+{1\\over 25}+\\dots")
        equation.scale(1.5)
        equation.move_to(1.5 * UP)
        
        # 使用 MathTex 替代 OldTex，並用 set_color 替代 color 參數
        q_mark = MathTex("=?").scale(5)
        q_mark.set_color(LIGHT_COLOR)
        q_mark.next_to(equation, DOWN, buff=1.5)

        lake_radius = 6
        lake_center = ORIGIN
        op_scale = 0.4

        # 創建湖泊圓形
        lake = Circle(
            radius=lake_radius,
            stroke_color=LAKE_STROKE_COLOR,
            stroke_width=LAKE_STROKE_WIDTH,
            fill_color=LAKE_COLOR,
            fill_opacity=LAKE_OPACITY
        )
        lake.move_to(lake_center)

        # 添加光源（由於 ManimCE 沒有 LightSource，用 Dot 替代）
        for i in range(16):
            theta = -TAU/4 + (i + 0.5) * TAU/16
            pos = lake_center + lake_radius * np.array([np.cos(theta), np.sin(theta), 0])
            # 創建簡單的光源表示
            light = Dot(
                point=pos,
                color=YELLOW,
                radius=0.3,
                fill_opacity=0.8
            )
            lake.add(light)

        self.add(lake)
        self.add(equation, q_mark)
        self.wait()
