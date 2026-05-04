# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示一段關於聲音能量損失的幽默文字說明。



from manim import *
class NoteOnEnergyLostToSound(Scene):
    def construct(self):
        self.add(Text(
            "Yeah yeah, the clack sound\n"
            "would require energy, but\n"
            "don't let accuracy get in the\n"
            "way of delight!",
            alignment="",
        ))
