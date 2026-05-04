# Source: 3b1b/_2018/eop/chapter1/show_uncertainty_dice.py
# Description: [3b1b translated] 展示一個理想化骰子機率分佈的直方圖，並旋轉後淡入顯示。


from manim import *
import numpy as np

class IdealizedDieHistogram(Scene):
    def construct(self):
        self.probs = 1.0 / 6 * np.ones(6)
        x_scale = 1.3

        y_labels = ["${1\\over 6}$"] * 6

        hist = Histogram(
            np.ones(6),
            self.probs,
            mode="widths",
            x_labels="none",
            y_labels=y_labels,
            y_label_position="center",
            y_scale=20,
            x_scale=x_scale,
        )
        hist.rotate(-TAU / 4)

        for label in hist.y_labels_group:
            label.rotate(TAU / 4)
        hist.remove(hist.y_labels_group)

        self.play(FadeIn(hist))
        self.play(LaggedStartMap(FadeIn, hist.y_labels_group))
