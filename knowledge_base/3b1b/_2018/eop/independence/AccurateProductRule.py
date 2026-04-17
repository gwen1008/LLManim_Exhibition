# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示條件機率乘積規則的視覺化推導，從二維樣本空間逐步劃分到三維立方體表示，最後以困惑的角色表情收尾。


from manim import *
import numpy as np

class AccurateProductRule(Scene):
    def construct(self):
        self.setup_terms()
        self.add_sample_space()
        self.wait()
        self.show_first_division()
        self.show_second_division()
        self.move_to_third_dimension()
        self.show_final_probability()
        self.show_confusion()

    def setup_terms(self):
        filler_tex = "Filler"
        lhs = MathTex("P(", filler_tex, ")", "=")
        p1 = MathTex("P(", filler_tex, ")")
        p2 = MathTex("P(", filler_tex, "|", filler_tex, ")")
        p3 = MathTex("P(", filler_tex, "|", filler_tex, ")")
        terms = VGroup(lhs, p1, p2, p3)
        terms.arrange(RIGHT, buff=SMALL_BUFF)
        terms.to_edge(UP, buff=LARGE_BUFF)

        # 注意：get_slot_group 函數未定義，保留原樣但可能需要額外定義
        kwargs = {"buff": SMALL_BUFF, "include_qs": False}
        slot_group_lists = [
            [get_slot_group([True, True, False], **kwargs)],
            [get_slot_group([True], **kwargs)],
            [
                get_slot_group([True, True], **kwargs),
                get_slot_group([True], **kwargs),
            ],
            [
                get_slot_group([True, True, False], **kwargs),
                get_slot_group([True, True], **kwargs),
            ],
        ]
        for term, slot_group_list in zip(terms, slot_group_lists):
            parts = [part for part in term if isinstance(part, VMobject) and part.get_tex_string() == filler_tex]
            for part, slot_group in zip(parts, slot_group_list):
                slot_group.replace(part, dim_to_match=0)
                # 替換子物件需要手動處理
                idx = term.submobjects.index(part)
                term.submobjects[idx] = slot_group
        
        value_texs = ["0.8", ">0.8", "<0.2"]
        for term, tex in zip(terms[1:], value_texs):
            term.value = MathTex(tex)
            term.value.next_to(term, UP)

        self.terms = terms
        self.add(terms[0])

    def add_sample_space(self):
        # 簡化樣本空間表示為矩形
        self.sample_space = Rectangle(height=4, width=5, stroke_color=WHITE, fill_color=BLUE_E, fill_opacity=0.5)
        self.sample_space.to_edge(DOWN)
        self.add(self.sample_space)

    def show_first_division(self):
        space = self.sample_space
        # 水平分割
        top_part = Rectangle(height=4*0.8, width=5, stroke_color=WHITE, fill_color=GREEN_E, fill_opacity=0.7)
        bottom_part = Rectangle(height=4*0.2, width=5, stroke_color=WHITE, fill_color=RED_E, fill_opacity=0.7)
        top_part.move_to(space.get_top(), DOWN)
        bottom_part.move_to(space.get_bottom(), UP)
        
        space.horizontal_parts = VGroup(top_part, bottom_part)
        space.horizontal_parts.set_opacity(0.9)
        
        top_label = self.terms[1].copy()
        bottom_label = top_label.copy()
        # 簡化 slot_group 替換
        slot_group = get_slot_group([False], buff=SMALL_BUFF, include_qs=False)
        slot_group.replace(bottom_label[1])
        
        # 創建括號和標籤
        top_brace = Brace(top_part, LEFT)
        bottom_brace = Brace(bottom_part, LEFT)
        top_label.next_to(top_brace, LEFT)
        bottom_label.next_to(bottom_brace, LEFT)
        braces_and_labels = VGroup(top_brace, bottom_brace, top_label, bottom_label)

        self.play(
            FadeIn(space.horizontal_parts),
            FadeIn(braces_and_labels)
        )
        self.play(ReplacementTransform(
            top_label.copy(), self.terms[1]
        ))
        self.wait()
        self.play(Write(self.terms[1].value))
        self.wait()

        self.add(braces_and_labels)
        self.top_part = space.horizontal_parts[0]

    def show_second_division(self):
        space = self.sample_space
        top_part = self.top_part
        
        # 垂直分割頂部區域
        left_part = Rectangle(height=top_part.height, width=5*0.9, stroke_color=WHITE, fill_color=GREEN_E, fill_opacity=0.7)
        right_part = Rectangle(height=top_part.height, width=5*0.1, stroke_color=WHITE, fill_color=average_color(GREEN_E, RED_E), fill_opacity=0.7)
        left_part.move_to(top_part.get_left(), RIGHT)
        right_part.move_to(top_part.get_right(), LEFT)
        
        top_part.vertical_parts = VGroup(left_part, right_part)
        
        label = self.terms[2].deepcopy()
        top_brace = Brace(left_part, UP)
        label.next_to(top_brace, UP)
        braces_and_labels = VGroup(top_brace, label)

        self.play(
            FadeIn(top_part.vertical_parts),
            FadeIn(braces_and_labels)
        )
        self.play(ReplacementTransform(
            label.copy(), self.terms[2]
        ))
        self.wait()
        self.play(Write(self.terms[2].value))
        self.wait()

        self.add(braces_and_labels)
        self.top_left_part = top_part.vertical_parts[0]

    def move_to_third_dimension(self):
        space = self.sample_space
        part = self.top_left_part
        
        # 創建立方體
        cube1 = Cube(side_length=1, fill_color=RED_E, fill_opacity=0, stroke_color=WHITE, stroke_width=1)
        cube2 = Cube(side_length=1, fill_color=GREEN_E, fill_opacity=0, stroke_color=WHITE, stroke_width=1)
        cubes = VGroup(cube1, cube2)
        
        # 調整大小和位置
        cubes.stretch_to_fit_width(part.get_width())
        cubes.stretch_to_fit_height(part.get_height())
        cubes[1].move_to(part.get_center())
        cubes[0].stretch(0.2, 2)  # Z軸方向
        cubes[0].move_to(cubes[1].get_edge_center(OUT), IN)
        
        self.add(cubes)

        # 旋轉到3D視角
        self.play(
            space.animate.rotate(0.9*np.pi/2, axis=LEFT),
            space.animate.rotate(np.pi/12, axis=UP),
            space.animate.to_corner(DOWN+RIGHT, buff=LARGE_BUFF)
        )
        self.remove(cubes)
        self.play(
            cubes[0].animate.set_fill(opacity=1),
            cubes[0].animate.set_stroke(color=WHITE, width=1),
            cubes[1].animate.set_fill(opacity=0.5),
            cubes[1].animate.set_stroke(color=WHITE, width=1),
        )
        self.wait()

        self.cubes = cubes

    def show_final_probability(self):
        cube = self.cubes[0]
        # 獲取立方體前面
        face = cube[2]  # 假設這是前面的索引
        points = face.get_vertices()
        line = Line(points[2], points[3])
        line.set_stroke(YELLOW, 8)
        brace = Brace(line, LEFT)
        label = self.terms[3].copy()
        label.next_to(brace, LEFT)

        self.play(
            GrowFromCenter(brace),
            FadeIn(label),
        )
        self.wait()
        self.play(ReplacementTransform(
            label.copy(), self.terms[3]
        ))
        self.wait()

    def show_confusion(self):
        randy = Randolph()
        randy.to_corner(DOWN+LEFT)

        self.play(FadeIn(randy))
        self.play(randy.animate.change("confused", self.terms))
        self.play(randy.animate.look_at(self.cubes))
        self.play(Blink(randy))
        self.play(randy.animate.look_at(self.terms))
        self.wait()

# 輔助函數定義（需要根據原始代碼補充）
def get_slot_group(pattern, buff=SMALL_BUFF, include_qs=False):
    """創建插槽組的簡化版本"""
    # 這裡只是一個佔位符，實際需要根據原始代碼實現
    group = VGroup()
    for val in pattern:
        if val:
            rect = Rectangle(height=0.3, width=0.5, fill_color=GREEN, fill_opacity=0.7, stroke_color=WHITE)
        else:
            rect = Rectangle(height=0.3, width=0.5, fill_color=RED, fill_opacity=0.7, stroke_color=WHITE)
        group.add(rect)
    group.arrange(RIGHT, buff=buff)
    return group

def average_color(color1, color2):
    """計算兩種顏色的平均值"""
    return interpolate_color(color1, color2, 0.5)
