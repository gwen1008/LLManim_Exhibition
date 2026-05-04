# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 在場景中央顯示一段文字，詢問觀眾對結尾的建議並引導至 Patreon 貼文。



from manim import *
class FinalComment(Scene):
    def construct(self):
        self.add(Text(
            "Thoughts on what ending should go here?\\\\"
            "See the Patreon post."
        ))
