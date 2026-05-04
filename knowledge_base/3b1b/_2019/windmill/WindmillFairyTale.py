# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個風車童話插圖的 SVG 圖形分層淡入動畫。



from manim import *
class WindmillFairyTale(Scene):
    def construct(self):
        # 載入 SVG 檔案
        paths = SVGMobject(file_name="windmill_fairytale")

        # 設定大小和樣式
        paths.set_height(config.frame_height - 1)
        paths.set_stroke(width=0)
        paths.set_fill([GREY_B, WHITE])

        # 反轉點順序（保持與原代碼一致）
        for path in paths:
            path.reverse_points()

        # 先寫入第一個路徑
        self.play(Write(paths[0], run_time=3))
        self.wait()
        # 然後以延遲方式淡入其餘路徑
        self.play(
            LaggedStart(
                FadeIn(paths[1], shift=RIGHT),
                FadeIn(paths[2], shift=RIGHT),
                lag_ratio=0.2,
                run_time=3,
            )
        )
