# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示一個目錄清單，其中每個項目可以依次放大並高亮顯示，其他項目則淡出。



from manim import *
class TableOfContents(Scene):
    def construct(self):
        items = VGroup(
            Text("How the ellipse will arise"),
            Text("Kepler's 2nd law"),
            Text("The shape of velocities"),
        )
        items.arrange(
            DOWN, buff=LARGE_BUFF, aligned_edge=LEFT
        )
        items.to_edge(LEFT, buff=1.5)
        for item in items:
            item.add(Dot().next_to(item, LEFT))
            item.generate_target()
            item.target.set_fill(GREY, opacity=0.5)

        title = Title("The plan")
        scale_factor = 1.2

        self.add(title)
        self.play(LaggedStart(
            *[FadeIn(item) for item in items],
            run_time=1,
            lag_ratio=0.7,
        ))
        self.wait()
        for item in items:
            other_items = VGroup(*[m for m in items if m is not item])
            new_item = item.copy()
            new_item.scale(scale_factor, about_edge=LEFT)
            new_item.set_fill(WHITE, 1)
            self.play(
                Transform(item, new_item),
                *[MoveToTarget(mob) for mob in other_items]
            )
            self.wait()
