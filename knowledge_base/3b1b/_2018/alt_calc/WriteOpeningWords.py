# Source: 3b1b/_2018/alt_calc.py
# Description: [3b1b translated] 逐字淡入顯示兩行文字，模擬打字機效果，逗號處有額外停頓。



from manim import *
class WriteOpeningWords(Scene):
    def construct(self):
        raw_string1 = "Dear calculus student,"
        raw_string2 = "You're about to go through your first course. Like " + \
                      "any new topic, it will take some hard work to understand,"
        # 使用 Text 替代 OldTexText，並移除 \Large 參數
        words1 = Text(raw_string1, font_size=36).split(" ")
        words2 = Text(raw_string2, font_size=36).split(" ")
        
        # 將單詞列表轉換為 VGroup
        words1_group = VGroup(*words1)
        words2_group = VGroup(*words2)
        
        # 排列位置
        words1_group.next_to(words2_group, UP, aligned_edge=LEFT, buff=LARGE_BUFF)
        words = VGroup(words1_group, words2_group)
        words.set_width(config.frame_width - 2 * LARGE_BUFF)
        words.to_edge(UP)

        letter_wait = 0.05
        word_wait = 2 * letter_wait
        comma_wait = 5 * letter_wait
        
        # 遍歷所有單詞
        for word_group in words:
            for word in word_group:
                # 為每個單詞創建逐字母淡入效果
                letters = [letter for letter in word]  # 獲取單詞中的字母
                self.play(LaggedStart(
                    *[FadeIn(letter, shift=0.1*DOWN) for letter in letters],
                    run_time=len(letters) * letter_wait,
                    lag_ratio=1.5 / len(letters)
                ))
                self.wait(word_wait)
                # 檢查單詞是否以逗號結尾
                if word.text[-1] == ",":
                    self.wait(comma_wait)
