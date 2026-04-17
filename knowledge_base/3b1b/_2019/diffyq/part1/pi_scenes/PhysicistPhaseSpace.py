# Source: 3b1b/_2019/diffyq/part1/pi_scenes.py
# Description: [3b1b translated] 物理學家在相空間圖旁，從生氣表情轉為舉手指向坐標軸標籤的動畫過程。



from manim import *
class PhysicistPhaseSpace(PiCreatureScene):
    def construct(self):
        physy = self.pi_creature
        name = Text("Physicist", font_size=48)  # OldTexText -> Text
        name.scale(1.5)
        name.to_corner(DL, buff=MED_SMALL_BUFF)
        physy.next_to(name, UP, buff=SMALL_BUFF)
        VGroup(name, physy).shift_onto_screen()

        axes = Axes(
            x_range=[-1, 10, 1],
            y_range=[-1, 7, 1],
            axis_config={"stroke_width": 1}
        )
        axes.set_height(6)
        axes.next_to(physy, RIGHT)
        axes.to_edge(UP)
        x_label = Text("Position")
        x_label.next_to(axes.x_axis.get_right(), UP)
        y_label = Text("Momentum")
        y_label.next_to(axes.y_axis.get_top(), RIGHT)

        title = Text("Phase space")
        title.scale(1.5)
        title.set_color(YELLOW)
        title.move_to(axes)

        self.add(name, physy)

        # 動畫序列
        self.play(
            physy.animate.change("angry"),
            Create(axes),  # Write -> Create for axes
            FadeIn(title, shift=DOWN)  # FadeInFromDown -> FadeIn with shift
        )
        self.wait(2)
        self.play(
            GrowFromPoint(x_label, physy.get_corner(UR)),
            physy.animate.change("raise_right_hand"),
        )
        self.play(
            GrowFromPoint(y_label, physy.get_corner(UR)),
            physy.animate.look_at(axes.y_axis.get_top()),  # 修正語法
        )
        self.wait(3)

    def create_pi_creature(self):
        return PiCreature(color=GREY).to_corner(DL)
