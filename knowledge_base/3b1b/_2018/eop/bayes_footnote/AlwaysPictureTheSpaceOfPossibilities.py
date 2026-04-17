# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示一個 PiCreature 角色在思考，並帶有一個大型的思考泡泡。



from manim import *
class AlwaysPictureTheSpaceOfPossibilities(PiCreatureScene):
    def construct(self):
        self.pi_creature_thinks(
            "",
            bubble_config={
                "height": 4.5,
                "width": 8,
            }
        )
        self.wait(3)

    def create_pi_creature(self):
        return Randolph().to_corner(DOWN + LEFT)
