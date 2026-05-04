# Source: 3b1b/_2018/eop/chapter1/area_model_expectation.py
# Description: [3b1b translated] 展示期望值公式與機率分佈直方圖的視覺化，並將直方圖轉換為平均值對應的矩形面積模型。


from manim import *
import numpy as np

class IllustrateAreaModelExpectation(Scene):
    def construct(self):
        formula = MathTex("E[X] = \sum_{i=1}^N p_i x_i").move_to(3 * LEFT + UP)
        self.play(Write(formula))

        x_scale = 5.0
        y_scale = 1.0

        probabilities = np.array([1./8, 3./8, 3./8, 1./8])
        prob_strings = ["{1\over 8}", "{3\over 8}", "{3\over 8}", "{1\over 8}"]
        cumulative_probabilities = np.cumsum(probabilities)
        cumulative_probabilities = np.insert(cumulative_probabilities, 0, 0)
        y_values = np.array([0, 1, 2, 3])

        # 注意：ManimCE 沒有內建 Histogram 類別，這裡假設有自定義的 Histogram 類
        # 如果沒有，需要自行實現或使用其他方式繪製直方圖
        hist = Histogram(probabilities, y_values,
            mode="widths",
            x_scale=x_scale,
            y_scale=y_scale,
            x_labels="none"
        )

        flat_hist = Histogram(probabilities, 0 * y_values,
            mode="widths",
            x_scale=x_scale,
            y_scale=y_scale,
            x_labels="none"
        )

        self.play(FadeIn(flat_hist))
        self.play(ReplacementTransform(flat_hist, hist))

        braces = VGroup()
        p_labels = VGroup()
        # add x labels (braces)
        for (p, string, bar) in zip(probabilities, prob_strings, hist.bars):
            brace = Brace(bar, DOWN, buff=0.1)
            p_label = MathTex(string).next_to(brace, DOWN, buff=SMALL_BUFF).scale(0.7)
            group = VGroup(brace, p_label)
            braces.add(brace)
            p_labels.add(p_label)
            
        self.play(
            LaggedStartMap(FadeIn, braces),
            LaggedStartMap(FadeIn, p_labels)
        )

        y_average = np.mean(y_values)
        averaged_y_values = y_average * np.ones(np.shape(y_values))

        averaged_hist = Histogram(probabilities, averaged_y_values,
            mode="widths",
            x_scale=x_scale,
            y_scale=y_scale,
            x_labels="none",
            y_labels="none"
        ).set_opacity(0.8)  # .fade(0.2) 改為 .set_opacity(0.8)

        ghost_hist = hist.copy().set_opacity(0.2)  # .fade(0.8) 改為 .set_opacity(0.2)
        self.add(ghost_hist)  # self.bring_to_back(ghost_hist) 改為 self.add(ghost_hist)

        self.play(Transform(hist, averaged_hist, run_time=3))
        self.wait()

        average_brace = Brace(averaged_hist, RIGHT, buff=0.1)
        average_label = MathTex(str(y_average)).scale(0.7)
        average_label.next_to(average_brace, RIGHT, SMALL_BUFF)
        average_group = VGroup(average_brace, average_label)

        one_brace = Brace(averaged_hist, DOWN, buff=0.1)
        one_p_label = MathTex(str(1)).next_to(one_brace, DOWN, buff=SMALL_BUFF).scale(0.7)
        one_group = VGroup(one_brace, one_p_label)

        self.play(
            FadeIn(average_group),
            Transform(braces, one_brace),
            Transform(p_labels, one_p_label),
        )
        
        rect = SurroundingRectangle(formula, buff=0.5 * MED_LARGE_BUFF)
        self.play(Create(rect))  # ShowCreation 改為 Create
