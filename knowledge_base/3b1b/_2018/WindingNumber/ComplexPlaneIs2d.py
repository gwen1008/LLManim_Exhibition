# Source: 3b1b/_2018/WindingNumber.py
# Description: [3b1b translated] 展示一個複數平面在二維空間中的視覺化。



from manim import *
class ComplexPlaneIs2d(Scene):
    def construct(self):
        com_plane = ComplexPlane()
        self.add(com_plane)
        # TODO: Add labels to axes, specific complex points
        self.wait()
