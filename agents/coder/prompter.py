# agents/prompter.py
from ..core.manim_api_rules import (
    MANIM_API_STRICT_RULES, 
    MANIM_LAYOUT_RULES, 
    MANIM_LAYOUT_ENGINE_DOCS, 
    MANIM_LANGUAGE_RULES,
    MANIM_BANNED_APIS,
    MANIM_GEOMETRY_RULES
)
from .templates import (
    CODER_SYSTEM_PART,
    OPUS_CODER_SYSTEM_PART,
    CODER_USER_PART,
    VISUAL_AUDIT_PROMPT_TEMPLATE
)

class CoderPrompter:
    def generate_initial_prompt(self, script_json, target_scene, rag_context="", spatial_hints="") -> tuple[str, str]:
        """
        回傳 (system_prompt, user_prompt) tuple。
        system_prompt 包含靜態規則，適合 DeepSeek Prompt Cache。
        user_prompt 包含動態的 script_json，每次呼叫都不同。
        """
        import os
        coder_model = os.getenv("CODER_MODEL", "deepseek-chat")
        
        if "opus" in coder_model.lower() or "claude-code" in coder_model.lower():
            system_prompt = OPUS_CODER_SYSTEM_PART
            user_prompt = CODER_USER_PART.format(
                rag_context=rag_context,
                spatial_hints=spatial_hints,
                script_json=script_json,
                target_scene=target_scene,
            )
        else:
            system_prompt = CODER_SYSTEM_PART
            for _k, _v in {
                "MANIM_API_STRICT_RULES": MANIM_API_STRICT_RULES,
                "MANIM_LAYOUT_RULES": MANIM_LAYOUT_RULES,
                "MANIM_LAYOUT_ENGINE_DOCS": MANIM_LAYOUT_ENGINE_DOCS,
                "MANIM_LANGUAGE_RULES": MANIM_LANGUAGE_RULES,
                "MANIM_BANNED_APIS": MANIM_BANNED_APIS,
                "MANIM_GEOMETRY_RULES": MANIM_GEOMETRY_RULES
            }.items():
                system_prompt = system_prompt.replace(f"{{{_k}}}", _v)
    
            user_prompt = CODER_USER_PART.format(
                rag_context=rag_context,
                spatial_hints=spatial_hints,
                script_json=script_json,
                target_scene=target_scene,
            )
        return system_prompt, user_prompt

class VisualFixPrompter:
    """
    Translates structured visual defects (JSON) into Manim code fix instructions.
    """
    def generate_visual_fix_prompt(self, audit_result, original_code, script_json=None, slim=False):
        defects = audit_result.get("defects", [])
        if not defects:
            return None
            
        # Group defects by code for summarized advice
        defect_summary = {}
        for d in defects:
            code = d.get("code", "UNKNOWN")
            desc = d.get("description", "No description")
            fix = d.get("suggested_fix", "No fix suggestion")
            if code not in defect_summary:
                defect_summary[code] = []
            defect_summary[code].append(f"- {desc} (Suggestion: {fix})")
            
        # Build the violation report string
        report = ""
        for code, details in defect_summary.items():
            report += f"\n🚨 **{code}** ({len(details)} occurrences):\n"
            report += "\n".join(details)
            
            # Append standard fix strategies for each type
            if code == "OVERLAP":
                report += "\n👉 **STRATEGY**: IDs colliding? Increase `buff` in `next_to()`, use `shift()` to separate, or `scale(0.8)` if too large."
            elif code == "OVERFLOW":
                report += "\n👉 **STRATEGY**: Content off-screen? Check coordinate bounds. Use `to_edge()` or `scale(0.7)` to fit within frame."
            elif code == "LOW_CONTRAST":
                report += "\n👉 **STRATEGY**: Text unreadable? Change color to `WHITE` or `YELLOW` if background is dark."
            elif code == "TINY_TEXT":
                report += "\n👉 **STRATEGY**: Text too small? Set `font_size >= 48` or `scale(1.5)`."
            elif code == "MISALIGNED":
                report += "\n👉 **STRATEGY**: Wobbly alignment? Use `align_to()` or `VGroup.arrange()` instead of manual shifting."
            elif code == "CLUTTER":
                report += "\n👉 **STRATEGY**: Too crowded? Increase `buff` parameter or spread out elements."
            elif code == "TOO_FAST":
                report += "\n👉 **STRATEGY**: Flashing too fast? Increase `run_time` or `wait()` duration."

        # [Improvement] slim mode: strip only layout_plan (large but not needed for visual fixes).
        # Previously omitted script_json entirely, causing the Coder to forget the animation plan.
        # Now we keep the scene description / sequence intact, saving ~30-50% tokens.
        _script_json_for_prompt = script_json
        if slim and script_json:
            import json as _json
            try:
                _parsed = _json.loads(script_json) if isinstance(script_json, str) else script_json
                layout_plan = _parsed.get("layout_plan", {})

                # Check if any defects are spatial (need layout coordinates to fix properly)
                SPATIAL_DEFECT_CODES = {"OVERLAP", "OVERFLOW", "MISALIGNED"}
                spatial_defects = [d for d in defects if d.get("code") in SPATIAL_DEFECT_CODES]

                if spatial_defects and layout_plan:
                    # Extract keywords from defect descriptions to filter relevant zones
                    import re as _re
                    defect_text = " ".join(
                        d.get("description", "") + " " + d.get("suggested_fix", "")
                        for d in spatial_defects
                    ).lower()
                    # Tokenize: split on non-alphanumeric, keep tokens >= 3 chars
                    keywords = set(w for w in _re.split(r'[^a-z0-9_]+', defect_text) if len(w) >= 3)

                    # Keep layout zones whose key matches any keyword
                    filtered_layout = {
                        k: v for k, v in layout_plan.items()
                        if any(kw in k.lower() for kw in keywords)
                    }
                    # Fallback: if no zones matched, keep all zones (better than none)
                    if not filtered_layout:
                        filtered_layout = layout_plan

                    _stripped = {k: v for k, v in _parsed.items() if k != "layout_plan"}
                    _stripped["layout_plan_relevant"] = filtered_layout  # inject filtered subset
                else:
                    # Non-spatial errors: strip layout_plan entirely (original behavior)
                    _stripped = {k: v for k, v in _parsed.items() if k != "layout_plan"}

                _script_json_for_prompt = _json.dumps(_stripped, ensure_ascii=False, indent=2)
            except Exception:
                pass  # If parse fails, send raw script_json as-is — safer than omitting

        prompt = VISUAL_AUDIT_PROMPT_TEMPLATE.format(
            defect_report=report,
            original_code=original_code,
            script_json=_script_json_for_prompt
        )

        return prompt
