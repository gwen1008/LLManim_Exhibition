# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個網址文字和一個從無到有繪製的螢幕矩形框，模擬擷取網頁畫面的過程。



from manim import *
class FeynmanLecturesScreenCaptureFrame(Scene):
    def construct(self):
        url = Text("http://www.feynmanlectures.caltech.edu/")
        url.to_edge(UP)

        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(url, DOWN)

        self.add(url)
        self.play(Create(screen_rect))
        self.wait()
