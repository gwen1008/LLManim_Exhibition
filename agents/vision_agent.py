import os
import base64
from openai import OpenAI
import logging

class VisionAgent:
    """
    The 'Eye' of the system. Uses GPT-4o to visually audit generated animations.
    """
    def __init__(self, llm_client=None):
        from .llm_client import LLMClient
        self.llm = llm_client if llm_client else LLMClient()
            
        # ========== SYSTEM PROMPT: PROFESSIONAL MATHEMATICAL ANIMATION QA AUDITOR ==========
        # Based on Deep Research: "Cognitive Architectural Strategies for VLMs in Animation QA"
        # Implements Chain-of-Visual-Thought (CoVT) framework for high-precision geometric auditing
        
        self.system_prompt = """# ROLE: PROFESSIONAL MATHEMATICAL ANIMATION QA AUDITOR

You are a Lead Visual QA Engineer specializing in mathematical animations rendered via Manim Community Edition.
Your objective is to audit video frames for **absolute technical accuracy**, **pedagogical clarity**, and **symbolic consistency**.
You operate as a "Critic" in an agentic loop, providing deterministic, actionable feedback to a "Coder" agent.

## CORE REASONING FRAMEWORK (Chain-of-Visual-Thought):

### Step 1: Global Alignment Check
- Compare the rendered frame against the "Expected Scene Layout" (provided in metadata).
- Identify all visible mathematical objects (shapes, equations, labels).

### Step 2: Geometric Precision Audit
- Inspect all junctions and intersections between shapes.
- Verify objects that should touch (distance = 0) have NO visible gaps or sub-pixel separations.
- Check for "Z-index flickering" or overlapping primitives.
- **CRITICAL**: In nested geometries (e.g., (a+b)² visual proofs), micro-gaps between tiles destroy pedagogical clarity.

### Step 3: Symbolic & LaTeX Consistency
- Cross-reference rendered MathTex with expected symbolic content.
- Verify symbolic continuity across temporal sequences.
- Flag "fuzzy" or low-resolution symbolic rendering.
- Ensure no symbol transformations (e.g., x → k) unless mathematically justified.

### Step 4: Pedagogical & Accessibility Audit (WCAG 2.2)
- **Color Contrast**: Text-to-background contrast ratio must be ≥ 4.5:1 (WCAG AA standard).
- **Line Thickness**: Lines should be ≥ 2.0pt equivalent for visibility.
- **Label Placement**: Labels must not touch frame edges; ensure safe zones.
- **Visual Crowding**: Verify adequate spacing between distinct mathematical elements.

### Step 5: Hallucination Mitigation & Defensive Reporting
- **Ground Truth Priority**: Use provided bounding box and coordinate data as your reference.
- **Defensive Prompting**: Report ONLY what you can clearly see and confirm via visual evidence.
- **No Assumptions**: If a feature is ambiguous, state uncertainty rather than guessing.

## OUTPUT REQUIREMENTS:

You MUST output a valid JSON object with the following structure:

```json
{
  "verdict": "PASS" or "FAIL",
  "overall_critique": "One-sentence technical summary",
  "defects": [
    {
      "id": "ERR_001",
      "category": "GeometricMisalignment" | "SymbolicInconsistency" | "PedagogicalClarity" | "Accessibility",
      "severity": "Critical" | "Major" | "Minor",
      "description": "Precise technical description of the defect",
      "suggested_fix": "Actionable code-level remediation (e.g., 'Use buff=0 in next_to()')"
    }
  ]
}
```

## CRITICAL RULES:
1. Always output valid JSON. No preamble, no conversational text.
2. If NO defects are found, return: `{"verdict": "PASS", "overall_critique": "All checks passed.", "defects": []}`
3. Use LaTeX notation for all mathematical symbols (e.g., $a^2$, not "a squared").
4. Be specific: Instead of "alignment is off", say "Top-left square has 0.1-unit gap from parent container's UL corner."
5. Focus on ACTIONABLE insights that help the Coder fix the issue.

Your audit determines whether the animation meets the standard for K-12 mathematical education.
"""

    def _encode_image(self, image_path):
        """Read image and encode to base64."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def audit_frame(self, image_path, script_context):
        """
        Audit a specific image frame against the script context using Chain-of-Visual-Thought.
        
        Args:
            image_path (str): Path to the image file (png/jpg)
            script_context (str): The 'Visual Rationale' or script description (JSON)
            
        Returns:
            dict: Structured audit report with verdict, defects, and remediation suggestions
            Format: {
                "verdict": "PASS"|"FAIL"|"ERROR",
                "overall_critique": str,
                "defects": [{"id, "category", "severity", "description", "suggested_fix"}],
                "raw_response": str (for debugging)
            }
        """
        try:
            base64_image = self._encode_image(image_path)
            
            # Enhanced user prompt with CoVT context
            user_text = f"""**AUDIT REQUEST**

Context (Expected Scene Layout from Planner's JSON):
{script_context}

**TASK**: Perform a complete Chain-of-Visual-Thought audit on this final frame.
Follow all 5 steps in your reasoning framework.
Return your analysis as a valid JSON object per the schema in your system prompt.
"""
            
            content = self.llm.ask_vision(self.system_prompt, user_text, base64_image)
            
            if "ERROR" in content:
                return {"verdict": "ERROR", "overall_critique": content, "defects": []}
            
            # Display raw response for debugging
            print("\n" + "="*40)
            print("👁️  [Vision Agent Audit - CoVT Framework]")
            print("-" * 40)
            print(content)
            print("="*40 + "\n")
            
            # Parse structured JSON response
            import json
            import re
            
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find raw JSON
                json_match = re.search(r'\{.*"verdict".*\}', content, re.DOTALL)
                json_str = json_match.group(0) if json_match else None
            
            if json_str:
                try:
                    audit_result = json.loads(json_str)
                    
                    # Validate required fields
                    verdict = audit_result.get("verdict", "FAIL")
                    overall_critique = audit_result.get("overall_critique", "No critique provided")
                    defects = audit_result.get("defects", [])
                    
                    # Display defects summary
                    if defects:
                        print(f"🔍 Detected {len(defects)} defect(s):")
                        for defect in defects:
                            severity_emoji = {"Critical": "🔴", "Major": "🟠", "Minor": "🟡"}.get(defect.get("severity", "Minor"), "⚪")
                            print(f"  {severity_emoji} [{defect.get('category', 'Unknown')}] {defect.get('description', 'No description')[:80]}...")
                    
                    return {
                        "verdict": verdict,
                        "overall_critique": overall_critique,
                        "defects": defects,
                        "raw_response": content
                    }
                    
                except json.JSONDecodeError as je:
                    print(f"⚠️ JSON parsing failed: {je}")
                    # Fallback to simple parsing
                    pass
            
            # Fallback: Legacy parsing for backward compatibility
            print("⚠️ Falling back to legacy parsing (VLM didn't return valid JSON)")
            verdict = "PASS"
            if "VERDICT: FAIL" in content or '"verdict": "FAIL"' in content:
                verdict = "FAIL"
            elif "VERDICT: PASS" in content or '"verdict": "PASS"' in content:
                verdict = "PASS"
            else:
                verdict = "FAIL"  # Conservative default
                
            return {
                "verdict": verdict,
                "overall_critique": "Legacy parsing mode - no structured defects",
                "defects": [],
                "raw_response": content
            }
            
        except Exception as e:
            import traceback
            print(f"❌ Vision Audit Error: {e}")
            print(traceback.format_exc())
            return {
                "verdict": "ERROR",
                "overall_critique": str(e),
                "defects": [],
                "raw_response": ""
            }
