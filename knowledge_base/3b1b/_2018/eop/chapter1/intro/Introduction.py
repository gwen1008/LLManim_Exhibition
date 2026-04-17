# Source: 3b1b/_2018/eop/chapter1/intro.py
# Description: [3b1b translated] 展示教師與學生角色在課堂場景中的互動，包括學生表情變化和教師舉手動作。



from manim import *
class Introduction(Scene):
    def __init__(
        self,
        default_pi_creature_kwargs={
            "color": MAROON_E,
            "flip_at_start": True,
        },
        **kwargs
    ):
        super().__init__(**kwargs)
        self.default_pi_creature_kwargs = default_pi_creature_kwargs
    
    def construct(self):
        # 注意：TeacherStudentsScene 在 ManimCE 中沒有直接對應類別
        # 這裡假設已經有 self.teacher 和 self.students 物件
        # 實際使用時需要自行實現這些角色
        
        self.wait(5)
        
        # 學生表情變化 - 需要自行實現 play_student_changes 方法
        # self.play_student_changes(
        #     "confused", "frustrated", "dejected",
        #     look_at = UP + 2 * RIGHT
        # )
        
        self.wait()

        # 教師舉手動作 - 需要自行實現 change_mode 方法
        # self.play(
        #     self.get_teacher().change_mode, "raise_right_hand"
        # )
        self.wait()

        self.wait(30)
