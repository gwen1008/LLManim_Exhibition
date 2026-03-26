# 🧠 Thinking Summary

```text
============================================================
🌳 **VISUAL TREE OF THOUGHTS (ToT)**
============================================================
```

```text
============================================================


============================================================
```

```text
============================================================
**Concept Extraction**: Parabola `y = (x-2)² - 3`. Vertex form `y = a(x-h)² + k` with `a=1, h=2, k=-3`. Vertex at `(h, k) = (2, -3)`. Axis of symmetry `x = h = 2`. Parent function `y = x²`.

**Visual Metaphor**: Transformational journey from parent to target.

**Spatial Plan**:
- **HEADER Zone (y ~ 3.0)**: Title and current function display.
- **CONTENT Zone (y ~ 0)**: Main coordinate plane, graphs, and key points/lines. This is the primary visual stage.
- **FOOTER Zone (y ~ -3.0)**: Explanatory text for each step.

**Layout & Overflow Prevention**:
- The coordinate `axes` will be centered at ORIGIN.
- The `parent_graph` and `final_graph` will be plotted on these same axes. We will use `ReplacementTransform` to morph the parent graph into the final graph, preventing vertical stacking.
- The `vertex_dot` and `axis_line` will be created in-place.
- The `function_label` in the header will be updated via `TransformMatchingTex` for each algebraic step, keeping it in a fixed location.
- The `explanation_text` in the footer will be replaced for each major step, also preventing stacking.

**Signal Strategy**:
1. Introduce parent function and its graph.
2. Signal the horizontal shift `(x-2)` and animate the graph moving right.
3. Signal the vertical shift `-3` and animate the graph moving down.
4. Indicate the resulting vertex point `(2, -3)`.
5. Draw the axis of symmetry `x=2` through the vertex.

**Coordinate Calculations**:
- Axes: `x_range=[-3, 7, 1], y_range=[-5, 6, 1]` to comfortably show vertex (2,-3) and shape.
- Parent Graph (`y=x²`): Sample points from x=-2 to x=4 for smooth curve.
- Final Graph (`y=(x-2)²-3`): Same shape, shifted.
- Vertex Dot: At `(2, -3)`.
- Axis Line: Vertical line from top to bottom of axes at `x=2`.
============================================================
```

```text
========================================
📊 **LLM USAGE SESSION REPORT**
========================================
```

```text
========================================
```

