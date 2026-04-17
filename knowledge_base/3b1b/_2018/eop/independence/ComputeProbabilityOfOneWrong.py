# Source: 3b1b/_2018/eop/independence.py
# Description: [3b1b translated] 展示三種錯誤模式機率計算，最後顯示總分為2的機率結果。



from manim import *
class ComputeProbabilityOfOneWrong(Scene):
    def __init__(self, score=2, final_result_rhs_tex=None, default_bool=True, default_p="0.8", default_q="0.2", **kwargs):
        super().__init__(**kwargs)
        self.score = score
        self.final_result_rhs_tex = final_result_rhs_tex or ["3", "(0.8)", "^2", "(0.2)", "=", "0.384"]
        self.default_bool = default_bool
        self.default_p = default_p
        self.default_q = default_q

    def construct(self):
        self.show_all_three_patterns()
        self.show_final_result()

    def show_all_three_patterns(self):
        probabilities = VGroup()
        point_8s = VGroup()
        point_2s = VGroup()
        
        for i in reversed(list(range(3))):
            bool_list = [self.default_bool] * 3
            bool_list[i] = not self.default_bool
            probs = ["(%s)" % self.default_p] * 3
            probs[i] = "(%s)" % self.default_q
            
            # 假設 get_probability_of_slot_group 函數在其他地方定義
            lhs = get_probability_of_slot_group(bool_list)
            rhs = MathTex("=", *probs)
            
            # 設置顏色
            for tex in rhs:
                if "0.8" in tex.tex_string:
                    tex.set_color(GREEN)
                elif "0.2" in tex.tex_string:
                    tex.set_color(RED)
            
            # 收集所有 0.8 和 0.2 的部分
            for tex in rhs:
                if "0.8" in tex.tex_string:
                    point_8s.add(tex)
                elif "0.2" in tex.tex_string:
                    point_2s.add(tex)
            
            rhs.next_to(lhs, RIGHT)
            probabilities.add(VGroup(lhs, rhs))
        
        probabilities.arrange(DOWN, buff=LARGE_BUFF)
        probabilities.center()

        self.play(Write(probabilities[0]))
        self.wait(2)
        
        for i in range(2):
            self.play(ReplacementTransform(
                probabilities[i].copy(),
                probabilities[i + 1]
            ))
        
        self.wait()
        
        for group in [point_8s, point_2s]:
            self.play(LaggedStart(
                *[Indicate(tex, rate_func=there_and_back) for tex in group],
                lag_ratio=0.7
            ))
            self.wait()

    def show_final_result(self):
        result = MathTex(
            "P(", "\\text{Score} = %s" % self.score, ")", "=",
            *self.final_result_rhs_tex
        )
        
        # 設置顏色
        for tex in result:
            tex_string = tex.tex_string
            if "0.8" in tex_string:
                tex.set_color(GREEN)
            elif "0.2" in tex_string:
                tex.set_color(RED)
            elif "Score" in tex_string:
                tex.set_color(YELLOW)
        
        # 設置最後一個元素的顏色
        result[-1].set_color(YELLOW)
        result.to_edge(UP)

        self.play(Write(result))
        self.wait()
