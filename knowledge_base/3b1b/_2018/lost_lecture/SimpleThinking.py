# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個藍色卡通人物從思考狀態轉變為歡呼狀態的動畫過程。



from manim import *
class SimpleThinking(Scene):
    def construct(self):
        randy = Randolph(color=BLUE_C)
        randy.flip()
        self.play(randy.animate.change("thinking", 3 * UP))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.animate.change("hooray", 3 * UP))
        self.play(Blink(randy))
        self.wait()
