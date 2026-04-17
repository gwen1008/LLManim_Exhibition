# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示圓柱繞流的向量場與流線動畫，圓柱周圍的向量場被移除，流線從左向右流動，中央有一個黃色圓柱。



from manim import *
class PureCylinderFlow(Scene):
    def construct(self):
        self.add_vector_field()
        self.begin_flow()
        self.add_circle()
        self.wait(5)

    def add_vector_field(self):
        # 注意：ManimCE 的 VectorField 需要 vector_func 參數
        # 假設 cylinder_flow_vector_field 是一個已定義的函數
        vector_field = VectorField(
            cylinder_flow_vector_field,
        )
        # 移除圓柱內部的向量
        for vector in vector_field:
            if np.linalg.norm(vector.get_start()) < 1:
                vector_field.remove(vector)
        vector_field.set_opacity(0.75)
        self.modify_vector_field(vector_field)
        self.add(vector_field)  # ManimCE 沒有 add_foreground_mobjects

    def begin_flow(self):
        # 注意：ManimCE 沒有內建的 StreamLines 和 AnimatedStreamLines
        # 這裡使用替代方案：創建一個自定義的流線動畫
        # 由於原代碼依賴特定類，這裡簡化為示意性實現
        stream_lines = VGroup()  # 使用 VGroup 代替 StreamLines
        # 生成流線點（示意）
        for x in np.arange(-4, 4, 0.125):
            for y in np.arange(-3, 3, 0.125):
                start_point = np.array([x, y, 0])
                if np.linalg.norm(start_point) >= 1:  # 移除圓柱內部的流線
                    # 創建一條簡單的線段作為流線示意
                    line = Line(start_point, start_point + RIGHT * 0.5, stroke_width=2)
                    line.set_color(random.choice([BLUE_E, BLUE_D, BLUE_C]))
                    stream_lines.add(line)
        
        self.modify_flow(stream_lines)
        self.add(stream_lines)
        
        # 創建流線動畫：讓線段向右移動
        animations = []
        for line in stream_lines:
            anim = line.animate.shift(RIGHT * 5).set_run_time(5)
            animations.append(anim)
        
        # 同時播放所有流線動畫
        self.play(*animations, run_time=5, lag_ratio=0)

    def add_circle(self):
        circle = Circle(
            radius=1,
            stroke_color=YELLOW,
            fill_color=BLACK,
            fill_opacity=1,
        )
        self.modify_flow(circle)
        self.add(circle)  # ManimCE 沒有 add_foreground_mobjects

    def modify_flow(self, mobject):
        # 可被子類覆蓋的方法
        pass

    def modify_vector_field(self, vector_field):
        # 可被子類覆蓋的方法
        pass
