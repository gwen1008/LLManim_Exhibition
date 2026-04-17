# Source: 3b1b/_2018/div_curl.py
# Description: [3b1b translated] 展示一個目標文字和下方出現的螢幕矩形框。



from manim import *
class GoalWrapper(Scene):
    def construct(self):
        goal = Text(
            "Goal: Teach/remind people \\\\ that they love math",
            font_size=48
        )
        goal.to_edge(UP)
        self.add(goal)

        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(goal, DOWN)
        self.play(Create(screen_rect))
        self.wait()
