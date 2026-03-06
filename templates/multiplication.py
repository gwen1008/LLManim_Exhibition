
"""
Integer Multiplication Template
Generates Manim code for step-by-step vertical multiplication with audio narration.
Uses partial products: multiply each digit of num2 by all digits of num1, then sum.
"""
from typing import List, Dict, Any
from .common import get_imports_code, get_setup_code, get_subtitle_methods_code


def generate_multiplication_narrative(num1: int, num2: int, interactive_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Generate step-by-step narrative for vertical multiplication.
    num1 is the multiplicand (top), num2 is the multiplier (bottom).
    """
    str1 = str(num1)
    str2 = str(num2)
    answer = num1 * num2
    places = ["個位", "十位", "百位", "千位", "萬位", "十萬位"]
    steps = []

    # ========== Intro ==========
    steps.append({"narrative": "今天我們要學習整數的直式乘法。", "phase": "intro"})
    steps.append({"narrative": f"題目是 {num1} 乘以 {num2}。", "phase": "intro"})
    steps.append({"narrative": "直式乘法的做法是：用乘數的每一位分別去乘被乘數，得到「部分積」，最後再把所有部分積加起來。", "phase": "intro"})
    steps.append({"narrative": "我們從乘數的個位數開始，由右往左計算每一位。", "phase": "intro"})

    # ========== Partial Products ==========
    partial_products = []
    for j in range(len(str2)):
        d2 = int(str2[len(str2) - 1 - j])
        place2 = places[j] if j < len(places) else "下一位"

        steps.append({
            "narrative": f"{'首先' if j == 0 else '接著'}，用乘數的{place2} {d2} 去乘被乘數 {num1}。",
            "phase": f"partial_{j}_intro"
        })

        carry = 0
        row_digits = []
        for i in range(len(str1)):
            d1 = int(str1[len(str1) - 1 - i])
            product = d1 * d2 + carry
            carry = product // 10
            rem = product % 10
            row_digits.append(rem)

            if carry > 0:
                steps.append({
                    "narrative": f"{d1} 乘以 {d2}{f'，加上進位 {product - rem}//10' if carry > 0 else ''}，等於 {product}，寫下 {rem}，進位 {carry}。",
                    "phase": f"partial_{j}_digit_{i}"
                })
            else:
                steps.append({
                    "narrative": f"{d1} 乘以 {d2} 等於 {product}，寫下 {product}。",
                    "phase": f"partial_{j}_digit_{i}"
                })

        if carry > 0:
            row_digits.append(carry)
            steps.append({
                "narrative": f"最後還有進位 {carry}，也寫下來。",
                "phase": f"partial_{j}_final_carry"
            })

        # partial product value
        pp_val = d2 * num1
        partial_products.append(pp_val)
        steps.append({
            "narrative": f"{num1} 乘以 {d2} 等於 {pp_val}。{'因為是' + place2 + '，這個部分積要向左移' + str(j) + '位。' if j > 0 else ''}",
            "phase": f"partial_{j}_result"
        })

    # ========== Final Sum ==========
    if len(str2) > 1:
        steps.append({"narrative": f"現在把所有部分積加起來。", "phase": "sum_intro"})
        steps.append({
            "narrative": f"全部加起來，{num1} 乘以 {num2} 等於 {answer}。",
            "phase": "sum_result"
        })

    # ========== Conclusion ==========
    steps.append({"narrative": "太棒了！計算完成。", "phase": "conclusion"})
    steps.append({"narrative": f"最終答案：{num1} × {num2} = {answer}。", "phase": "conclusion"})
    steps.append({"narrative": "記住，直式乘法要注意部分積的位移，每往左一位就代表乘以 10！", "phase": "conclusion"})

    return steps


def generate_vertical_multiplication_code(num1: int, num2: int, scene_name: str = "VerticalMultiplication", audio_steps: List[Dict] = None) -> str:
    """
    Generate complete Manim code for vertical multiplication.
    """
    str1 = str(num1)
    str2 = str(num2)
    answer = num1 * num2

    # Pre-compute partial products and their digit rows
    partial_rows = []
    for j in range(len(str2)):
        d2 = int(str2[len(str2) - 1 - j])
        carry = 0
        row = []
        for i in range(len(str1)):
            d1 = int(str1[len(str1) - 1 - i])
            prod = d1 * d2 + carry
            carry = prod // 10
            row.append(prod % 10)
        if carry:
            row.append(carry)
        partial_rows.append(row)  # digits right-to-left, shifted by j

    code_parts = []
    code_parts.append(get_imports_code())
    code_parts.append(f"class {scene_name}(Scene):")
    code_parts.append('    """')
    code_parts.append(f'    Vertical Multiplication: {num1} × {num2} = {answer}')
    code_parts.append('    """')
    code_parts.append(get_setup_code())
    code_parts.append(get_subtitle_methods_code())
    code_parts.append("    def construct(self):")
    code_parts.append("        self.camera.background_color = BLACK")
    code_parts.append("")
    code_parts.append(f'        title = Text("整數乘法：{num1} × {num2}", font_size=36, color=WHITE)')
    code_parts.append("        title.to_edge(UP, buff=0.5)")
    code_parts.append("        self.add(title)")
    code_parts.append("")
    code_parts.append(f'        str1 = "{str1}"')
    code_parts.append(f'        str2 = "{str2}"')
    code_parts.append("")
    code_parts.append("        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])")
    code_parts.append("        mob1.arrange(RIGHT, buff=0.2).move_to(UP * 1.5)")
    code_parts.append("        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])")
    code_parts.append("        mob2.arrange(RIGHT, buff=0.2)")
    code_parts.append("        mob2.next_to(mob1, DOWN, buff=0.5).align_to(mob1, RIGHT)")
    code_parts.append("        times_sign = MathTex('\\\\times', font_size=60, color=BLUE)")
    code_parts.append("        times_sign.next_to(mob2, LEFT, buff=0.3)")
    code_parts.append("        line1 = Line(")
    code_parts.append("            start=times_sign.get_left() + LEFT * 0.2,")
    code_parts.append("            end=mob2.get_right() + RIGHT * 0.2,")
    code_parts.append("            color=WHITE")
    code_parts.append("        ).next_to(mob2, DOWN, buff=0.2)")
    code_parts.append("        # partial_row_mobs[j] = list of Tex mobs for row j")
    code_parts.append("        partial_row_mobs = []")
    code_parts.append("        # Reference x for rightmost column (ones place of mob1)")
    code_parts.append("        ref_x = mob1[-1].get_center()[0]")
    code_parts.append("        digit_w = mob1[-1].get_width() + 0.2  # digit width + buff")
    code_parts.append("")

    if audio_steps:
        # track which partial rows have been rendered
        rendered_partials = []

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

            if 'intro' in phase and 'partial' not in phase and 'sum' not in phase:
                if idx == 0:
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append("        self.play(")
                    code_parts.append("            FadeIn(mob1), FadeIn(mob2),")
                    code_parts.append("            Write(times_sign), Create(line1),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            elif phase.startswith('partial_') and '_intro' in phase:
                j = int(phase.split('_')[1])
                d2 = int(str2[len(str2) - 1 - j])
                col2 = len(str2) - 1 - j
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                if col2 >= 0:
                    code_parts.append("        self.play(")
                    code_parts.append(f"            Circumscribe(mob2[{col2}], color=YELLOW),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f"        self.wait({duration})")

            elif phase.startswith('partial_') and '_result' in phase:
                # Render the full partial product row
                j = int(phase.split('_')[1])
                row = partial_rows[j]
                # row[0] = ones digit, row[1] = tens, etc. (right-to-left)
                # shift j positions to the left from ones column
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                # Calculate y position: below line1, each partial row stacks down
                code_parts.append(f"        row_{j}_mobs = []")
                for k, digit in enumerate(row):
                    # column from right: k + j (shift)
                    col_offset = k + j
                    code_parts.append(f"        d_{j}_{k} = MathTex('{digit}', font_size=48, color=YELLOW)")
                    code_parts.append(f"        d_{j}_{k}.move_to([ref_x - {col_offset} * digit_w, line1.get_center()[1] - 0.6 - {j} * 0.8, 0])")
                    code_parts.append(f"        row_{j}_mobs.append(d_{j}_{k})")
                code_parts.append(f"        partial_row_mobs.append(row_{j}_mobs)")
                code_parts.append("        self.play(")
                code_parts.append(f"            *[FadeIn(m, shift=UP*0.2) for m in row_{j}_mobs],")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                rendered_partials.append(j)

            elif phase == 'sum_intro':
                # Draw line2 below all partial rows
                n_rows = len(str2)
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append(f"        last_row_y = line1.get_center()[1] - 0.6 - {n_rows - 1} * 0.8")
                code_parts.append("        line2 = Line(")
                code_parts.append("            start=times_sign.get_left() + LEFT * 0.2,")
                code_parts.append(f"            end=mob1.get_right() + RIGHT * {1.0 + 0.2 * (len(str2) - 1)},")
                code_parts.append("            color=WHITE")
                code_parts.append("        ).move_to([0, last_row_y - 0.5, 0])")
                code_parts.append(f"        self.play(Create(line2), run_time={duration})")

            elif phase == 'sum_result':
                ans_str = str(answer)
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append(f"        ans_mobs = []")
                for k, d in enumerate(reversed(ans_str)):
                    code_parts.append(f"        ans_{k} = MathTex('{d}', font_size=60, color=GREEN)")
                    code_parts.append(f"        ans_{k}.move_to([ref_x - {k} * digit_w, line2.get_center()[1] - 0.6, 0])")
                    code_parts.append(f"        ans_mobs.append(ans_{k})")
                code_parts.append("        self.play(")
                code_parts.append("            *[FadeIn(m, shift=UP*0.2) for m in ans_mobs],")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append("        answer_box = SurroundingRectangle(VGroup(*ans_mobs), color=GREEN, buff=0.15)")
                code_parts.append(f"        self.play(Create(answer_box), run_time=1.0)")

            elif 'conclusion' in phase:
                if '太棒了' in narrative or '完成' in narrative:
                    # Single-digit multiplier: no sum_result step, draw answer directly
                    if len(str2) == 1:
                        ans_str = str(answer)
                        code_parts.append(f'        ans_mobs_c = []')
                        for k, d in enumerate(reversed(ans_str)):
                            code_parts.append(f"        ans_c_{k} = MathTex('{d}', font_size=60, color=GREEN)")
                            code_parts.append(f"        ans_c_{k}.move_to([ref_x - {k} * digit_w, line1.get_center()[1] - 0.6, 0])")
                            code_parts.append(f"        ans_mobs_c.append(ans_c_{k})")
                        code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                        code_parts.append("        self.remove(self.subtitle_area)")
                        code_parts.append("        self.subtitle_area = new_sub")
                        code_parts.append("        self.add(self.subtitle_area)")
                        code_parts.append("        self.play(")
                        code_parts.append("            *[FadeIn(m, shift=UP*0.2) for m in ans_mobs_c],")
                        code_parts.append(f"            run_time={duration}")
                        code_parts.append("        )")
                        code_parts.append("        answer_box_c = SurroundingRectangle(VGroup(*ans_mobs_c), color=GREEN, buff=0.15)")
                        code_parts.append(f"        self.play(Create(answer_box_c), run_time=1.0)")
                    else:
                        code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
            else:
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            code_parts.append("")

    code_parts.append("        self.wait(2)")
    return "\n".join(code_parts)
