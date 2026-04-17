# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個圓形湖泊中心向四個方向延伸的線條，並在相鄰線條之間短暫顯示直角標記的動畫。



from manim import *
class RightAnglesOverlay(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.BASELINE_YPOS = -2.5
        self.OBSERVER_POINT = np.array([0, self.BASELINE_YPOS, 0])
        self.LAKE0_RADIUS = 1.5 * 2
        self.INDICATOR_RADIUS = 0.6
        self.TICK_SIZE = 0.5
        self.LIGHTHOUSE_HEIGHT = 0.2
        self.LAKE_COLOR = BLUE
        self.LAKE_OPACITY = 0.15
        self.LAKE_STROKE_WIDTH = 5.0
        self.LAKE_STROKE_COLOR = BLUE
        self.TEX_SCALE = 0.8
        self.DOT_COLOR = BLUE
        self.RIGHT_ANGLE_SIZE = 0.3

    def right_angle(self, pointA, pointB, pointC, size=1):
        v1 = pointA - pointB
        v1 = size * v1 / np.linalg.norm(v1)
        v2 = pointC - pointB
        v2 = size * v2 / np.linalg.norm(v2)
        
        P = pointB
        Q = pointB + v1
        R = Q + v2
        S = R - v1
        
        angle_sign = VMobject()
        angle_sign.set_points_as_corners([P, Q, R, S, P])
        angle_sign.mark_paths_closed = True
        angle_sign.set_fill(color=WHITE, opacity=1)
        angle_sign.set_stroke(width=0)
        return angle_sign

    def construct(self):
        lake_center = self.OBSERVER_POINT + self.LAKE0_RADIUS * UP
        points = []
        lines = VGroup()
        
        for i in range(4):
            theta = -TAU/4 + (i + 0.5) * TAU/4
            v = np.array([np.cos(theta), np.sin(theta), 0])
            P = lake_center + self.LAKE0_RADIUS * v
            points.append(P)
            lines.add(Line(lake_center, P, stroke_width=8))
        
        self.play(FadeIn(lines))
        self.wait()
        
        for i in range(4):
            sign = self.right_angle(points[i-1], lake_center, points[i], self.RIGHT_ANGLE_SIZE)
            self.play(FadeIn(sign))
            self.play(FadeOut(sign))
        
        self.wait()
        self.play(FadeOut(lines))
        
        # Note: flash_arcs(3) 在 ManimCE 中沒有直接對應方法
        # 如果這是自定義函數，需要另外實現
        # 這裡暫時略過不影響核心邏輯
