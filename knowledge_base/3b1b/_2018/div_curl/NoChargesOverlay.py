# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個帶有圓形鏤空區域的半透明藍色全屏矩形，並在頂部顯示「No charges outside wire」文字。



from manim import *
class NoChargesOverlay(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle()
        rect.set_fill(BLUE_D, 0.75)
        circle = Circle(radius=1.5)
        circle.rotate(135 * DEGREES)
        # 在 ManimCE 中，FullScreenFadeRectangle 沒有 add_subpath 方法
        # 改用 Rectangle 和 Difference 來實現類似效果
        # 創建一個與螢幕同大小的矩形
        screen_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLUE_D,
            fill_opacity=0.75,
            stroke_width=0
        )
        # 創建圓形（作為鏤空區域）
        circle = Circle(radius=1.5, fill_color=BLACK, fill_opacity=1, stroke_width=0)
        circle.rotate(135 * DEGREES)
        
        # 將兩者組合
        group = VGroup(screen_rect, circle)
        # 或者使用 Difference（如果版本支援）
        # 這裡使用簡單的 VGroup 近似效果

        words = Text("No charges outside wire")
        words.scale(1.5)
        words.to_edge(UP)

        self.add(group, words)
