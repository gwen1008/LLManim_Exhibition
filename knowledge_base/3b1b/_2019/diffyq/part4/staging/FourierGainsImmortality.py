# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示傅立葉的肖像與其他數學家肖像並列，並將傅立葉的肖像複製到「數學不朽者」群像中。



from manim import *
class FourierGainsImmortality(Scene):
    def __init__(self, mathematicians=None, **kwargs):
        super().__init__(**kwargs)
        if mathematicians is None:
            mathematicians = [
                "Pythagoras",
                "Euclid",
                "Archimedes",
                "Fermat",
                "Newton",
                "Leibniz",
                "Johann_Bernoulli2",
                "Euler",
                "Joseph Fourier",
                "Gauss",
                "Riemann",
                "Cantor",
                "Noether",
                "Ramanujan",
                "Godel",
                "Turing",
            ]
        self.mathematicians = mathematicians

    def construct(self):
        # 使用 ImageMobject 載入圖片，在 ManimCE 中對應的是 Image
        fourier = ImageMobject("Joseph Fourier")
        fourier.set_height(5)
        fourier.to_edge(LEFT)
        name = TexText("Joseph Fourier")
        name.next_to(fourier, DOWN)

        immortals = self.get_immortals()
        # 移除傅立葉的肖像（因為一開始在左邊）
        immortals.remove(immortals.fourier)
        immortals.to_edge(RIGHT)

        self.add(fourier, name)
        self.play(LaggedStart(
            *[FadeIn(img) for img in immortals[2:]],  # 跳過 title 和 frame
            lag_ratio=0.1,
            run_time=2,
        ))
        self.play(
            TransformFromCopy(fourier, immortals.fourier)
        )
        self.wait()

    def get_immortals(self):
        images = Group(*[
            ImageMobject(name)
            for name in self.mathematicians
        ])
        for image in images:
            image.set_height(1)
        images.arrange_in_grid(n_rows=4, buff=(0.2, 0.2))

        last_row = images[-4:]
        low_center = last_row.get_center()
        last_row.arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        last_row.move_to(low_center)

        frame = SurroundingRectangle(images)
        frame.set_color(WHITE)
        title = TexText("Immortals of Math")
        title.match_width(frame)
        title.next_to(frame, UP)

        result = Group(title, frame, *images)
        result.set_height(config.frame_height - 1)
        result.to_edge(RIGHT)
        for image, name in zip(images, self.mathematicians):
            # 將數學家的姓氏（小寫）設為 result 的屬性，方便存取
            last_name = name.split(" ")[-1].lower()
            setattr(result, last_name, image)
        return result
