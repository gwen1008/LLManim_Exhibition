# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示傅立葉的頭像與思考泡泡，並從泡泡中飛出三個主要觀察要點的文字，最後逐一強調每個觀察的內容。



from manim import *
class ThreeMainObservations(Scene):
    def construct(self):
        # 傅立葉圖像與名字
        fourier = ImageMobject("Joseph Fourier")
        name = Text("Joseph Fourier")
        name.match_width(fourier)
        name.next_to(fourier, DOWN, buff=SMALL_BUFF)
        fourier.add(name)
        fourier.set_height(5)
        fourier.to_corner(DR)
        fourier.shift(LEFT)
        
        # 思考泡泡
        bubble = ThoughtBubble(
            direction=RIGHT,
            height=3,
            width=4,
        )
        bubble.move_tip_to(fourier.get_corner(UL) + 0.5 * DR)

        # 三個觀察要點
        observations = VGroup(
            Text("1)  Sine = Nice"),
            Text("2)  Linearity"),
            Text("3)  Fourier series"),
        )
        
        # 排列觀察要點
        observations.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=2 * LARGE_BUFF,
        )
        observations.set_height(config.frame_height - 2)
        observations.to_corner(UL, buff=LARGE_BUFF)

        # 動畫開始
        self.add(fourier)
        self.play(Create(bubble))
        self.wait()
        
        # 從泡泡飛出數字編號
        self.play(LaggedStart(*[
            TransformFromCopy(bubble, observation[0])
            for observation in observations
        ], lag_ratio=0.2))
        
        # 淡出傅立葉和泡泡
        self.play(
            FadeOut(fourier),
            FadeOut(bubble),
        )
        self.wait()
        
        # 逐一顯示每個觀察的內容
        for obs in observations:
            self.play(FadeIn(obs[1:], shift=LEFT))
            self.wait()
