# Source: 3b1b/_2018/wallis.py
# Description: [3b1b translated] 展示一個帶有藍色圓點標記的目錄列表，並逐項高亮顯示每個主題。



from manim import *
class TableOfContents(Scene):
    def construct(self):
        topics = VGroup(
            Text("The setup"),
            Text("Circle geometry with complex polynomials"),
            Text("Proof of the Wallis product"),
            Text("Formalities not discussed"),
            Text("Generalizing this proof to get \\\\ the product formula for sine"),
        )
        for topic in topics:
            dot = Dot(color=BLUE)
            dot.next_to(topic, LEFT)
            topic.add(dot)
        topics.arrange(
            DOWN, aligned_edge=LEFT, buff=LARGE_BUFF
        )
        self.add(topics)
        self.wait()
        for i in range(len(topics)):
            self.play(
                topics[i + 1:].animate.set_opacity(0.25),
                topics[:i].animate.set_opacity(0.25),
                topics[i].animate.set_opacity(1),
            )
            self.wait(2)
