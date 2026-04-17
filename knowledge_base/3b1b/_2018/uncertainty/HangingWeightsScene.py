# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一排懸掛在天花板上的彈簧與重物，模擬波動傳播，並與量子力學中的德布羅意波類比。


from manim import *
import numpy as np

class HangingWeightsScene(MovingCameraScene):
    def __init__(
        self,
        frequency=0.5,
        ceiling_radius=3 * config.frame_width / 2,
        n_springs=72,
        amplitude=0.6,
        spring_radius=0.15,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.frequency = frequency
        self.ceiling_radius = ceiling_radius
        self.n_springs = n_springs
        self.amplitude = amplitude
        self.spring_radius = spring_radius

    def construct(self):
        self.setup_springs()
        self.setup_weights()
        self.introduce()
        self.show_analogy_with_electron()
        self.metaphor_for_something()
        self.moving_reference_frame()

    def setup_springs(self):
        ceiling = self.ceiling = Line(LEFT, RIGHT)
        ceiling.scale(self.ceiling_radius)
        ceiling.to_edge(UP, buff=LARGE_BUFF)
        self.add(ceiling)

        def get_spring(alpha, height=2):
            t_max = 6.5
            r = self.spring_radius
            s = (height - r) / (t_max**2)
            spring = ParametricFunction(
                lambda t: np.array([
                    r * np.sin(TAU * t),
                    -s * ((t_max - t) ** 2),
                    0
                ]),
                t_range=[0, t_max],
                color=WHITE,
                stroke_width=2,
            )
            spring.alpha = alpha
            spring.move_to(ceiling.point_from_proportion(alpha), UP)
            spring.set_color_by_gradient(GREY_A, GREY_E)
            return spring

        alphas = np.linspace(0, 1, self.n_springs)
        springs = self.springs = VGroup(*[get_spring(a) for a in alphas])

        k_tracker = self.k_tracker = VectorizedPoint()
        t_tracker = self.t_tracker = VectorizedPoint()
        t_tracker.add_updater(lambda m, dt: m.shift(RIGHT * dt))
        self.t_tracker_walk = t_tracker
        equilibrium_height = springs.get_height()

        def update_springs(springs):
            for spring in springs:
                k = k_tracker.get_center()[0]
                t = t_tracker.get_center()[0]
                f = self.frequency
                x = spring.get_top()[0]
                A = self.amplitude
                d_height = A * np.cos(TAU * f * t - k * x)
                new_spring = get_spring(spring.alpha, 2 + d_height)
                spring.become(new_spring)

        springs.add_updater(update_springs)
        self.spring_update_anim = springs
        update_springs(springs)

        self.play(
            Create(ceiling),
            LaggedStartMap(Create, springs)
        )

    def setup_weights(self):
        weights = self.weights = VGroup()
        weight_anims = []
        for spring in self.springs:
            x = spring.get_top()[0]
            mass = np.exp(-0.1 * x**2)
            weight = Circle(radius=0.15)
            weight.start_radius = 0.15
            weight.target_radius = 0.25 * mass
            weight.spring = spring
            weight_anim = weight.add_updater(
                lambda w: w.move_to(w.spring.get_bottom())
            )
            weight_anim.update(0)
            weight_anims.append(weight_anim)
            weights.add(weight)
        weights.set_fill(opacity=1)
        weights.set_color_by_gradient(BLUE_D, BLUE_E, BLUE_D)
        weights.set_stroke(WHITE, 1)

        self.play(LaggedStartMap(GrowFromCenter, weights))
        self.add(self.t_tracker_walk)
        self.add(self.spring_update_anim)
        for anim in weight_anims:
            self.add(anim)

    def introduce(self):
        arrow = Arrow(4 * LEFT, LEFT)
        arrows = VGroup(arrow, arrow.copy().flip(about_point=ORIGIN))
        arrows.set_color(WHITE)

        self.wait(3)
        self.play(*[GrowArrow(a) for a in arrows])
        self.play(*[
            UpdateFromAlphaFunc(
                weight,
                lambda w, a: w.set_width(
                    2 * interpolate(w.start_radius, w.target_radius, a)
                ),
                run_time=2
            )
            for weight in self.weights
        ])
        self.play(FadeOut(arrows))
        self.wait(3)

    def show_analogy_with_electron(self):
        words = Text(
            "Analogous to the energy of a particle\n"
            "(in the sense of $E=mc^2$)",
            font_size=36
        )
        words.move_to(DOWN)

        self.play(Write(words))
        self.wait(3)
        self.play(FadeOut(words))

    def metaphor_for_something(self):
        de_broglie = ImageMobject("de_Broglie")
        de_broglie.set_height(3.5)
        de_broglie.to_corner(DOWN + RIGHT)
        words = Text(
            "If a photon's energy is carried as a wave\n"
            "is this true for any particle?",
            font_size=36
        )
        words.next_to(de_broglie, LEFT)

        einstein = ImageMobject("Einstein")
        einstein.match_height(de_broglie)
        einstein.to_corner(DOWN + LEFT)

        for picture in [de_broglie, einstein]:
            picture.backdrop = Rectangle()
            picture.backdrop.replace(picture, stretch=True)
            picture.backdrop.set_fill(BLACK, 1)
            picture.backdrop.set_stroke(BLACK, 0)

        self.play(
            FadeOut(de_broglie.backdrop),
            FadeIn(de_broglie)
        )
        self.play(Write(words))
        self.wait(7)
        self.play(
            FadeOut(words),
            FadeOut(einstein.backdrop),
            FadeIn(einstein)
        )
        self.wait(2)

        self.de_broglie = de_broglie
        self.einstein = einstein

    def moving_reference_frame(self):
        rect = ScreenRectangle(height=2.1 * config.frame_height / 2)
        rect.add_updater(lambda m, dt: m.shift(LEFT * 2 * dt))
        camera_frame = self.camera.frame

        self.add(rect)
        self.play(
            FadeOut(self.de_broglie.backdrop),
            FadeOut(self.de_broglie),
            FadeOut(self.einstein.backdrop),
            FadeOut(self.einstein),
        )
        self.play(camera_frame.animate.scale(3, about_point=2 * UP))
        self.play(rect.animate.shift(FRAME_WIDTH * RIGHT).rotate(-TAU / 2))
        self.wait(3)

        def zoom_into_reference_frame():
            original_height = camera_frame.height
            original_center = camera_frame.get_center()
            self.play(
                UpdateFromAlphaFunc(
                    camera_frame,
                    lambda c, a: c.set_height(
                        interpolate(original_height, 0.95 * rect.height, a)
                    ).move_to(
                        interpolate(original_center, rect.get_center(), a)
                    )
                ),
                self.k_tracker.animate.shift(RIGHT)
            )
            self.play(
                camera_frame.animate.move_to(rect.get_center()),
                run_time=6
            )
            self.play(
                camera_frame.animate.set_height(original_height).move_to(original_center),
                self.k_tracker.animate.shift(LEFT)
            )

        zoom_into_reference_frame()
        self.wait()
        self.play(
            UpdateFromAlphaFunc(rect, lambda m, a: m.set_stroke(width=2 * (1 - a)))
        )

        index = int(0.5 * len(self.springs))
        weights = VGroup(self.weights[index], self.weights[index + 4])
        flashes = [self.get_peak_flash_anim(w) for w in weights]
        weights.save_state()
        weights.set_fill(RED)
        for flash in flashes:
            self.add(flash)
        self.wait(5)

        rect.align_to(camera_frame, RIGHT)
        self.play(UpdateFromAlphaFunc(rect, lambda m, a: m.set_stroke(width=2 * a)))

        randy = Randolph()
        randy.look(UP + RIGHT)
        de_broglie = ImageMobject("de_Broglie")
        de_broglie.set_height(6)
        de_broglie.next_to(4 * DOWN, DOWN)
        randy.add_updater(
            lambda m: m.next_to(
                rect.get_corner(DOWN + LEFT), UP + RIGHT, MED_LARGE_BUFF
            ).look_at(weights)
        )
        self.add(randy, de_broglie)
        self.wait(2)

        zoom_into_reference_frame()
        self.wait(8)

    def get_peak_flash_anim(self, weight):
        mobject = Mobject()
        mobject.last_y = 0
        mobject.last_dy = 0
        mobject.curr_anim = None
        mobject.curr_anim_time = 0
        mobject.time_since_last_flash = 0

        def update(mob, dt):
            mob.time_since_last_flash += dt
            point = weight.get_center()
            y = point[1]
            mob.dy = y - mob.last_y
            different_dy = np.sign(mob.dy) != np.sign(mob.last_dy)
            if different_dy and mob.time_since_last_flash > 0.5:
                mob.curr_anim = Flash(
                    VectorizedPoint(point),
                    flash_radius=0.5,
                    line_length=0.3,
                    run_time=0.2,
                )
                mob.submobjects = [mob.curr_anim.mobject]
                mob.time_since_last_flash = 0
            mob.last_y = float(y)
            mob.last_dy = float(mob.dy)
            if mob.curr_anim:
                mob.curr_anim_time += dt
                if mob.curr_anim_time > mob.curr_anim.run_time:
                    mob.curr_anim = None
                    mob.submobjects = []
                    mob.curr_anim_time = 0
                    return
                mob.curr_anim.update(mob.curr_anim_time / mob.curr_anim.run_time)

        mobject.add_updater(update)
        return mobject
