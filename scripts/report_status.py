
import sys
import os
from pathlib import Path
import json

# Add scripts directory to path to allow imports
sys.path.append(str(Path(__file__).parent))

try:
    import stats_knowledge_base
    import verify_examples
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def main():
    report_path = Path("knowledge_base_report.md")
    
    # 1. Gather Stats
    print("Gathering stats...")
    stats = stats_knowledge_base.analyze_knowledge_base()
    
    # 2. Verify Examples
    print("Verifying examples...")
    # Suppress stdout/stderr during verification to avoid noise/encoding issues
    # But verify_examples prints progress, so we might want to capture it or just let it run if we can handle encoding
    # We'll use the return value mostly.
    verify_stats = verify_examples.verify_all_examples(verbose=False)
    
    # 3. Write Report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Knowledge Base Status Report\n\n")
        
        # Stats Section
        f.write("## 1. Statistics\n\n")
        f.write(f"- **Total Files**: {stats['total_files']}\n")
        
        f.write("\n### Category Breakdown\n")
        f.write("| Category | Files | Total Lines | Comment Ratio |\n")
        f.write("|----------|-------|-------------|---------------|\n")
        
        for category, cat_stats in sorted(stats['categories'].items()):
            ratio = (cat_stats['comment_lines'] / cat_stats['total_lines'] * 100) if cat_stats['total_lines'] > 0 else 0
            f.write(f"| {category} | {cat_stats['files']} | {cat_stats['total_lines']} | {ratio:.1f}% |\n")
            
        # Verification Section
        f.write("\n## 2. Verification Results\n\n")
        f.write(f"- **Passed**: {verify_stats['passed']}\n")
        f.write(f"- **Failed**: {verify_stats['failed']}\n")
        f.write(f"- **Pass Rate**: {(verify_stats['passed'] / verify_stats['total'] * 100) if verify_stats['total'] else 0:.1f}%\n")
        
        f.write("\n### Issues by Category\n")
        for category, cat_stats in verify_stats['categories'].items():
            if cat_stats['failed'] > 0:
                f.write(f"- **{category}**: {cat_stats['failed']} failed / {cat_stats['total']} total\n")
        
    print(f"Report generated at {report_path.absolute()}")

if __name__ == "__main__":
    # Force utf-8 for stdout just in case
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
            
    main()
