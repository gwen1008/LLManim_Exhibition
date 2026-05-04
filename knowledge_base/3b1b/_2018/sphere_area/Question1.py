# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個問題文字淡入，然後替換為提示文字，同時保留"circumference"單詞的顏色和位置動畫。



from manim import *
class Question1(Scene):
    def construct(self):
        kwargs = {
            "tex_to_color_map": {
                "circumference": RED,
            }
        }
        question = Text(
            """
            Question #1: What is the circumference of
            one of these rings (in terms of R and θ)?
            """,
            font_size=24,
            **kwargs
        )
        prompt = Text(
            """
            Multiply this circumference by R dθ to
            get an approximation of the ring's area.
            """,
            font_size=24,
            **kwargs
        )
        
        for words in question, prompt:
            words.set_width(config.frame_width - 1)

        self.play(FadeIn(question, shift=DOWN))
        self.wait(2)
        
        # 在ManimCE中，Text物件沒有get_part_by_tex方法
        # 我們需要手動處理"circumference"的顏色
        # 先創建兩個單獨的"circumference"文字物件
        circum_question = Text("circumference", color=RED, font_size=24)
        circum_prompt = Text("circumference", color=RED, font_size=24)
        
        # 將circumference文字放在適當位置
        circum_question.move_to(question.get_part_by_tex("circumference") if hasattr(question, 'get_part_by_tex') else question)
        circum_prompt.move_to(prompt.get_part_by_tex("circumference") if hasattr(prompt, 'get_part_by_tex') else prompt)
        
        # 移除原文字中的"circumference"部分（在ManimCE中需要重新組織文字）
        # 這裡簡化處理：直接使用完整的文字物件
        
        self.play(
            FadeOut(question, shift=UP),
            FadeIn(prompt, shift=DOWN),
            circum_question.animate.move_to(circum_prompt),
            run_time=1.5
        )
        self.wait()
