
"""
Integer Vertical Addition Template
Generates Manim code for step-by-step vertical addition with audio narration and interactive elements.
"""
from typing import List, Dict, Any
from .common import get_imports_code, get_setup_code, get_subtitle_methods_code

def generate_addition_narrative(num1: int, num2: int, interactive_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Generate step-by-step narrative for vertical addition.
    """
    str1 = str(num1)
    str2 = str(num2)
    steps = []
    
    # ========== Intro Phase ==========
    steps.append({
        "narrative": "今天我們要學習整數的直式加法。",
        "phase": "intro"
    })
    steps.append({
        "narrative": f"題目是 {num1} 加 {num2}。",
        "phase": "intro"
    })
    steps.append({
        "narrative": "在開始計算之前，我們要記得兩個數字要靠右對齊，也就是個位對個位、十位對十位，這樣才能正確計算。",
        "phase": "intro"
    })
    steps.append({
        "narrative": "現在，讓我們從個位數開始，一步一步往左邊計算。",
        "phase": "intro"
    })
    
    # ========== Digit-by-Digit Calculation Phase ==========
    carry = 0
    places = ["個位", "十位", "百位", "千位", "萬位", "十萬位", "百萬位"]
    max_len = max(len(str1), len(str2))
    
    for i in range(max_len):
        place_name = places[i] if i < len(places) else "下一位"
        val1 = int(str1[len(str1) - 1 - i]) if i < len(str1) else 0
        val2 = int(str2[len(str2) - 1 - i]) if i < len(str2) else 0
        
        current_sum = val1 + val2 + carry
        new_carry = current_sum // 10
        remainder = current_sum % 10
        
        # Sub-step 1: Identify
        narrative = f"首先，我們從{place_name}開始計算。" if i == 0 else f"接下來計算{place_name}。"
        steps.append({
            "narrative": narrative,
            "phase": f"digit_{i}_identify"
        })
        
        # Sub-step 2: State
        steps.append({
            "narrative": f"{place_name}上面是 {val1}，下面是 {val2}。",
            "phase": f"digit_{i}_state"
        })
        
        # [INTERACTIVE] Ask for sum
        if interactive_mode:
            step_desc = f"{val1} 加 {val2}"
            if carry > 0:
                step_desc += f" 再加 {carry}"
            
            steps.append({
                "narrative": f"{place_name}是 {step_desc}，你想想看等於多少呢？",
                "phase": f"digit_{i}_interactive_ask_sum"
            })
        
        # Sub-step 3: Calculate
        if carry > 0:
            steps.append({
                "narrative": f"別忘了，我們還有從前一位進上來的 {carry}。",
                "phase": f"digit_{i}_carry_reminder"
            })
            steps.append({
                "narrative": f"所以現在要算的是：{val1} 加 {val2} 再加 {carry}，等於 {current_sum}。",
                "phase": f"digit_{i}_calculate"
            })
        else:
            steps.append({
                "narrative": f"我們把它們相加：{val1} 加 {val2}，等於 {current_sum}。",
                "phase": f"digit_{i}_calculate"
            })
        
        # Sub-step 4: Write Result/Carry
        if new_carry > 0:
            # [INTERACTIVE] Ask about carry
            if interactive_mode:
                 steps.append({
                    "narrative": f"相加等於 {current_sum}，超過 10 了，這時候我們該怎麼做？",
                    "phase": f"digit_{i}_interactive_ask_carry"
                })

            next_place = places[i+1] if i+1 < len(places) else '下一位'
            steps.append({
                "narrative": f"因為 {current_sum} 大於等於 10，所以我們在{place_name}寫下 {remainder}，然後把 {new_carry} 進到{next_place}。",
                "phase": f"digit_{i}_write_carry"
            })
        else:
            if current_sum < 10:
                steps.append({
                    "narrative": f"因為 {current_sum} 小於 10，所以我們直接在{place_name}寫下 {remainder}，不需要進位。",
                    "phase": f"digit_{i}_write_no_carry"
                })
            else:
                 # Should theoretically not happen for single digits sum < 10 (max 9+9=18), 
                 # but logic kept for completeness if extended beyond base-10 digits conceptually
                steps.append({
                    "narrative": f"我們在{place_name}寫下 {remainder}。",
                    "phase": f"digit_{i}_write"
                })
        
        carry = new_carry
    
    # ========== Final Carry ==========
    if carry > 0:
        final_place_name = places[max_len] if max_len < len(places) else "下一位"
        steps.append({
            "narrative": f"最後，我們還有從{places[max_len-1]}進上來的 {carry}。",
            "phase": f"digit_{max_len}_identify"
        })
        steps.append({
            "narrative": f"所以{final_place_name}是 {carry}。",
            "phase": f"digit_{max_len}_write_final_carry"
        })
    
    # ========== Conclusion ==========
    answer = num1 + num2
    steps.append({
        "narrative": "太棒了！我們已經完成了所有位數的計算。",
        "phase": "conclusion"
    })
    steps.append({
        "narrative": f"讓我們確認一下答案：{num1} 加 {num2} 等於 {answer}。",
        "phase": "conclusion"
    })
    steps.append({
        "narrative": "記住，在做直式加法時，一定要記得位數對齊、從右到左計算、還有注意進位，這樣就不會算錯了！",
        "phase": "conclusion"
    })
    
    return steps

def generate_vertical_addition_code(num1: int, num2: int, scene_name: str = "VerticalAddition", audio_steps: List[Dict] = None) -> str:
    """
    Generate complete Manim code for vertical addition.
    """
    str1 = str(num1)
    str2 = str(num2)
    answer = num1 + num2
    
    code_parts = []
    
    # 1. Imports
    code_parts.append(get_imports_code())
    
    # 2. Class Definition
    code_parts.append(f"class {scene_name}(Scene):")
    code_parts.append('    """')
    code_parts.append(f'    Perfect Vertical Addition: {num1} + {num2} = {answer}')
    code_parts.append('    Generated with modular addition template.')
    code_parts.append('    """')
    
    # 3. Setup & Subtitle Methods from Common
    code_parts.append(get_setup_code())
    code_parts.append(get_subtitle_methods_code())
    
    # 4. Construct Method
    code_parts.append("    def construct(self):")
    code_parts.append("        # ==================== Scene Setup ====================")
    code_parts.append("        self.camera.background_color = BLACK")
    code_parts.append("")
    code_parts.append(f'        # Title')
    code_parts.append(f'        title = Text("整數加法：{num1} + {num2}", font_size=36, color=WHITE)')
    code_parts.append("        title.to_edge(UP, buff=0.5)")
    code_parts.append("        self.add(title)")
    code_parts.append("        ")
    
    # Number Construction (Visuals)
    code_parts.append("        # ==================== Number Construction ====================")
    code_parts.append(f'        str1 = "{str1}"')
    code_parts.append(f'        str2 = "{str2}"')
    code_parts.append("        ")
    code_parts.append("        # Build number mobjects")
    code_parts.append("        mob1 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str1])")
    code_parts.append("        mob1.arrange(RIGHT, buff=0.2).move_to(UP * 1.0)")
    code_parts.append("        ")
    code_parts.append("        mob2 = VGroup(*[MathTex(c, font_size=60, color=BLUE) for c in str2])")
    code_parts.append("        mob2.arrange(RIGHT, buff=0.2)")
    code_parts.append("        mob2.next_to(mob1, DOWN, buff=0.5).align_to(mob1, RIGHT)")
    code_parts.append("        ")
    code_parts.append("        plus_sign = MathTex('+', font_size=60, color=BLUE)")
    code_parts.append("        plus_sign.next_to(mob2, LEFT, buff=0.3)")
    code_parts.append("        ")
    code_parts.append("        line = Line(")
    code_parts.append("            start=plus_sign.get_left() + LEFT * 0.2,")
    code_parts.append("            end=mob2.get_right() + RIGHT * 0.2,")
    code_parts.append("            color=WHITE")
    code_parts.append("        ).next_to(mob2, DOWN, buff=0.2)")
    code_parts.append("        ")
    code_parts.append("        ans_mobs = []")
    code_parts.append("        carry_mobs = []")
    code_parts.append("        ")

    # Animation Loop
    code_parts.append("        # ==================== Phase-Based Step Processing ====================")
    
    if audio_steps:
        # We need to recreate the carry logic locally to know which animations to generate
        max_len = max(len(str1), len(str2))
        carries = [0] * max_len
        for i in range(max_len):
            val1 = int(str1[len(str1) - 1 - i]) if i < len(str1) else 0
            val2 = int(str2[len(str2) - 1 - i]) if i < len(str2) else 0
            carry_in = carries[i-1] if i > 0 else 0
            total = val1 + val2 + carry_in
            if i < max_len:
                carries[i] = total // 10

        for idx, step in enumerate(audio_steps):
            phase = step.get('phase', '')
            narrative = step.get('narrative', '').replace('"', '\\"')
            duration = step.get('duration', 2.0)
            audio_path = step.get('audio_path', '')
            
            if audio_path:
                duration += 0.2  # Audio buffer
            
            code_parts.append(f"        # Step {idx}: [{phase}]")
            if audio_path:
                code_parts.append(f'        self.add_sound("{audio_path}")')
            
            # Logic for subtitle based on phase type
            if 'interactive' in phase:
                if 'ask_sum' in phase:
                    # Interactive Ask Sum
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    
                    # Parse digit index from phase string "digit_X_..."
                    digit_idx = int(phase.split('_')[1])
                    
                    # Calculate positions for question mark
                    col_idx2 = len(str2) - 1 - digit_idx
                    if col_idx2 >= 0:
                        x_pos = f"mob2[{col_idx2}].get_center()[0]"
                    else:
                        x_pos = "0"
                        
                    code_parts.append(f"        self.remove(self.subtitle_area)")
                    code_parts.append(f"        self.subtitle_area = new_sub")
                    code_parts.append(f"        self.add(self.subtitle_area)")

                    code_parts.append(f"        q_mark = MathTex('?', font_size=60, color=YELLOW)")
                    code_parts.append(f"        q_mark.move_to([{x_pos}, line.get_center()[1] - 0.6, 0])")
                    
                    code_parts.append("        self.play(")
                    code_parts.append("            FadeIn(q_mark, scale=0.5),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                    code_parts.append("        self.wait(2.0)")
                    code_parts.append("        self.play(FadeOut(q_mark), run_time=0.5)")
                
                elif 'ask_carry' in phase:
                    # Interactive Ask Carry
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
                    code_parts.append("        self.wait(1.5)")
            
            elif 'intro' in phase:
                if idx == 0:
                     # Initial setup animation
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append("        self.play(")
                    code_parts.append("            FadeIn(mob1), FadeIn(mob2),")
                    code_parts.append("            Write(plus_sign), Create(line),")
                    code_parts.append(f"            run_time={duration}")
                    code_parts.append("        )")
                else:
                    code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
            
            elif 'identify' in phase:
                 # Highlight digits
                parts = phase.split('_')
                digit_idx = int(parts[1])
                
                if digit_idx < max_len:
                    col_idx1 = len(str1) - 1 - digit_idx
                    col_idx2 = len(str2) - 1 - digit_idx
                    
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    
                    # Highlight logic
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
                else:
                    # Final carry identify
                     # Only need to highlight if there is something to highlight? 
                     # Actually for final carry (e.g. 9+1=10), the carry is "virtual" until written
                     # Or maybe we highlight the previous carry?
                     # Existing logic just plays subtitle
                    code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                    code_parts.append("        self.remove(self.subtitle_area)")
                    code_parts.append("        self.subtitle_area = new_sub")
                    code_parts.append("        self.add(self.subtitle_area)")
                    code_parts.append(f"        self.wait({duration})")

            elif 'write_no_carry' in phase or 'write_carry' in phase or 'write' in phase and 'final' not in phase:
                parts = phase.split('_')
                digit_idx = int(parts[1])
                
                # Re-calculate value locally to know what to write
                v1 = int(str1[len(str1) - 1 - digit_idx]) if digit_idx < len(str1) else 0
                v2 = int(str2[len(str2) - 1 - digit_idx]) if digit_idx < len(str2) else 0
                # Use carries array we prepopulated
                c_in = carries[digit_idx-1] if digit_idx > 0 else 0
                s = v1 + v2 + c_in
                rem = s % 10
                new_c = s // 10
                
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                
                # 1. Write result digit
                col_i2 = len(str2) - 1 - digit_idx
                if col_i2 >= 0:
                    x_ref = f"mob2[{col_i2}].get_center()[0]"
                else:
                    # If num2 is shorter, we need to calculate position relative to neighbors
                    # Simplified: assume aligned to right, so we can use index from right
                    # Each digit is width approx... 
                    # Let's use the logic that mob2 is right aligned.
                    # mob2[-1] is ones place. mob2[-1-digit_idx]
                    x_ref = "0" # Fallback
                
                # Correct X position logic from original:
                if col_i2 >= 0:
                     x_pos = f"mob2[{col_i2}].get_center()[0]"
                else:
                     # Calculate based on rightmost digit of mob2 and offset
                     # mob2 has 'len(str2)' digits. 
                     # The digit_idx-th place from right.
                     # Dist is digit_idx * (width + buff)
                     # But mob2 might be VGroup. 
                     # Safe fallback from original code logic?
                     # Original used col_idx2 check. 
                     # If num2 has 2 digits (idx 0,1), and we are at digit 2 (hundreds), col_idx2 = -1.
                     # We need position of hundreds place.
                     # We can align to mob2[0] (leftmost) and shift left?
                     x_pos = f"mob2[0].get_center()[0] - ({digit_idx} - {len(str2)-1}) * (mob2[0].width + 0.2)"

                code_parts.append(f"        digit_{digit_idx} = MathTex('{rem}', font_size=60, color=GREEN)")
                code_parts.append(f"        digit_{digit_idx}.move_to([{x_pos}, line.get_center()[1] - 0.6, 0])")
                
                anim_parts = [f"FadeIn(digit_{digit_idx}, shift=UP * 0.2)"]
                
                # 2. Write carry if exists
                if 'write_carry' in phase:
                    # Carry goes to next position (digit_idx + 1)
                    # Position: above top of mob2 (or mob1 if exists?)
                    # Usually small number above.
                    # Align with next column
                    next_col_idx = len(str2) - 1 - (digit_idx + 1)
                    if next_col_idx >= 0:
                         c_x = f"mob2[{next_col_idx}].get_center()[0]"
                    else:
                         c_x = f"mob2[0].get_center()[0] - ({digit_idx+1} - {len(str2)-1}) * (mob2[0].width + 0.2)"
                    
                    code_parts.append(f"        carry_{digit_idx} = MathTex('{new_c}', font_size=36, color=RED)")
                    code_parts.append(f"        carry_{digit_idx}.move_to([{c_x}, mob2.get_top()[1] + 0.3, 0])")
                    code_parts.append(f"        carry_mobs.append(carry_{digit_idx})")
                    anim_parts.append(f"Write(carry_{digit_idx})")
                
                code_parts.append("        self.play(")
                code_parts.append(f"            {', '.join(anim_parts)},")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        ans_mobs.append(digit_{digit_idx})")

            elif 'write_final_carry' in phase:
                parts = phase.split('_')
                digit_idx = int(parts[1])
                # This is the 'last' carry being written as a main digit
                # e.g. 985 + 84 -> 1069. The '1' is the final carry.
                
                code_parts.append(f'        new_sub = self.create_wrapped_subtitle("{narrative}")')
                code_parts.append("        self.remove(self.subtitle_area)")
                code_parts.append("        self.subtitle_area = new_sub")
                code_parts.append("        self.add(self.subtitle_area)")
                
                # Position: Left of the leftmost answer digit so far
                # Current answer digits are in ans_mobs (reversed later, but currently appended in order 0, 1, 2...)
                # The visual query for X should be relative to mob2 leftmost?
                
                # Safest: Use calculate logic
                # Left of the 'hundreds' place (which is digit_idx-1)
                # digit_3 means thousands place.
                
                code_parts.append(f"        digit_{digit_idx} = MathTex('1', font_size=60, color=GREEN)")
                code_parts.append(f"        # Calculate X position: to the left of the leftmost digit")
                # Fallback logic for safety
                code_parts.append(f"        left_x = mob2[0].get_center()[0] - mob2[0].get_width()/2 - 0.2 - digit_{digit_idx}.get_width()/2")
                code_parts.append(f"        digit_{digit_idx}.move_to([left_x, line.get_center()[1] - 0.6, 0])")
                
                code_parts.append("        self.play(")
                code_parts.append(f"            FadeIn(digit_{digit_idx}, shift=UP * 0.2),")
                code_parts.append(f"            run_time={duration}")
                code_parts.append("        )")
                code_parts.append(f"        ans_mobs.append(digit_{digit_idx})")

            elif 'conclusion' in phase:
                 if '已經完成' in narrative: # First part of conclusion
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
                # Default case for generic narration
                code_parts.append(f'        self.update_subtitle("{narrative}", {duration})')
            
            code_parts.append("        ")
            
    code_parts.append("        # Final wait")
    code_parts.append("        self.wait(2)")
    
    return "\n".join(code_parts)
