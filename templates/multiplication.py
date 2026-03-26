"""
Integer Multiplication Template
Generates Manim code for step-by-step vertical multiplication with audio narration and interactive elements.
"""
from typing import List, Dict, Any
from .common import get_imports_code, get_setup_code, get_subtitle_methods_code

def generate_multiplication_narrative(num1: int, num2: int, interactive_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Generate step-by-step narrative for vertical multiplication.
    """
    str1 = str(num1)
    str2 = str(num2)
    steps = []
    
    # ========== Intro Phase ==========
    steps.append({
        "narrative": "今天我們要學習整數的直式乘法。",
        "phase": "intro"
    })
    steps.append({
        "narrative": f"題目是 {num1} 乘以 {num2}。",
        "phase": "intro"
    })
    steps.append({
        "narrative": "一樣要記得把數字靠右對齊，從個位數開始計算。",
        "phase": "intro"
    })
    
    # ========== Calculation Phase ==========
    places = ["個位", "十位", "百位", "千位", "萬位", "十萬位", "百萬位", "千萬位", "億位", "十億位", "百億位", "千億位", "兆位", "十兆位", "百兆位"]
    
    for i in range(len(str2)):
        idx2 = len(str2) - 1 - i
        val2 = int(str2[idx2])
        place_name2 = places[i] if i < len(places) else "下一位"
        
        if len(str2) > 1:
            steps.append({
                "narrative": f"現在用下面{place_name2}的 {val2}，分別去乘以上的每一位數字。",
                "phase": f"row_{i}_start"
            })
            if i > 0:
                steps.append({
                    "narrative": f"因為這裡是{place_name2}，所以算出來的結果要從{place_name2}開始寫，後面補 {i} 個 0。",
                    "phase": f"row_{i}_padding"
                })

        carry = 0
        for j in range(len(str1)):
            idx1 = len(str1) - 1 - j
            val1 = int(str1[idx1])
            place_name1 = places[j] if j < len(places) else "下一位"
            
            prod = val1 * val2
            current_sum = prod + carry
            new_carry = current_sum // 10
            remainder = current_sum % 10
            
            steps.append({
                "narrative": f"用 {val2} 乘以上面{place_name1}的 {val1}。",
                "phase": f"digit_{i}_{j}_identify"
            })
            
            if interactive_mode:
                if carry > 0:
                    steps.append({
                        "narrative": f"{val2} 乘以 {val1} 等於 {prod}，再加上進位的 {carry}，等於多少呢？",
                        "phase": f"digit_{i}_{j}_interactive_ask_prod"
                    })
                else:
                    steps.append({
                        "narrative": f"{val2} 乘以 {val1} 等於多少呢？",
                        "phase": f"digit_{i}_{j}_interactive_ask_prod"
                    })
            
            if carry > 0:
                steps.append({
                    "narrative": f"{val2} 乘以 {val1} 等於 {prod}，加上進位的 {carry}，等於 {current_sum}。",
                    "phase": f"digit_{i}_{j}_calculate"
                })
            else:
                steps.append({
                    "narrative": f"{val2} 乘以 {val1} 等於 {current_sum}。",
                    "phase": f"digit_{i}_{j}_calculate"
                })
                
            if new_carry > 0:
                next_place = places[j+1] if j+1 < len(places) else '下一位'
                steps.append({
                    "narrative": f"寫下 {remainder}，並把 {new_carry} 進到{next_place}。",
                    "phase": f"digit_{i}_{j}_write_carry"
                })
            else:
                steps.append({
                    "narrative": f"寫下 {remainder}。",
                    "phase": f"digit_{i}_{j}_write_no_carry"
                })
                
            carry = new_carry
            
        if carry > 0:
            steps.append({
                "narrative": f"最後把進位的 {carry} 寫下來。",
                "phase": f"digit_{i}_{len(str1)}_write_final_carry"
            })
            
    # ========== Addition Phase ==========
    if len(str2) > 1:
        steps.append({
            "narrative": "最後，我們把這幾個乘出來的結果全部加起來。",
            "phase": "add_partial_products"
        })
        
    answer = num1 * num2
    steps.append({
        "narrative": f"這樣我們就算出答案了，{num1} 乘以 {num2} 等於 {answer}。",
        "phase": "conclusion"
    })
    
    return steps

def generate_vertical_multiplication_code(num1: int, num2: int, scene_name: str = "VerticalMultiplication", audio_steps: List[Dict] = None) -> str:
    """
    Generate complete Manim code for vertical multiplication.
    """
    str1 = str(num1)
    str2 = str(num2)
    answer = num1 * num2
    
    code_parts = []
    
    # 1. Imports
    code_parts.append(get_imports_code())
    
    # 2. Class Definition
    code_parts.append(f"class {scene_name}(Scene):")
    code_parts.append('    """')
    code_parts.append(f'    Perfect Vertical Multiplication: {num1} * {num2} = {answer}')
    code_parts.append('    """')
    
    # 3. Setup & Subtitle Methods from Common
    code_parts.append(get_setup_code())
    code_parts.append(get_subtitle_methods_code())
    
    # 4. Construct Method
    code_parts.append("    def construct(self):")
    code_parts.append("        # ==================== Scene Setup ====================")
    code_parts.append("        self.camera.background_color = BLACK")
    code_parts.append("")
    code_parts.append(f'        title = Text("整數乘法：{num1} × {num2}", font_size=36, color=WHITE)')
    code_parts.append("        title.to_edge(UP, buff=0.5)")
    code_parts.append("        self.add(title)")
    code_parts.append("        ")
    
    # Number Construction (Visuals)
    code_parts.append("        # ==================== Number Construction ====================")
    code_parts.append(f'        str1 = "{str1}"')
    code_parts.append(f'        str2 = "{str2}"')
    code_parts.append("        ")
    code_parts.append("        # Build number mobjects grid")
    code_parts.append("        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])")
    code_parts.append("        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])")
    code_parts.append("        ")
    code_parts.append("        col_spacing = 0.55")
    code_parts.append("        for i, m in enumerate(reversed(mob1)):")
    code_parts.append("            m.move_to([-i * col_spacing, 1.0, 0])")
    code_parts.append("        for i, m in enumerate(reversed(mob2)):")
    code_parts.append("            m.move_to([-i * col_spacing, 0.0, 0])")
    code_parts.append("        ")
    code_parts.append("        calc_group = VGroup(mob1, mob2)")
    code_parts.append("        calc_group.center().shift(UP * 1.0)")
    code_parts.append("        ")
    code_parts.append("        y_diff = mob1.get_y() - mob2.get_y()")
    code_parts.append("        base_x = mob1[-1].get_center()[0]")
    code_parts.append("        ")
    code_parts.append("        def get_col_x(col_idx):")
    code_parts.append("            return base_x - col_idx * col_spacing")
    code_parts.append("        ")
    code_parts.append("        times_sign = MathTex('\\\\times', font_size=60, color=BLUE)")
    code_parts.append("        times_sign_x = get_col_x(max(len(str1), len(str2))) - 0.2")
    code_parts.append("        times_sign.move_to([times_sign_x, mob2.get_y(), 0])")
    code_parts.append("        ")
    code_parts.append("        line_y = mob2.get_y() - y_diff * 0.5")
    code_parts.append("        end_x = base_x + 0.4")
    code_parts.append("        start_x = times_sign.get_left()[0] - 0.3")
    code_parts.append("        line = Line(")
    code_parts.append("            start=[start_x, line_y, 0],")
    code_parts.append("            end=[end_x, line_y, 0],")
    code_parts.append("            color=WHITE")
    code_parts.append("        )")
    code_parts.append("        ")
    code_parts.append("        row_mobs = []")
    code_parts.append("        carry_mobs = VGroup()")
    code_parts.append("        self.add(carry_mobs)")
    code_parts.append("        ")

    # Animation Loop
    code_parts.append("        # ==================== Phase-Based Step Processing ====================")
    
    if audio_steps:
        # Prepopulate carries for correctly writing digits locally
        carries_matrix = [] # [row_i][col_j] -> carry generated when multiplying mob2[i] and mob1[j]
        for i in range(len(str2)):
            val2 = int(str2[len(str2) - 1 - i])
            carries = [0] * (len(str1) + 1)
            c = 0
            for j in range(len(str1)):
                val1 = int(str1[len(str1) - 1 - j])
                prod = val1 * val2 + c
                c = prod // 10
                carries[j] = c
            if c > 0:
                carries[len(str1)] = 0
            carries_matrix.append(carries)

        for idx, step in enumerate(audio_steps):
            phase = step.get('phase', '')
            narrative = step.get('narrative', '').replace('"', '\\"')
            duration = step.get('duration', 2.0)
            audio_path = step.get('audio_path', '')
            
            if audio_path:
                duration += 0.2  # Audio buffer
            
            code_parts.append(f"        # Step {idx}: [{phase}]")
            if audio_path:
                audio_path_normalized = audio_path.replace('\\', '/')
                code_parts.append(f'        self.add_sound("{audio_path_normalized}")')
            
            if phase == 'intro':
                if idx == 0:
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append("        self.play(")
                    code_parts.append("            FadeIn(mob1), FadeIn(mob2),")
                    code_parts.append("            Write(times_sign), Create(line),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
            
            elif phase.startswith('row_') and 'start' in phase:
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                code_parts.append("        if len(carry_mobs) > 0:")
                code_parts.append("            self.play(FadeOut(carry_mobs), run_time=0.5)")
                code_parts.append("            carry_mobs.submobjects = []")

            elif phase.startswith('row_') and 'padding' in phase:
                row_idx = int(phase.split('_')[1])
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                code_parts.append("        padding_zeros = VGroup()")
                code_parts.append(f"        for pd in range({row_idx}):")
                code_parts.append("            x_pos = get_col_x(pd)")
                code_parts.append(f"            y_pos = mob2.get_y() - y_diff * ({row_idx} + 1)")
                code_parts.append(f"            zero_mob = MathTex('0', font_size=60, color=GRAY)")
                code_parts.append(f"            zero_mob.move_to([x_pos, y_pos, 0])")
                code_parts.append(f"            padding_zeros.add(zero_mob)")
                code_parts.append("        if len(padding_zeros) > 0:")
                code_parts.append("            self.play(FadeIn(padding_zeros), run_time=0.5)")
                code_parts.append(f"            row_mobs.append(padding_zeros)")

            elif 'identify' in phase:
                parts = phase.split('_')
                i = int(parts[1])
                
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                
                if len(parts) > 3:
                     j = int(parts[2])
                     col_idx1 = len(str1) - 1 - j
                     col_idx2 = len(str2) - 1 - i
                     code_parts.append(f"        self.play(Circumscribe(mob2[{col_idx2}], color=YELLOW, time_width=2.5), Circumscribe(mob1[{col_idx1}], color=YELLOW, time_width=2.5), run_time={duration})")
                else:
                     code_parts.append(f"        self.wait({duration})")

            elif 'interactive_ask_prod' in phase:
                parts = phase.split('_')
                i = int(parts[1])
                j = int(parts[2])
                
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                
                code_parts.append(f"        col_idx = {i} + {j}")
                code_parts.append("        x_pos = get_col_x(col_idx)")
                code_parts.append(f"        y_pos = mob2.get_y() - y_diff * ({i} + 1)")
                code_parts.append("        q_mark = MathTex('?', font_size=60, color=YELLOW)")
                code_parts.append("        q_mark.move_to([x_pos, y_pos, 0])")
                code_parts.append("        self.play(FadeIn(q_mark, scale=0.5), run_time=0.5)")
                code_parts.append("        self.wait(1.5)")
                code_parts.append(f"        self.play(FadeOut(q_mark), run_time={max(duration-2.0, 0.1)})")

            elif 'calculate' in phase:
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')

            elif 'write' in phase and 'final' not in phase:
                parts = phase.split('_')
                i = int(parts[1])
                j = int(parts[2])
                
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                
                val1 = int(str1[len(str1) - 1 - j])
                val2 = int(str2[len(str2) - 1 - i])
                c_in = carries_matrix[i][j-1] if j > 0 else 0
                s = val1 * val2 + c_in
                rem = s % 10
                new_c = s // 10
                
                code_parts.append(f"        col_idx = {i} + {j}")
                code_parts.append("        x_pos = get_col_x(col_idx)")
                code_parts.append(f"        y_pos = mob2.get_y() - y_diff * ({i} + 1)")
                
                code_parts.append(f"        digit_{i}_{j} = MathTex('{rem}', font_size=60, color=GREEN)")
                code_parts.append(f"        digit_{i}_{j}.move_to([x_pos, y_pos, 0])")
                
                anim_parts = [f"FadeIn(digit_{i}_{j}, shift=UP * 0.2)"]
                
                if 'write_carry' in phase:
                    code_parts.append(f"        c_col_idx = {j} + 1")
                    code_parts.append("        c_x = get_col_x(c_col_idx)")
                    code_parts.append(f"        carry_{i}_{j} = MathTex('{new_c}', font_size=36, color=RED)")
                    code_parts.append(f"        carry_{i}_{j}.move_to([c_x, mob1.get_top()[1] + 0.3, 0])")
                    code_parts.append(f"        carry_mobs.add(carry_{i}_{j})")
                    anim_parts.append(f"Write(carry_{i}_{j})")
                
                code_parts.append("        self.play(")
                code_parts.append(f"            {', '.join(anim_parts)},")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        row_mobs.append(digit_{i}_{j})")

            elif 'write_final_carry' in phase:
                parts = phase.split('_')
                i = int(parts[1])
                j = int(parts[2])
                
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                
                c_in = carries_matrix[i][j-1]
                
                code_parts.append(f"        col_idx = {i} + {j}")
                code_parts.append("        x_pos = get_col_x(col_idx)")
                code_parts.append(f"        y_pos = mob2.get_y() - y_diff * ({i} + 1)")
                
                code_parts.append(f"        digit_{i}_{j} = MathTex('{c_in}', font_size=60, color=GREEN)")
                code_parts.append(f"        digit_{i}_{j}.move_to([x_pos, y_pos, 0])")
                
                code_parts.append(f"        self.play(FadeIn(digit_{i}_{j}, shift=UP * 0.2), run_time={duration})")
                code_parts.append(f"        row_mobs.append(digit_{i}_{j})")

            elif 'add_partial_products' in phase:
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                code_parts.append("        if len(carry_mobs) > 0:")
                code_parts.append("            self.play(FadeOut(carry_mobs), run_time=0.5)")
                
                code_parts.append(f"        ans_str = str({answer})")
                code_parts.append(f"        ans_mobs = VGroup(*[MathTex(c, font_size=60, color=YELLOW) for c in ans_str])")
                code_parts.append("        ans_y = mob2.get_y() - y_diff * (len(str2) + 1)")
                code_parts.append("        for idx, m in enumerate(reversed(ans_mobs)):")
                code_parts.append("            m.move_to([get_col_x(idx), ans_y, 0])")
                
                code_parts.append("        leftmost_col = len(ans_str)")
                code_parts.append("        plus_x = min(start_x, get_col_x(leftmost_col + 0.5))")
                code_parts.append("        left_x = plus_x - 0.3")
                
                code_parts.append("        final_line_y = mob2.get_y() - y_diff * (len(str2) + 0.5)")
                code_parts.append("        final_line = Line(")
                code_parts.append("            start=[left_x, final_line_y, 0],")
                code_parts.append("            end=[end_x, final_line_y, 0],")
                code_parts.append("            color=WHITE")
                code_parts.append("        )")
                
                code_parts.append("        plus_sign = MathTex('+', font_size=60, color=BLUE)")
                code_parts.append("        plus_sign_y = mob2.get_y() - y_diff * len(str2)")
                code_parts.append("        plus_sign.move_to([plus_x, plus_sign_y, 0])")
                
                code_parts.append("        self.play(Create(final_line), Write(plus_sign))")
                code_parts.append("        self.play(FadeIn(ans_mobs, shift=UP * 0.2))")

            elif 'conclusion' in phase:
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                
                if idx == len(audio_steps) - 1:
                    code_parts.append("        # Draw Box")
                    code_parts.append("        if len(str2) > 1:")
                    code_parts.append("            answer_box = SurroundingRectangle(ans_mobs, color=GREEN, buff=0.15)")
                    code_parts.append("        else:")
                    code_parts.append("            ans_group = VGroup(*row_mobs)")
                    code_parts.append("            answer_box = SurroundingRectangle(ans_group, color=GREEN, buff=0.15)")
                    code_parts.append("        self.play(Create(answer_box))")

            else:
                 code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                 
    code_parts.append("        self.wait(2)")
    return "\n".join(code_parts)