# Source: 3b1b/_2018/basel/basel.py
# Description: [3b1b translated] 展示地球模型與螢幕的互動，模擬光源照射下螢幕從獨立位置移動到地球表面特定緯度的過程。



from manim import *
class EarthScene(Scene):

    def construct(self):

        SCREEN_THICKNESS = 10

        self.screen_height = 2.0
        self.brightness_rect_height = 1.0

        # screen
        self.screen = VMobject(stroke_color = WHITE, stroke_width = SCREEN_THICKNESS)
        self.screen.set_points_as_corners([
            [0,-self.screen_height/2,0],
            [0,self.screen_height/2,0]
        ])

        # Earth

        earth_center_x = 2
        earth_center = [earth_center_x,0,0]
        earth_radius = 3
        earth = Circle(radius = earth_radius)
        earth.add(self.screen)
        earth.move_to(earth_center)
        #self.remove(self.screen_tracker)

        theta0 = 70 * DEGREES
        dtheta = 10 * DEGREES
        theta1 = theta0 + dtheta
        theta = (theta0 + theta1)/2

        # ManimCE 沒有 add_foreground_mobject，用 add 代替
        self.add(self.screen)

        # background Earth
        background_earth = SVGMobject(
            file_name = "earth",
            width = 2 * earth_radius,
            fill_color = BLUE,
        )
        background_earth.move_to(earth_center)
        # Morty

        morty = Mortimer().scale(0.5).next_to(self.screen, RIGHT, buff = 1.5)
        self.add(morty)  # 替代 add_foreground_mobject


        # Light source (far-away Sun)
        # ManimCE 沒有 LightSource 類別，用 Dot 替代示意
        sun_position = [-100,0,0]

        self.sun = Dot(
            point = sun_position,
            color = YELLOW,
            radius = 0.5
        )

        # 移除 screen_tracker 相關代碼，因為 ManimCE 沒有 ScreenTracker
        # Add elements to scene

        self.add(self.sun, self.screen)
        # 移除 bring_to_back 調用
        # screen_tracker = ScreenTracker(self.sun)
        # self.add(screen_tracker)
        
        self.wait()

        self.play(
            FadeIn(earth),
            FadeIn(background_earth)
        )
        self.add(earth)  # 替代 add_foreground_mobject
        self.add(self.screen)  # 替代 add_foreground_mobject


        # move screen onto Earth
        screen_on_earth = self.screen.copy()
        screen_on_earth.rotate(-theta)
        screen_on_earth.scale(0.3)
        screen_on_earth.move_to(np.array([
            earth_center_x - earth_radius * np.cos(theta),
            earth_radius * np.sin(theta),
            0]))

        polar_morty = morty.copy().scale(0.5).next_to(screen_on_earth,DOWN,buff = 0.5)
        polar_morty.set_color(BLUE_C)

        self.play(
            Transform(self.screen, screen_on_earth),
            Transform(morty,polar_morty)
        )

        self.wait()


        tropical_morty = polar_morty.copy()
        tropical_morty.move_to(np.array([0,0,0]))
        tropical_morty.set_color(RED)

        morty.target = tropical_morty

        # move screen to equator

        self.play(
            Rotate(earth, theta0 + dtheta/2,run_time = 3),
            MoveToTarget(morty, path_arc = 70*DEGREES, run_time = 3),
        )
