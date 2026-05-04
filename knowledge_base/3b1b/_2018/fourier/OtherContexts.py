# Source: 3b1b/_2018/fourier.py
# Description: [3b1b translated] 展示一個 PiCreature 角色與一系列文字項目互動，文字項目依序從半透明變為不透明，同時角色做出思考動作。



from manim import *
class OtherContexts(PiCreatureScene):
    def construct(self):
        items = VGroup(*[
            Text("Extracting frequencies from sound"),
            Text("Uncertainty principle"),
            Text("Riemann Zeta function and primes"),
            Text("Differential equations"),
        ])
        items.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        items.to_corner(UL)
        items[1:].set_opacity(0.2)

        morty = self.pi_creature
        morty.to_corner(UR)

        self.add(items)
        for item in items[1:]:
            self.play(
                LaggedStartMap(
                    ApplyMethod, item,
                    lambda m: (m.set_opacity, 1),
                ), 
                morty.animate.change("thinking"),
            )
            self.wait()
