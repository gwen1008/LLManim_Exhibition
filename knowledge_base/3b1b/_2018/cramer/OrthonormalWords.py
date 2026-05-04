# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示正交變換的定義條件，並用顏色標示向量與關鍵詞。



from manim import *
class OrthonormalWords(Scene):
    def construct(self):
        v_tex = "\\vec{\\textbf{v}}"
        w_tex = "\\vec{\\textbf{w}}"
        top_words = MathTex(
            "\\text{If }",
            "T(", v_tex, ")", "\\cdot",
            "T(", w_tex, ")", "=",
            v_tex, "\\cdot", w_tex,
            "\\text{ for all }", v_tex, "\\text{ and }", w_tex,
        )
        # 替換 set_color_by_tex_to_color_map
        for tex, color in [(v_tex, YELLOW), (w_tex, MAROON_B)]:
            for part in top_words.get_parts_by_tex(tex):
                part.set_color(color)
        
        bottom_words = Tex("$T$", "is", "``Orthonormal''")
        bottom_words.set_color_by_tex("Orthonormal", BLUE)
        
        words = VGroup(top_words, bottom_words)
        words.arrange(DOWN, buff=MED_LARGE_BUFF)
        for word in words:
            word.add_background_rectangle()
        words.to_edge(UP)

        self.play(Write(words))
        self.wait()
