# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 將燈塔光源轉變為太陽，展示光源的變形過程，並包含一個觀察者 Pi 生物和屏幕。



from manim import *
class MorphIntoSunScene(PiCreatureScene):
    def construct(self):
        self.setup_elements()
        self.morph_lighthouse_into_sun()

    def setup_elements(self):
        self.remove(self.get_primary_pi_creature())

        SCREEN_SIZE = 3.0
        DISTANCE_FROM_LIGHTHOUSE = 10.0
        source_point = [-DISTANCE_FROM_LIGHTHOUSE/2, 0, 0]
        observer_point = [DISTANCE_FROM_LIGHTHOUSE/2, 0, 0]

        # Light source
        # 注意：ManimCE 沒有內建的 LightSource 類別
        # 這裡保留原結構，但需要自定義或使用替代方案
        self.light_source = LightSource(
            opacity_function=lambda r: inverse_quadratic(1, SPOTLIGHT_SCALE, 1),
            num_levels=NUM_LEVELS,
            radius=10,
            max_opacity_ambient=AMBIENT_FULL,
            max_opacity_spotlight=SPOTLIGHT_FULL,
        )
        self.light_source.move_source_to(source_point)

        # Pi Creature
        morty = self.get_primary_pi_creature()
        morty.scale(0.5)
        morty.move_to(observer_point)
        morty.shift(2 * OUT)
        self.add(morty)  # ManimCE 沒有 add_foreground_mobject，直接 add

        # 假設 light_source 有 lighthouse 和 ambient_light 屬性
        self.add(self.light_source.lighthouse, self.light_source.ambient_light)

        # Screen
        self.screen = Rectangle(
            width=0.06,
            height=2,
            fill_color=WHITE,
            fill_opacity=1.0,
            stroke_width=0.0
        )
        self.screen.next_to(morty, LEFT)

        self.light_source.set_screen(self.screen)
        self.add(self.screen, self.light_source.shadow)
        self.add(self.light_source.shadow)  # 替代 add_foreground_mobject
        self.add(morty)  # 再次添加確保在前景
        self.light_source.dim_ambient  # 假設是方法或屬性
        self.add(self.light_source.spotlight)
        self.screen_tracker = ScreenTracker(self.light_source)  # 假設 ScreenTracker 已定義
        self.add(self.screen_tracker)

        self.wait()

    def morph_lighthouse_into_sun(self):
        sun_position = np.array([-100, 0, 0])

        # 複製光源作為太陽
        self.sun = self.light_source.copy()

        # 修改太陽的光源不透明度函數
        # 注意：ManimCE 沒有 change_spotlight_opacity_function 方法
        # 這裡假設有 set_opacity 或類似屬性
        self.sun.spotlight.set_opacity(0.1)  # 替代方案

        # 重新初始化點（如果需要的話）
        self.sun.spotlight.init_points()

        self.wait()

        # 使用 Transform 動畫將燈塔變為太陽
        self.play(
            Transform(self.light_source, self.sun)
        )

        self.wait()
