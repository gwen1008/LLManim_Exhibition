# Source: 3b1b/_2019/clacks/solution1.py
# Description: [3b1b translated] 展示相空間概念的視覺化，包括標題、相關領域圖像、狀態與點的對應關係，以及動態與幾何的轉換。



from manim import *
class FinalCommentsOnPhaseSpace(Scene):
    def construct(self):
        self.add_title()
        self.show_related_fields()
        self.state_to_point()
        self.puzzle_as_remnant()

    def add_title(self):
        title = self.title = Text("Phase space")
        title.scale(2)
        title.to_edge(UP)
        title.set_color(YELLOW)

        self.play(Write(title))

    def show_related_fields(self):
        title = self.title

        images = Group(
            ImageMobject("ClacksThumbnail"),
            ImageMobject("PictoralODE"),
            # ImageMobject("DoublePendulumStart"),
            ImageMobject("MobiusStrip"),
        )
        colors = [BLUE_D, GREY_BROWN, BLUE_C]
        for image, color in zip(images, colors):
            image.set_height(2.5)
            image.add(SurroundingRectangle(
                image,
                color=color,
                stroke_width=5,
                buff=0,
            ))
        images.arrange(RIGHT)
        images.move_to(DOWN)

        arrows = VGroup(*[
            Arrow(
                title.get_bottom(), image.get_top(),
                color=WHITE,
            )
            for image in images
        ])

        for image, arrow in zip(images, arrows):
            self.play(
                GrowArrow(arrow),
                GrowFromPoint(image, title.get_bottom()),
            )
            self.wait()
        self.wait()

        self.to_fade = Group(images, arrows)

    def state_to_point(self):
        state = Text("State")
        arrow = Arrow(
            2 * LEFT, 2 * RIGHT,
            color=WHITE,
            stroke_width=10,
            tip_length=0.5
        )
        point = Text("Point")
        dynamics = Text("Dynamics")
        geometry = Text("Geometry")
        words = VGroup(state, point, dynamics, geometry)
        for word in words:
            word.scale(2)

        group = VGroup(state, arrow, point)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        group.move_to(2.5 * DOWN)

        dynamics.move_to(state, RIGHT)
        geometry.move_to(point, LEFT)

        self.play(
            FadeOut(self.to_fade, shift=UP),
            FadeIn(state, shift=UP)
        )
        self.play(
            GrowArrow(arrow),
            FadeIn(point, shift=LEFT)
        )
        self.wait(2)
        for w1, w2 in [(state, dynamics), (point, geometry)]:
            self.play(
                FadeOut(w1, shift=UP),
                FadeIn(w2, shift=DOWN),
            )
            self.wait()
        self.wait()

    def puzzle_as_remnant(self):
        pass
