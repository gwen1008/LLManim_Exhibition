# Source: 3b1b/_2019/diffyq/part4/pi_creature_scenes.py
# Description: [3b1b translated] 展示一個教師與學生場景，其中一名學生打斷並展示階梯函數與傅立葉級數逼近的動畫對比。


from manim import *
import numpy as np
import itertools as it

class HangOnThere(TeacherStudentsScene):
    def construct(self):
        student = self.students[2]

        axes1 = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1.5, 1.5, 0.5],
            x_length=3,
            y_length=4.5,
            axis_config={
                "stroke_width": 2,
                "include_tip": False,
            },
        )
        axes2 = axes1.copy()
        neq = MathTex("\\neq")
        neq.scale(2)

        group = VGroup(axes1, neq, axes2)
        group.arrange(RIGHT)
        group.set_height(4)
        group.next_to(
            student.get_corner(UL), UP,
            buff=LARGE_BUFF,
        )

        # 階梯函數
        step_graph = axes1.plot(
            lambda x: (1 if x < 0.5 else -1),
            discontinuities=[0.5],
            color=YELLOW,
        )
        
        # 傅立葉級數逼近序列
        wave_graphs = VGroup()
        for max_n in range(3, 103, 2):
            def func(x, max_n=max_n):
                total = 0
                for u, n in zip(it.cycle([1, -1]), range(1, max_n, 2)):
                    total += (u / n) * np.cos(n * np.pi * x)
                return (4 / np.pi) * total
            graph = axes2.plot(func, color=WHITE)
            wave_graphs.add(graph)
        
        wave_graphs.set_stroke(width=3)
        # 漸層顏色
        colors = color_gradient([WHITE, PINK], len(wave_graphs))
        for graph, color in zip(wave_graphs, colors):
            graph.set_color(color)
        
        last_wave_graph = wave_graphs[-1]
        last_wave_graph.set_stroke(PINK, 2)
        wave_graphs.remove(last_wave_graph)
        group.add(step_graph)

        self.student_says(
            "Hang on\\\\hang on\\\\hang on...",
            target_mode="surprised",
            bubble_class=SpeechBubble,
            index=2,
        )
        self.play(
            self.teacher.animate.change("guilty")
        )
        self.wait()
        
        # 移除對話框並讓學生舉手
        self.play(
            FadeOut(self.students[2].bubble),
            FadeOut(self.students[2].bubble.content),
            student.animate.change("raise_left_hand", group),
            FadeIn(group, shift=DOWN),
        )

        last_wg = VectorizedPoint()
        n_first_fades = 4
        for wg in wave_graphs[:n_first_fades]:
            self.play(
                last_wg.animate.set_stroke(width=0.1),
                FadeIn(wg),
            )
            last_wg = wg
        
        # 動畫顯示剩餘的波形
        def update_stroke_width(mob, alpha):
            # there_and_back 函數的近似
            t = 2 * alpha if alpha < 0.5 else 2 * (1 - alpha)
            width = 3 * t + 0.1 * alpha
            mob.set_stroke(width=width)
        
        animations = []
        for wg in wave_graphs[n_first_fades:]:
            anim = UpdateFromAlphaFunc(wg, update_stroke_width)
            animations.append(anim)
        
        self.play(
            LaggedStart(*animations, run_time=5, lag_ratio=0.2),
            last_wg.animate.set_stroke(width=0.1),
            FadeIn(
                last_wave_graph,
                rate_func=lambda t: smooth(min(1, 0.9 + 0.1 * t)),
                run_time=5,
            ),
            self.teacher.animate.change("thinking"),
        )
        
        self.play_student_changes(
            "confused", "confused", "angry"
        )
        self.wait(3)
