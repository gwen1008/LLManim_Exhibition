# Source: 3b1b/_2018/WindingNumber_G.py
# Description: [3b1b translated] 展示一個網格排列的縮圖牆，所有縮圖隨機淡入後靜止。


from manim import *
import os
import random

class AllOfTheVideos(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_opacity = 1

    def construct(self):
        # 假設 MEDIA_DIR 已定義，若未定義請替換為實際路徑
        # 例如: MEDIA_DIR = "/path/to/media"
        thumbnail_dir = os.path.join(MEDIA_DIR, "3b1b_videos/Winding/OldThumbnails")
        n = 4
        images = Group(*[
            ImageMobject(os.path.join(thumbnail_dir, file))
            for file in os.listdir(thumbnail_dir)[:n**2]
        ])
        for image in images:
            rect = SurroundingRectangle(image, buff=0)
            rect.set_stroke(WHITE, 1)
            image.add(rect)
        images.arrange_in_grid(n, n, buff=0)
        images.set_height(config.frame_height)
        random.shuffle(images.submobjects)

        self.play(LaggedStartMap(FadeIn, images, run_time=4))
        self.wait()
