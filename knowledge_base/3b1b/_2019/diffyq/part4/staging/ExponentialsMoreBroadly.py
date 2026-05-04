# Source: 3b1b/_2019/diffyq/part4/staging.py
# Description: [3b1b translated] 展示傅立葉級數公式，從中提取複數指數項並可視化為旋轉的點，最後轉換為矩陣指數形式並結合向量場動畫。



from manim import *
class ExponentialsMoreBroadly(Scene):
    def construct(self):
        self.write_fourier_series()
        self.pull_out_complex_exponent()
        self.show_matrix_exponent()

    def write_fourier_series(self):
        formula = MathTex(
            "f({t}) = "
            "\\sum_{n = -\\infty}^\\infty",
            "c_{n}", "e^{{n} \\cdot 2\\pi i {t}}"
            "",
            tex_to_color_map={
                "{t}": LIGHT_PINK,
                "{n}": YELLOW
            }
        )
        formula[2][4].set_color(YELLOW)
        formula.scale(1.5)
        formula.to_edge(UP)
        # 添加背景矩形
        for submob in formula.submobjects:
            submob.add_background_rectangle()

        plane = ComplexPlane(
            axis_config={"unit_size": 2}
        )

        self.play(FadeIn(formula, shift=DOWN))
        self.wait()
        self.add(plane, formula)
        self.play(
            formula.animate.scale(0.7).to_corner(UL),
            Create(plane)
        )

        self.formula = formula
        self.plane = plane

    def pull_out_complex_exponent(self):
        formula = self.formula

        c_exp = MathTex("e^{it}")
        c_exp[0][2].set_color(LIGHT_PINK)
        c_exp.set_stroke(BLACK, 3, background=True)
        # 找到公式中 e^ 的位置
        for part in formula:
            if "e^" in part.tex_string:
                c_exp.move_to(part.get_corner(DL))
                break
        c_exp.set_opacity(0)

        dot = Dot()
        circle = Circle(radius=2)
        circle.set_color(YELLOW)
        dot.add_updater(lambda d: d.move_to(circle.get_end()))

        self.play(
            c_exp.animate.set_opacity(1).scale(1.5).next_to(dot, UR, buff=SMALL_BUFF),
            GrowFromCenter(dot),
        )
        c_exp.add_updater(
            lambda m: m.next_to(dot, UR, buff=SMALL_BUFF)
        )
        self.play(
            Create(circle),
            run_time=4,
        )
        self.wait()

        self.c_exp = c_exp
        self.circle = circle
        self.dot = dot

    def show_matrix_exponent(self):
        c_exp = self.c_exp
        formula = self.formula
        circle = self.circle
        dot = self.dot

        m_exp = MathTex(
            "\\text{exp}\\left("
            "\\left[ \\begin{array}{cc}0 & -1 \\\\ 1 & 0 \\end{array} \\right]",
            "{t} \\right)",
            "=",
            "\\left[ \\begin{array}{cc}"
            "\\cos(t) & -\\sin(t) \\\\ \\sin(t) & \\cos(t)"
            "\\end{array} \\right]",
        )
        # 設置粉色部分
        pink_indices = [1, 5, 12, 18, 24]
        for idx in pink_indices:
            if idx < len(m_exp[0]):
                m_exp[0][idx].set_color(LIGHT_PINK)
        m_exp.to_corner(UL)
        # 添加背景矩形
        for submob in m_exp.submobjects:
            submob.add_background_rectangle()

        # 創建向量場（簡化版本）
        vector_field = VGroup()
        for x in np.arange(-7, 7, 0.5):
            for y in np.arange(-4, 4, 0.5):
                point = np.array([x, y, 0])
                # 旋轉向量 90 度
                rotated = np.array([-y, x, 0])
                norm = np.linalg.norm(rotated[:2])
                if norm > 0:
                    length = 0.35 * (1 / (1 + np.exp(-norm)))
                    vector = Arrow(
                        start=point,
                        end=point + length * rotated / norm,
                        buff=0,
                        max_tip_length_to_length_ratio=0.15,
                        stroke_width=2
                    )
                    vector_field.add(vector)

        self.play(
            FadeIn(m_exp, shift=DOWN),
            FadeOut(formula, shift=UP),
            FadeOut(c_exp)
        )
        self.add(vector_field, circle, dot, m_exp)
        self.play(
            Create(vector_field, lag_ratio=0.001),
        )
        self.play(Rotate(circle, angle=TAU, run_time=TAU))
        self.wait()
