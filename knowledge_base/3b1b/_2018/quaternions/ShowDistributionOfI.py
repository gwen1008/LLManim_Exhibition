# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數乘法分配律的推導過程，教師與學生場景中，將 q 乘以 (w1 + xi + yj + zk) 展開為各項之和，並用顏色區分變數。



from manim import *
class ShowDistributionOfI(TeacherStudentsScene):
    def construct(self):
        tex_to_color_map = {
            "q": PINK,
            "w": YELLOW,
            "x": GREEN,
            "y": RED,
            "z": BLUE,
        }
        top_product = MathTex(
            "q", "\\cdot", "\\left(",
            "w", "1", "+", "x", "i", "+", "y", "j", "+", "z", "k",
            "\\right)"
        )
        top_product.to_edge(UP)
        self.add(top_product)
        bottom_product = MathTex(
            "w", "q", "\\cdot", "1",
            "+", "x", "q", "\\cdot", "i",
            "+", "y", "q", "\\cdot", "j",
            "+", "z", "q", "\\cdot", "k",
        )
        bottom_product.next_to(top_product, DOWN, buff=MED_LARGE_BUFF)

        for product in [top_product, bottom_product]:
            for tex, color in tex_to_color_map.items():
                product.set_color_by_tex(tex, color)

        self.student_says(
            "What does it do \\\\ to other quaternions?",
            target_mode="raise_left_hand"
        )
        self.play_student_changes(
            "pondering", "raise_left_hand", "erm",
            look_at=top_product,
        )
        self.wait(2)
        self.play(
            self.teacher.animate.change("raise_right_hand"),
            RemovePiCreatureBubble(self.students[1], target_mode="pondering"),
            *[
                TransformFromCopy(
                    top_product.get_parts_by_tex(tex),
                    bottom_product.get_parts_by_tex(tex),
                    run_time=2
                )
                for tex in ["1", "w", "x", "i", "y", "j", "z", "k", "+"]
            ]
        )
        self.play(*[
            TransformFromCopy(
                top_product.get_parts_by_tex(tex),
                bottom_product.get_parts_by_tex(tex),
                run_time=2
            )
            for tex in ["q", "\\cdot"]
        ])
        self.play_all_student_changes("thinking")
        self.wait(3)
