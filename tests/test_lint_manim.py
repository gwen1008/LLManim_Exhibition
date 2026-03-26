"""
Unit tests for agents/coder/lint_manim.py

Strategy: lint_file() requires a real file path.
We use a helper that writes a temp file, runs lint_file(), and cleans up.
Each test is a single focused Manim snippet targeting one linter rule.
"""
import os
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.coder.lint_manim import lint_file, ManimLinter


# ─── helper ──────────────────────────────────────────────────────────────────
def lint_snippet(code: str):
    """Write code to a temp file, run lint_file(), return (success, errors)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", encoding="utf-8", delete=False
    ) as f:
        f.write(code)
        path = f.name
    try:
        return lint_file(path)
    finally:
        os.unlink(path)


def assert_rule(code: str, expected_code: str):
    success, errors = lint_snippet(code)
    codes = [e["code"] for e in errors]
    assert not success, f"Expected lint failure for rule {expected_code}, but PASSED"
    assert expected_code in codes, (
        f"Expected error code '{expected_code}', got: {codes}\n"
        f"Snippet:\n{code}"
    )


def assert_pass(code: str):
    success, errors = lint_snippet(code)
    assert success, f"Expected lint PASS but got errors: {errors}"


# ─── DEPRECATED_API ───────────────────────────────────────────────────────────
class TestDeprecatedAPI:
    def test_get_lines(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        obj.get_lines()\n",
            "DEPRECATED_API",
        )

    def test_ShowCreation(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        self.play(ShowCreation(obj))\n",
            "DEPRECATED_API",
        )

    def test_get_graph(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        axes.get_graph(lambda x: x)\n",
            "DEPRECATED_API",
        )

    def test_create_is_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        self.play(Create(Circle()))\n        self.wait(1)\n"
        )


# ─── INVALID_SET_KWARG ────────────────────────────────────────────────────────
class TestInvalidSetKwarg:
    def test_animate_set_width(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        self.play(obj.animate.set(width=3))\n",
            "INVALID_SET_KWARG",
        )

    def test_animate_set_radius(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        self.play(c.animate.set(radius=2))\n",
            "INVALID_SET_KWARG",
        )

    def test_animate_set_color_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        self.play(obj.animate.set(color=RED))\n        self.wait(1)\n"
        )


# ─── HALLUCINATED_ARG ─────────────────────────────────────────────────────────
class TestHallucinatedArg:
    def test_get_part_by_tex_substrings(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        t = MathTex(r'x^2')\n        t.get_part_by_tex('x', substrings=['x'])\n",
            "HALLUCINATED_ARG",
        )

    def test_get_parts_by_tex_substrings(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        t = MathTex(r'x^2')\n        t.get_parts_by_tex('x', substrings=['x'])\n",
            "HALLUCINATED_ARG",
        )

    def test_get_part_by_tex_no_substrings_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        t = MathTex(r'x^2')\n        t.get_part_by_tex('x')\n        self.wait(1)\n"
        )


# ─── HALLUCINATED_METHOD ──────────────────────────────────────────────────────
class TestHallucinatedMethod:
    def test_arrange_in_circle(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        g = VGroup(Circle(), Square())\n        g.arrange_in_circle()\n",
            "HALLUCINATED_METHOD",
        )


# ─── INVALID_CONSTRUCTOR_ARG ──────────────────────────────────────────────────
class TestInvalidConstructorArg:
    def test_circle_opacity(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        c = Circle(opacity=0.5)\n",
            "INVALID_CONSTRUCTOR_ARG",
        )

    def test_mathtex_opacity(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        t = MathTex(r'x', opacity=0.5)\n",
            "INVALID_CONSTRUCTOR_ARG",
        )

    def test_set_opacity_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        c = Circle().set_opacity(0.5)\n        self.wait(1)\n"
        )


# ─── RAW_COORD_ON_PLANE ────────────────────────────────────────────────────────
class TestRawCoordOnPlane:
    def test_arrow_with_plane(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        plane = NumberPlane()\n        a = Arrow([0, 0, 0], [1, 1, 0])\n",
            "RAW_COORD_ON_PLANE",
        )

    def test_arrow_without_plane_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        a = Arrow([0, 0, 0], [1, 1, 0])\n        self.wait(1)\n"
        )


# ─── MATHTEX_PLAIN_TEXT ───────────────────────────────────────────────────────
class TestMathTexPlainText:
    def test_plain_english_words(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        t = MathTex('slope equals rise divided by run')\n",
            "MATHTEX_PLAIN_TEXT",
        )

    def test_math_formula_ok(self):
        assert_pass(
            r"""from manim import *
class S(Scene):
    def construct(self):
        t = MathTex(r'\frac{rise}{run}')
        self.wait(1)
"""
        )


# ─── LATEX_TEXT_CMD ───────────────────────────────────────────────────────────
class TestLatexTextCmd:
    def test_text_in_mathtex(self):
        assert_rule(
            r"""from manim import *
