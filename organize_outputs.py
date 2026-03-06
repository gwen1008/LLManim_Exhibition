import os
import shutil

# Configuration
BASE_DIR = "stable_outputs"
CATEGORIES = {
    "Arithmetic": ["+", "-", "*", "_plus_", "_minus_", "addition", "subtraction", "multiplication", "division", "加法", "減法", "乘法", "除法"],
    "Algebra": ["x", "y", "equation", "solve", "expand", "proof", "polynomial", "quadratic", "方程式", "展開", "代數", "因式分解"],
    "Geometry": ["circle", "triangle", "square", "area", "angle", "pythagorean", "sin", "cos", "tan", "geometry", "圓", "三角形", "面積", "角度", "畢氏", "幾何"],
    "Calculus": ["limit", "integral", "derivative", "riemann", "sum", "calculus", "微積分", "極限", "導數", "積分", "黎曼"],
    "Misc": ["fibonacci", "sequence", "費氏", "數列"]
}

def get_category(filename):
    """Determine category based on keywords in filename."""
    name_lower = filename.lower()
    
    # Priority check: Calculus > Geometry > Algebra > Arithmetic
    # This prevents complex topics (e.g., area of circle via integral) from being misclassified as just Arithmetic
    
    for keyword in CATEGORIES["Calculus"]:
        if keyword in name_lower:
            return "Calculus"
            
    for keyword in CATEGORIES["Geometry"]:
        if keyword in name_lower:
            return "Geometry"
            
    for keyword in CATEGORIES["Algebra"]:
        if keyword in name_lower:
            return "Algebra"
            
    for keyword in CATEGORIES["Arithmetic"]:
        if keyword in name_lower:
            return "Arithmetic"
            
    for keyword in CATEGORIES["Misc"]:
        if keyword in name_lower:
            return "Misc"
            
    return None # Stays in Inbox

def organize():
    if not os.path.exists(BASE_DIR):
        print(f"❌ Directory '{BASE_DIR}' not found.")
        return

    # Create category directories
    for cat in CATEGORIES:
        cat_path = os.path.join(BASE_DIR, cat)
        os.makedirs(cat_path, exist_ok=True)
        
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    
    moved_count = 0
    
    for file in files:
        if file.startswith("."): continue # Skip hidden files
        if file == os.path.basename(__file__): continue # Skip self
        
        category = get_category(file)
        
        if category:
            src = os.path.join(BASE_DIR, file)
            dst = os.path.join(BASE_DIR, category, file)
            
            # Move file
            shutil.move(src, dst)
            print(f"✅ Moved: {file} -> {category}/")
            moved_count += 1
            
    print(f"\n🎉 Organization Complete! Moved {moved_count} files.")
    print(f"📂 Uncategorized files remain in '{BASE_DIR}' (Inbox).")

if __name__ == "__main__":
    organize()
