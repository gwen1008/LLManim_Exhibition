# Source: 3b1b/_2018/eop/chapter1/million_flips.py
# Description: [3b1b translated] 展示一百萬次硬幣投擲的模擬過程，從單個硬幣動畫逐步聚合到百個、萬個硬幣的統計方塊，並同步更新投擲次數和正面次數的計數器。


from manim import *
import random
import numpy as np

class MillionFlips(Scene):
    def construct(self):
        title = Tex("1{,}000{,}000 flips")
        title.to_edge(UP)
        self.add(title)

        small_wait_time = 1.0 / 15  # Um...

        n_flips_label = Tex("\\# Flips: ")
        n_heads_label = Tex("\\# Heads: ")
        n_flips_count = Integer(0)
        n_heads_count = Integer(0)
        n_heads_label.to_edge(RIGHT, buff=2 * LARGE_BUFF)
        n_flips_label.next_to(n_heads_label, DOWN, aligned_edge=LEFT)
        n_flips_count.next_to(n_flips_label[-1], RIGHT)
        n_heads_count.next_to(n_heads_label[-1], RIGHT)
        VGroup(n_flips_count, n_heads_count).shift(0.5 * SMALL_BUFF * UP)
        self.add(n_flips_label, n_heads_label, n_flips_count, n_heads_count)

        # 假設 FlatHeads 和 FlatTails 是自定義的硬幣圖形
        # 這裡用簡單的圓形替代，並用顏色區分
        COLOR_HEADS = YELLOW
        COLOR_TAILS = BLUE
        
        coins = VGroup(*[
            Circle(radius=0.2, color=COLOR_HEADS, fill_opacity=1) if random.random() < 0.5 
            else Circle(radius=0.2, color=COLOR_TAILS, fill_opacity=1)
            for x in range(100)
        ])
        self.organize_group(coins)

        proportions = np.random.normal(0.5, 0.5 * 0.1, 100)
        hundred_boxes = VGroup(*[
            Square(
                side_length=0.5,
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=1,
                fill_color=interpolate_color(COLOR_HEADS, COLOR_TAILS, prop)
            )
            for prop in proportions
        ])
        self.organize_group(hundred_boxes)

        ten_k_proportions = np.random.normal(0.5, 0.5 * 0.01, 100)
        ten_k_boxes = VGroup(*[
            Square(
                side_length=0.5,
                stroke_width=1,
                stroke_color=WHITE,
                fill_opacity=1,
                fill_color=interpolate_color(COLOR_HEADS, COLOR_TAILS, prop)
            )
            for prop in ten_k_proportions
        ])
        self.organize_group(ten_k_boxes)

        # Animations
        for coin in coins:
            self.add(coin)
            self.increment(n_flips_count)
            if coin.color == COLOR_HEADS:
                self.increment(n_heads_count)
            self.wait(small_wait_time)

        self.play(
            FadeIn(hundred_boxes[0]),
            coins.animate.set_stroke(width=0),
            coins.animate.replace(hundred_boxes[0])
        )
        hundred_boxes[0].add(coins)
        for box, prop in list(zip(hundred_boxes, proportions))[1:]:
            self.add(box)
            self.increment(n_flips_count, 100)
            self.increment(n_heads_count, int(np.round(prop * 100)))
            self.wait(small_wait_time)

        self.play(
            FadeIn(ten_k_boxes[0]),
            hundred_boxes.animate.set_stroke(width=0),
            hundred_boxes.animate.replace(ten_k_boxes[0])
        )
        ten_k_boxes[0].add(hundred_boxes)
        for box, prop in list(zip(ten_k_boxes, ten_k_proportions))[1:]:
            self.add(box)
            self.increment(n_flips_count, 10000)
            self.increment(n_heads_count, int(np.round(prop * 10000)))
            self.wait(small_wait_time)
        self.wait()

    def organize_group(self, group):
        group.arrange_in_grid(rows=10, cols=10, buff=0.1)
        group.set_height(5)
        group.shift(DOWN + 2 * LEFT)

    def increment(self, integer_mob, value=1):
        new_int = Integer(integer_mob.number + value)
        new_int.move_to(integer_mob, DL)
        integer_mob.number += value
        integer_mob.submobjects = new_int.submobjects
