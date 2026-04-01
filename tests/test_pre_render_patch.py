"""
Unit tests for RefiningLoop.pre_render_patch()

pre_render_patch() is a static method — we test it directly without
instantiating RefiningLoop (which requires env vars / LLM setup).
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.orchestrator.refining_loop import RefiningLoop

patch = RefiningLoop.pre_render_patch  # static method, call directly


# ─── Patch 1: get_graph → plot ───────────────────────────────────────────────
class TestGetGraphToPlot:
    def test_replaces_get_graph(self):
        code = "axes.get_graph(lambda x: x**2)"
        assert ".plot(" in patch(code)
        assert ".get_graph(" not in patch(code)

    def test_replaces_get_lines(self):
        code = "obj.get_lines()"
        assert ".get_vertices()" in patch(code)
        assert ".get_lines()" not in patch(code)

    def test_unrelated_plot_untouched(self):
        code = "axes.plot(lambda x: x)"
        assert patch(code) == code


# ─── Patch 2: color name fixes ───────────────────────────────────────────────
class TestColorReplacements:
    PAIRS = [
        ("LIGHT_BLUE", "BLUE_C"),
        ("DARK_BLUE", "BLUE_E"),
        ("LIGHT_GREEN", "GREEN_C"),
        ("DARK_GREEN", "GREEN_E"),
        ("LIGHT_RED", "RED_C"),
        ("DARK_RED", "RED_E"),
        ("LIGHT_GRAY", "GRAY_C"),
        ("DARK_GRAY", "GRAY_E"),
        ("LIGHT_PINK", "PINK"),
    ]

    @pytest.mark.parametrize("bad,good", PAIRS)
    def test_color_replaced(self, bad, good):
        code = f"color = {bad}"
        result = patch(code)
        assert good in result
        assert bad not in result

    def test_valid_color_untouched(self):
        code = "color = BLUE"
        assert patch(code) == code


# ─── Patch 3: Python 3.10+ type union syntax ─────────────────────────────────
class TestTypeAnnotationStripping:
    def test_return_type_annotation_stripped(self):
        code = "def foo() -> int | None:\n    pass"
        result = patch(code)
        assert "-> int | None" not in result
        assert "):" in result

    def test_param_type_annotation_stripped(self):
        code = "def foo(x: int | str, y: float):\n    pass"
        result = patch(code)
        # x should have annotation stripped
        assert "x: int | str" not in result

    def test_no_annotation_untouched(self):
        code = "def foo(x, y):\n    pass"
        assert patch(code) == code


# ─── Patch 4: \text{} → \mathrm{} ───────────────────────────────────────────
class TestTextToMathrm:
    def test_text_replaced(self):
        code = r"t = MathTex(r'\text{slope}')"
        result = patch(code)
        assert r"\mathrm{slope}" in result
        assert r"\text{slope}" not in result

    def test_text_with_content(self):
        code = r"MathTex(r'm = \frac{\text{rise}}{\text{run}}')"
        result = patch(code)
        assert r"\mathrm{rise}" in result
        assert r"\mathrm{run}" in result
        assert r"\text{" not in result

    def test_no_text_cmd_untouched(self):
        code = r"MathTex(r'\frac{1}{2}')"
        assert patch(code) == code


# ─── Patch 5: Enforce final wait ─────────────────────────────────────────────
class TestEnforceFinalWait:
    def test_wait_injected_when_missing(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def construct(self):\n"
            "        self.play(Create(Circle()))\n"
        )
        result = patch(code)
        assert "self.wait(" in result
        # injected wait comes AFTER the play call
        play_pos = result.find("self.play(")
        wait_pos = result.rfind("self.wait(")
        assert wait_pos > play_pos

    def test_no_double_wait_when_already_present(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def construct(self):\n"
            "        self.play(Create(Circle()))\n"
            "        self.wait(2)\n"
        )
        result = patch(code)
        # Only one self.wait() should exist
        assert result.count("self.wait(") == 1

    def test_return_statement_does_not_get_wait(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def construct(self):\n"
            "        self.play(Create(Circle()))\n"
            "        return\n"
        )
        result = patch(code)
        # return should remain; wait might not be injected (last stmt is Return)
        assert "return" in result

    def test_invalid_syntax_handled_gracefully(self):
        code = "this is not valid python {"
        # Should not raise; returns something (possibly unchanged)
        result = patch(code)
        assert isinstance(result, str)


# ─── Combined: multiple patches on same code ─────────────────────────────────
# ─── Patch 4d: "is not None=" invalid syntax fix ──────────────────────────────
class TestIsNotNoneAssignment:
    def test_basic_fix(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def interpolate_mobject(self, alpha):\n"
            "        run_time = 1.0\n"
            "        if self._current is not None= min(0.2, run_time)\n"
        )
        result = patch(code)
        assert "is not None=" not in result
        assert "if self._current is not None:" in result
        assert "self._current = min(0.2, run_time)" in result

    def test_valid_if_untouched(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def construct(self):\n"
            "        if self.x is not None:\n"
            "            self.x = 1\n"
        )
        result = patch(code)
        assert "if self.x is not None:" in result

    def test_indentation_preserved(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def f(self):\n"
            "        if self._t is not None= max(0.0, alpha)\n"
        )
        result = patch(code)
        lines = result.splitlines()
        if_line = next(l for l in lines if "if self._t is not None:" in l)
        body_line = next(l for l in lines if "self._t = max" in l)
        assert if_line.startswith("        ")    # 8 spaces
        assert body_line.startswith("            ")  # 12 spaces


class TestCombinedPatches:
    def test_all_patches_applied_together(self):
        code = (
            "from manim import *\n"
            "class S(Scene):\n"
            "    def construct(self):\n"
            "        axes.get_graph(lambda x: x)\n"
            "        c = Circle(color=LIGHT_BLUE)\n"
        )
        result = patch(code)
        assert ".plot(" in result
        assert "LIGHT_BLUE" not in result
        assert "BLUE_C" in result
        assert "self.wait(" in result  # final wait injected
