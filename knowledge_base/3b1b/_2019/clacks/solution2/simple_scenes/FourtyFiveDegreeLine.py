# Source: 3b1b/_2019/clacks/solution2/simple_scenes.py
# Description: [3b1b translated] 展示一條線從水平位置旋轉45度，同時顯示角度標籤和弧線的動畫過程。



from manim import *
class FourtyFiveDegreeLine(Scene):
    def __init__(self, angle=45 * DEGREES, label_config=None, degrees=True, **kwargs):
        super().__init__(**kwargs)
        self.angle = angle
        if label_config is None:
            label_config = {
                "num_decimal_places": 0,
                "unit": "^\\circ",
                "label_height": 0.3,
            }
        self.label_config = label_config
        self.degrees = degrees

    def construct(self):
        angle = self.angle
        arc = Arc(angle, radius=1)
        label = DecimalNumber(0, **self.label_config)
        label.set_height(self.label_config["label_height"])
        label.next_to(arc, RIGHT)
        label.shift(0.5 * SMALL_BUFF * UP)
        line1 = Line(ORIGIN, 3 * RIGHT)
        line2 = line1.copy()

        if self.degrees:
            target_value = int(angle / DEGREES)
        else:
            target_value = angle

        self.add(line1, label)
        self.play(
            ChangeDecimalToValue(label, target_value),
            Create(arc),
            Rotate(line2, angle, about_point=ORIGIN)
        )
        self.wait()
