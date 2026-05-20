# [VISUAL REASONING]
# Show original expression, student's wrong sign expansion, highlight the error,
# present corrected line, and reveal final answer -44 with sign rule reminder.

from manim import *

class IntegerSubtractionErrorAnalysis(Scene):
    """
    整數加減: 負號提取規則 = 括號前的負號改變括號內所有項的符號

    題目：錯誤分析：學生計算 -58 - (-31) + (-17)，請找出符號處理錯誤的步驟並改正
    """
    def construct(self):
        title = Text("Error Analysis: Sign Handling", color=WHITE, font_size=38).to_edge(UP, buff=0.5)
        original_expr = MathTex("-58 - (-31) + (-17)", color=WHITE).move_to(ORIGIN + np.array([0, 1.8, 0]))
        wrong_step = MathTex("= -58 + 31 + 17", color=WHITE).move_to(ORIGIN + np.array([0, 0.7, 0]))
        wrong_label = Text("Wrong! sign of -17 not handled", color=RED, font_size=28).move_to(ORIGIN + np.array([0, -0.1, 0]))
        correct_step = MathTex("= -58 + 31 - 17", color=GREEN).move_to(ORIGIN + np.array([0, -1.0, 0]))
        final_answer = MathTex("= -44", color=YELLOW).move_to(ORIGIN + np.array([0, -2.0, 0]))

        self.add(title)

        # Step 1
        anim_time_1 = 1.8
        self.play(Write(original_expr), run_time=anim_time_1)
        self.wait(5.37)

        # Step 2
        anim_time_2 = 1.8
        self.play(Write(wrong_step), run_time=anim_time_2)
        self.play(Circumscribe(wrong_step, color=RED))
        self.wait(5.6)

        # Step 3
        anim_time_3 = 1.5
        self.play(FadeIn(wrong_label), run_time=anim_time_3)
        self.play(Indicate(wrong_label, color=RED))
        self.wait(4.79)

        # Step 4
        self.play(FadeOut(wrong_label))
        anim_time_4 = 1.8
        self.play(Write(correct_step), run_time=anim_time_4)
        self.play(Circumscribe(correct_step, color=GREEN))
        self.wait(2.79)

        # Step 5
        anim_time_5 = 1.8
        self.play(Write(final_answer), run_time=anim_time_5)
        self.play(Indicate(final_answer, color=YELLOW))
        self.wait(5.76)
