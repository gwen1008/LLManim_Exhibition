# Source: 3b1b/_2019/diffyq/part3/staging.py
# Description: [3b1b translated] 展示猛獁象體內碳原子隨時間隨機衰減的過程，模擬放射性衰變的視覺效果。



from manim import *
class CarbonDecayingInMammoth(Scene):
    def construct(self):
        mammoth = SVGMobject("Mammoth")
        mammoth.set_color(
            interpolate_color(GREY_BROWN, WHITE, 0.25)
        )
        mammoth.set_height(4)
        body = mammoth[9]

        atoms = VGroup(*[
            self.get_atom(body)
            for n in range(600)
        ])

        p_decay = 0.2

        def update_atoms(group, dt):
            for atom in list(group):  # 創建副本避免迭代時修改
                if np.random.random() < dt * p_decay:
                    group.remove(atom)
            return group
        atoms.add_updater(update_atoms)

        self.add(mammoth)
        self.add(atoms)
        self.wait(20)

    def get_atom(self, body):
        atom = Dot(color=GOLD)
        atom.set_height(0.05)

        dl = body.get_corner(DL)
        ur = body.get_corner(UR)

        wn = 0
        while wn == 0:
            point = np.array([
                interpolate(dl[0], ur[0], np.random.random()),
                interpolate(dl[1], ur[1], np.random.random()),
                0
            ])
            # ManimCE 中沒有 get_winding_number，用簡單的邊界檢查替代
            # 假設 body 是凸多邊形，檢查點是否在邊界框內
            if (dl[0] <= point[0] <= ur[0] and 
                dl[1] <= point[1] <= ur[1]):
                wn = 1
            else:
                wn = 0

        atom.move_to(point)
        return atom
