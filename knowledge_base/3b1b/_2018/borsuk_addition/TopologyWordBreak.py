# Source: 3b1b/_2018/borsuk_addition.py
# Description: [3b1b translated] 將 "Topology" 單詞中的字母按拓撲虧格分類，並用不同顏色標示，最後按類別重新排列展示。



from manim import *
class TopologyWordBreak(Scene):
    def construct(self):
        word = Text("Topology", font_size=96)  # OldTexText -> Text, scale(2) 改為 font_size
        colors = [BLUE, YELLOW, RED]
        classes = VGroup(*[VGroup() for x in range(3)])
        
        # 為每個字母設定目標顏色和目標物件
        for letter in word:
            genus = len(letter.submobjects)  # 假設 submobjects 數量代表虧格
            letter.target_color = colors[genus]
            letter.generate_target()
            letter.target.set_color(colors[genus])
            classes[genus].add(letter.target)
        
        # 在每個類別中的字母之間加入 ≃ 符號
        signs = VGroup()
        for group in classes:
            new_group = VGroup()
            for elem in group[:-1]:
                new_group.add(elem)
                sign = MathTex("\\simeq")  # OldTex -> MathTex
                new_group.add(sign)
                signs.add(sign)
            new_group.add(group[-1])
            # 替換 group 的 submobjects
            group.submobjects = list(new_group.submobjects)
            group.arrange(RIGHT)
        
        # 微調特定字母位置
        word[2].target.shift(0.1 * DOWN)
        word[7].target.shift(0.1 * DOWN)
        
        # 排列類別
        classes.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        classes.shift(2 * RIGHT)
        
        # 添加虧格標籤
        genus_labels = VGroup(*[
            Text(f"Genus {d}:", font_size=48).next_to(  # OldTexText -> Text, scale(1.5) 改為 font_size
                classes[d], LEFT, MED_LARGE_BUFF
            )
            for d in range(3)
        ])
        genus_labels.shift(SMALL_BUFF * UP)
        
        # 動畫序列
        self.play(Write(word))
        self.play(LaggedStartMap(
            ApplyMethod, word,
            lambda m: (m.set_color, m.target_color),
            run_time=1
        ))
        self.play(
            LaggedStartMap(MoveToTarget, word),
            LaggedStartMap(FadeIn, signs),
            LaggedStartMap(FadeIn, genus_labels, shift=DOWN),  # FadeInFromDown -> FadeIn(shift=DOWN)
        )
        self.wait(3)
