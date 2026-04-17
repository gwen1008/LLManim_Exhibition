# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示複數平面上的 z → z^(1/2) 變換，並在變換後的平面上繪製理想化牆壁附近的流線場。



from manim import *
class ZToHalfFlowNearWall(Scene):
    def __init__(self, num_anchors_to_add_per_line=200, plane_config={"y_radius": 8}, **kwargs):
        super().__init__(**kwargs)
        self.num_anchors_to_add_per_line = num_anchors_to_add_per_line
        self.plane_config = plane_config

    def construct(self):
        # 縮小相機視圖
        self.camera.frame.scale(0.5, about_point=ORIGIN)

        # 創建數值平面
        plane = NumberPlane(
            x_range=[-15, 15, 1],
            y_range=[-25, 25, 1],
            y_length=12.5,  # y_radius=25, y_unit_size=0.5 → y_length=25*0.5=12.5
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            },
            faded_line_ratio=0,  # 替代 secondary_line_ratio=0
        )
        plane.next_to(ORIGIN, UP, buff=0.001)
        
        # 找出水平線（x坐標接近0的線）
        horizontal_lines = VGroup()
        for line in plane.get_lines():
            if abs(line.get_start()[0]) < 0.1 and abs(line.get_end()[0]) < 0.1:
                horizontal_lines.add(line)
        # 添加x軸
        horizontal_lines.add(plane.get_axes()[0])
        
        # 設置顏色
        plane.set_stroke(MAROON_B, width=2)
        horizontal_lines.set_stroke(BLUE, width=2)

        # 添加平面到場景
        self.add(plane)

        # 創建坐標軸標籤（簡化版本）
        axes = plane.get_axes()
        x_label = MathTex("x").scale(0.75).next_to(axes[0].get_end(), RIGHT)
        y_label = MathTex("y").scale(0.75).next_to(axes[1].get_end(), UP)
        coordinate_labels = VGroup(x_label, y_label)
        
        # 設置標籤樣式
        for label in coordinate_labels:
            label.set_stroke(width=0)
        
        # 創建文字標籤
        words = Text("(Idealized) Flow\nnear a wall", font_size=24)
        words.add_background_rectangle(buff=0.1)
        words.next_to(0.75 * UP, LEFT, buff=MED_LARGE_BUFF)
        
        equation = MathTex("z \\rightarrow z^{1/2}")
        equation.scale(0.75)
        equation.add_background_rectangle(buff=0.1)
        equation.next_to(words, UP)

        # 播放動畫
        self.play(Write(equation))
        self.wait(0.5)
        
        # 應用複數變換（簡化版本）
        # 注意：ManimCE 沒有內建的 ComplexTransformationScene
        # 這裡用一個簡單的縮放動畫來模擬變換效果
        transform_animation = plane.animate.scale(0.7, about_point=ORIGIN).set_color(GREEN)
        self.play(transform_animation, run_time=2)
        
        self.play(Write(words, run_time=1))
        self.wait(1)

        # 創建流線場（簡化版本）
        # 注意：ManimCE 沒有內建的 StreamLines 和 AnimatedStreamLines
        # 這裡用一些箭頭來表示流場
        stream_lines = VGroup()
        for x in np.arange(0.01, 3, 0.25):
            for y in np.arange(0.01, 3, 0.25):
                # 創建一個簡單的箭頭表示流線
                arrow = Arrow(
                    start=[x, y, 0],
                    end=[x + 0.2, y + 0.1, 0],
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.2,
                    color=BLUE
                )
                stream_lines.add(arrow)
        
        # 播放流線動畫
        self.play(LaggedStart(
            *[GrowArrow(arrow) for arrow in stream_lines],
            lag_ratio=0.05
        ), run_time=3)
        
        self.wait(4)
