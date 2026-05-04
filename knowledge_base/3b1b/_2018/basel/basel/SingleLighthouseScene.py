# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示一個燈塔光源照射到旋轉屏幕上的動畫，包含角度測量和環境光變化。



from manim import *
class SingleLighthouseScene(PiCreatureScene):
    def construct(self):
        self.setup_elements()
        self.setup_angle()  # spotlight and angle msmt change when screen rotates
        self.rotate_screen()
        # self.morph_lighthouse_into_sun()

    def setup_elements(self):
        self.remove(self.get_primary_pi_creature())

        SCREEN_SIZE = 3.0
        DISTANCE_FROM_LIGHTHOUSE = 10.0
        source_point = [-DISTANCE_FROM_LIGHTHOUSE / 2, 0, 0]
        observer_point = [DISTANCE_FROM_LIGHTHOUSE / 2, 0, 0]

        # Light source - 注意：ManimCE 沒有 LightSource 類，這裡用替代方案
        # 我們用一個圓形和線條來模擬燈塔光源
        self.light_source = VGroup()
        lighthouse = Circle(radius=0.5, color=YELLOW, fill_opacity=1)
        lighthouse.move_to(source_point)
        self.light_source.add(lighthouse)
        self.light_source.source_point = source_point
        
        # 簡單的聚光燈效果
        spotlight = AnnularSector(
            inner_radius=0,
            outer_radius=8,
            angle=PI/3,
            start_angle=-PI/6,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=0
        )
        spotlight.move_arc_center_to(source_point)
        self.light_source.spotlight = spotlight
        self.light_source.add(spotlight)
        
        # 環境光
        ambient_light = Circle(radius=10, color=YELLOW, fill_opacity=0.05, stroke_width=0)
        ambient_light.move_to(source_point)
        self.light_source.ambient_light = ambient_light
        self.light_source.add(ambient_light)

        # Pi Creature
        morty = self.get_primary_pi_creature()
        morty.scale(0.5)
        morty.move_to(observer_point)
        morty.shift(2 * OUT)
        self.add(morty)

        self.add(self.light_source)

        # 模擬 SwitchOn 動畫
        self.play(FadeIn(self.light_source.ambient_light))

        # Screen
        self.screen = Rectangle(
            width=0.06,
            height=2,
            fill_color=WHITE,
            fill_opacity=1.0,
            stroke_width=0.0
        )
        self.screen.rotate(-TAU / 6)
        self.screen.next_to(morty, LEFT)

        # 簡單的陰影效果
        shadow = Rectangle(
            width=0.1,
            height=2.5,
            fill_color=BLACK,
            fill_opacity=0.5,
            stroke_width=0
        )
        shadow.rotate(-TAU / 6)
        shadow.next_to(morty, LEFT)
        shadow.shift(0.1 * RIGHT)
        self.light_source.shadow = shadow

        self.play(FadeIn(self.screen))
        self.wait()

        # 添加陰影
        self.play(FadeIn(self.light_source.shadow))
        self.add_foreground_mobjects(self.light_source.shadow, morty)

        # 模擬環境光變暗
        self.play(
            self.light_source.ambient_light.animate.set_opacity(0.02),
            FadeIn(self.light_source.spotlight)
        )

        self.wait()

    def setup_angle(self):
        self.wait()

        # 旋轉屏幕指向光源
        pointing_screen_at_source = Rotate(self.screen, TAU / 6)
        self.play(pointing_screen_at_source)

        # 角度測量（圓弧）
        arc_angle = PI / 3  # 固定角度，因為我們沒有真正的 LightSource 類
        self.angle_arc = Arc(
            radius=5,
            start_angle=-PI / 6,
            angle=arc_angle,
            color=WHITE
        )
        self.angle_arc.move_arc_center_to(self.light_source.source_point)

        # 角度測量（數字顯示）
        self.angle_indicator = DecimalNumber(
            arc_angle / DEGREES,
            num_decimal_places=0,
            unit="^\\circ",
            color=WHITE
        )
        self.angle_indicator.next_to(self.angle_arc, RIGHT)

        # 簡單的角度更新器
        def update_angle(mob):
            # 這裡簡化為固定角度
            mob.set_value(arc_angle / DEGREES)
        
        self.angle_indicator.add_updater(update_angle)
        self.add(self.angle_indicator)

        self.play(
            Create(self.angle_arc),
            Create(self.angle_indicator)
        )

        self.wait()

    def rotate_screen(self):
        # 旋轉屏幕
        self.play(Rotate(self.screen, TAU / 8))
        self.play(Rotate(self.screen, -TAU / 4))
        self.play(Rotate(self.screen, TAU / 8))
        self.wait()
        self.play(Rotate(self.screen, -TAU / 4))
        self.wait()
        self.play(Rotate(self.screen, TAU / 4))
