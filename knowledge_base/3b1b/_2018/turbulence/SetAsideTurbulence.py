# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個 PiCreature 角色先說「忘記渦環」，然後驚訝地說「看那個湍流！」的對話場景。



from manim import *
class SetAsideTurbulence(PiCreatureScene):
    def construct(self):
        self.pi_creature_says(
            "Forget vortex rings",
            target_mode="speaking"
        )
        self.wait()
        self.pi_creature_says(
            "look at that\\\\ turbulence!",
            target_mode="surprised"
        )
        self.wait()

    def create_pi_creature(self):
        morty = Mortimer()
        morty.to_corner(DR)
        return morty
