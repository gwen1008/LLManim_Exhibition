"""
agents/coder/positioning_ast.py

AST utilities for finding and analyzing Manim positioning method calls.
Used by misalign_fixer.py to locate candidate parameters for T1/T2 fixes.
"""
import ast
from typing import Optional


POSITIONING_METHODS = {
    'next_to', 'shift', 'move_to', 'align_to',
    'to_edge', 'to_corner', 'arrange', 'set_x', 'set_y',
}


class PositioningCall:
    """Represents a single positioning method call found in Manim code."""

    def __init__(
        self,
        lineno: int,
        method: str,
        object_name: Optional[str],
        buff_value: Optional[float],
        buff_node: Optional[ast.keyword],
        call_node: ast.Call,
    ):
        self.lineno = lineno
        self.method = method
        self.object_name = object_name   # Best-effort receiver name (e.g. "circle")
        self.buff_value = buff_value      # float value of buff= kwarg, or None
        self.buff_node = buff_node        # The ast.keyword node for buff=
        self.call_node = call_node        # The full Call AST node

    def __repr__(self):
        return (
            f"<PositioningCall L{self.lineno}: "
            f"{self.object_name}.{self.method}(buff={self.buff_value})>"
        )


class _PositioningCallFinder(ast.NodeVisitor):
    """Walk AST and collect all positioning method calls."""

    def __init__(self):
        self.calls: list[PositioningCall] = []

    def visit_Call(self, node: ast.Call):
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr in POSITIONING_METHODS
        ):
            # Best-effort: recover receiver object name
            try:
                obj_name = ast.unparse(node.func.value)
            except Exception:
                obj_name = None

            # Find buff= keyword argument
            buff_value: Optional[float] = None
            buff_node: Optional[ast.keyword] = None
            for kw in node.keywords:
                if (
                    kw.arg == 'buff'
                    and isinstance(kw.value, ast.Constant)
                    and isinstance(kw.value.value, (int, float))
                ):
                    buff_value = float(kw.value.value)
                    buff_node = kw
                    break

            self.calls.append(
                PositioningCall(
                    lineno=node.lineno,
                    method=node.func.attr,
                    object_name=obj_name,
                    buff_value=buff_value,
                    buff_node=buff_node,
                    call_node=node,
                )
            )
        self.generic_visit(node)


def find_positioning_calls(source_code: str) -> list[PositioningCall]:
    """Parse source_code and return all detected positioning method calls."""
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return []
    finder = _PositioningCallFinder()
    finder.visit(tree)
    return finder.calls


def get_source_lines_around(source_code: str, lineno: int, context: int = 5) -> str:
    """
    Return source lines around a given 1-indexed line number with context.
    Output is prefixed with line numbers for LLM readability.
    """
    lines = source_code.splitlines()
    start = max(0, lineno - 1 - context)
    end = min(len(lines), lineno + context)
    numbered = [f"{i + 1:4d}: {lines[i]}" for i in range(start, end)]
    return "\n".join(numbered)
