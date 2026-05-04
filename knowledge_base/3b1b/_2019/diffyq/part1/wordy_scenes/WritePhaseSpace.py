# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示「Phase space」文字周圍出現放射狀閃光線條的動畫效果。



from manim import *
class WritePhaseSpace(Scene):
    def construct(self):
        word = Text("Phase space", font_size=96)
        word.scale(2)
        word.shift(config.frame_width * LEFT / 4)
        word.to_edge(UP)
        word.add_background_rectangle()

        # 生成放射狀線條
        lines = VGroup(*[
            Line(v, 1.3 * v)
            for v in [np.array([np.cos(theta), np.sin(theta), 0])
                     for theta in np.linspace(0, 2*np.pi, 50, endpoint=False)]
        ])
        lines.replace(word, stretch=True)
        lines.scale(1.5)
        lines.set_stroke(YELLOW)
        # 隨機排序線條
        lines_list = list(lines)
        np.random.shuffle(lines_list)
        lines = VGroup(*lines_list)

        self.add(word)
        # 使用 ShowPassingFlash 替代 ShowPassingFlashWithThinningStrokeWidth
        self.play(
            ShowPassingFlash(
                lines.copy(),
                lag_ratio=0.002,
                run_time=1.5,
                time_width=0.9,
            )
        )
        self.wait()
