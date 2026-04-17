# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示一個思考泡泡從角色頭部出現，並在其中旋轉三個橢圓形狀的動畫過程。



from manim import *
class ThinkAboutPondScene(PiCreatureScene):
    def __init__(self, default_pi_creature_class=Randolph, **kwargs):
        super().__init__(default_pi_creature_class=default_pi_creature_class, **kwargs)
    
    def construct(self):
        randy = self.pi_creature
        randy.to_corner(DOWN+LEFT)
        
        # 創建思考泡泡
        bubble = ThoughtBubble(
            width=11,
            height=8,
        )
        
        # 獲取泡泡中的圓形部分（前三個元素）
        circles = bubble[:3]
        angle = -15*DEGREES
        
        # 旋轉和移動圓形
        circles.rotate(angle, about_point=bubble.get_bubble_center())
        circles.shift(LARGE_BUFF*LEFT)
        for circle in circles:
            circle.rotate(-angle)
        
        # 將泡泡固定在角色上
        bubble.pin_to(randy)
        bubble.shift(DOWN)
        
        # 進一步調整泡泡中的圓形
        bubble[:3].rotate(PI, axis=UP+2*RIGHT, about_edge=UP+LEFT)
        bubble[:3].scale(0.7, about_edge=DOWN+RIGHT)
        bubble[:3].shift(1.5*DOWN)
        
        # 旋轉每個橢圓
        for oval in bubble[:3]:
            oval.rotate(TAU/3)
        
        # 播放動畫
        self.play(
            randy.change("thinking"),
            Create(bubble)
        )
        self.wait(2)
        
        self.play(
            randy.change("happy"),
            FadeOut(bubble)
        )
        self.wait(4)
        
        self.play(
            randy.change("hooray"),
            FadeIn(bubble)
        )
        self.wait(2)
