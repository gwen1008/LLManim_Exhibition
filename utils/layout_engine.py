"""
utils/layout_engine.py

A constraint-based layout engine for Manim using Kiwisolver (Cassowary algorithm).
Handles dynamic positioning of Mobjects based on relational rules.
"""
import numpy as np

try:
    from kiwisolver import Solver, Variable, strength
except ImportError:
    # Fallback or error if not installed, but Coder should handle this via pip
    raise ImportError("ManimLayoutEngine requires `kiwisolver`. Please run `pip install kiwisolver`.")


class LayoutObject:
    """
    Wraps a Mobject (or its dimensions) for layout purposes.
    """
    def __init__(self, mobject_or_size, name: str = "obj"):
        self.name = name
        
        # Determine initial size
        if hasattr(mobject_or_size, "width"):
             # It's a Mobject
            self.width_val = mobject_or_size.width
            self.height_val = mobject_or_size.height
            self.mobject = mobject_or_size
        else:
            # It's a tuple (width, height)
            self.width_val, self.height_val = mobject_or_size
            self.mobject = None

        # Create Layout Variables
        self.left = Variable(f"{name}_L")
        self.right = Variable(f"{name}_R")
        self.top = Variable(f"{name}_T")
        self.bottom = Variable(f"{name}_B")
        self.width = Variable(f"{name}_W")
        self.height = Variable(f"{name}_H")
        self.center_x = Variable(f"{name}_CX")
        self.center_y = Variable(f"{name}_CY")

    # === Manim-style Proxy Properties ===
    # These exist so AI-generated code that assumes Manim MObject API
    # (e.g. obj.center, obj.get_center()) won't crash with AttributeError.

    @property
    def center(self):
        """Proxy: returns [center_x, center_y] as kiwisolver Variables.
        Allows constraint expressions like: obj.center == some_point
        """
        return [self.center_x, self.center_y]

    def get_center(self):
        """Returns solved [x, y, 0] numpy array. Call after layout.solve()."""
        return np.array([self.center_x.value(), self.center_y.value(), 0])

    def get_left(self):
        """Returns solved left-center point as [x, y, 0]."""
        return np.array([self.left.value(), self.center_y.value(), 0])

    def get_right(self):
        """Returns solved right-center point as [x, y, 0]."""
        return np.array([self.right.value(), self.center_y.value(), 0])

    def get_top(self):
        """Returns solved top-center point as [x, y, 0]."""
        return np.array([self.center_x.value(), self.top.value(), 0])

    def get_bottom(self):
        """Returns solved bottom-center point as [x, y, 0]."""
        return np.array([self.center_x.value(), self.bottom.value(), 0])

    def structural_constraints(self):
        """Returns internal consistency constraints."""
        return [
            self.width == self.width_val,
            self.height == self.height_val,
            self.right == self.left + self.width,
            self.top == self.bottom + self.height,
            self.center_x == (self.left + self.right) / 2,
            self.center_y == (self.top + self.bottom) / 2
        ]

class LayoutZone:
    """
    Represents a specific region on the screen (e.g., Header, Content, Footer).
    Objects added to a zone are constrained to stay within its boundaries.
    """
    def __init__(self, name, x_range, y_range):
        self.name = name
        self.min_x, self.max_x = x_range
        self.min_y, self.max_y = y_range

class LayoutEngine:
    def __init__(self):
        self.solver = Solver()
        self.objects = []
        self.zones = {
            "HEADER": LayoutZone("HEADER", [-7.0, 7.0], [2.7, 4.0]),
            "CONTENT": LayoutZone("CONTENT", [-6.5, 6.5], [-2.5, 2.7]),
            "FOOTER": LayoutZone("FOOTER", [-7.0, 7.0], [-4.0, -2.5]),
        }

    def add(self, obj: LayoutObject):
        self.objects.append(obj)
        for c in obj.structural_constraints():
            self.solver.addConstraint(c | strength.required)
        
        # Add default "gravity" towards center (weak strength)
        # This prevents objects from being pushed to edges when constraints are under-specified.
        self.solver.addConstraint((obj.center_x == 0) | strength.weak)
        self.solver.addConstraint((obj.center_y == 0) | strength.weak)
        
        return obj

    def add_to_zone(self, obj: LayoutObject, zone_name: str):
        """Constrains an object to stay within a named zone using STRONG strength."""
        if zone_name not in self.zones:
            raise ValueError(f"Zone '{zone_name}' not defined. Available: {list(self.zones.keys())}")
        
        zone = self.zones[zone_name]
        
        # Add boundary constraints with STRONG strength to prevent unsatisfiable crashes
        # if the object is too large for the zone.
        self.solver.addConstraint((obj.left >= zone.min_x) | strength.strong)
        self.solver.addConstraint((obj.right <= zone.max_x) | strength.strong)
        self.solver.addConstraint((obj.bottom >= zone.min_y) | strength.strong)
        self.solver.addConstraint((obj.top <= zone.max_y) | strength.strong)

    def add_constraint(self, constraint, str_val=strength.medium):
        self.solver.addConstraint(constraint | str_val)

    def align_to(self, objA, objB, direction, buff=0):
        """Align objA to match objB on the given direction edge, with optional buff."""
        if direction == 'LEFT':
            self.add_constraint(objA.left == objB.left + buff)
        elif direction == 'RIGHT':
            self.add_constraint(objA.right == objB.right - buff)
        elif direction == 'TOP': # UP
            self.add_constraint(objA.top == objB.top - buff)
        elif direction == 'BOTTOM': # DOWN
            self.add_constraint(objA.bottom == objB.bottom + buff)
        elif direction == 'CENTER_X':
            self.add_constraint(objA.center_x == objB.center_x + buff)
        elif direction == 'CENTER_Y':
            self.add_constraint(objA.center_y == objB.center_y + buff)

    def next_to(self, objA, objB, direction, buff=0.5):
        """Place objA next to objB in the given direction."""
        if direction == 'RIGHT':
            self.add_constraint(objA.left == objB.right + buff)
            self.add_constraint(objA.center_y == objB.center_y, strength.weak)
        elif direction == 'LEFT':
            self.add_constraint(objA.right == objB.left - buff)
            self.add_constraint(objA.center_y == objB.center_y, strength.weak)
        elif direction == 'UP':
            self.add_constraint(objA.bottom == objB.top + buff)
            self.add_constraint(objA.center_x == objB.center_x, strength.weak)
        elif direction == 'DOWN':
            self.add_constraint(objA.top == objB.bottom - buff)
            self.add_constraint(objA.center_x == objB.center_x, strength.weak)

    def arrange(self, objects, direction='RIGHT', buff=0.5):
        """Arrange a list of objects in a sequence."""
        for i in range(len(objects) - 1):
            self.next_to(objects[i+1], objects[i], direction, buff)

    def get_object(self, name: str):
        """Retrieve a registered LayoutObject by name."""
        for obj in self.objects:
            if obj.name == name:
                return obj
        raise KeyError(f"LayoutObject '{name}' not found. Registered: {[o.name for o in self.objects]}")

    def get(self, name: str):
        """Alias for get_object."""
        return self.get_object(name)

    def solve(self):
        self.solver.updateVariables()
        # Optionally apply to mobjects immediately if they exist
        for obj in self.objects:
            if obj.mobject:
                # Update Mobject position using move_to
                new_x = obj.center_x.value()
                new_y = obj.center_y.value()
                obj.mobject.move_to([new_x, new_y, 0])
