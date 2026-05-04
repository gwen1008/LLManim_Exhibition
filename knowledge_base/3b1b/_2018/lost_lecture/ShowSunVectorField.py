# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個以太陽為中心的向量場，其向量隨距離衰減，並以黃色高亮脈動三次。



from manim import *
class ShowSunVectorField(Scene):
    def __init__(self, sun_center=ORIGIN, **kwargs):
        super().__init__(**kwargs)
        self.sun_center = sun_center

    def construct(self):
        # 定義力場函數（模擬萬有引力）
        def get_force_field_func(center, strength=-1):
            def func(point):
                vec = point - center
                distance = np.linalg.norm(vec)
                if distance < 0.001:
                    return np.zeros(3)
                # 力的大小與 1/r^2 成正比，方向指向中心
                force = strength * vec / (distance**3)
                return force
            return func

        # 創建向量場
        vector_field = VectorField(
            get_force_field_func(self.sun_center, -1),
            length_func=lambda norm: 0.5 * np.tanh(norm),
        )
        vector_field.set_opacity(0.8)
        # 按距離排序（從遠到近）
        vector_field.submobjects.sort(
            key=lambda v: -np.linalg.norm(v.get_start() - self.sun_center)
        )

        # 為每個向量創建目標狀態（高亮）
        for vector in vector_field:
            vector.target = vector.copy()
            vector.target.set_opacity(1)
            vector.target.set_stroke(YELLOW, 0.5)

        self.add(vector_field)
        # 播放三次脈動動畫
        for _ in range(3):
            self.play(LaggedStart(
                *[MoveToTarget(v) for v in vector_field],
                rate_func=there_and_back,
                lag_ratio=0.5,
            ))
        self.wait()
