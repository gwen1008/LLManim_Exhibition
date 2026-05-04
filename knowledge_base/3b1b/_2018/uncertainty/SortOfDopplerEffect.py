# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示多普勒效應的視覺化，包含移動的波函數、參考系變換以及頻率概念的動畫解釋。



from manim import *
class SortOfDopplerEffect(PiCreatureScene):
    def __init__(self, omega=np.pi, arrow_spacing=0.25, **kwargs):
        super().__init__(**kwargs)
        self.omega = omega
        self.arrow_spacing = arrow_spacing
        
    def setup(self):
        super().setup()
        rect = self.screen_rect = ScreenRectangle(height=FRAME_HEIGHT)
        rect.set_stroke(width=0)
        # 在ManimCE中，通常不需要特別處理相機移動，直接使用場景相機
        # 移除MovingCamera相關代碼
        
    def construct(self):
        screen_rect = self.screen_rect

        # x-coordinate gives time
        t_tracker = Dot(point=ORIGIN, radius=0.001)  # 替代VectorizedPoint
        # x-coordinate gives wave number
        k_tracker = Dot(point=2*RIGHT, radius=0.001)  # 替代VectorizedPoint
        
        # 替代always_shift
        def update_t_tracker(mob, dt):
            mob.shift(RIGHT * dt)
        t_tracker.add_updater(update_t_tracker)
        
        def get_wave():
            t = t_tracker.get_center()[0]
            k = k_tracker.get_center()[0]
            omega = self.omega
            color = interpolate_color(
                BLUE, RED, (k-2)/2.0
            )
            func = lambda x: 0.5*np.cos(omega*t - k*x)
            
            # 創建函數圖形
            graph = FunctionGraph(
                func,
                x_range=[-5*FRAME_WIDTH/2, FRAME_WIDTH/2],
                color=color,
            )
            
            # 創建箭頭
            arrows = VGroup(*[
                Arrow(
                    start=x*RIGHT,
                    end=x*RIGHT + func(x)*UP,
                    color=color,
                    buff=0
                )
                for x in np.arange(
                    -4*FRAME_WIDTH/2, FRAME_WIDTH/2,
                    self.arrow_spacing
                )
            ])
            
            return VGroup(graph, arrows)
        
        wave = get_wave()
        
        # 更新波形的updater
        def update_wave(mob):
            new_wave = get_wave()
            mob.become(new_wave)
        wave.add_updater(update_wave)

        rect = ScreenRectangle(height=2)
        rect.to_edge(RIGHT)
        
        # 替代always_shift
        def update_rect(mob, dt):
            mob.shift(LEFT * dt)
        rect.add_updater(update_rect)
        
        randy = self.pi_creature
        
        # 讓randy看著rect
        def update_randy_look(mob):
            mob.look_at(rect)
        randy.add_updater(update_randy_look)

        ref_frame1 = Text("Reference frame 1")
        ref_frame1.to_edge(UP)
        ref_frame2 = Text("Reference frame 2")
        ref_frame2.next_to(rect, UP)
        
        # 讓ref_frame2跟隨rect
        def update_ref_frame2(mob):
            mob.next_to(rect, UP)
        ref_frame2.add_updater(update_ref_frame2)

        self.add(t_tracker, wave, rect, randy, ref_frame2)
        self.add(ref_frame1)
        
        self.play(randy.animate.change("pondering"))
        self.wait(4)
        
        start_height = screen_rect.get_height()
        start_center = screen_rect.get_center()
        
        # 移動screen_rect到rect的位置
        self.play(
            screen_rect.animate.move_to(rect.get_center()),
            k_tracker.animate.shift(2*RIGHT),
        )
        
        # 保持screen_rect相對於rect的位置
        self.wait(4)  # 替代MaintainPositionRelativeTo
        
        self.play(
            screen_rect.animate.move_to(rect.get_right() + FRAME_WIDTH/2*LEFT),
            k_tracker.animate.shift(2*LEFT),
        )

        # Frequency words
        temporal_frequency = Text("Temporal frequency")
        spatial_frequency = Text("Spatial frequency")
        temporal_frequency.move_to(screen_rect).to_edge(UP)
        spatial_frequency.next_to(temporal_frequency, DOWN)
        cross = Cross(temporal_frequency)

        time_text = Text("Time")
        space_text = Text("Space")
        time_text.next_to(temporal_frequency, RIGHT, buff=2)
        space_text.next_to(time_text, DOWN)
        space_text.align_to(spatial_frequency, LEFT)

        self.play(FadeIn(temporal_frequency))
        self.play(Create(cross))
        self.play(Write(spatial_frequency))
        self.wait()
        self.play(FadeIn(time_text), FadeIn(space_text))
        self.play(
            Transform(time_text, space_text.copy()),
            Transform(space_text, time_text.copy()),
            lag_ratio=0.5,
            run_time=1,
        )
        self.play(FadeOut(time_text), FadeOut(space_text))
        self.wait(3)

    def create_pi_creature(self):
        return Randolph().scale(0.5).to_corner(DOWN+LEFT)
