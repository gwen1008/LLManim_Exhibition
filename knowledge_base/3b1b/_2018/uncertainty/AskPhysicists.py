# Source: 3b1b/_2018/uncertainty.py
# Description: [3b1b translated] 展示一個物理公式和三個 PiCreature 角色討論物理原理的對話場景。



from manim import *
class AskPhysicists(PiCreatureScene):
    def construct(self):
        morty, physy1, physy2, physy3 = self.pi_creatures
        formula = MathTex("p", "=", "h", "\\xi")
        formula.set_color_by_tex_to_color_map({
            "p": BLUE,
            "\\xi": YELLOW,
        })
        formula.scale(1.5)

        formula.to_edge(UP)
        formula.save_state()
        formula.shift(DOWN)
        formula.set_opacity(0)
        self.play(Restore(formula))
        self.pi_creature_says(
            morty, "So...why?",
            target_mode="maybe"
        )
        self.wait(2)
        self.play(
            FadeOut(morty.bubble, shift=DOWN),
            FadeOut(morty.bubble.content, shift=DOWN),
            PiCreatureSays(
                physy2,
                "Take the Schrödinger equation \\\\ with $H = \\frac{p^2}{2m}+V(x)$",
                bubble_config={"fill_opacity": 0.9},
            ),
        )
        self.play(
            PiCreatureSays(
                physy1,
                "Even classically position and \\\\ momentum are conjugate",
                target_mode="surprised",
                bubble_config={"fill_opacity": 0.9},
            ),
        )
        self.play(
            PiCreatureSays(
                physy3,
                "Consider special relativity \\\\ together with $E = hf$",
                target_mode="hooray",
                bubble_config={"fill_opacity": 0.9},
            ),
            morty.animate.change("guilty")
        )
        self.wait(2)

    def create_pi_creatures(self):
        scale_factor = 0.85
        morty = Mortimer().flip()
        morty.scale(scale_factor)
        morty.to_corner(DOWN + LEFT)

        physies = VGroup(*[
            PiCreature(color=c).flip()
            for c in (GREY, GREY_B, GREY_D)
        ])
        physies.arrange(RIGHT, buff=MED_SMALL_BUFF)
        physies.scale(scale_factor)
        physies.to_corner(DOWN + RIGHT)

        self.add(physies)
        return VGroup(morty, *physies)
