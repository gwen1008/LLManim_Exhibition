
"""
Integer Subtraction Template
Generates Manim code for step-by-step vertical subtraction with audio narration.
Handles borrowing (borrowing from higher digit).
"""
from typing import List, Dict, Any
from .common import get_imports_code, get_setup_code, get_subtitle_methods_code


def generate_subtraction_narrative(num1: int, num2: int, interactive_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Generate step-by-step narrative for vertical subtraction.
    Assumes num1 >= num2.
    """
    str1 = str(num1)
    str2 = str(num2)
    max_len = max(len(str1), len(str2))
    places = ["個位", "十位", "百位", "千位", "萬位", "十萬位", "百萬位"]
    steps = []

    # ========== Intro ==========
    steps.append({"narrative": "今天我們要學習整數的直式減法。", "phase": "intro"})
    steps.append({"narrative": f"題目是 {num1} 減 {num2}。", "phase": "intro"})
    steps.append({"narrative": "和加法一樣，兩個數字要靠右對齊，從個位數開始，由右往左計算。", "phase": "intro"})
    steps.append({"narrative": "當某一位不夠減時，我們要向高位借位，這個叫做「退位」。", "phase": "intro"})

    # ========== Pre-compute borrows ==========
    # borrows[i] = 1 means digit i has borrowed from digit i+1
    digits1 = [int(str1[len(str1) - 1 - i]) if i < len(str1) else 0 for i in range(max_len)]
    digits2 = [int(str2[len(str2) - 1 - i]) if i < len(str2) else 0 for i in range(max_len)]
    borrows = [0] * (max_len + 1)

    for i in range(max_len):
        top = digits1[i] - borrows[i]
        bot = digits2[i]
        if top < bot:
            borrows[i + 1] = 1
            top += 10
        # result digit = top - bot (computed in code gen too)

    # ========== Digit-by-Digit ==========
    for i in range(max_len):
        place_name = places[i] if i < len(places) else "下一位"
        top = digits1[i] - borrows[i]   # after being borrowed from
        bot = digits2[i]
        needs_borrow = top < bot
        if needs_borrow:
            top += 10
        result = top - bot

        intro_word = "首先，我們從" if i == 0 else "接下來計算"
        steps.append({"narrative": f"{intro_word}{place_name}。", "phase": f"digit_{i}_identify"})

        borrow_note = f"（已被高位借走 1，所以實際上是 {digits1[i]} - 1 = {digits1[i] - borrows[i]}）" if borrows[i] else ""
        steps.append({
            "narrative": f"{place_name}上面是 {digits1[i]}{borrow_note}，下面是 {bot}。",
            "phase": f"digit_{i}_state"
        })

        if needs_borrow:
            next_place = places[i + 1] if i + 1 < len(places) else "下一位"
            steps.append({
                "narrative": f"{digits1[i] - borrows[i]} 比 {bot} 小，不夠減，所以要向{next_place}借 1，借來後{place_name}變成 {top}。",
                "phase": f"digit_{i}_borrow"
            })
            steps.append({
                "narrative": f"現在 {top} 減 {bot}，等於 {result}，寫在{place_name}。",
                "phase": f"digit_{i}_calculate"
            })
        else:
            steps.append({
                "narrative": f"{top} 減 {bot}，等於 {result}，直接寫在{place_name}。",
                "phase": f"digit_{i}_calculate"
            })

    # ========== Conclusion ==========
    answer = num1 - num2
    steps.append({"narrative": "太棒了！所有位數都計算完了。", "phase": "conclusion"})
    steps.append({"narrative": f"讓我們確認答案：{num1} 減 {num2} 等於 {answer}。", "phase": "conclusion"})
    steps.append({"narrative": "記住，直式減法要注意對齊位數，不夠減時要向高位借位！", "phase": "conclusion"})

    return steps


def generate_vertical_subtraction_code(num1: int, num2: int, scene_name: str = "VerticalSubtraction", audio_steps: List[Dict] = None) -> str:
    """
    Generate complete Manim code for vertical subtraction.
    """
    str1 = str(num1)
    str2 = str(num2)
    answer = num1 - num2
    max_len = max(len(str1), len(str2))

    # Pre-compute borrows and results
    digits1 = [int(str1[len(str1) - 1 - i]) if i < len(str1) else 0 for i in range(max_len)]
    digits2 = [int(str2[len(str2) - 1 - i]) if i < len(str2) else 0 for i in range(max_len)]
    borrows = [0] * (max_len + 1)
    results = []
    for i in range(max_len):
        top = digits1[i] - borrows[i]
        bot = digits2[i]
        if top < bot:
            borrows[i + 1] = 1
            top += 10
        results.append(top - bot)

    code_parts = []
    code_parts.append(get_imports_code())
    code_parts.append(f"class {scene_name}(Scene):")
    code_parts.append('    """')
    code_parts.append(f'    Vertical Subtraction: {num1} - {num2} = {answer}')
    code_parts.append('    """')
    code_parts.append(get_setup_code())
    code_parts.append(get_subtitle_methods_code())
    code_parts.append("    def construct(self):")
    code_parts.append("        self.camera.background_color = BLACK")
    code_parts.append("")
    code_parts.append(f'        title = Text("整數減法：{num1} - {num2}", font_size=36, color=WHITE)')
    code_parts.append("        title.to_edge(UP, buff=0.5)")
    code_parts.append("        self.add(title)")
    code_parts.append("")
    code_parts.append(f'        str1 = "{str1}"')
    code_parts.append(f'        str2 = "{str2}"')
    code_parts.append("")
    code_parts.append("        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])")
    code_parts.append("        mob1.arrange(RIGHT, buff=0.2).move_to(UP * 1.0)")
    code_parts.append("        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])")
    code_parts.append("        mob2.arrange(RIGHT, buff=0.2)")
    code_parts.append("        mob2.next_to(mob1, DOWN, buff=0.5).align_to(mob1, RIGHT)")
    code_parts.append("        minus_sign = MathTex('-', font_size=60, color=BLUE)")
    code_parts.append("        minus_sign.next_to(mob2, LEFT, buff=0.3)")
    code_parts.append("        line = Line(")
    code_parts.append("            start=minus_sign.get_left() + LEFT * 0.2,")
    code_parts.append("            end=mob2.get_right() + RIGHT * 0.2,")
    code_parts.append("            color=WHITE")
    code_parts.append("        ).next_to(mob2, DOWN, buff=0.2)")
    code_parts.append("        ans_mobs = []")
    code_parts.append("        # borrow_mobs stores (digit_idx, crossed_mob, new_top_mob)")
    code_parts.append("        borrow_mobs = []")
    code_parts.append("")

    if audio_steps:
        for idx, step in enumerate(audio_steps):
            phase = step.get('phase', '')
            narrative = step.get('narrative', '').replace('"', '\\"')
            duration = step.get('duration', 2.0)
            audio_path = step.get('audio_path', '')
            if audio_path:
                duration += 0.2

            code_parts.append(f"        # Step {idx}: [{phase}]")
            if audio_path:
                code_parts.append(f'        self.add_sound("{audio_path}")')

            if 'intro' in phase:
                if idx == 0:
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
                parts = phase.split('_')
                digit_idx = int(parts[1])
                col1 = len(str1) - 1 - digit_idx
                col2 = len(str2) - 1 - digit_idx
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                highlights = []
                if col1 >= 0:
                    highlights.append(f"Circumscribe(mob1[{col1}], color=YELLOW)")
                if col2 >= 0:
                    highlights.append(f"Circumscribe(mob2[{col2}], color=YELLOW)")
                if highlights:
                    code_parts.append("        self.play(")
                    code_parts.append(f"            {', '.join(highlights)},")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f"        self.wait({duration})")

            elif 'borrow' in phase:
                parts = phase.split('_')
                digit_idx = int(parts[1])
                col1 = len(str1) - 1 - digit_idx
                # Show crossed-out original digit and new value above
                original_top = digits1[digit_idx] - borrows[digit_idx]
                new_top = original_top + 10
                # Cross out the top digit and show new value
                if col1 >= 0:
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append(f"        cross_{digit_idx} = Cross(mob1[{col1}], color=RED, stroke_width=3)")
                    code_parts.append(f"        new_top_{digit_idx} = MathTex('{new_top}', font_size=36, color=ORANGE)")
                    code_parts.append(f"        new_top_{digit_idx}.next_to(mob1[{col1}], UP, buff=0.1)")
                    code_parts.append("        self.play(")
                    code_parts.append(f"            Create(cross_{digit_idx}),")
                    code_parts.append(f"            FadeIn(new_top_{digit_idx}),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                    code_parts.append(f"        borrow_mobs.append(cross_{digit_idx})")
                    code_parts.append(f"        borrow_mobs.append(new_top_{digit_idx})")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            elif 'calculate' in phase:
                parts = phase.split('_')
                digit_idx = int(parts[1])
                rem = results[digit_idx]
                col2 = len(str2) - 1 - digit_idx
                if col2 >= 0:
                    x_pos = f"mob2[{col2}].get_center()[0]"
                else:
                    x_pos = f"mob2[0].get_center()[0] - ({digit_idx} - {len(str2)-1}) * (mob2[0].width + 0.2)"

                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append(f"        digit_{digit_idx} = MathTex('{rem}', font_size=60, color=GREEN)")
                code_parts.append(f"        digit_{digit_idx}.move_to([{x_pos}, line.get_center()[1] - 0.6, 0])")
                code_parts.append("        self.play(")
                code_parts.append(f"            FadeIn(digit_{digit_idx}, shift=UP * 0.2),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        ans_mobs.append(digit_{digit_idx})")

            elif 'conclusion' in phase:
                if '已經' in narrative or '完成' in narrative or '太棒了' in narrative:
                    code_parts.append(f'        ans_mobs_rev = list(reversed(ans_mobs))')
                    code_parts.append(f'        full_answer = VGroup(*ans_mobs_rev)')
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
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            code_parts.append("")

    code_parts.append("        self.wait(2)")
    return "\n".join(code_parts)
