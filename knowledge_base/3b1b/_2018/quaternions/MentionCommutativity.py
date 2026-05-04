# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示教師與學生場景中，說明四元數乘法不可交換性的動畫，包含公式變換與文字轉換。



from manim import *
class MentionCommutativity(TeacherStudentsScene):
    def construct(self):
        kwargs = {
            "tex_to_color_map": {
                "q": MAROON_B,
                "p": YELLOW,
                "i": GREEN,
                "j": RED,
                "k": BLUE,
            }
        }
        general_eq = MathTex("q \\cdot p \\ne p \\cdot q", **kwargs)
        # ManimCE 中沒有 get_part_by_tex，改用索引或直接操作
        # 反轉不等號部分的子物件順序（視覺效果）
        ne_index = general_eq.index_of_part_by_tex("\\ne")
        if ne_index != -1:
            general_eq[ne_index].submobjects.reverse()
        
        ij_eq = MathTex("i \\cdot j = k", **kwargs)
        ji_eq = MathTex("j \\cdot i = -k", **kwargs)

        for mob in [general_eq, ij_eq, ji_eq]:
            mob.move_to(self.hold_up_spot, DOWN)

        words = Text("Multiplication doesn't\ncommute", font_size=36)
        words.next_to(general_eq, UP, buff=MED_LARGE_BUFF)
        words.shift_onto_screen()

        joke = Text("Quaternions work from home", font_size=24)
        joke.to_corner(UL, buff=MED_SMALL_BUFF)

        self.play(
            FadeIn(general_eq, shift=DOWN),
            self.teacher.animate.change("raise_right_hand"),
            self.change_students("erm", "confused", "sassy")
        )
        self.play(FadeIn(words, shift=RIGHT))
        self.wait(2)
        self.play(
            ReplacementTransform(words, joke),
            general_eq.animate.shift(UP),
            FadeIn(ij_eq, shift=DOWN),
            self.change_students(*["pondering"] * 3)
        )
        self.look_at(self.screen)
        self.wait(3)
        self.play(
            FadeIn(ji_eq),
            LaggedStart(
                *[m.animate.shift(UP) for m in [ij_eq, general_eq]],
                lag_ratio=0.8,
            )
        )
        self.look_at(self.screen)
        self.wait(5)
