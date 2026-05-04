# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示兩個球面面積證明的縮圖，並用相機縮放聚焦每個縮圖。



from manim import *
class PreviewTwoMethods(MovingCameraScene):
    def construct(self):
        thumbnails = Group(
            ImageMobject("SphereSurfaceProof1"),
            ImageMobject("SphereSurfaceProof2"),
        )
        for thumbnail in thumbnails:
            thumbnail.set_width(config.frame_width / 2 - 1)
            thumbnail.add_to_back(SurroundingRectangle(
                thumbnail, buff=0,
                stroke_color=WHITE,
                stroke_width=5
            ))
        thumbnails.arrange(RIGHT, buff=LARGE_BUFF)

        title = Tex("Two proofs")
        title.scale(2)
        title.to_edge(UP)

        frame = self.camera.frame

        self.add(title)
        for thumbnail in thumbnails:
            self.play(FadeIn(thumbnail, shift=DOWN))
        self.wait()
        for thumbnail in thumbnails:
            frame.save_state()
            self.play(
                frame.animate.replace(thumbnail),
                run_time=2
            )
            self.wait()
            self.play(Restore(frame, run_time=2))
