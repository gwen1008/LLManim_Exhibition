# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 在畫面頂部顯示一個靜態的文字標籤。



from manim import *
class TopLabel(Scene):
    def __init__(self, text="Text", **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def construct(self):
        label = Text(self.text)
        label.move_to(3 * UP)
        self.add(label)
        self.wait()
