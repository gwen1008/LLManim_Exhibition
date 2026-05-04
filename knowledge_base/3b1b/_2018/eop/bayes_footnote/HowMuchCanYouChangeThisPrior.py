# Source: 3b1b/_2018/eop/bayes_footnote.py
# Description: [3b1b translated] 展示從一群角色中選出一個特殊角色，並將其與其他分組隔離的過程。


from manim import *
import itertools as it

class HowMuchCanYouChangeThisPrior(Scene):
    def construct(self):
        self.create_pi_creatures()
        self.single_out_new_sick_one()
        self.show_subgroups()
        self.isolate_special_group()

    def create_pi_creatures(self):
        # 創建所有角色
        creatures = self.get_all_creatures()
        creatures.set_height(6.5)
        creatures.center()
        # 展平子物件列表
        creatures.submobjects = list(it.chain(*creatures))

        self.add(creatures)
        self.sick_one = creatures.sick_one
        self.pi_creatures = creatures
        return creatures

    def single_out_new_sick_one(self):
        creatures = self.pi_creatures
        sick_one = self.sick_one
        new_sick_one = sick_one.copy()
        new_sick_one.shift(1.3*sick_one.get_width()*RIGHT)
        sick_one.change_mode("plain")
        sick_one.set_color(BLUE_E)

        self.add(new_sick_one)
        self.sick_one = new_sick_one

    def show_subgroups(self):
        # 創建子分組
        subgroups = VGroup(*[
            VGroup(*it.chain(
                self.pi_creatures[i:i+5],
                self.pi_creatures[i+25:i+25+5]
            ))
            for i in range(0, 1000)
            if i%5 == 0 and (i//25)%2 == 0
        ])
        special_group = subgroups[-5]
        special_group.add(self.sick_one)
        
        # 創建目標位置
        subgroups.generate_target()
        width_factor = config.frame_width/subgroups.get_width()
        height_factor = config.frame_height/subgroups.get_height()
        subgroups.target.stretch(width_factor, 0)
        subgroups.target.stretch(height_factor, 1)
        for subgroup in subgroups.target:
            subgroup.stretch(1./width_factor, 0)
            subgroup.stretch(1./height_factor, 1)

        self.wait()
        self.play(MoveToTarget(subgroups))
        subgroups.remove(special_group)

        # 為每個子分組添加邊框
        rects = VGroup(*[
            SurroundingRectangle(
                group, buff=0, color=GREEN
            )
            for group in subgroups
        ])
        special_rect = SurroundingRectangle(
            special_group, buff=0, color=RED
        )
        self.play(FadeIn(rects), FadeIn(special_rect))
        self.wait()

        self.to_fade = VGroup(subgroups, rects)
        self.special_group = special_group
        self.special_rect = special_rect

    def isolate_special_group(self):
        to_fade, special_group = self.to_fade, self.special_group
        self.play(FadeOut(to_fade))
        self.play(
            FadeOut(self.special_rect),
            special_group.animate.set_height(6).center()
        )
        self.wait()

    # 輔助方法：獲取所有角色（需要根據實際情況實現）
    def get_all_creatures(self):
        # 這裡需要根據實際情況實現創建角色的邏輯
        # 暫時返回一個空的VGroup作為佔位
        return VGroup()
