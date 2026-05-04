# Source: 3b1b/_2019/hyperdarts.py
# Description: [3b1b translated] 展示一個目錄頁面，其中每個部分依次放大並高亮顯示，同時恢復前一個部分到原始狀態。



from manim import *
class TableOfContents(Scene):
    def construct(self):
        rect = FullScreenFadeRectangle(opacity=0.75)
        self.add(rect)

        parts = VGroup(
            Text("The game"),
            Text("The puzzle"),
            Text("The micropuzzles"),
            Text("The answer"),
        )

        parts.scale(1.5)
        parts.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        parts.to_edge(LEFT, buff=2)

        parts.set_opacity(0.5)
        self.add(parts)

        for part in parts:
            dot = Dot()
            dot.next_to(part, LEFT, SMALL_BUFF)
            dot.match_style(part)
            self.add(dot)

        last_part = VMobject()
        last_part.save_state()

        for part in parts:
            part.save_state()
            self.play(
                part.animate.scale(1.5, about_edge=LEFT),
                part.animate.set_opacity(1),
                Restore(last_part)
            )
            self.wait()
            last_part = part
