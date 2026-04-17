# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示一個光源照射到屏幕上，並隨著屏幕旋轉時光線角度變化的動畫過程。



from manim import *
class IntroduceScreen(Scene):
    def __init__(
        self,
        num_levels=100,
        radius=10,
        num_rays=250,
        min_ray_angle=0,
        max_ray_angle=TAU,
        source_point=2.5*LEFT,
        observer_point=3.5*RIGHT,
        screen_height=2,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.num_levels = num_levels
        self.radius = radius
        self.num_rays = num_rays
        self.min_ray_angle = min_ray_angle
        self.max_ray_angle = max_ray_angle
        self.source_point = source_point
        self.observer_point = observer_point
        self.screen_height = screen_height

    def construct(self):
        self.setup_elements()
        self.setup_angle()  # spotlight and angle msmt change when screen rotates
        self.rotate_screen()
        # self.morph_lighthouse_into_sun()

    def setup_elements(self):
        SCREEN_SIZE = 3.0
        source_point = self.source_point
        observer_point = self.observer_point

        # Light source
        light_source = self.light_source = self.get_light_source()

        # Screen
        screen = self.screen = Rectangle(
            width=0.05,
            height=self.screen_height,
            fill_color=WHITE,
            fill_opacity=1.0,
            stroke_width=0.0
        )

        screen.next_to(observer_point, LEFT)

        screen_label = Text("Screen")
        screen_label.next_to(screen, UP + LEFT)
        screen_arrow = Arrow(
            screen_label.get_bottom(),
            screen.get_center(),
        )

        # Pi creature
        morty = Mortimer()
        morty.shift(screen.get_center() - morty.eyes.get_left())
        morty.look_at(source_point)

        # Camera
        camera = SVGMobject(file_name="camera")
        camera.rotate(TAU / 4)
        camera.set_height(1.5)
        camera.move_to(morty.eyes, LEFT)

        # Animations
        light_source.set_max_opacity_spotlight(0.001)
        screen_tracker = self.screen_tracker = ScreenTracker(light_source)

        self.add(light_source.lighthouse)
        self.play(FadeIn(light_source.ambient_light))
        self.play(
            Write(screen_label),
            GrowArrow(screen_arrow),
            FadeIn(screen)
        )
        self.wait()
        self.play(*[FadeOut(mob) for mob in [screen_label, screen_arrow]])
        screen.save_state()
        self.play(
            FadeIn(morty),
            screen.animate.match_height(morty.eyes),
            screen.animate.next_to(morty.eyes, LEFT, buff=SMALL_BUFF)
        )
        self.play(Blink(morty))
        self.play(
            FadeOut(morty),
            FadeIn(camera),
            screen.animate.scale(2, about_edge=UP),
        )
        self.wait()
        self.play(
            FadeOut(camera),
            screen.animate.restore(),
        )

        light_source.set_screen(screen)
        light_source.spotlight.opacity_function = lambda r: 0.2 / (r + 1)
        screen_tracker.update(0)

        ## Ask about proportion
        self.add_foreground_mobjects(light_source.shadow, screen)
        self.shoot_rays()

        ##
        self.play(FadeIn(light_source.spotlight))

    def setup_angle(self):
        self.wait()

        # angle msmt (arc)
        arc_angle = self.light_source.spotlight.opening_angle()
        # draw arc arrows to show the opening angle
        self.angle_arc = Arc(
            radius=3,
            start_angle=self.light_source.spotlight.start_angle(),
            angle=self.light_source.spotlight.opening_angle(),
        )
        # angle_arc.add_tip(at_start=True, at_end=True)
        self.angle_arc.move_arc_center_to(self.light_source.get_source_point())

        # angle msmt (decimal number)
        self.angle_indicator = DecimalNumber(
            arc_angle / DEGREES,
            num_decimal_places=0,
        )
        self.angle_indicator.next_to(self.angle_arc, RIGHT)

        angle_update_func = lambda: self.light_source.spotlight.opening_angle() / DEGREES
        self.angle_indicator.add_updater(
            lambda d: d.set_value(angle_update_func())
        )
        self.add(self.angle_indicator)

        arc_tracker = AngleUpdater(
            self.angle_arc,
            self.light_source.spotlight
        )
        self.add(arc_tracker)

        self.play(
            Create(self.angle_arc),
            Create(self.angle_indicator)
        )

        self.wait()

    def rotate_screen(self):
        self.add(
            self.light_source.add_updater(
                lambda m: m.update()
            ),
        )
        self.add(
            self.angle_indicator.add_updater(
                lambda m: m.set_stroke(width=0).set_fill(opacity=1)
            )
        )
        self.remove(self.light_source.ambient_light)

        def rotate_screen(angle):
            self.play(
                Rotate(self.light_source.spotlight.screen, angle),
                Animation(self.angle_arc),
                run_time=2,
            )

        for angle in [TAU / 8, -TAU / 4, TAU / 8, -TAU / 6]:
            rotate_screen(angle)
            self.wait()
        self.shoot_rays()
        rotate_screen(TAU / 6)

    ##

    def get_light_source(self):
        light_source = LightSource(
            opacity_function=lambda x: 1 / (x**2 + 2*x + 1),  # inverse_quadratic(1,2,1)
            num_levels=self.num_levels,
            radius=self.radius,
            max_opacity_ambient=1.0,  # AMBIENT_FULL
        )
        light_source.move_source_to(self.source_point)
        return light_source

    def shoot_rays(self, show_creation_kwargs=None):
        if show_creation_kwargs is None:
            show_creation_kwargs = {}
        source_point = self.source_point
        screen = self.screen

        # Rays
        step_size = (self.max_ray_angle - self.min_ray_angle) / self.num_rays
        rays = VGroup(*[
            Line(ORIGIN, self.radius * rotate_vector(RIGHT, angle))
            for angle in np.arange(
                self.min_ray_angle,
                self.max_ray_angle,
                step_size
            )
        ])
        rays.shift(source_point)
        rays.set_stroke(YELLOW, 1)
        max_angle = np.max([
            angle_of_vector(point - source_point)
            for point in screen.get_points()
        ])
        min_angle = np.min([
            angle_of_vector(point - source_point)
            for point in screen.get_points()
        ])
        for ray in rays:
            if min_angle <= ray.get_angle() <= max_angle:
                ray.target_color = GREEN
            else:
                ray.target_color = RED

        self.play(*[
            Create(ray, run_time=3, **show_creation_kwargs)
            for ray in rays
        ])
        self.play(*[
            ray.animate.set_color(ray.target_color)
            for ray in rays
        ])
        self.wait()
        self.play(FadeOut(rays))
