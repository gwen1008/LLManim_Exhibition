"""
Templates module for deterministic Manim code generation.

This package contains pre-built, guaranteed-correct templates for 
standard mathematical operations like arithmetic, ensuring 100% 
accuracy and consistency.
"""

from .addition import generate_vertical_addition_code, generate_addition_narrative
from .subtraction import generate_vertical_subtraction_code, generate_subtraction_narrative
from .multiplication import generate_vertical_multiplication_code, generate_multiplication_narrative
from .division import generate_long_division_code, generate_division_narrative

__all__ = [
    'generate_vertical_addition_code', 'generate_addition_narrative',
    'generate_vertical_subtraction_code', 'generate_subtraction_narrative',
    'generate_vertical_multiplication_code', 'generate_multiplication_narrative',
    'generate_long_division_code', 'generate_division_narrative',
]
