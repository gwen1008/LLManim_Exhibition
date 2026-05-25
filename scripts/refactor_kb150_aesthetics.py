#!/usr/bin/env python3
"""
Automated Refactoring Script for kb150 Math Scenes.
Applies the Premium Visual Design & Aesthetic Protocol:
  1. Deep slate dark background (#0B0F19)
  2. Sleek thin background dot grid (NumberPlane)
  3. Premium neon color mapping (BLUE, RED, GREEN, YELLOW, PURPLE, WHITE -> Curated Hex)
  4. Glassmorphism rounded glow highlights (SurroundingRectangle -> self.get_glow_rect)
  5. Elegant FadeOut(*self.mobjects) graceful cleanup at the end.
"""

import re
from pathlib import Path

COLOR_MAP = {
    "BLUE": '"#3A86FF"',
    "RED": '"#FF006E"',
    "GREEN": '"#06D6A0"',
    "YELLOW": '"#FFBE0B"',
    "PURPLE": '"#8338EC"',
    "WHITE": '"#F8FAFC"',
}


def refactor_content(content: str) -> tuple[str, bool]:
    changed = False

    # Skip files that don't define a Scene class
    if not re.search(r"class\s+\w+\(\s*Scene\s*\)\s*:", content):
        return content, False

    # 1. Inject Deep Slate Background & Modern Coordinate Grid (Idempotent)
    if "background_color = \"#0B0F19\"" not in content and "background_color = '#0B0F19'" not in content:
        m = re.search(r"(\s+)def construct\(self\):", content)
        if m:
            indent = m.group(1) + "    "
            grid_injection = (
                f"\n{indent}# 🌌 Set sleek deep-dark slate background\n"
                f"{indent}self.camera.background_color = \"#0B0F19\"\n\n"
                f"{indent}# 📐 Add modern thin background coordinate grid\n"
                f"{indent}grid = NumberPlane(\n"
                f"{indent}    x_range=[-7, 7, 1], y_range=[-4, 4, 1],\n"
                f"{indent}    background_line_style={{\"stroke_color\": \"#1E293B\", \"stroke_opacity\": 0.4, \"stroke_width\": 1}}\n"
                f"{indent})\n"
                f"{indent}self.add(grid)\n"
            )
            # Find the position of def construct(self): and insert right after it
            idx = m.end()
            content = content[:idx] + grid_injection + content[idx:]
            changed = True

    # 2. Inject get_glow_rect helper method if SurroundingRectangle is used (Idempotent)
    if "SurroundingRectangle" in content and "def get_glow_rect(self" not in content:
        m = re.search(r"(\s+)def construct\(self\):", content)
        if m:
            class_indent = m.group(1)
            glow_rect_method = (
                f"{class_indent}def get_glow_rect(self, mobject, color=\"#3A86FF\", buff=0.15):\n"
                f"{class_indent}    return RoundedRectangle(\n"
                f"{class_indent}        corner_radius=0.15,\n"
                f"{class_indent}        color=color,\n"
                f"{class_indent}        stroke_width=3,\n"
                f"{class_indent}        fill_color=color,\n"
                f"{class_indent}        fill_opacity=0.15\n"
                f"{class_indent}    ).surround(mobject, buff=buff)\n\n"
            )
            idx = m.start()
            content = content[:idx] + glow_rect_method + content[idx:]
            changed = True

    # 3. Replace SurroundingRectangle with self.get_glow_rect
    if "SurroundingRectangle" in content:
        content = content.replace("SurroundingRectangle", "self.get_glow_rect")
        changed = True

    # 4. Map Premium Neon Colors in attributes
    for color_name, color_hex in COLOR_MAP.items():
        # Matches: color=BLUE, fill_color=BLUE, stroke_color=BLUE, etc.
        pattern = rf"\b(color|fill_color|stroke_color|background_color)\s*=\s*{color_name}\b"
        new_content = re.sub(pattern, rf'\1={color_hex}', content)
        if new_content != content:
            content = new_content
            changed = True

    # 5. Ensure elegant FadeOut cleanup at the end (Idempotent)
    # Check if construct method has FadeOut(*self.mobjects) or FadeOut(all mobjects/similar)
    # We'll check if FadeOut is in the last 15 lines before the end or class/function boundaries
    m_construct = list(re.finditer(r"(\s+)def construct\(self\):", content))
    if m_construct:
        # Simple check: does the file have "FadeOut" in it?
        # Many already have self.play(FadeOut(*self.mobjects)), let's check
        if "FadeOut" not in content:
            # We will append the elegant FadeOut at the very end of construct() if not present
            # We search for the last non-empty line of the construct method
            lines = content.splitlines()
            last_line_idx = -1
            # Find indentation level
            m_indent = re.search(r"(\s+)def construct\(self\):", content)
            construct_indent = m_indent.group(1) + "    "
            
            # Scan backward to find where to append
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip() and lines[i].startswith(construct_indent):
                    last_line_idx = i
                    break
            
            if last_line_idx != -1:
                # Add self.play(FadeOut(*self.mobjects)) and wait(1)
                lines.insert(last_line_idx + 1, f"{construct_indent}self.play(FadeOut(*self.mobjects))")
                lines.insert(last_line_idx + 2, f"{construct_indent}self.wait(1)")
                content = "\n".join(lines) + "\n"
                changed = True

    return content, changed


def main():
    kb_dir = Path("knowledge_base/kb150")
    refactored = 0
    skipped = 0
    
    print("=" * 60)
    print("🚀 STARTING AUTOMATED PREMIUM REFITTING ON KB150 SCENES")
    print("=" * 60)
    
    for slug_dir in sorted(kb_dir.iterdir()):
        if not slug_dir.is_dir():
            continue
        for f in sorted(slug_dir.glob("*.py")):
            try:
                content = f.read_text(encoding="utf-8")
                new_content, changed = refactor_content(content)
                if changed:
                    f.write_text(new_content, encoding="utf-8")
                    print(f"  [REFACTORED] {slug_dir.name}/{f.name}")
                    refactored += 1
                else:
                    print(f"  [SKIPPED]    {slug_dir.name}/{f.name} (already compliant)")
                    skipped += 1
            except Exception as e:
                print(f"  [ERR]        {slug_dir.name}/{f.name}: {e}")
                
    print("\n" + "=" * 60)
    print(f"🎉 COMPLETED: refactored={refactored}  skipped={skipped}")
    print("=" * 60)


if __name__ == "__main__":
    main()
