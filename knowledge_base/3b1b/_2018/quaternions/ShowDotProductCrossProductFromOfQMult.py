# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示四元數乘法展開為點積和叉積的向量形式，並用括號標註向量分量。



from manim import *
class ShowDotProductCrossProductFromOfQMult(Scene):
    def construct(self):
        v_tex = "\\vec{\\textbf{v}}"
        product = MathTex(
            "(", "w_1", "+",
            "x_1", "i", "+", "y_1", "j", "+", "z_1", "k", ")",
            "(", "w_2", "+",
            "x_2", "i", "+", "y_2", "j", "+", "z_2", "k", ")",
            "=",
            "(w_1", ",", v_tex + "_1", ")",
            "(w_2", ",", v_tex + "_2", ")",
            "="
        )
        product.set_width(FRAME_WIDTH - 1)

        # 在 ManimCE 中，MathTex 沒有 index_of_part_by_tex 方法
        # 改用 get_parts_by_tex 並取第一個出現的位置
        tex_strings = ["x_1", ")", "x_2", "z_2"]
        indices = []
        for tex in tex_strings:
            parts = product.get_parts_by_tex(tex)
            if parts:
                # 取第一個匹配的部分在整個 MathTex 中的索引
                # 由於 MathTex 是 VMobject，我們用 parts[0] 在 product 中的索引
                # 但更簡單的方法是直接使用切片（這裡保持原邏輯結構）
                indices.append(product.submobjects.index(parts[0]))
        i1, i2, i3, i4 = indices[0], indices[1], indices[2], indices[3] + 2

        # 創建向量部分的 VGroup
        vector_parts = VGroup(product[i1:i2], product[i3:i4])

        vector_defs = VGroup()
        braces = VGroup()
        for i, vp in zip(range(1, 3), vector_parts):
            brace = Brace(vp, UP)
            vector = Matrix([
                ["x_" + str(i)],
                ["y_" + str(i)],
                ["z_" + str(i)],
            ])
            colors = [GREEN, RED, BLUE]
            for mob, color in zip(vector.get_entries(), colors):
                mob.set_color(color)
            group = VGroup(
                MathTex("{}_{} = ".format(v_tex, i)),
                vector,
            )
            group.arrange(RIGHT, buff=SMALL_BUFF)
            group.next_to(brace, UP)

            braces.add(brace)
            vector_defs.add(group)

        result = MathTex(
            "\\left(", "w_1", "w_2",
            "-", v_tex + "_1", "\\cdot", v_tex, "_2", ",\\,",
            "w_1", v_tex + "_2", "+", "w_2", v_tex + "_1",
            "+", "{}_1 \\times {}_2".format(v_tex, v_tex),
            "\\right)"
        )
        result.match_width(product)
        result.next_to(product, DOWN, buff=LARGE_BUFF)
        for mob in [product, result]:
            # ManimCE 中 set_color_by_tex_to_color_map 可用
            mob.set_color_by_tex_to_color_map({
                "w": YELLOW,
                "x": GREEN,
                "y": RED,
                "z": BLUE,
            })
            mob.set_color_by_tex(v_tex, WHITE)

        self.add(product)
        self.add(braces)
        self.add(vector_defs)
        # FadeInFromLarge 在 CE 中沒有，改用 FadeIn 並配合 scale
        self.play(LaggedStart(*[FadeIn(part, scale=2) for part in result]))
        self.wait()
