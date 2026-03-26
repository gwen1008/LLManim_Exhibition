
"""
Integer Long Division Template
Generates Manim code for step-by-step long division with audio narration.
Format: num1 ÷ num2 (dividend ÷ divisor), assumes integer result (no remainder handling shown).
"""
from typing import List, Dict, Any
from .common import get_imports_code, get_setup_code, get_subtitle_methods_code


def generate_division_narrative(num1: int, num2: int, interactive_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Generate step-by-step narrative for long division.
    num1 = dividend, num2 = divisor.
    """
    steps = []

    # ========== Intro ==========
    steps.append({"narrative": "今天我們要學習整數的長除法。", "phase": "intro"})
    steps.append({"narrative": f"題目是 {num1} 除以 {num2}。", "phase": "intro"})
    steps.append({"narrative": "長除法的步驟是：除、乘、減、落，反覆進行，直到沒有剩餘數字為止。", "phase": "intro"})
    steps.append({"narrative": "我們從被除數的最高位開始，逐步往右進行。", "phase": "intro"})

    # ========== Long Division Steps ==========
    str1 = str(num1)
    quotient_digits = []
    remainder = 0
    step_data = []  # (current_dividend, quotient_digit, product, new_remainder)

    for i, ch in enumerate(str1):
        current = remainder * 10 + int(ch)
        q = current // num2
        product = q * num2
        new_remainder = current - product
        step_data.append((current, q, product, new_remainder))
        quotient_digits.append(q)
        remainder = new_remainder

    for i, (current, q, product, new_remainder) in enumerate(step_data):
        place_desc = f"第 {i+1} 步"

        steps.append({
            "narrative": f"{place_desc}：目前的被除數是 {current}。",
            "phase": f"step_{i}_divide"
        })
        steps.append({
            "narrative": f"{current} 除以 {num2}，商是 {q}，寫在上方。",
            "phase": f"step_{i}_quotient"
        })
        steps.append({
            "narrative": f"{q} 乘以 {num2} 等於 {product}，寫在下方。",
            "phase": f"step_{i}_multiply"
        })
        steps.append({
            "narrative": f"{current} 減去 {product}，餘數是 {new_remainder}。",
            "phase": f"step_{i}_subtract"
        })
        if i < len(str1) - 1:
            next_digit = str1[i + 1]
            steps.append({
                "narrative": f"把下一位 {next_digit} 落下來，得到 {new_remainder * 10 + int(next_digit)}，繼續除。",
                "phase": f"step_{i}_bring_down"
            })

    # ========== Conclusion ==========
    quotient = num1 // num2
    final_remainder = num1 % num2
    steps.append({"narrative": "所有位數都處理完了！", "phase": "conclusion"})
    if final_remainder == 0:
        steps.append({"narrative": f"{num1} 除以 {num2} 等於 {quotient}，整除，沒有餘數。", "phase": "conclusion"})
    else:
        steps.append({"narrative": f"{num1} 除以 {num2} 等於 {quotient} 餘 {final_remainder}。", "phase": "conclusion"})
    steps.append({"narrative": "記住長除法四步驟：除、乘、減、落，每一步都要認真計算！", "phase": "conclusion"})

    return steps


def generate_long_division_code(num1: int, num2: int, scene_name: str = "LongDivision", audio_steps: List[Dict] = None) -> str:
    """
    Generate complete Manim code for long division.
    Layout: divisor ) dividend  (standard long division bracket notation)
    """
    str1 = str(num1)
    quotient = num1 // num2
    final_remainder = num1 % num2

    # Pre-compute all steps
    step_data = []
    remainder = 0
    quotient_digits = []
    for ch in str1:
        current = remainder * 10 + int(ch)
        q = current // num2
        product = q * num2
        new_remainder = current - product
        step_data.append((current, q, product, new_remainder))
        quotient_digits.append(q)
        remainder = new_remainder

    code_parts = []
    code_parts.append(get_imports_code())
    code_parts.append(f"class {scene_name}(Scene):")
    code_parts.append('    """')
    code_parts.append(f'    Long Division: {num1} ÷ {num2} = {quotient}' + (f' R {final_remainder}' if final_remainder else ''))
    code_parts.append('    """')
    code_parts.append(get_setup_code())
    code_parts.append(get_subtitle_methods_code())
    code_parts.append("    def construct(self):")
    code_parts.append("        self.camera.background_color = BLACK")
    code_parts.append("")
    code_parts.append(f'        title = Text("整數除法：{num1} ÷ {num2}", font_size=36, color=WHITE)')
    code_parts.append("        title.to_edge(UP, buff=0.5)")
    code_parts.append("        self.add(title)")
    code_parts.append("")

    # Layout constants
    code_parts.append("        # ===== Long Division Layout =====")
    code_parts.append("        # Divisor on left, dividend under bracket")
    code_parts.append(f'        divisor_tex = MathTex("{num2}", font_size=60, color=BLUE)')
    code_parts.append("        divisor_tex.move_to(LEFT * 3)")
    code_parts.append(f'        dividend_str = "{str1}"')
    code_parts.append("        dividend_mobs = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in dividend_str])")
    code_parts.append("        dividend_mobs.arrange(RIGHT, buff=0.3)")
    code_parts.append("        dividend_mobs.next_to(divisor_tex, RIGHT, buff=0.5)")
    code_parts.append("        # Division bracket: vertical line + horizontal line over dividend")
    code_parts.append("        v_line = Line(")
    code_parts.append("            start=divisor_tex.get_right() + RIGHT * 0.15 + UP * 0.6,")
    code_parts.append("            end=divisor_tex.get_right() + RIGHT * 0.15 + DOWN * 0.6,")
    code_parts.append("            color=WHITE")
    code_parts.append("        )")
    code_parts.append("        h_line = Line(")
    code_parts.append("            start=divisor_tex.get_right() + RIGHT * 0.15 + UP * 0.6,")
    code_parts.append("            end=dividend_mobs.get_right() + RIGHT * 0.2 + UP * 0.6,")
    code_parts.append("            color=WHITE")
    code_parts.append("        )")
    code_parts.append("        # Quotient digits appear above the h_line")
    code_parts.append("        quotient_mobs = []")
    code_parts.append("        # Subtraction work area mobs")
    code_parts.append("        work_mobs = []")
    code_parts.append("        digit_w = dividend_mobs[0].get_width() + 0.3")
    code_parts.append("        ref_x = dividend_mobs[0].get_center()[0]  # leftmost dividend digit x")
    code_parts.append("        base_y = dividend_mobs[0].get_center()[1]")
    code_parts.append("")

    if audio_steps:
        current_work_y_offset = [0]  # mutable for closure-like tracking

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
                    code_parts.append("            FadeIn(divisor_tex), FadeIn(dividend_mobs),")
                    code_parts.append("            Create(v_line), Create(h_line),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            elif phase.startswith('step_') and '_divide' in phase:
                i = int(phase.split('_')[1])
                current, q, product, new_remainder = step_data[i]
                # Highlight the dividend digits used so far (0..i)
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append("        self.play(")
                code_parts.append(f"            Circumscribe(dividend_mobs[{i}], color=YELLOW),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")

            elif phase.startswith('step_') and '_quotient' in phase:
                i = int(phase.split('_')[1])
                q = step_data[i][1]
                # Place quotient digit above h_line, aligned with dividend_mobs[i]
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append(f"        q_{i} = MathTex('{q}', font_size=60, color=GREEN)")
                code_parts.append(f"        q_{i}.move_to([dividend_mobs[{i}].get_center()[0], h_line.get_center()[1] + 0.6, 0])")
                code_parts.append("        self.play(")
                code_parts.append(f"            FadeIn(q_{i}, shift=UP*0.2),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        quotient_mobs.append(q_{i})")

            elif phase.startswith('step_') and '_multiply' in phase:
                i = int(phase.split('_')[1])
                current, q, product, new_remainder = step_data[i]
                product_str = str(product)
                # product shown below current segment, right-aligned to dividend_mobs[i]
                y_offset = current_work_y_offset[0]
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append(f"        prod_{i}_mobs = VGroup(*[MathTex(c, font_size=48, color=ORANGE) for c in '{product_str}'])")
                code_parts.append(f"        prod_{i}_mobs.arrange(RIGHT, buff=0.3)")
                code_parts.append(f"        prod_{i}_mobs.move_to([dividend_mobs[{i}].get_center()[0], base_y - 1.0 - {y_offset} * 1.6, 0])")
                code_parts.append("        self.play(")
                code_parts.append(f"            FadeIn(prod_{i}_mobs),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        work_mobs.append(prod_{i}_mobs)")

            elif phase.startswith('step_') and '_subtract' in phase:
                i = int(phase.split('_')[1])
                current, q, product, new_remainder = step_data[i]
                y_offset = current_work_y_offset[0]
                # Draw subtraction line and show remainder
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                code_parts.append(f"        sub_line_{i} = Line(")
                code_parts.append(f"            start=dividend_mobs[{i}].get_center() + LEFT * 0.3 + DOWN * (1.0 + {y_offset} * 1.6 + 0.4),")
                code_parts.append(f"            end=dividend_mobs[{i}].get_center() + RIGHT * 0.3 + DOWN * (1.0 + {y_offset} * 1.6 + 0.4),")
                code_parts.append("            color=WHITE")
                code_parts.append("        )")
                code_parts.append(f"        rem_{i} = MathTex('{new_remainder}', font_size=48, color=WHITE)")
                code_parts.append(f"        rem_{i}.move_to([dividend_mobs[{i}].get_center()[0], base_y - 1.0 - {y_offset} * 1.6 - 0.8, 0])")
                code_parts.append("        self.play(")
                code_parts.append(f"            Create(sub_line_{i}), FadeIn(rem_{i}),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        work_mobs.append(rem_{i})")
                current_work_y_offset[0] += 1

            elif phase.startswith('step_') and '_bring_down' in phase:
                i = int(phase.split('_')[1])
                next_digit = str1[i + 1]
                y_offset = current_work_y_offset[0]
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                # Animate the next dividend digit dropping down
                code_parts.append(f"        brought_{i} = MathTex('{next_digit}', font_size=48, color=YELLOW)")
                code_parts.append(f"        brought_{i}.move_to([dividend_mobs[{i+1}].get_center()[0], base_y - 1.0 - {y_offset - 1} * 1.6 - 0.8, 0])")
                code_parts.append("        self.play(")
                code_parts.append(f"            FadeIn(brought_{i}, shift=DOWN*0.5),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        work_mobs.append(brought_{i})")

            elif 'conclusion' in phase:
                if '完成' in narrative or '所有' in narrative:
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append("        answer_box = SurroundingRectangle(VGroup(*quotient_mobs), color=GREEN, buff=0.15)")
                    code_parts.append(f"        self.play(Create(answer_box), run_time={duration})")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
            else:
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            code_parts.append("")

    code_parts.append("        self.wait(2)")
    return "\n".join(code_parts)
