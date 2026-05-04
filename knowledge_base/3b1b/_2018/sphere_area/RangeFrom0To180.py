# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個整數角度從 0 度動態變化到 180 度的過程。



from manim import *
class RangeFrom0To180(Scene):
    def construct(self):
        angle = Integer(0, unit="^\\circ")
        angle.scale(2)

        self.add(angle)
        self.wait()
        self.play(ChangeDecimalToValue(
            angle, 180,
            run_time=2,
        ))
        self.wait()
