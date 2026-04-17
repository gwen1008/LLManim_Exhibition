# Source: 3b1b/_2019/diffyq/part3/wordy_scenes.py
# Description: [3b1b translated] 展示在偏微分方程邊界條件下，從文字描述過渡到數學方程式的動態過程，並包含圖像和邊框的視覺元素。



from manim import *
class WriteOutBoundaryCondition(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 繼承類的屬性需要初始化
        self.items = []
        self.pde = None
        self.bc_paren = None
        self.tex_mobject_config = {}
        
    def construct(self):
        # 模擬 ThreeConstraints.construct() 的內容
        self.setup_constraints()
        
        self.add_ic()
        self.write_bc_words()
        self.write_bc_equation()

    def setup_constraints(self):
        # 這裡模擬 ThreeConstraints 類的設置
        # 實際使用時需要根據原始代碼調整
        pass

    def add_ic(self):
        from PIL import Image
        # 注意：ManimCE 中 ImageMobject 已改為 ImageMobject 或 Image
        # 這裡使用 SVGMobject 作為替代，實際使用時需要調整
        image = ImageMobject("temp_initial_condition_example")
        image.set_width(3)
        border = SurroundingRectangle(image, buff=SMALL_BUFF)
        border.shift(SMALL_BUFF * UP)
        border.set_stroke(WHITE, 2)
        group = Group(image, border)
        # 假設 self.items[2] 已定義
        if hasattr(self, 'items') and len(self.items) > 2:
            group.next_to(self.items[2], DOWN)
        self.add(group)

    def get_bc_words(self):
        # 模擬獲取邊界條件文字的方法
        # 實際使用時需要根據原始代碼實現
        return Text("Boundary Conditions").scale(0.8)

    def write_bc_words(self):
        bc_paren = self.bc_paren if hasattr(self, 'bc_paren') else None
        bc_words = self.get_bc_words()
        
        # 假設 self.items[1][1] 存在
        if hasattr(self, 'items') and len(self.items) > 1 and len(self.items[1]) > 1:
            bc_words.match_width(self.items[1][1])
        
        if bc_paren:
            bc_words.move_to(bc_paren.get_center() + UP * bc_words.height/2)
        
        # 設置顏色 - 假設有 {t} 標記
        bc_words.set_color_by_tex("{t}", YELLOW)

        # 假設 self.items[0] 和 self.pde 存在
        if hasattr(self, 'items') and len(self.items) > 0 and hasattr(self, 'pde'):
            highlight_group = VGroup(self.items[0], self.pde)
            self.play(
                Create(SurroundingRectangle(highlight_group, buff=SMALL_BUFF).set_stroke(YELLOW, 2)),
                run_time=1.5
            )
            self.play(FadeOut(SurroundingRectangle(highlight_group)))

        if bc_paren:
            self.play(
                FadeOut(bc_paren, shift=UP),
                FadeIn(bc_words, shift=DOWN),
            )
        else:
            self.play(FadeIn(bc_words, shift=DOWN))
            
        self.wait()

        self.bc_words = bc_words

    def write_bc_equation(self):
        if not hasattr(self, 'bc_words'):
            return
            
        bc_words = self.bc_words

        # OldTex 改為 MathTex
        equation = MathTex(
            r"{\partial {T} \over \partial {x}}(0, {t}) = ",
            r"{\partial {T} \over \partial {x}}(L, {t}) = ",
            r"0",
            **self.tex_mobject_config,
        )
        equation.next_to(bc_words, DOWN, buff=MED_LARGE_BUFF)

        # 移動相機幀
        self.play(
            self.camera.frame.animate.shift(0.8 * DOWN),
        )
        self.play(FadeIn(equation, shift=UP))
        self.wait()
