# Source: 3b1b/_2019/diffyq/part1/staging.py
# Description: [3b1b translated] 展示從常微分方程到向量場的轉換，上方顯示向量微分方程，下方用黃色箭頭指示轉換方向。



from manim import *
class FromODEToVectorField(Scene):
    def construct(self):
        matrix_config = {
            "bracket_v_buff": 2 * SMALL_BUFF,
            "element_to_mobject_config": {
                "tex_to_color_map": {
                    "x": GREEN,
                    "y": RED,
                    "z": BLUE,
                },
            }
        }
        
        # 定義向量符號函數（如果不存在則創建一個簡單版本）
        def get_vector_symbol(*entries, **config):
            # 簡化實現：創建一個包含條目的矩陣
            element_config = config.get("element_to_mobject_config", {})
            bracket_v_buff = config.get("bracket_v_buff", SMALL_BUFF)
            
            entries_mob = VGroup(*[
                MathTex(entry, **element_config) for entry in entries
            ])
            entries_mob.arrange(DOWN, buff=0.3)
            
            # 添加括號
            bracket = Matrix(
                [[entry] for entry in entries],
                left_bracket="\\begin{pmatrix}",
                right_bracket="\\end{pmatrix}",
                bracket_v_buff=bracket_v_buff,
                element_to_mobject_config=element_config
            )
            return bracket
        
        vect = get_vector_symbol(
            "x(t)", "y(t)", "z(t)",
            **matrix_config,
        )
        d_vect = get_vector_symbol(
            "\\sigma\\big(y(t) - x(t)\\big)",
            "x(t)\\big(\\rho - z(t)\\big) - y(t)",
            "x(t)y(t) - \\beta z(t)",
            **matrix_config
        )
        
        equation = VGroup(
            MathTex("d \\over dt").scale(1.5),
            vect,
            MathTex("="),
            d_vect
        )
        equation.scale(0.8)
        equation.arrange(RIGHT)
        equation.to_edge(UP)

        arrow = Arrow(DOWN, color=YELLOW)
        arrow.next_to(equation, DOWN)

        self.add(equation)
        self.play(Create(arrow))
        self.wait()
