# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示流體動力學領域的六位重要人物圖像，先以網格排列出現，最後聚焦在最後一位人物上，其他人物淡出並移開。



from manim import *
class FiguresOfFluidDynamics(Scene):
    def construct(self):
        names = [
            "Leonhard Euler",
            "George Stokes",
            "Hermann von Helmholtz",
            "Lewis Richardson",
            "Geoffrey Taylor",
            "Andrey Kolmogorov",
        ]
        images = Group(*[
            ImageMobject(name.replace(" ", "_"), height=3)
            for name in names
        ])
        images.arrange(RIGHT, buff=MED_SMALL_BUFF)
        image_groups = Group()
        for image, name in zip(images, names):
            name_mob = Text(name, font_size=36)  # OldTexText 改為 Text
            name_mob.scale(0.6)
            name_mob.next_to(image, DOWN)
            image_groups.add(Group(image, name_mob))
        image_groups.arrange_in_grid(2, 3)
        image_groups.set_height(config.frame_height - 1)  # FRAME_HEIGHT 改為 config.frame_height

        # FadeInFromDown 改為 FadeIn 配合 shift 參數
        self.play(LaggedStart(
            *[FadeIn(group, shift=DOWN) for group in image_groups],
            lag_ratio=0.5,
            run_time=3
        ))
        self.wait()
        
        to_fade = image_groups[:-1]
        to_fade.generate_target()
        to_fade.target.space_out_submobjects(3)
        to_fade.target.shift(3 * UL)
        to_fade.target.set_opacity(0)  # .fade(1) 改為 .set_opacity(0)
        
        self.play(
            MoveToTarget(to_fade, remover=True),
            image_groups[-1].animate.set_height(5),  # 改為 .animate 語法
            image_groups[-1].animate.center(),  # 改為 .animate 語法
        )
        self.wait()
