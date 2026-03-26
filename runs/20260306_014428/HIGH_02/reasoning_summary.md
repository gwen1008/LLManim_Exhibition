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
**Concept Extraction**: Parabola defined by y = (x-2)² - 3. Vertex at (2, -3). Axis of symmetry: vertical line x=2. The equation is in vertex form y = a(x-h)² + k, with a=1, h=2, k=-3.

**Visual Metaphor (Selected: Abstract)**: Transform the parent parabola y = x² into the target parabola.

**Spatial Plan & Zone Assignment**:
- **HEADER Zone (y ~ 3.5)**: Title "Graphing y = (x-2)² - 3".
- **CONTENT Zone (y ~ 0)**: Central stage for the coordinate plane, graphs, and key equations. This is the primary visual area.
- **FOOTER Zone (y ~ -3.0)**: Area for step-by-step textual explanations.

**Layout Logic**:
1.  A coordinate axes object (`axes`) will be centered at the CONTENT zone anchor (`global_center`). Its scale will be set so the vertex (2,-3) and a reasonable range of x-values (e.g., -1 to 5) are clearly visible.
2.  The parent function `y=x²` will be plotted first, centered at (0,0).
3.  The transformation to `y=(x-2)²` (shift right) will be animated.
4.  The transformation to `y=(x-2)² - 3` (shift down) will be animated.
5.  Final annotations (vertex dot, vertex label, axis of symmetry line) will be added to the final graph.

**Constraint Calculations**:
- Axes range: x from -2 to 6, y from -5 to 5. This ensures vertex (2,-3) is centered and there's room for labels.
- Vertex dot radius: 0.08.
- Axis of symmetry line: A dashed vertical line from top to bottom of the axes at x=2.
- Label positions: Vertex label `(2, -3)` placed to the right of the vertex dot. Axis label `x = 2` placed above the axes.

**Signal Strategy**:
- Use `Indicate` (color change/pulse) on the `(x-2)` part of the equation to signal horizontal shift.
- Use `Indicate` on the `-3` to signal vertical shift.
- Use `Circumscribe` to highlight the vertex point and the axis line once drawn.
============================================================
```

```text
========================================
👁️  [Vision Agent Audit - CoVT Framework]
----------------------------------------
{
  "visual_rationale": "The final frame displays the completed graph of the parabola y = (x-2)² - 3, with the vertex marked at (2, -3) and the axis of symmetry indicated by a dashed line at x = 2. The labels for the vertex and the axis of symmetry are clearly visible, and the parabola is shown in its final yellow form.",
  "temporal_analysis": "In the transition from 70% to 95%, the vertex dot and its label appear, followed by the dashed line for the axis of symmetry. All expected elements are present in the final frame, and the transitions occur smoothly without premature appearances.",
  "confidence_score": 5,
  "verdict": "PASS",
  "overall_critique": "All checks passed.",
  "defects": []
}
========================================
```

```text
========================================
📊 **LLM USAGE SESSION REPORT**
========================================
```

```text
========================================
```

