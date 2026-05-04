# Source: 3b1b/_2019/windmill.py
# Description: [3b1b translated] 展示一個 PiCreature 思考六個問題，每個問題旁邊有一個燈泡發光動畫的場景。



from manim import *
class SpiritOfIMO(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature

        problems = VGroup(*[
            Text(f"P{i})")
            for i in range(1, 7)
        ])
        problems.arrange_in_grid(n_cols=2, buff=LARGE_BUFF)
        problems.scale(1.5)
        problems[3:].shift(1.5 * RIGHT)
        problems.to_corner(UR, buff=LARGE_BUFF)
        problems.shift(2 * LEFT)

        light_bulbs = VGroup()
        lights = VGroup()
        for problem in problems:
            light_bulb = SVGMobject("lightbulb")  # 需要替換為實際的燈泡SVG路徑
            # 如果沒有燈泡SVG，可以用簡單形狀替代
            if not light_bulb.has_points():
                light_bulb = Circle(fill_color=WHITE, fill_opacity=1, stroke_width=0)
                light_bulb.set_height(1)
            else:
                light_bulb.set_height(1)
            light_bulb.next_to(problem, RIGHT)
            light_bulbs.add(light_bulb)

            light = self.get_light(light_bulb.get_center())
            lights.add(light)

        self.play(
            LaggedStartMap(FadeIn, problems, shift=DOWN)
        )
        self.play(
            LaggedStartMap(
                FadeIn, light_bulbs,
                run_time=1,
            ),
            LaggedStartMap(
                lambda l: AnimationGroup(
                    FadeIn(l, target_position=l.get_center()),
                    FadeOut(l, target_position=l.get_center())
                ),
                lights,
                run_time=3
            ),
            randy.animate.change("thinking")
        )
        self.wait()
        self.pi_creature_says(
            "Oh, I've\\\\seen this...",
            target_mode="surprised",
        )
        self.wait(3)

    def get_light(self, point):
        radii = np.arange(0, 5, 0.1)
        result = VGroup(*[
            Annulus(
                inner_radius=r1,
                outer_radius=r2,
                arc_center=point,
                fill_opacity=(1 / (r1 + 1)**2),
                fill_color=YELLOW,
            )
            for r1, r2 in zip(radii[1:], radii[2:])
        ])
        return result
