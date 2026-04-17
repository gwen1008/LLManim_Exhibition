# Source: 3b1b/_2019/diffyq/part1/wordy_scenes.py
# Description: [3b1b translated] 展示文字逐個出現的效果，每個字出現後等待的時間與其長度成正比。



from manim import *
class ReallyHardToSolve(Scene):
    def construct(self):
        words = MathTex(
            "They're", "really\\\\",
            "freaking", "hard\\\\",
            "to", "solve\\\\",
        )
        words.set_height(6)

        self.wait()
        for word in words:
            wait_time = 0.05 * len(word)
            self.add(word)
            self.wait(wait_time)
        self.wait()
