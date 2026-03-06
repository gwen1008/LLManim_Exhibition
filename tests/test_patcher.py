"""
Unit tests for utils/patcher.py — apply_patch_block()
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.patcher import apply_patch_block


def make_patch(search: str, replace: str) -> str:
    return f"<<<< SEARCH\n{search}\n====\n{replace}\n>>>>"


# ─── Basic exact-match ────────────────────────────────────────────────────────
class TestExactMatch:
    def test_simple_replacement(self):
        original = "a = 1\nb = 2\n"
        patch = make_patch("a = 1", "a = 99")
        result = apply_patch_block(original, patch)
        assert result == "a = 99\nb = 2\n"

    def test_multiline_replacement(self):
        original = "x = 1\ny = 2\nz = 3\n"
        patch = make_patch("x = 1\ny = 2", "x = 10\ny = 20")
        result = apply_patch_block(original, patch)
        assert "x = 10" in result
        assert "y = 20" in result
        assert "z = 3" in result

    def test_replaces_only_first_occurrence(self):
        original = "foo()\nfoo()\n"
        patch = make_patch("foo()", "bar()")
        result = apply_patch_block(original, patch)
        assert result.count("bar()") == 1
        assert result.count("foo()") == 1

    def test_empty_replace_block_deletes_lines(self):
        original = "a = 1\ndelete_me = True\nb = 2\n"
        patch = make_patch("delete_me = True", "")
        result = apply_patch_block(original, patch)
        assert "delete_me" not in result
        assert "a = 1" in result


# ─── Fuzzy match (trailing whitespace difference) ────────────────────────────
class TestFuzzyMatch:
    def test_trailing_whitespace_ignored(self):
        original = "    self.play(Create(c))   \n"
        # search block has no trailing spaces
        patch = make_patch("    self.play(Create(c))", "    self.play(Write(c))")
        result = apply_patch_block(original, patch)
        assert "Write(c)" in result

    def test_indentation_preserved(self):
        original = "class S:\n    def foo(self):\n        x = 1\n"
        patch = make_patch("        x = 1", "        x = 99")
        result = apply_patch_block(original, patch)
        assert "        x = 99" in result


# ─── Multiple patches in one block ───────────────────────────────────────────
class TestMultiplePatches:
    def test_two_patches_sequential(self):
        original = "a = 1\nb = 2\nc = 3\n"
        patch_str = (
            "<<<< SEARCH\na = 1\n====\na = 10\n>>>>\n"
            "<<<< SEARCH\nb = 2\n====\nb = 20\n>>>>"
        )
        result = apply_patch_block(original, patch_str)
        assert "a = 10" in result
        assert "b = 20" in result
        assert "c = 3" in result


# ─── Failure cases ────────────────────────────────────────────────────────────
class TestFailureCases:
    def test_search_not_found_returns_none(self):
        original = "x = 1\n"
        patch = make_patch("this_does_not_exist", "replacement")
        result = apply_patch_block(original, patch)
        assert result is None

    def test_empty_patch_string_returns_none(self):
        result = apply_patch_block("x = 1\n", "")
        assert result is None

    def test_malformed_patch_no_delimiters_returns_none(self):
        result = apply_patch_block("x = 1\n", "just some random text")
        assert result is None

    def test_missing_close_delimiter_ignored(self):
        # A patch block without >>>> should be silently skipped (no search_block added)
        original = "x = 1\n"
        patch = "<<<< SEARCH\nx = 1\n====\nx = 99\n"  # no >>>>
        result = apply_patch_block(original, patch)
        assert result is None  # no valid patches parsed


# ─── Real-world Manim code patches ───────────────────────────────────────────
class TestManimCodePatches:
    def test_fix_class_name(self):
        original = (
            "from manim import *\n\n"
            "class WrongName(Scene):\n"
            "    def construct(self):\n"
            "        self.wait(1)\n"
        )
        patch = make_patch(
            "class WrongName(Scene):",
            "class CorrectName(Scene):",
        )
        result = apply_patch_block(original, patch)
        assert "class CorrectName(Scene):" in result
        assert "WrongName" not in result

    def test_fix_animation_call(self):
        original = (
            "from manim import *\n\n"
            "class S(Scene):\n"
            "    def construct(self):\n"
            "        self.play(ShowCreation(circle))\n"
            "        self.wait(1)\n"
        )
        patch = make_patch(
            "        self.play(ShowCreation(circle))",
            "        self.play(Create(circle))",
        )
        result = apply_patch_block(original, patch)
        assert "Create(circle)" in result
        assert "ShowCreation" not in result
