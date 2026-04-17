# Source: 3b1b/_2018/basel/basel2.py
# Description: [3b1b translated] 展示老師與學生場景中，學生提問時光源動畫與角色表情變化的過程。



from manim import *
class AskAboutBrightness(TeacherStudentsScene):
    def __init__(self, num_levels=200, radius=10, **kwargs):
        super().__init__(**kwargs)
        self.num_levels = num_levels
        self.radius = radius

    def construct(self):
        # 注意：ManimCE 沒有內建的 LightSource 類別
        # 這裡用替代方案展示核心邏輯
        # 實際使用時需要自定義 LightSource 或使用其他視覺元素替代
        
        # 創建替代光源視覺元素
        ambient_light = Circle(
            radius=self.radius,
            color=YELLOW,
            fill_opacity=0.1,
            stroke_width=0
        )
        lighthouse = Triangle(
            color=WHITE,
            fill_opacity=1,
            stroke_width=2
        ).scale(0.5)
        lighthouse.move_to(self.teacher.get_top(), aligned_edge=UP)
        
        # 將光源移到指定位置
        light_group = VGroup(ambient_light, lighthouse)
        light_group.move_to(5*LEFT + 2*UP)
        
        self.add_foreground_mobjects(self.pi_creatures)
        
        # 學生說話
        self.student_says(
            "What do you mean \\\\ by ``brightness''?",
            added_anims = [
                FadeIn(ambient_light, scale=0.5),
                FadeIn(lighthouse)
            ]
        )
        
        # 老師表情變化
        self.play(self.teacher.change("happy"))
        self.wait(4)
