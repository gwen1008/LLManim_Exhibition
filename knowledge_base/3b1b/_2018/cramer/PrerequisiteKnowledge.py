# Source: 3b1b/_2018/cramer.py
# Description: [3b1b translated] 展示一個教學場景，老師和學生在標題下方排列三個圖片縮圖，每個圖片帶有藍色邊框，並伴隨學生表情變化。



from manim import *
class PrerequisiteKnowledge(TeacherStudentsScene):
    def __init__(self, camera_config={"background_opacity": 1}, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)

    def construct(self):
        self.remove(*self.pi_creatures)
        randy = self.students[1]
        self.add(randy)

        title = Text("Prerequisites")
        title.to_edge(UP)

        h_line = Line(LEFT, RIGHT).scale(5)
        h_line.next_to(title, DOWN)

        images = Group(*[
            ImageMobject(f"eola{d}_thumbnail")
            for d in [5, 7, 6]
        ])
        images.arrange(RIGHT, buff=LARGE_BUFF)
        images.next_to(h_line, DOWN, buff=MED_LARGE_BUFF)
        for image in images:
            rect = SurroundingRectangle(image, color=BLUE)
            image.rect = rect

        self.add(title)
        self.play(
            Create(h_line),
            randy.animate.change("erm")
        )
        self.wait()
        for image in images:
            self.play(
                FadeIn(image, shift=DOWN),
                FadeIn(image.rect, shift=DOWN),
                randy.animate.change("pondering")
            )
            self.wait()