class S(Scene):
    def construct(self):
        t = MathTex(r'\text{slope} = \frac{rise}{run}')
""",
            "LATEX_TEXT_CMD",
        )


# ─── MATHRM_IN_MATHTEX ────────────────────────────────────────────────────────
class TestMathrm:
    def test_mathrm_in_mathtex(self):
        assert_rule(
            r"""from manim import *
class S(Scene):
    def construct(self):
        t = MathTex(r'\mathrm{slope}')
""",
            "MATHRM_IN_MATHTEX",
        )


# ─── MATHTEX_SPECIAL_CHAR ─────────────────────────────────────────────────────
class TestMathTexSpecialChar:
    def test_unescaped_percent(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        t = MathTex('50% profit')\n",
            "MATHTEX_SPECIAL_CHAR",
        )

    def test_escaped_percent_ok(self):
        assert_pass(
            r"""from manim import *
class S(Scene):
    def construct(self):
        t = MathTex(r'50\% profit')
        self.wait(1)
"""
        )


# ─── UPDATER_BECOME_RISK ──────────────────────────────────────────────────────
class TestUpdaterBecomeRisk:
    def test_lambda_become(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        obj = Circle()\n        obj.add_updater(lambda m: m.become(Circle()))\n",
            "UPDATER_BECOME_RISK",
        )

    def test_always_redraw_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        tracker = ValueTracker(0)\n        obj = always_redraw(lambda: Circle(radius=tracker.get_value()))\n        self.play(tracker.animate.set_value(2))\n        self.wait(1)\n"
        )


# ─── TRANSFORM_MATCHING_GROUP ────────────────────────────────────────────────
class TestTransformMatchingGroup:
    def test_vgroup_arg(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        self.play(TransformMatchingTex(VGroup(MathTex('a')), MathTex('b')))\n",
            "TRANSFORM_MATCHING_GROUP",
        )

    def test_mathtex_to_mathtex_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        a = MathTex('a')\n        b = MathTex('b')\n        self.play(TransformMatchingTex(a, b))\n        self.wait(1)\n"
        )


# ─── HARDCODED_MOBJECT_INDEX ─────────────────────────────────────────────────
class TestHardcodedMobjectIndex:
    def test_eq_subscript(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        eq = MathTex(r'x^2 + y^2')\n        part = eq[0]\n",
            "HARDCODED_MOBJECT_INDEX",
        )

    def test_eq_underscore_name(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        step_eq = MathTex(r'x')\n        part = step_eq[1]\n",
            "HARDCODED_MOBJECT_INDEX",
        )

    def test_get_part_by_tex_ok(self):
        assert_pass(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        eq = MathTex(r'x^2')\n        part = eq.get_part_by_tex('x')\n        self.wait(1)\n"
        )


# ─── INFINITE_LOOP ────────────────────────────────────────────────────────────
class TestInfiniteLoop:
    def test_while_true(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        while True:\n            pass\n",
            "INFINITE_LOOP",
        )


# ─── JSON_SYNTAX_ERROR ────────────────────────────────────────────────────────
class TestJsonSyntaxError:
    def test_null_instead_of_none(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        x = null\n",
            "JSON_SYNTAX_ERROR",
        )


# ─── PYTHON310_SYNTAX ─────────────────────────────────────────────────────────
class TestPython310Syntax:
    def test_type_union(self):
        assert_rule(
            "from manim import *\nclass S(Scene):\n    def construct(self):\n        pass\n\ndef foo(x: int | None):\n    return x\n",
            "PYTHON310_SYNTAX",
        )


# ─── LATEX_COLOR_ERROR ────────────────────────────────────────────────────────
class TestLatexColorError:
    def test_uppercase_color_in_latex(self):
        assert_rule(
            r"""from manim import *
class S(Scene):
    def construct(self):
        t = MathTex(r'{\color{RED} x^2}')
""",
            "LATEX_COLOR_ERROR",
        )


# ─── TRUNCATED_LATEX ─────────────────────────────────────────────────────────
class TestTruncatedLatex:
    def test_truncated_frac(self):
        assert_rule(
            r"""from manim import *
class S(Scene):
    def construct(self):
        t = MathTex(r'x = \fr')
""",
            "TRUNCATED_LATEX",
        )


# ─── FILE-LEVEL EDGE CASES ────────────────────────────────────────────────────
class TestEdgeCases:
    def test_file_not_found(self):
        success, errors = lint_file("/nonexistent/path/fake.py")
        assert not success
        assert errors[0]["code"] == "FILE_NOT_FOUND"

    def test_syntax_error_in_file(self):
        success, errors = lint_snippet("def foo(\n")
        assert not success
        assert errors[0]["code"] == "SYNTAX_ERROR"

    def test_empty_file_passes(self):
        assert_pass("")

    def test_clean_scene_passes(self):
        assert_pass(
            "from manim import *\n\nclass MyScene(Scene):\n    def construct(self):\n        c = Circle(color=BLUE)\n        self.play(Create(c))\n        self.wait(2)\n"
        )
