# Source: 3b1b/_2019/clacks/question.py
# Description: [3b1b translated] 展示兩個滑動方塊與牆壁碰撞的示意圖，包含加粗的線條、放大的標籤、紅色速度向量和黃色問題文字。



from manim import *
class Thumbnail(Scene):
    def __init__(
        self,
        sliding_blocks_config={
            "block1_config": {
                "mass": 1e4,
                "velocity": -1.5,
            },
            "collect_clack_data": False,
        },
        wait_time=0,
        count_clacks=False,
        show_flash_animations=False,
        floor_y=-3.0,
        include_sound=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.sliding_blocks_config = sliding_blocks_config
        self.wait_time = wait_time
        self.count_clacks = count_clacks
        self.show_flash_animations = show_flash_animations
        self.floor_y = floor_y
        self.include_sound = include_sound

    def construct(self):
        # 初始化 BlocksAndWallExample 的組件
        self.setup_blocks_and_wall()
        
        # 調整相機視角
        self.camera.frame.shift(0.9 * UP)
        
        # 加粗線條
        self.thicken_lines()
        
        # 放大標籤
        self.grow_labels()
        
        # 添加速度向量
        self.add_vector()
        
        # 添加問題文字
        self.add_text()

    def setup_blocks_and_wall(self):
        # 創建地板
        self.floor = Line(
            start=LEFT * 10,
            end=RIGHT * 10,
            stroke_color=WHITE,
            stroke_width=2
        )
        self.floor.shift(DOWN * self.floor_y)
        
        # 創建牆壁
        self.wall = Line(
            start=DOWN * 5,
            end=UP * 5,
            stroke_color=WHITE,
            stroke_width=2
        )
        self.wall.shift(LEFT * 5)
        
        # 創建方塊
        block1 = Square(side_length=1, color=BLUE, fill_opacity=0.8)
        block1.shift(LEFT * 2 + DOWN * (self.floor_y + 0.5))
        block1_label = Text("m1", font_size=24).move_to(block1)
        block1.add(block1_label)
        
        block2 = Square(side_length=0.5, color=RED, fill_opacity=0.8)
        block2.shift(RIGHT * 1 + DOWN * (self.floor_y + 0.25))
        block2_label = Text("m2", font_size=18).move_to(block2)
        block2.add(block2_label)
        
        self.blocks = VGroup(block1, block2)
        self.blocks.block1 = block1
        self.blocks.block2 = block2
        
        self.add(self.floor, self.wall, self.blocks)

    def thicken_lines(self):
        self.floor.set_stroke(width=10)
        self.wall.set_stroke(width=10)

    def grow_labels(self):
        blocks = self.blocks
        for block in [blocks.block1, blocks.block2]:
            # 移除原標籤並創建新的大標籤
            for mob in block:
                if isinstance(mob, Text):
                    block.remove(mob)
            
            # 創建放大後的標籤
            if block == blocks.block1:
                label = Text("m1", font_size=60, color=WHITE)
            else:
                label = Text("m2", font_size=45, color=WHITE)
            
            label.move_to(block.get_top() + UP * 0.5)
            self.add(label)
            block.label = label

    def add_vector(self):
        blocks = self.blocks
        arrow = Arrow(
            start=RIGHT,
            end=LEFT * 2.5,
            color=RED,
            stroke_width=15,
            tip_length=0.3,
            max_tip_length_to_length_ratio=0.3
        )
        arrow.move_to(blocks.block1.get_center())
        arrow.shift(RIGHT * 0.5)
        
        # 添加陰影效果
        shadow = arrow.copy()
        shadow.set_stroke(GREY, width=5, opacity=0.7)
        shadow.shift(UP * 0.1 + RIGHT * 0.1)
        arrow.add_to_back(shadow)
        
        self.arrow = arrow
        self.add(arrow)

    def add_text(self):
        question = Text(
            "How many\ncollisions?",
            font_size=72,
            color=YELLOW,
            weight=BOLD
        )
        question.scale(1.2)
        question.to_edge(UP, buff=0.5)
        
        # 添加描邊效果
        question.set_stroke(color=RED, width=5, background=True)
        
        self.question = question
        self.add(question)
