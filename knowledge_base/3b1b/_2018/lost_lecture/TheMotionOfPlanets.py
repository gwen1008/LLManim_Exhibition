# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示太陽系行星繞橢圓軌道運行的動畫，並在後半段加入書籍封面與人物介紹。


from manim import *
import numpy as np

class TheMotionOfPlanets(Scene):
    def __init__(self, camera_config={"background_opacity": 1}, random_seed=2, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)
        self.random_seed = random_seed

    def construct(self):
        self.add_title()
        self.setup_orbits()

    def add_title(self):
        title = Text("``The motion of planets around the sun''", color=YELLOW)
        title.to_edge(UP)
        title.add_to_back(title.copy().set_stroke(BLACK, 5))
        self.add(title)
        self.title = title

    def setup_orbits(self):
        # 注意：ImageMobject 在 ManimCE 中改為 Image
        sun = ImageMobject("sun") if hasattr(self, 'ImageMobject') else Image("sun.png")
        sun.set_height(0.7)
        planets, ellipses, orbits = self.get_planets_ellipses_and_orbits(sun)

        archivist_words = Text("Judith Goodstein (Caltech archivist)")
        archivist_words.to_corner(UL)
        archivist_words.shift(1.5 * DOWN)
        archivist_words.add_background_rectangle()
        alt_name = Text("David Goodstein (Caltech physicist)")
        alt_name.next_to(archivist_words, DOWN, aligned_edge=LEFT)
        alt_name.add_background_rectangle()

        book = ImageMobject("Lost_Lecture_cover") if hasattr(self, 'ImageMobject') else Image("Lost_Lecture_cover.png")
        book.set_height(4)
        book.next_to(alt_name, DOWN)

        self.add(SunAnimation(sun))
        self.add(ellipses, planets)
        self.add(self.title)
        self.add(*orbits)
        self.add_foreground_mobjects(planets)
        self.wait(10)
        self.play(
            VGroup(ellipses, sun).animate.shift(3 * RIGHT),
            FadeIn(archivist_words, shift=DOWN),
            Animation(self.title)
        )
        self.add_foreground_mobjects(archivist_words)
        self.wait(3)
        self.play(FadeIn(alt_name, shift=DOWN))
        self.add_foreground_mobjects(alt_name)
        self.wait()
        self.play(FadeIn(book, shift=DOWN))
        self.wait(15)

    def get_planets_ellipses_and_orbits(self, sun):
        # 注意：ImageMobject 在 ManimCE 中改為 Image
        planets = VGroup(
            ImageMobject("mercury") if hasattr(self, 'ImageMobject') else Image("mercury.png"),
            ImageMobject("venus") if hasattr(self, 'ImageMobject') else Image("venus.png"),
            ImageMobject("earth") if hasattr(self, 'ImageMobject') else Image("earth.png"),
            ImageMobject("mars") if hasattr(self, 'ImageMobject') else Image("mars.png"),
            ImageMobject("comet") if hasattr(self, 'ImageMobject') else Image("comet.png")
        )
        sizes = [0.383, 0.95, 1.0, 0.532, 0.3]
        orbit_radii = [0.254, 0.475, 0.656, 1.0, 3.0]
        orbit_eccentricies = [0.206, 0.006, 0.0167, 0.0934, 0.967]

        for planet, size in zip(planets, sizes):
            planet.set_height(0.5)
            planet.scale(size)

        ellipses = VGroup(*[
            Circle(radius=r, color=WHITE, stroke_width=1)
            for r in orbit_radii
        ])
        for circle, ec in zip(ellipses, orbit_eccentricies):
            a = circle.get_height() / 2
            c = ec * a
            b = np.sqrt(a**2 - c**2)
            circle.stretch(b / a, 1)
            c = np.sqrt(a**2 - b**2)
            circle.shift(c * RIGHT)
        for circle in ellipses:
            circle.rotate(
                TAU * np.random.random(),
                about_point=ORIGIN
            )

        ellipses.scale(3.5, about_point=ORIGIN)

        orbits = [
            Orbiting(
                planet, sun, circle,
                rate=0.25 * r**(2 / 3)
            )
            for planet, circle, r in zip(planets, ellipses, orbit_radii)
        ]
        orbits[-1].proportion = 0.15
        orbits[-1].rate = 0.5

        return planets, ellipses, orbits
