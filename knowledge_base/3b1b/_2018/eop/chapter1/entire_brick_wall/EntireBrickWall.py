# Source: 3b1b/_2018/eop/chapter1/entire_brick_wall.py
# Description: [3b1b translated] 展示一個由磚塊組成的牆面逐行生成，並在最後一行高亮顯示特定磚塊及其對應的機率百分比，最後鏡頭縮小聚焦到牆面右下角。


from manim import *
import math

class EntireBrickWall(Scene):
    def construct(self):
        # 初始化參數
        row_height = 0.3
        nb_rows = 20
        start_point = 3 * UP + 1 * LEFT
        
        # 創建第一行磚塊
        rows = VGroup()
        first_row = self.create_brick_row(0, height=row_height)
        first_row.move_to(start_point)
        rows.add(first_row)
        self.add(rows)
        
        # 添加翻轉計數器
        zero_counter = Integer(0).next_to(start_point + 0.5 * first_row.width * RIGHT)
        nb_flips_text = Text("# of flips")
        nb_flips_text.next_to(zero_counter, RIGHT, buff=LARGE_BUFF)
        self.add(zero_counter, nb_flips_text)
        flip_counters = VGroup(zero_counter)
        
        # 逐行生成磚牆
        for i in range(1, nb_rows + 1):
            rows.add(rows[-1].copy())
            self.bring_to_back(rows[-1])
            
            anims = [
                rows[-1].animate.shift(row_height * DOWN),
                Animation(rows[-2])
            ]
            
            if i % 5 == 0:
                counter = Integer(i)
                counter.next_to(rows[-1].get_right() + row_height * DOWN, RIGHT)
                flip_counters.add(counter)
                anims.append(FadeIn(counter))
            
            self.play(*anims)
            
            # 分割磚塊（模擬SplitRectsInBrickWall效果）
            self.play(self.split_rects(rows[-1]))
            rows.submobjects[-1] = self.merge_rects_by_subdiv(rows[-1])
            rows.submobjects[-1] = self.merge_rects_by_coloring(rows[-1])
        
        # 添加tails計數器
        tails_counters = VGroup()
        for i, rect in enumerate(rows[-1].rects):
            if i < 6 or i > 14:
                continue
            if i == 6:
                counter = MathTex("\\dots", color=BLUE)
                counter.next_to(rect, DOWN, buff=1.5 * MED_SMALL_BUFF)
            elif i == 14:
                counter = MathTex("\\dots", color=BLUE)
                counter.next_to(rect, DOWN, buff=1.5 * MED_SMALL_BUFF)
                counter.shift(0.2 * RIGHT)
            else:
                counter = Integer(i, color=BLUE)
                counter.next_to(rect, DOWN)
            tails_counters.add(counter)
        
        nb_tails_text = Text("# of tails", color=BLUE)
        nb_tails_text.next_to(tails_counters[-1], RIGHT, buff=LARGE_BUFF)
        
        self.play(
            LaggedStartMap(FadeIn, tails_counters),
            FadeIn(nb_tails_text)
        )
        
        # 清理並移動所有物件
        self.clear()
        self.add(nb_flips_text)
        
        mobs_to_shift = VGroup(
            rows, flip_counters, tails_counters, nb_tails_text
        )
        self.play(mobs_to_shift.animate.shift(3 * UP))
        
        # 高亮最後一行
        last_row_rect = SurroundingRectangle(rows[-1], buff=0)
        last_row_rect.set_stroke(color=YELLOW, width=6)
        
        rows.save_state()
        self.play(
            rows.animate.set_opacity(0.1),
            Create(last_row_rect)
        )
        
        # 創建高亮磚塊
        highlighted_bricks = [
            self.highlighted_brick(rows, row=20, nb_tails=i, row_height=row_height)
            for i in range(20)
        ]
        
        self.wait()
        self.play(FadeIn(highlighted_bricks[10]))
        self.wait()
        self.play(
            FadeOut(highlighted_bricks[10]),
            FadeIn(highlighted_bricks[9]),
            FadeIn(highlighted_bricks[11]),
        )
        self.wait()
        self.play(
            FadeOut(highlighted_bricks[9]),
            FadeOut(highlighted_bricks[11]),
            FadeIn(highlighted_bricks[8]),
            FadeIn(highlighted_bricks[12]),
        )
        self.wait()
        self.play(
            FadeOut(highlighted_bricks[8]),
            FadeOut(highlighted_bricks[12]),
            FadeOut(last_row_rect),
            rows.animate.restore(),
        )
        self.wait()
        
        # 鏡頭縮小動畫
        new_frame = self.camera.frame.copy()
        new_frame.scale(0.0001).move_to(rows.get_corner(DR))
        
        self.play(
            self.camera.frame.animate.move_to(new_frame.get_center()).scale(0.0001),
            run_time=9,
            rate_func=exponential_decay
        )
    
    def create_brick_row(self, n, height=0.3):
        """創建一行磚塊"""
        row = VGroup()
        row.rects = VGroup()
        width = 0.5
        for i in range(n + 1):
            rect = Rectangle(width=width, height=height)
            rect.set_fill(color=WHITE, opacity=1)
            rect.set_stroke(color=BLACK, width=2)
            rect.move_to(i * width * RIGHT)
            row.add(rect)
            row.rects.add(rect)
        row.width = (n + 1) * width
        return row
    
    def split_rects(self, row):
        """分割磚塊的動畫（簡化版本）"""
        anims = []
        for rect in row.rects:
            new_rect = rect.copy()
            new_rect.set_height(rect.get_height() * 0.5)
            anims.append(Transform(rect, new_rect))
        return AnimationGroup(*anims)
    
    def merge_rects_by_subdiv(self, row):
        """合併磚塊（簡化版本）"""
        return row
    
    def merge_rects_by_coloring(self, row):
        """根據顏色合併磚塊（簡化版本）"""
        return row
    
    def highlighted_brick(self, rows, row, nb_tails, row_height):
        """創建高亮磚塊及其標籤"""
        brick_copy = rows[row-1].rects[nb_tails].copy()
        brick_copy.set_fill(color=YELLOW, opacity=0.8)
        
        # 計算機率
        prob_percentage = float(math.comb(row, nb_tails)) / (2**row) * 100
        brick_label = DecimalNumber(
            prob_percentage,
            unit="\\%",
            num_decimal_places=1,
            color=BLACK
        )
        brick_label.move_to(brick_copy)
        brick_label.set_height(0.8 * brick_copy.get_height())
        
        return VGroup(brick_copy, brick_label)
