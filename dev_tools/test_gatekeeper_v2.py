"""
Test cases for the enhanced Gatekeeper (ManimLinter).
Tests the new error detection patterns:
1. `null` vs `None` detection
2. LaTeX `\color{PYTHON_VAR}` detection
"""

from manim import *

class TestNullError(Scene):
    """This should trigger JSON_SYNTAX_ERROR"""
    def construct(self):
        # Intentional error: using 'null' instead of 'None'
        step = {
            "step": 1,
            "signal_action": null,  # ERROR: Should be None
            "visual_action": {"type": "Write"}
        }
        text = Text("Hello")
        self.play(Write(text))

class TestLatexColorError(Scene):
    """This should trigger LATEX_COLOR_ERROR"""
    def construct(self):
        # Intentional error: using Python constant BRIGHT_RED in LaTeX string
        formula = MathTex("x = \\frac{-b {\\color{BRIGHT_RED}\\pm} \\sqrt{b^2}}{2a}")
        # ERROR: BRIGHT_RED is a Python constant, not a LaTeX color
        self.play(Write(formula))

class TestCorrectCode(Scene):
    """This should pass without errors"""
    def construct(self):
        # Correct way 1: Use None instead of null
        step = {
            "step": 1,
            "signal_action": None,  # Correct
            "visual_action": {"type": "Write"}
        }
        
        # Correct way 2: Use .set_color() method
        formula = MathTex("x = \\frac{-b \\pm \\sqrt{b^2}}{2a}")
        formula.set_color_by_tex("\\pm", RED)  # Correct
        self.play(Write(formula))
