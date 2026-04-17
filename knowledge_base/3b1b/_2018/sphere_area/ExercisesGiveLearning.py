# Source: 3b1b/_2018/sphere_area.py
# Description: [3b1b translated] 展示一個燈泡圖示從「講座」切換到「練習」的過程，並加入自學者的角色。



from manim import *
class ExercisesGiveLearning(MovingCameraScene):
    def construct(self):
        bulb = Lightbulb()
        arrow1 = Arrow(ORIGIN, RIGHT, buff=0)
        lectures = Text("Lectures")
        exercises = Text("Exercises")
        frame = self.camera_frame
        frame.scale(0.7)

        bulb.next_to(arrow1, RIGHT)
        for word in lectures, exercises:
            word.next_to(arrow1, LEFT)

        cross = Cross(lectures)

        # Knock down lectures
        self.add(lectures)
        self.play(GrowArrow(arrow1))
        self.play(LaggedStartMap(DrawBorderThenFill, bulb))
        self.play(Create(cross))
        self.play(
            VGroup(lectures, cross).animate.shift(DOWN),
            FadeIn(exercises, shift=UP)
        )
        self.wait()

        # Show self
        arrow2 = arrow1.copy()
        arrow2.next_to(lectures, LEFT)
        logo = Logo()
        logo.set_height(1)
        logo.next_to(arrow2, LEFT)
        pupil_copy = logo.pupil.copy()

        self.add(logo, pupil_copy)
        self.play(
            frame.animate.shift(1.5 * LEFT),
            Write(logo, run_time=1.5)
        )
        self.remove(pupil_copy)
        self.play(
            GrowArrow(arrow2),
            FadeOut(cross)
        )
        self.wait()
        self.play(
            VGroup(logo, arrow2).animate.next_to(exercises, LEFT)
        )
        self.wait()
