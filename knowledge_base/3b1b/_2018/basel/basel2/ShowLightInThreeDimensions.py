# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 在三維空間中展示光源照射到不同形狀的屏幕上，並隨著屏幕形狀變換而動態調整光錐效果。



from manim import *
class ShowLightInThreeDimensions(ThreeDScene):
    def __init__(self, num_levels=200, **kwargs):
        super().__init__(**kwargs)
        self.num_levels = num_levels
    
    def construct(self):
        # 創建光源（假設 get_light_source 方法存在）
        light_source = self.get_light_source()
        
        # 創建三種不同形狀的屏幕
        screens = VGroup(
            Square(),
            RegularPolygon(8),
            Circle().insert_n_curves(25),
        )
        
        # 設置屏幕大小和位置
        screen_height = 2  # 假設的屏幕高度，可能需要根據實際情況調整
        for screen in screens:
            screen.set_height(screen_height)
        
        # 將屏幕旋轉並放置到觀察者左側
        screens.rotate(PI/2, UP)
        screens.next_to(np.array([-3, 0, 0]), LEFT)  # 假設的觀察者位置
        screens.set_stroke(WHITE, 2)
        screens.set_fill(WHITE, 0.5)
        
        # 使用第一個屏幕（正方形）作為起始
        screen = screens[0]
        
        # 創建三維光錐效果
        # 注意：ThreeDSpotlight 和 ContinualThreeDLightConeUpdate 是自定義類
        # 在 ManimCE 中需要重新實現或使用替代方案
        cone = ThreeDSpotlight(
            screen, light_source.ambient_light,
            light_source.get_source_point
        )
        cone_update_anim = ContinualThreeDLightConeUpdate(cone)
        
        # 添加物體到場景
        self.add(light_source, screen, cone)
        self.add(cone_update_anim)
        
        # 移動相機視角
        self.move_camera(
            phi=60*DEGREES,
            theta=-155*DEGREES,
            run_time=3,
        )
        
        # 開始環境相機旋轉
        self.begin_ambient_camera_rotation()
        
        # 動畫參數
        kwargs = {"run_time": 2}
        
        # 屏幕變形動畫序列
        self.play(screen.animate.stretch(0.5, 1), **kwargs)
        self.play(screen.animate.stretch(2, 2), **kwargs)
        
        self.play(Rotate(
            screen, PI/2,
            axis=UP+OUT,
            rate_func=there_and_back,
            run_time=3,
        ))
        
        self.play(Transform(screen, screens[1]), **kwargs)
        self.play(screen.animate.stretch(0.5, 2), **kwargs)
        self.play(Transform(screen, screens[2]), **kwargs)
        self.wait(2)
        
        self.play(
            screen.animate.stretch(0.5, 1),
            screen.animate.stretch(2, 2),
            **kwargs
        )
        
        self.play(
            screen.animate.stretch(3, 1),
            screen.animate.stretch(0.7, 2),
            **kwargs
        )
        
        self.wait(2)

# 注意：以下為可能需要實現的自定義類的框架
# 由於原代碼中的 ThreeDSpotlight 和 ContinualThreeDLightConeUpdate
# 不是 ManimCE 的標準類，這裡提供基本框架

class ThreeDSpotlight(ThreeDScene):
    """自定義的三維光錐類"""
    def __init__(self, screen, ambient_light, source_point_func, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.ambient_light = ambient_light
        self.source_point_func = source_point_func
        # 實現具體的光錐幾何體

class ContinualThreeDLightConeUpdate(Animation):
    """持續更新光錐的動畫類"""
    def __init__(self, cone, **kwargs):
        super().__init__(cone, **kwargs)
        self.cone = cone
    
    def interpolate_mobject(self, alpha):
        # 根據屏幕位置和光源位置更新光錐形狀
        pass
