# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示「真實物理」與「此過程」兩個文字標籤，其中「此過程」向右快速移出畫面。



from manim import *
class RealPhysicsVsThis(Scene):
    def construct(self):
        physics = Text("Real physics")
        this = Text("This process")
        this.set_color(BLUE)  # 預設顏色，可根據原意調整
        physics.to_edge(LEFT)
        this.next_to(physics, RIGHT)
        self.add(physics, this)
        self.play(
            this.animate.shift(FRAME_WIDTH * RIGHT),
            rate_func=rush_into,
            run_time=3,
        )
        self.wait()
