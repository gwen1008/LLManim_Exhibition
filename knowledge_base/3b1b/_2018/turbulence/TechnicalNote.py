# Source: 3b1b/_2018/turbulence.py
# Description: [3b1b translated] 展示一個技術註解的標題和詳細文字說明，標題為紅色並置於頂部，下方為縮放後的文字內容。



from manim import *
class TechnicalNote(Scene):
    def construct(self):
        title = Text("Technical note:", color=RED)
        title.to_edge(UP)
        self.add(title)

        words = Text("""
            This idea of quantifying the energy held at different
            length scales is typically defined
            in terms of an ``energy spectrum'' involving the Fourier
            transform of a function measuring the correlations
            between the fluid's velocities at different points in space.
            I know, yikes!
            
            
            Building up the relevant background for that is a bit cumbersome,
            so we'll be thinking about the energy at different scales in
            terms of all eddy's with a given diameter.  This is admittedly
            a less well-defined notion, but it does capture the spirit
            of Kolmogorov's result.
            
            
            See the links in the description for more details,
            if you're curious.
        """, font_size=24, line_spacing=1.2)
        words.next_to(title, DOWN, buff=LARGE_BUFF)

        self.add(title, words)
