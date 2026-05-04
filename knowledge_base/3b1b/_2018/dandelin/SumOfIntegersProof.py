# Source: 3b1b/_2018/dandelin.py
# Description: [3b1b translated] 展示用幾何排列證明前 n 個正整數和公式的視覺化過程。



from manim import *
class SumOfIntegersProof(Scene):
    def __init__(self, n=6, **kwargs):
        super().__init__(**kwargs)
        self.n = n

    def construct(self):
        equation = MathTex(
            "1", "+", "2", "+", "3", "+",
            "\\cdots", "+", "n",
            "=", "\\frac{n(n+1)}{2}"
        )
        equation.scale(1.5)
        equation.to_edge(UP)
        
        # 提取數字部分
        one, two, three, dots, n = numbers = VGroup(*[
            equation.get_part_by_tex(tex, substring=False).copy()
            for tex in ("1", "2", "3", "\\cdots", "n",)
        ])
        
        # 創建目標位置
        for number in numbers:
            number.generate_target()
            number.target.scale(0.75)

        rows = self.get_rows()
        rows.next_to(equation, DOWN, buff=MED_LARGE_BUFF)
        flipped_rows = self.get_flipped_rows(rows)

        # 設置數字目標位置
        for row, num in zip(rows, [one, two, three]):
            num.target.next_to(row, LEFT)
        dots.target.rotate(90 * DEGREES)
        dots.target.next_to(rows[3:-1], LEFT)
        dots.target.align_to(one.target, LEFT)
        n.target.next_to(rows[-1], LEFT)

        # 準備行動畫狀態
        for row in rows:
            row.save_state()
            for square in row:
                square.stretch(0, 0)
                square.move_to(row, LEFT)
            row.set_opacity(0)

        # 動畫序列
        self.play(LaggedStartMap(
            lambda mob: FadeIn(mob, shift=DOWN), 
            equation[:-1]
        ))
        self.wait()
        
        self.play(
            LaggedStartMap(
                MoveToTarget, numbers,
                path_arc=-90 * DEGREES,
                lag_ratio=1,
                run_time=1
            )
        )
        self.play(LaggedStartMap(Restore, rows))
        self.wait()
        
        self.play(
            ReplacementTransform(
                rows.copy().set_fill(opacity=0), 
                flipped_rows,
                path_arc=-PI,
                run_time=2
            )
        )
        self.wait()
        self.play(Write(equation[-1]))
        self.wait(5)

    def get_rows(self):
        rows = VGroup()
        for count in range(1, self.n + 1):
            row = VGroup(*[Square() for k in range(count)])
            row.arrange(RIGHT, buff=0)
            rows.add(row)
        rows.arrange(DOWN, buff=0, aligned_edge=LEFT)
        rows.set_height(5)
        rows.set_stroke(WHITE, 3)
        rows.set_fill(BLUE, 0.5)
        return rows

    def get_flipped_rows(self, rows):
        result = rows.copy()
        result.rotate(PI)
        result.set_fill(RED_D, 0.5)
        result.move_to(rows, LEFT)
        result.shift(rows[0][0].get_width() * RIGHT)
        return result
