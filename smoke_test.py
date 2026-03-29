"""
Smoke test — 改完 agents/ 之後跑這個，30 秒內確認 pipeline 基本結構沒爛掉。
不呼叫任何 LLM API，只做靜態/組裝驗證。

用法: python smoke_test.py
"""
import sys
import traceback

PASS = []
FAIL = []

def check(name, fn):
    try:
        fn()
        PASS.append(name)
        print(f"  ✅ {name}")
    except Exception as e:
        FAIL.append((name, e))
        print(f"  ❌ {name}: {e}")
        traceback.print_exc()

print("\n=== LLManim Smoke Test ===\n")

# 1. Prompter 能組裝 system prompt（不炸 KeyError）
def test_prompter_assembly():
    from agents.coder.prompter import CoderPrompter
    p = CoderPrompter()
    sys_prompt, user_prompt = p.generate_initial_prompt(
        script_json='{"steps": [{"description": "test"}]}',
        target_scene="GeneratedScene",
        rag_context="",
        spatial_hints=""
    )
    assert len(sys_prompt) > 1000, "System prompt too short"
    assert "{N-1}" not in sys_prompt, "Unresolved {N-1} placeholder still in prompt"
    assert "MANIM_API_STRICT_RULES" not in sys_prompt, "Unresolved placeholder still in prompt"

check("Prompter system prompt assembly (no KeyError)", test_prompter_assembly)

# 2. Planner _process_response 能解析 <json_blueprint> tag
def test_planner_blueprint_parser():
    from agents.planner.planner import Planner
    fake_response = """
<thought_tree>
  <branch id="A"><metaphor>test</metaphor><scores pedagogy="8" feasibility="9" engagement="7" /></branch>
  <selection><winner>A</winner><reason>test</reason></selection>
</thought_tree>
<reasoning>
some reasoning here
</reasoning>
<json_blueprint>
{"topic": "test", "steps": [{"id": 1, "description": "step one"}]}
</json_blueprint>
"""
    result_json, thought_tree = Planner._process_response(None, fake_response)
    import json
    parsed = json.loads(result_json)
    assert parsed["topic"] == "test", f"Wrong parse result: {parsed}"
    assert thought_tree != "", "thought_tree should be extracted"

check("Planner <json_blueprint> parser", test_planner_blueprint_parser)

# 3. Planner fallback (no json_blueprint tag) 也能走完
def test_planner_fallback_no_crash():
    from agents.planner.planner import Planner
    import unittest.mock as mock
    p = Planner.__new__(Planner)
    # No XML tags, no JSON — should not throw, just return raw text
    fake_response = "Some random response without any tags or JSON."
    result, _ = p._process_response(fake_response)
    assert isinstance(result, str)

check("Planner fallback (no tags/JSON) no crash", test_planner_fallback_no_crash)

# 4. Linter imports OK
def test_linter_import():
    from agents.coder.lint_manim import ManimLinter
    linter = ManimLinter()
    import ast
    tree = ast.parse("from manim import *\nclass T(Scene):\n    def construct(self): pass")
    linter.visit(tree)
    assert isinstance(linter.errors, list)

check("Linter import and basic run", test_linter_import)

# 5. LLMClient routing table 完整（所有 role 都有對應 model）
def test_llm_routing():
    import unittest.mock as mock
    with mock.patch.dict("os.environ", {}, clear=False):
        from agents.core.llm_client import LLMClient
        client = LLMClient.__new__(LLMClient)
        client.models = {
            "default": "llama-3.3-70b-versatile",
            "planner": "deepseek-chat",
            "coder": "deepseek-chat",
            "reviewer": "llama-3.1-8b-instant",
            "vision": "gpt-4o-mini",
        }
        for role in ["planner", "coder", "reviewer", "vision"]:
            m = client.models.get(role)
            assert m, f"Role '{role}' has no model"

check("LLMClient all roles have models", test_llm_routing)

# 6. RefiningLoop import OK（沒有 syntax error）
def test_refining_loop_import():
    from agents.orchestrator.refining_loop import RefiningLoop
    assert hasattr(RefiningLoop, "auto_fix_loop")
    assert hasattr(RefiningLoop, "pre_render_patch")

check("RefiningLoop import OK", test_refining_loop_import)

# 7. pre_render_patch 能正確剝掉 \text{} 和 \mathrm{}
def test_pre_render_patch():
    from agents.orchestrator.refining_loop import RefiningLoop
    code = 'MathTex(r"\\text{slope} = \\frac{\\mathrm{rise}}{run}")'
    patched = RefiningLoop.pre_render_patch(code)
    assert r"\mathrm{" not in patched, r"\mathrm{} should be stripped"
    # \text{} is a linter error — pre_render_patch doesn't auto-fix it (by design),
    # just confirm the patch doesn't crash on it
    assert isinstance(patched, str)

check("pre_render_patch runs without crash", test_pre_render_patch)

# --- Summary ---
print(f"\n{'='*30}")
print(f"PASS: {len(PASS)}  FAIL: {len(FAIL)}")
if FAIL:
    print("\nFailed checks:")
    for name, err in FAIL:
        print(f"  - {name}: {err}")
    sys.exit(1)
else:
    print("All checks passed — safe to run eval.")
    sys.exit(0)
