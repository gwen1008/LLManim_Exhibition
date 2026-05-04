# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 展示一個旋轉的球體，並在畫面上方顯示「什麼是球體？」的文字問題。



from manim import *
class DrawSphere(ThreeDScene):
    def construct(self):
        sphere = Sphere()
        sphere.shift(IN)
        question = Text("What is a sphere?", font_size=48)
        question.set_width(config.frame_width - 3)
        question.to_edge(UP)
        
        self.set_camera_orientation(phi=70 * DEGREES, theta=0)
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # 將2D物件固定在畫面上（不受3D相機影響）
        self.add_fixed_in_frame_mobjects(question)
        
        self.play(
            Create(sphere),
            FadeIn(question, shift=DOWN)
        )
        self.wait(4)
