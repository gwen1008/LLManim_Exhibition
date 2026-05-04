# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示從謎題到解決方案的過渡，透過縮放相機框聚焦於兩個圖像並恢復視角。



from manim import *
class FromPuzzleToSolution(MovingCameraScene):
    def construct(self):
        big_rect = FullScreenFadeRectangle()
        big_rect.set_fill(GREY_D, 0.5)
        self.add(big_rect)

        rects = VGroup(ScreenRectangle(), ScreenRectangle())
        rects.set_height(3)
        rects.arrange(RIGHT, buff=2)

        titles = VGroup(
            Text("Puzzle"),
            Text("Solution"),
        )

        images = Group(
            ImageMobject("BlocksAndWallExampleMass16"),
            ImageMobject("AnalyzeCircleGeometry"),
        )
        for title, rect, image in zip(titles, rects, images):
            title.scale(1.5)
            title.next_to(rect, UP)
            image.replace(rect)
            self.add(image, rect, title)

        frame = self.camera.frame
        frame.save_state()

        self.play(
            frame.animate.replace(images[0]),
            run_time=3
        )
        self.wait()
        self.play(Restore(frame, run_time=3))
        self.play(
            frame.animate.replace(images[1]),
            run_time=3,
        )
        self.wait()
