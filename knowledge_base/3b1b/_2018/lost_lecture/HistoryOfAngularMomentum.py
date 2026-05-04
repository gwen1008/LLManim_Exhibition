# Source: 3b1b/_2018/lost_lecture.py
# Description: [3b1b translated] 展示角動量與克卜勒第二定律的關係，教師在課堂上舉起圖示並引導學生思考。



from manim import *
class HistoryOfAngularMomentum(TeacherStudentsScene):
    def __init__(self, camera_config={"fill_opacity": 1}, **kwargs):
        super().__init__(camera_config=camera_config, **kwargs)
    
    def construct(self):
        am = VGroup(Text("Angular momentum"))
        k2l = Text("Kepler's 2nd law")
        arrow = Arrow(ORIGIN, RIGHT)

        group = VGroup(am, arrow, k2l)
        group.arrange(RIGHT)
        group.next_to(self.hold_up_spot, UL)

        # 注意：ImageMobject在ManimCE中需要指定檔案路徑
        # 這裡假設圖片檔案存在，否則需要調整
        k2l_image = ImageMobject("Kepler2ndLaw")
        k2l_image.match_width(k2l)
        k2l_image.next_to(k2l, UP)
        k2l.add(k2l_image)

        angular_momentum_formula = MathTex(
            "R", "\\times", "m", "\\vec{\\textbf{v}}_\\perp",
        )
        angular_momentum_formula.set_color_by_tex_to_color_map({
            "R": PINK,
            "v": YELLOW,
        })
        angular_momentum_formula.next_to(am, UP)
        am.add(angular_momentum_formula)

        self.play(
            self.teacher.animate.change("raise_right_hand"),
            FadeIn(group, shift=DOWN),
            self.change_students(*3 * ["pondering"])
        )
        self.wait()
        self.play(
            am.animate.next_to(arrow, RIGHT, aligned_edge=0),
            k2l.animate.next_to(arrow, LEFT, aligned_edge=0),
            path_arc=90 * DEGREES,
            run_time=2
        )
        self.wait(3)
