# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示網路廣告中對齊與不對齊的兩種情況，並以滑塊和圖示說明理想狀態。



from manim import *
class ThoughtsOnAds(Scene):
    def construct(self):
        title = Title(
            "Internet advertising",
            match_underline_width_to_text=True,
            underline_buff=SMALL_BUFF,
        )

        line = NumberLine(
            color=GREY_B,
            x_range=[0, 12, 1],
            length=12,
            include_numbers=False,
        )
        line.move_to(DOWN)

        arrows = VGroup(Arrow(LEFT, ORIGIN).scale(2), Arrow(ORIGIN, RIGHT).scale(2))
        arrows.arrange(RIGHT, buff=2)
        arrows.next_to(line, DOWN)

        misaligned = Text("Misaligned")
        misaligned.next_to(arrows[0], DOWN)
        aligned = Text("Well-aligned")
        aligned.next_to(arrows[1], DOWN)

        VGroup(arrows[0], misaligned).set_color(RED)
        VGroup(arrows[1], aligned).set_color(BLUE)

        left_text = Text(
            "Any website presented\n"
            "as a click-maximizing\nslideshow",
            font_size=24
        )
        left_text.next_to(line, UP, buff=MED_LARGE_BUFF)
        left_text.to_edge(LEFT)

        viewer, brand, creator = vcb = VGroup(
            Text("viewer"),
            Text("brand"),
            Text("creator")
        )
        brand.next_to(creator, LEFT, LARGE_BUFF)
        viewer.next_to(vcb[1:], UP, LARGE_BUFF)
        arrow_config = {
            "path_arc": 60 * DEGREES,
            "tip_length": 0.15,
        }
        vcb_arrows = VGroup(*[
            VGroup(
                Arrow(p1, p2, **arrow_config),
                Arrow(p2, p1, **arrow_config),
            )
            for p1, p2 in [
                (creator.get_left(), brand.get_right()),
                (brand.get_top(), viewer.get_bottom()),
                (viewer.get_bottom(), creator.get_top()),
            ]
        ])
        vcb_arrows.set_stroke(width=2)
        vcb_arrows.set_color(BLUE)
        vcb_group = VGroup(vcb, vcb_arrows)
        vcb_group.next_to(line, UP, buff=MED_LARGE_BUFF)
        vcb_group.to_edge(RIGHT)

        knob = Triangle(start_angle=-90 * DEGREES)
        knob.set_height(0.25)
        knob.set_stroke(width=0)
        knob.set_fill(YELLOW, 1)
        knob.move_to(line.get_left() + DOWN * line.get_height() / 2)

        right_rect = Rectangle(
            width=3,
            height=0.25,
            stroke_color=WHITE,
            stroke_width=2,
            fill_color=BLUE,
            fill_opacity=0.5
        )
        right_rect.move_to(line.get_right() + RIGHT * right_rect.width / 2)
        right_rect_label = Group(
            # 註: ImageMobject 在 ManimCE 中改為 Image，但需要實際圖片檔案
            # 這裡用替代的 Text 表示
            Text("3b1b", font_size=24),
            Text("(hopefully)", font_size=20)
        )
        right_rect_label.arrange(DOWN, buff=SMALL_BUFF)
        right_rect_label.next_to(
            right_rect, UP, SMALL_BUFF
        )

        self.add(title)
        self.play(Create(line))
        self.play(
            Write(misaligned),
            Write(aligned),
            *[GrowArrow(arrow) for arrow in arrows],
            run_time=1
        )

        self.play(
            FadeIn(left_text),
            FadeIn(knob, shift=2 * RIGHT)
        )
        self.wait()
        self.play(
            LaggedStart(*[FadeIn(obj, shift=DOWN) for obj in vcb]),
            LaggedStart(*[Create(arrow) for arrow in vcb_arrows]),
            knob.animate.move_to(line.get_right() + DOWN * line.get_height() / 2),
            run_time=2
        )
        self.wait(2)
        self.play(vcb_group.animate.shift(2 * UP))
        self.play(
            Create(right_rect),
            FadeIn(right_rect_label),
        )
        self.wait()
