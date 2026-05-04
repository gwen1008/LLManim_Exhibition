# Source: 3b1b/_2019/spirals.py
# Description: [3b1b translated] 展示從「每個（互質）剩餘類在質數中密度相等」到「每個（互質）剩餘類有無限多個質數」的轉換動畫，並帶有交叉標記和顏色強調。



from manim import *
class MoreModestDirichlet(Scene):
    def construct(self):
        ed = TexText(
            "Each (coprime) residue class ",
            "is equally dense with ",
            "primes."
        )
        inf = TexText(
            "Each (coprime) residue class ",
            "has infinitely many ",
            "primes."
        )
        ed[1].set_color(BLUE)
        inf[1].set_color(GREEN)

        for mob in [*ed, *inf]:
            mob.save_state()

        cross = Cross(ed[1])
        c_group = VGroup(ed[1], cross)

        self.add(ed)
        self.wait()
        self.play(Create(cross))
        self.play(
            c_group.animate.shift(DOWN),
            c_group.animate.set_opacity(0.5),
            ReplacementTransform(ed[::2], inf[::2]),
            FadeIn(inf[1])
        )
        self.wait()
        self.remove(*inf)
        self.play(
            inf[1].animate.shift(UP),
            Restore(ed[0]),
            Restore(ed[1]),
            Restore(ed[2]),
            FadeOut(cross),
        )
        self.wait()
