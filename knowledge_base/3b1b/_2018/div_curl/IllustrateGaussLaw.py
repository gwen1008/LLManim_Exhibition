# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示兩個帶電粒子（質子與電子）周圍的向量場流線動畫，並透過鏡頭縮放聚焦於場線細節。



from manim import *
class IllustrateGaussLaw(Scene):
    def __init__(
        self,
        flow_time=10,
        stream_line_config={
            "start_points_generator_config": {
                "delta_x": 1.0 / 16,
                "delta_y": 1.0 / 16,
                "x_min": -2,
                "x_max": 2,
                "y_min": -1.5,
                "y_max": 1.5,
            },
            "color_lines_by_magnitude": True,
            "colors": [BLUE_E, BLUE_D, BLUE_C],
            "stroke_width": 3,
        },
        stream_line_animation_config={
            "line_anim_class": ShowPassingFlash,
            "line_anim_config": {
                "n_segments": 5,
            }
        },
        final_frame_width=4,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.flow_time = flow_time
        self.stream_line_config = stream_line_config
        self.stream_line_animation_config = stream_line_animation_config
        self.final_frame_width = final_frame_width

    def construct(self):
        particles = self.get_particles()
        vector_field = self.get_vector_field()

        # 在 ManimCE 中沒有 add_foreground_mobjects，直接加入並確保順序
        self.add(vector_field, particles)
        self.zoom_in()
        self.show_flow()

    def get_particles(self):
        # 假設 get_proton 和 get_electron 是自定義函數，返回帶顏色的圓形
        # 這裡用簡單的圓形替代
        proton = Circle(radius=0.1, color=RED, fill_opacity=1)
        electron = Circle(radius=0.1, color=BLUE, fill_opacity=1)
        
        particles = VGroup(proton, electron)
        particles.arrange(RIGHT, buff=2.25)
        particles.shift(0.25 * UP)
        
        # 為粒子添加電荷屬性
        particles[0].charge = +1  # 質子
        particles[1].charge = -1  # 電子

        self.particles = particles
        return particles

    def get_vector_field(self):
        # 簡化：建立一個向量場（這裡用 StreamLines 替代）
        # 實際應根據粒子電荷計算電場
        from manim.mobject.vector_field import StreamLines
        stream_lines = StreamLines(
            lambda p: np.array([
                p[0] - self.particles[0].get_center()[0],
                p[1] - self.particles[0].get_center()[1],
                0
            ]) * 0.5 - np.array([
                p[0] - self.particles[1].get_center()[0],
                p[1] - self.particles[1].get_center()[1],
                0
            ]) * 0.5,
            **self.stream_line_config
        )
        return stream_lines

    def zoom_in(self):
        self.play(
            self.camera.frame.animate.set_width(self.final_frame_width),
            run_time=2
        )

    def show_flow(self):
        # 簡化：播放流線動畫
        stream_lines = self.get_vector_field()
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.0)
        self.wait(self.flow_time)
