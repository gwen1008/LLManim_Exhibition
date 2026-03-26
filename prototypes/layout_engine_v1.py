"""
Manim Layout Engine Prototype (v1)
==================================
This script demonstrates the core logic of a Constraint-Based Layout Engine for Manim
using the `kiwisolver` library (Cassowary algorithm).

Concepts:
- LayoutVariable: Wraps a Mobject's attribute (left, right, top, bottom, width, height)
- LayoutEngine: Manages the solver and the Mobjects
- Constraints: Defined as linear equations (e.g., A.right + 1.0 == B.left)

Prerequisites:
    pip install kiwisolver
"""

try:
    from kiwisolver import Solver, Variable, Strength
except ImportError:
    print("❌ Critical: `kiwisolver` is not installed.")
    print("Please run: pip install kiwisolver")
    exit(1)

class LayoutObject:
    """
    A lightweight wrapper around a Manim Mobject (or a mock)
    that exposes Kiwi variables for layout.
    """
    def __init__(self, name, width=1.0, height=1.0):
        self.name = name
        
        # Define edge variables
        self.left = Variable(f"{name}_L")
        self.right = Variable(f"{name}_R")
        self.top = Variable(f"{name}_T")
        self.bottom = Variable(f"{name}_B")
        self.width = Variable(f"{name}_W")
        self.height = Variable(f"{name}_H")
        self.center_x = Variable(f"{name}_CX")
        self.center_y = Variable(f"{name}_CY")
        
        # Helper to track intrinsic size
        self._intrinsic_width = width
        self._intrinsic_height = height

    def get_constraints(self):
        """
        Returns structural constraints defining the object's geometry.
        """
        return [
            self.width == self._intrinsic_width,
            self.height == self._intrinsic_height,
            self.right == self.left + self.width,
            self.top == self.bottom + self.height,
            self.center_x == (self.left + self.right) / 2,
            self.center_y == (self.top + self.bottom) / 2
        ]

class LayoutEngine:
    def __init__(self):
        self.solver = Solver()
        self.objects = []

    def add(self, obj: LayoutObject):
        self.objects.append(obj)
        for c in obj.get_constraints():
            self.solver.addConstraint(c)

    def add_constraint(self, constraint):
        self.solver.addConstraint(constraint)

    def solve(self):
        self.solver.updateVariables()

if __name__ == "__main__":
    print("Initializing Layout Engine...")
    engine = LayoutEngine()

    # 1. Create Virtual Objects
    eq = LayoutObject("Equation", width=2.0, height=1.0)
    label = LayoutObject("Label", width=1.0, height=0.5)

    engine.add(eq)
    engine.add(label)

    # 2. Add Constraints
    # Equation centered
    engine.add_constraint(eq.center_x == 0)
    engine.add_constraint(eq.center_y == 0)
    
    # Label to the RIGHT of Equation with padding >= 0.5
    engine.add_constraint(label.left >= eq.right + 0.5)
    
    # Label vertically aligned
    engine.add_constraint(label.center_y == eq.center_y)

    print("Solving...")
    engine.solve()

    print(f"Equation X: {eq.center_x.value()}")
    print(f"Label X:    {label.center_x.value()}")
    print(f"Gap:        {label.left.value() - eq.right.value()}")
