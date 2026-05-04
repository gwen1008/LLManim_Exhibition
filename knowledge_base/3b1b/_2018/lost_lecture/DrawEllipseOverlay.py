# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個紅色橢圓形在畫面上被繪製出來，然後淡出消失的過程。



from manim import *
class DrawEllipseOverlay(Scene):
    def construct(self):
        ellipse = Circle()
        ellipse.stretch_to_fit_width(7.0)
        ellipse.stretch_to_fit_height(3.8)
        ellipse.shift(1.05 * UP + 0.48 * LEFT)
        ellipse.set_stroke(RED, 8)

        # 註解掉 ImageMobject 相關代碼，因為在 CE 中需要調整路徑處理
        # 如果確實需要圖片，請使用 ImageMobject 的 CE 等效方法並確保路徑正確
        # image = ImageMobject(
        #     os.path.join(
        #         get_image_output_directory(self.__class__),
        #         "HeldUpEllipse.jpg"
        #     )
        # )
        # image.set_height(config.frame_height)
        # self.add(image)

        self.play(Create(ellipse))
        self.wait()
        self.play(FadeOut(ellipse))
