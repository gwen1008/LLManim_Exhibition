
"""
Integer Vertical Subtraction Template
Generates Manim code for step-by-step vertical subtraction with audio narration and interactive elements.
Supports borrowing (借位) logic for multi-digit numbers.
"""
from typing import List, Dict, Any
from .common import get_imports_code, get_setup_code


def generate_subtraction_narrative(num1: int, num2: int, interactive_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Generate step-by-step narrative for vertical subtraction.
    Handles borrowing (借位) across multiple digits.
    If num1 < num2, the result is negative; we compute |num1 - num2| by swapping.
    """
    is_negative = num1 < num2
    # 內部計算永遠用大減小，確保借位邏輯正確
    calc_num1, calc_num2 = (num2, num1) if is_negative else (num1, num2)
    str1 = str(calc_num1)
    str2 = str(calc_num2)
    steps = []

    # ========== Intro Phase ==========
    steps.append({
        "narrative": "今天我們要學習整數的直式減法。",
        "phase": "intro"
    })
    steps.append({
        "narrative": f"題目是 {num1} 減 {num2}。",
        "phase": "intro"
    })
    if is_negative:
        steps.append({
            "narrative": f"因為 {num1} 比 {num2} 小，結果會是負數。我們先算 {calc_num1} 減 {calc_num2}，最後加上負號。",
            "phase": "intro"
        })
    steps.append({
        "narrative": "在開始計算之前，記住要把兩個數字靠右對齊，個位對個位、十位對十位。",
        "phase": "intro"
    })
    steps.append({
        "narrative": "我們從個位開始，一位一位往左計算。如果上面的數字比下面小，就需要向左邊借位。",
        "phase": "intro"
    })

    # ========== Digit-by-Digit Calculation with Borrow ==========
    places = ["個位", "十位", "百位", "千位", "萬位", "十萬位", "百萬位"]
    max_len = max(len(str1), len(str2))
    answer = num1 - num2
    answer_len = len(str(abs(answer)))  # 用絕對值算位數，跳過前導零

    # Pre-compute borrow state for each position
    borrows = [0] * (max_len + 1)
    for i in range(max_len):
        val1 = int(str1[len(str1) - 1 - i]) if i < len(str1) else 0
        val2 = int(str2[len(str2) - 1 - i]) if i < len(str2) else 0
        effective_val1 = val1 - borrows[i]
        if effective_val1 < val2:
            borrows[i + 1] = 1
        else:
            borrows[i + 1] = 0

    for i in range(max_len):

        place_name = places[i] if i < len(places) else "下一位"
        val1 = int(str1[len(str1) - 1 - i]) if i < len(str1) else 0
        val2 = int(str2[len(str2) - 1 - i]) if i < len(str2) else 0
        borrow_in = borrows[i]
        effective_val1 = val1 - borrow_in
        needs_borrow = effective_val1 < val2
        if needs_borrow:
            compute_val1 = effective_val1 + 10
        else:
            compute_val1 = effective_val1
        result_digit = compute_val1 - val2

        # Sub-step 1: Identify position
        narrative = f"首先，我們從{place_name}開始計算。" if i == 0 else f"接下來計算{place_name}。"
        steps.append({
            "narrative": narrative,
            "phase": f"digit_{i}_identify"
        })

        # Sub-step 2: State the digits
        if borrow_in > 0:
            if val1 == 0:
                steps.append({
                    "narrative": f"{place_name}原本是 0，因為不夠借給右邊，所以它也向左邊借了 1 變成 10，然後借出 1，現在變成 9。下面是 {val2}。",
                    "phase": f"digit_{i}_state"
                })
            else:
                steps.append({
                    "narrative": f"{place_name}上面原本是 {val1}，但因為我們借出去了 1，所以變成 {effective_val1}，下面是 {val2}。",
                    "phase": f"digit_{i}_state"
                })
        elif i >= len(str2):
            # 減數在此位置沒有數字，視為 0
            steps.append({
                "narrative": f"{place_name}下面的減數沒有這一位，我們把它當作 0，上面是 {val1}。",
                "phase": f"digit_{i}_state"
            })
        else:
            steps.append({
                "narrative": f"{place_name}上面是 {val1}，下面是 {val2}。",
                "phase": f"digit_{i}_state"
            })


        # [INTERACTIVE] Ask for result
        if interactive_mode:
            if needs_borrow:
                steps.append({
                    "narrative": f"需要借位！借來之後上面是 {compute_val1}，請問 {compute_val1} 減 {val2} 等於多少呢？",
                    "phase": f"digit_{i}_interactive_ask"
                })
            else:
                steps.append({
                    "narrative": f"請問 {effective_val1} 減 {val2} 等於多少呢？",
                    "phase": f"digit_{i}_interactive_ask"
                })

        # Sub-step 3: Handle borrow
        if needs_borrow:
            next_place = places[i + 1] if i + 1 < len(places) else "下一位"
            if effective_val1 < 0:
                steps.append({
                    "narrative": f"剛才說過它向{next_place}借了 1，所以{place_name}現在可以當作 {compute_val1} 來計算。",
                    "phase": f"digit_{i}_borrow"
                })
            else:
                steps.append({
                    "narrative": f"{effective_val1} 比 {val2} 小，所以我們要向{next_place}借 1，{place_name}就變成 {compute_val1}。",
                    "phase": f"digit_{i}_borrow"
                })

        # Sub-step 4: Calculate
        steps.append({
            "narrative": f"我們計算：{compute_val1} 減 {val2}，等於 {result_digit}。",
            "phase": f"digit_{i}_calculate"
        })

        # Sub-step 5: Write result
        if i >= answer_len:
            # 這是前導零，已經計算過了，告訴學生不需寫下
            steps.append({
                "narrative": f"結果是 0，但因為在最左邊，所以我們不需要寫下來。",
                "phase": f"digit_{i}_write"
            })
        else:
            steps.append({
                "narrative": f"所以{place_name}寫下 {result_digit}。",
                "phase": f"digit_{i}_write"
            })

    # ========== Conclusion ==========
    steps.append({
        "narrative": "太棒了！我們已經完成了所有位數的計算。",
        "phase": "conclusion"
    })
    if is_negative:
        steps.append({
            "narrative": f"因為原本是 {num1} 減 {num2}，結果是負數，所以答案是 {answer}。",
            "phase": "conclusion"
        })
    else:
        steps.append({
            "narrative": f"讓我們確認一下答案：{num1} 減 {num2} 等於 {answer}。",
            "phase": "conclusion"
        })
    steps.append({
        "narrative": "記住，做直式減法時，要對齊位數、從右往左算，上面不夠減時記得向左借位，這樣就不會算錯了！",
        "phase": "conclusion"
    })

    return steps


def generate_vertical_subtraction_code(num1: int, num2: int, scene_name: str = "VerticalSubtraction", audio_steps: List[Dict] = None) -> str:
    """
    Generate complete Manim code for vertical subtraction.
    """
    is_negative = num1 < num2
    # 內部計算永遠用大減小，確保借位邏輯正確；顯示仍維持原始順序
    calc_num1, calc_num2 = (num2, num1) if is_negative else (num1, num2)
    str1 = str(calc_num1)  # 被減數（較大）
    str2 = str(calc_num2)  # 減數（較小）
    # 版面顯示：原始輸入順序
    disp_str1 = str(num1)
    disp_str2 = str(num2)
    answer = num1 - num2


    code_parts = []

    # 1. Imports
    code_parts.append(get_imports_code())

    # 2. Class Definition
    code_parts.append(f"class {scene_name}(Scene):")
    code_parts.append('    """')
    code_parts.append(f'    Perfect Vertical Subtraction: {num1} - {num2} = {answer}')
    code_parts.append('    Generated with modular subtraction template.')
    code_parts.append('    """')

    # 3. Setup & Subtitle Methods from Common
    code_parts.append(get_setup_code())
    # Subtitle methods: override common to support Chinese line-wrapping
    code_parts.append("""
    def _split_text(self, text, max_chars=26):
        if len(text) <= max_chars:
            return [text]
        lines = []
        while len(text) > 0:
            split_at = min(max_chars, len(text))
            for punct in ['，', '。', '、', '！', '？', ' ']:
                idx = text.rfind(punct, 0, max_chars + 1)
                if idx > 0:
                    split_at = idx + 1
                    break
            lines.append(text[:split_at])
            text = text[split_at:]
        return lines

    def create_wrapped_subtitle(self, text):
        new_sub = Text(text, font_size=30, font="Microsoft JhengHei", color=WHITE).to_edge(DOWN, buff=0.35)
        if new_sub.get_width() > self.camera.frame_width * 0.88:
            new_sub.scale_to_fit_width(self.camera.frame_width * 0.88)
        return new_sub

    def get_audio_duration(self, path):
        try:
            from mutagen.mp3 import MP3
            audio = MP3(path)
            return audio.info.length
        except Exception:
            return 2.0

    def update_subtitle(self, text, duration=1.0):
        lines = self._split_text(text, max_chars=26)
        time_per_line = max(duration / len(lines), 1.0)
        for line in lines:
            new_sub = self.create_wrapped_subtitle(line)
            self.remove(self.subtitle_area)
            self.subtitle_area = new_sub
            self.add(self.subtitle_area)
            self.play(Wait(time_per_line))
""")

    # 4. Construct Method
    code_parts.append("    def construct(self):")
    code_parts.append("        # ==================== Scene Setup ====================")
    code_parts.append("        self.camera.background_color = BLACK")
    code_parts.append("")
    code_parts.append(f'        title = Text("整數減法：{num1} - {num2}", font_size=36, font="Microsoft JhengHei", color=WHITE)')
    code_parts.append("        title.to_edge(UP, buff=0.5)")
    code_parts.append("        self.add(title)")
    code_parts.append("        ")

    # Number Construction
    code_parts.append("        # ==================== Number Construction ====================")
    # mob1 = 較大的被減數（用於計算），mob2 = 較小的減數
    code_parts.append(f'        str1 = "{str1}"')
    code_parts.append(f'        str2 = "{str2}"')
    code_parts.append("        ")
    code_parts.append("        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])")
    code_parts.append("        mob1.arrange(RIGHT, buff=0.2).move_to(UP * 1.0)")
    code_parts.append("        ")
    code_parts.append("        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])")
    code_parts.append("        mob2.arrange(RIGHT, buff=0.2)")
    code_parts.append("        mob2.next_to(mob1, DOWN, buff=0.5).align_to(mob1, RIGHT)")
    code_parts.append("        ")
    code_parts.append("        minus_sign = MathTex('-', font_size=60, color=BLUE)")
    code_parts.append("        # 取 mob1/mob2 中最左邊的隣線，確保減號不覆蓋任何數字")
    code_parts.append("        _leftmost_x = min(mob1.get_left()[0], mob2.get_left()[0])")
    code_parts.append("        minus_sign.move_to([_leftmost_x - 0.3 - minus_sign.get_width() / 2, mob2.get_center()[1], 0])")
    code_parts.append("        ")
    code_parts.append("        # 直線：預先計算 y 座標避免 next_to 將線水平偏移")
    code_parts.append("        line_y = mob2.get_bottom()[1] - 0.2")
    code_parts.append("        line = Line(")
    code_parts.append("            start=np.array([minus_sign.get_left()[0] - 0.2, line_y, 0]),")
    code_parts.append("            end=np.array([mob1.get_right()[0] + 0.2, line_y, 0]),")
    code_parts.append("            color=WHITE")
    code_parts.append("        )")
    code_parts.append("        ")
    code_parts.append("        ans_mobs = []")
    code_parts.append("        borrow_mobs = []")
    code_parts.append("        ")

    # Pre-compute borrow states for code generation
    max_len = max(len(str1), len(str2))
    answer_len = len(str(abs(answer)))  # 用絕對值計算位數，過濾前導零
    borrows = [0] * (max_len + 1)
    for i in range(max_len):
        v1 = int(str1[len(str1) - 1 - i]) if i < len(str1) else 0
        v2 = int(str2[len(str2) - 1 - i]) if i < len(str2) else 0
        eff_v1 = v1 - borrows[i]
        borrows[i + 1] = 1 if eff_v1 < v2 else 0

    # Animation Loop
    code_parts.append("        # ==================== Phase-Based Step Processing ====================")

    digit_phase_keywords = ('identify', 'state', 'borrow', 'calculate', 'write')

    if audio_steps:
        for idx, step in enumerate(audio_steps):
            phase = step.get('phase', '')
            narrative = step.get('narrative', '').replace('"', '\\"')

            # 移除了強制跳過前導零的邏輯，讓全部計算步驟走完，只在 write 階段不寫數字
            duration = step.get('duration', 2.0)
            audio_path = step.get('audio_path', '')

            code_parts.append(f"        # Step {idx}: [{phase}]")
            if audio_path:
                safe_audio_path = audio_path.replace("\\", "/")
                code_parts.append(f'        _dur_{idx} = self.get_audio_duration("{safe_audio_path}")')
                code_parts.append(f'        self.add_sound("{safe_audio_path}")')
                duration = f'_dur_{idx}'  # use dynamic variable
            else:
                duration = round(duration, 4)  # keep as float literal

            if 'interactive' in phase and 'ask' in phase:
                # Interactive: show question mark
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                digit_idx = int(phase.split('_')[1])
                col_idx2 = len(str2) - 1 - digit_idx
                x_pos = f"mob2[{col_idx2}].get_center()[0]" if col_idx2 >= 0 else "0"

                code_parts.append(f"        self.remove(self.subtitle_area)")
                code_parts.append(f"        self.subtitle_area = new_sub")
                code_parts.append(f"        self.add(self.subtitle_area)")
                code_parts.append(f"        q_mark = MathTex('?', font_size=60, color=YELLOW)")
                code_parts.append(f"        q_mark.move_to([{x_pos}, line.get_center()[1] - 0.6, 0])")
                code_parts.append(f"        self.play(FadeIn(q_mark, scale=0.5), run_time={duration})")
                code_parts.append(f"        self.wait(2.0)")
                code_parts.append(f"        self.play(FadeOut(q_mark), run_time=0.5)")

            elif 'intro' in phase:
                if idx == 0:
                    # First intro: fade in the scene
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append("        self.play(")
                    code_parts.append("            FadeIn(mob1), FadeIn(mob2),")
                    code_parts.append("            Write(minus_sign), Create(line),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            elif 'identify' in phase:
                # Highlight the digits at the current position
                parts = phase.split('_')
                digit_idx = int(parts[1])
                col_idx1 = len(str1) - 1 - digit_idx
                col_idx2 = len(str2) - 1 - digit_idx

                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")

                highlights = []
                if col_idx1 >= 0:
                    highlights.append(f"Circumscribe(mob1[{col_idx1}], color=YELLOW)")
                if col_idx2 >= 0:
                    highlights.append(f"Circumscribe(mob2[{col_idx2}], color=YELLOW)")

                if highlights:
                    code_parts.append("        self.play(")
                    code_parts.append(f"            {', '.join(highlights)},")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f"        self.wait({duration})")

            elif 'borrow' in phase:
                # Animate borrow: show new value above current digit + slash on donor digit
                parts = phase.split('_')
                digit_idx = int(parts[1])
                next_col_idx1 = len(str1) - 1 - (digit_idx + 1)
                cur_col_idx1 = len(str1) - 1 - digit_idx

                v1_cur = int(str1[len(str1) - 1 - digit_idx]) if digit_idx < len(str1) else 0
                borrow_in = borrows[digit_idx]
                eff_v1 = v1_cur - borrow_in
                compute_val1 = eff_v1 + 10  # after borrow

                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")

                if cur_col_idx1 >= 0:
                    code_parts.append(f"        borrow_label_{digit_idx} = MathTex('{compute_val1}', font_size=40, color=ORANGE)")
                    code_parts.append(f"        borrow_label_{digit_idx}.next_to(mob1[{cur_col_idx1}], UP, buff=0.1)")
                    code_parts.append(f"        borrow_mobs.append(borrow_label_{digit_idx})")

                    borrow_anims = [f"FadeIn(borrow_label_{digit_idx}, shift=UP*0.2)"]

                    if next_col_idx1 >= 0:
                        # Draw red slash over donor digit
                        code_parts.append(f"        slash_{digit_idx} = Line(")
                        code_parts.append(f"            mob1[{next_col_idx1}].get_corner(DL),")
                        code_parts.append(f"            mob1[{next_col_idx1}].get_corner(UR),")
                        code_parts.append(f"            color=RED, stroke_width=3")
                        code_parts.append(f"        )")
                        code_parts.append(f"        borrow_mobs.append(slash_{digit_idx})")
                        borrow_anims.append(f"Create(slash_{digit_idx})")

                    code_parts.append("        self.play(")
                    code_parts.append(f"            {', '.join(borrow_anims)},")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f"        self.wait({duration})")

            elif 'write' in phase and 'conclusion' not in phase:
                # Write the result digit below the line
                parts = phase.split('_')
                digit_idx = int(parts[1])

                v1 = int(str1[len(str1) - 1 - digit_idx]) if digit_idx < len(str1) else 0
                v2 = int(str2[len(str2) - 1 - digit_idx]) if digit_idx < len(str2) else 0
                borrow_in = borrows[digit_idx]
                eff_v1 = v1 - borrow_in
                compute_v1 = eff_v1 + 10 if eff_v1 < v2 else eff_v1
                result_digit = compute_v1 - v2

                if digit_idx >= answer_len:
                    # 前導零不寫下數字，只更新字幕
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                else:
                    # 答案數字的 x 座標：永遠用 mob1 對應列
                    # mob1 是最寬的數，所有位置都有對應的 digit，對位最精確
                    col_i1 = len(str1) - 1 - digit_idx  # 永遠 >= 0
                    x_pos = f"mob1[{col_i1}].get_center()[0]"

                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append(f"        digit_{digit_idx} = MathTex('{result_digit}', font_size=60, color=GREEN)")
                    code_parts.append(f"        digit_{digit_idx}.move_to([{x_pos}, line.get_center()[1] - 0.6, 0])")
                    code_parts.append("        self.play(")
                    code_parts.append(f"            FadeIn(digit_{digit_idx}, shift=UP * 0.2),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                    code_parts.append(f"        ans_mobs.append(digit_{digit_idx})")

            elif 'conclusion' in phase:
                if '已經完成' in narrative:
                    code_parts.append(f'        ans_mobs.reverse()')
                    code_parts.append(f'        full_answer = VGroup(*ans_mobs)')
                    code_parts.append(f'        answer_box = SurroundingRectangle(full_answer, color=GREEN, buff=0.15)')
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append("        self.play(")
                    code_parts.append("            Create(answer_box),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            else:
                # Default: just update subtitle
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            code_parts.append("        ")

    code_parts.append("        # Final wait")
    code_parts.append("        self.wait(2)")

    return "\n".join(code_parts)
