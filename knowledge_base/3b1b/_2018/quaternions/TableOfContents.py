# Source: 3b1b/_2018/quaternions.py
# Description: [3b1b translated] 展示目錄章節標題依序淡入，並輪流放大每個章節、淡化其他章節的動畫效果。



from manim import *
class TableOfContents(Scene):
    def construct(self):
        chapters = VGroup(
            TexText(
                "\\underline{Chapter 1}\\\\", "Linus the Linelander"
            ),
            TexText(
                "\\underline{Chapter 2}\\\\", "Felix the Flatlander"
            ),
            TexText(
                "\\underline{Chapter 3}\\\\", " You, the 3d-lander"
            ),
        )
        for chapter in chapters:
            chapter.space_out_submobjects(1.5)
        chapters.arrange(
            DOWN, buff=1.5, aligned_edge=LEFT
        )
        chapters.to_edge(LEFT)

        for chapter in chapters:
            self.play(FadeIn(chapter, shift=DOWN))
            self.wait(2)
        for chapter in chapters:
            chapters.save_state()
            other_chapters = VGroup(*[
                c for c in chapters if c is not chapter
            ])
            self.play(
                chapter.animate.set_width(0.5 * config.frame_width).center(),
                other_chapters.animate.set_opacity(0)
            )
            self.wait(3)
            self.play(chapters.animate.restore())
