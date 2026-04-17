"""
TDD tests for agents/coder/positioning_ast.py

All tests are pure AST parsing — zero subprocess, zero LLM, zero I/O.
Run with: pytest tests/test_positioning_ast.py -v
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.coder.positioning_ast import (
    POSITIONING_METHODS,
    find_positioning_calls,
    get_source_lines_around,
)


# ── find_positioning_calls ────────────────────────────────────────────────────

class TestFindPositioningCalls:
    # ── tracer bullet ──
    def test_single_next_to(self):
        code = "circle.next_to(square, RIGHT)\n"
        calls = find_positioning_calls(code)
        assert len(calls) == 1
        assert calls[0].method == "next_to"
        assert calls[0].object_name == "circle"

    # ── zero results ──
    def test_empty_code_returns_empty(self):
        assert find_positioning_calls("") == []

    def test_syntax_error_returns_empty_not_crash(self):
        assert find_positioning_calls("def (broken syntax:::") == []

    def test_no_positioning_calls_returns_empty(self):
        code = "self.play(Write(text))\nself.wait(1)\n"
        assert find_positioning_calls(code) == []

    # ── all known methods detected ──
    @pytest.mark.parametrize("method", list(POSITIONING_METHODS))
    def test_all_positioning_methods_detected(self, method):
        code = f"obj.{method}(something)\n"
        calls = find_positioning_calls(code)
        assert len(calls) == 1
        assert calls[0].method == method

    # ── buff= kwarg ──
    def test_buff_kwarg_extracted(self):
        code = "label.next_to(box, DOWN, buff=0.3)\n"
        calls = find_positioning_calls(code)
        assert calls[0].buff_value == pytest.approx(0.3)
        assert calls[0].buff_node is not None

    def test_no_buff_kwarg_is_none(self):
        code = "label.next_to(box, DOWN)\n"
        calls = find_positioning_calls(code)
        assert calls[0].buff_value is None
        assert calls[0].buff_node is None

    def test_buff_as_integer_coerced_to_float(self):
        code = "obj.shift(UP, buff=1)\n"
        calls = find_positioning_calls(code)
        assert isinstance(calls[0].buff_value, float)
        assert calls[0].buff_value == 1.0

    # ── multiple calls ──
    def test_multiple_calls_all_found(self):
        code = (
            "a.move_to(ORIGIN)\n"
            "b.next_to(a, RIGHT)\n"
            "c.shift(UP * 2)\n"
        )
        calls = find_positioning_calls(code)
        assert len(calls) == 3
        methods = {c.method for c in calls}
        assert methods == {"move_to", "next_to", "shift"}

    def test_calls_ordered_by_source_line(self):
        code = (
            "a.shift(UP)\n"       # line 1
            "b.move_to(LEFT)\n"   # line 2
        )
        calls = find_positioning_calls(code)
        assert calls[0].lineno < calls[1].lineno

    # ── object_name recovery ──
    def test_chained_receiver_unparse(self):
        """obj.animate.move_to() → object_name should unparse to 'obj.animate'."""
        code = "obj.animate.move_to(target)\n"
        calls = find_positioning_calls(code)
        assert len(calls) == 1
        assert "obj" in calls[0].object_name

    def test_subscript_receiver_no_crash(self):
        """mobs[0].next_to(ref) → should not crash, object_name is best-effort."""
        code = "mobs[0].next_to(ref, UP)\n"
        calls = find_positioning_calls(code)
        assert len(calls) == 1
        assert calls[0].method == "next_to"

    # ── lineno ──
    def test_lineno_is_correct(self):
        code = "# comment\n\ncircle.shift(RIGHT)\n"
        calls = find_positioning_calls(code)
        assert calls[0].lineno == 3

    # ── non-method call (bare function) ignored ──
    def test_bare_function_call_not_collected(self):
        """next_to(obj) as a standalone function (not method) must not be collected."""
        code = "next_to(obj)\n"
        calls = find_positioning_calls(code)
        assert calls == []


# ── get_source_lines_around ───────────────────────────────────────────────────

class TestGetSourceLinesAround:
    CODE = "\n".join(f"line_{i}" for i in range(1, 21))  # 20 lines

    # ── tracer bullet ──
    def test_returns_string(self):
        result = get_source_lines_around(self.CODE, lineno=10)
        assert isinstance(result, str)

    def test_target_line_included(self):
        result = get_source_lines_around(self.CODE, lineno=10)
        assert "line_10" in result

    def test_line_numbers_prefixed(self):
        result = get_source_lines_around(self.CODE, lineno=10)
        # format is "  10: line_10"
        assert "10:" in result

    def test_default_context_5_lines_each_side(self):
        result = get_source_lines_around(self.CODE, lineno=10, context=5)
        lines = result.strip().splitlines()
        # lines 5–15 → 11 lines total
        assert len(lines) == 11

    def test_context_0_returns_only_target(self):
        result = get_source_lines_around(self.CODE, lineno=10, context=0)
        lines = result.strip().splitlines()
        assert len(lines) == 1
        assert "line_10" in lines[0]

    def test_clamps_at_start_of_file(self):
        """lineno=1 with context=5 → no negative index crash, starts at line 1."""
        result = get_source_lines_around(self.CODE, lineno=1, context=5)
        assert "line_1" in result
        # Must not contain a line before line 1
        assert "line_0" not in result

    def test_clamps_at_end_of_file(self):
        """lineno=20 with context=5 → no out-of-bounds crash, ends at last line."""
        result = get_source_lines_around(self.CODE, lineno=20, context=5)
        assert "line_20" in result

    def test_custom_context_respected(self):
        result = get_source_lines_around(self.CODE, lineno=10, context=2)
        lines = result.strip().splitlines()
        # lines 8–12 → 5 lines
        assert len(lines) == 5
