# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示一個角色思考時，燈泡上方出現逐漸擴散的同心圓環動畫，象徵靈感湧現。



from manim import *
class Rediscovery(Scene):
    def construct(self):
        randy = Randolph()
        randy.to_edge(DOWN)
        randy.shift(2 * RIGHT)

        lightbulb = Lightbulb()
        lightbulb.set_stroke(width=4)
        lightbulb.scale(1.5)
        lightbulb.next_to(randy, UP)

        rings = self.get_rings(
            lightbulb.get_center(),
            max_radius=10.0,
            delta_r=0.1,
        )

        bubble = ThoughtBubble()
        bubble.pin_to(randy)
        # bubble[-1].set_fill(GREEN_SCREEN, 0.5)
        self.play(
            randy.animate.change("pondering"),
            Create(bubble),
            FadeIn(lightbulb, shift=DOWN),
        )
        self.add(rings, bubble)
        self.play(
            randy.animate.change("thinking"),
            LaggedStartMap(
                VFadeInThenOut,
                rings,
                lag_ratio=0.002,
                run_time=3,
            )
        )
        self.wait(4)

    def get_rings(self, center, max_radius, delta_r):
        radii = np.arange(0, max_radius, delta_r)
        rings = VGroup(*[
            Annulus(
                inner_radius=r1,
                outer_radius=r2,
                fill_opacity=0.75 * (1 - (r1 / max_radius)),
                fill_color=YELLOW
            )
            for r1, r2 in zip(radii, radii[1:])
        ])
        rings.move_to(center)
        return rings
