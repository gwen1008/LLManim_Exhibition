def apply_patch_block(original: str, patch: str) -> str:
    """
    Applies a simple SEARCH/REPLACE patch block to the original string.
    
    Format:
    <<<< SEARCH
    (old lines)
    ====
    (new lines)
    >>>> 
    """
    lines = original.splitlines()
    patch_lines = patch.splitlines()
    
    search_block = []
    replace_block = []
    mode = None
    
    patches = [] # List of (search_block, replace_block)
    
    for line in patch_lines:
        if line.strip() == "<<<< SEARCH":
            mode = "SEARCH"
            search_block = []
        elif line.strip() == "====":
            mode = "REPLACE"
            replace_block = []
        elif line.strip() == ">>>>":
            mode = None
            if search_block: # Only add if search block has content
                 patches.append((search_block, replace_block))
        else:
            if mode == "SEARCH":
                search_block.append(line)
            elif mode == "REPLACE":
                replace_block.append(line)

    if not patches:
        return None

    # Apply patches sequentially
    # This is a naive implementation that might fail if multiple patches overlap or context is ambiguous
    # But for LLM single-block fixes it usually works
    
    # Reconstruct string to facilitate search
    content = original
    
    for search, replace in patches:
        search_str = "\n".join(search)
        replace_str = "\n".join(replace)
        
        # Try exact match first
        if search_str in content:
            content = content.replace(search_str, replace_str, 1)
        else:
            # Fallback: Relaxed matching (ignoring trailing whitespace)
            content_lines = content.split("\n")
            search_lines = [l.rstrip() for l in search]

            found = False
            for start_idx in range(len(content_lines) - len(search_lines) + 1):
                window = content_lines[start_idx:start_idx + len(search_lines)]
                if [l.rstrip() for l in window] == search_lines:
                    # Found! Adjust replace block indentation.
                    original_indent = len(window[0]) - len(window[0].lstrip())
                    search_indent = len(search[0]) - len(search[0].lstrip()) if search[0].strip() else 0
                    indent_diff = original_indent - search_indent

                    adjusted_replace = []
                    for line in replace:
                        if line.strip() == "":
                            adjusted_replace.append("")
                        elif indent_diff > 0:
                            adjusted_replace.append(" " * indent_diff + line)
                        elif indent_diff < 0:
                            adjusted_replace.append(line[min(-indent_diff, len(line) - len(line.lstrip())):])
                        else:
                            adjusted_replace.append(line)

                    content_lines[start_idx:start_idx + len(search_lines)] = adjusted_replace
                    content = "\n".join(content_lines)
                    found = True
                    break

            if not found:
                print(f"⚠️ Patch failed: Search block not found (even with fuzzy match).")
                return None

    return content
