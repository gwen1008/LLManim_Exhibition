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
**Concept Extraction**: Parabola defined by `y = (x-2)^2 - 3`. Vertex at (2, -3). Axis of symmetry: x = 2. Key pedagogical goal: Show the relationship between the vertex form equation and the graph's features.

**Selected Strategy (C): Progressive Transformation**
1.  Start with the parent function `y = x^2` (centered at origin).
2.  Animate the horizontal shift to get `y = (x-2)^2`.
3.  Animate the vertical shift to get the final equation `y = (x-2)^2 - 3`.
4.  Label the vertex (2, -3) and draw the axis of symmetry x=2.
5.  Demonstrate symmetry by plotting symmetric points.

**Spatial Plan & Zone Assignment**:
-   **HEADER Zone (y ~ 3.5)**: Title and current equation display.
-   **CONTENT Zone (y ~ 0)**: Coordinate axes and the parabola plot. This is the main stage.
-   **FOOTER Zone (y ~ -3.0)**: Explanatory text for each transformation step.

**Coordinate & Geometry Calculations**:
-   Axes: `x_range=[-2, 6, 1], y_range=[-5, 5, 1]`. This ensures vertex (2,-3) is well-centered.
-   Parent Parabola (`y=x^2`): Sample points e.g., (-2,4), (-1,1), (0,0), (1,1), (2,4).
-   Shifted Parabola: Vertex at (2, -3). Symmetric points: (1, -2), (3, -2); (0, 1), (4, 1).
-   Axis of Symmetry: Vertical line from (2, -5) to (2, 5).

**Visual Hierarchy & Constraints**:
-   Primary: Axes and Parabola curve (Scale=1.0, in CONTENT zone).
-   Secondary: Vertex dot, Axis line, Equation display (Scale=0.9, attached to primary).
-   Tertiary: Grid lines, step labels (Faded, in background/FOOTER).

**Signal Strategy**:
-   Use `Indicate` (red) on the `(x-2)` and `-3` in the equation as the corresponding shift occurs.
-   Use `Circumscribe` (yellow) around the vertex point (2,-3) when labeling it.
-   Use `Indicate` on symmetric points to demonstrate reflection across the axis.

**Overflow Prevention**:
-   The main equation will be displayed in the HEADER zone, separate from the graph.
-   Explanatory text is kept to one line in the FOOTER zone.
-   The graph in the CONTENT zone has ample space. We will use `ReplacementTransform` to update the equation in the header and the explanation in the footer, preventing stacking.
============================================================
```

```text
========================================
👁️  [Vision Agent Audit - CoVT Framework]
----------------------------------------
{
  "visual_rationale": "The final frame displays the completed transformation of the parabola, with the equation y = (x-2)² - 3 prominently shown in yellow. The vertex at (2, -3) is marked with a red dot and labeled, while the axis of symmetry is represented by a purple line and label. The overall layout adheres to the planned three-zone structure, with the equation in the header, the graph in the center, and the explanation at the bottom.",
  "temporal_analysis": "From 70% to 95%, the vertex dot, vertex label, axis line, and axis label are added, completing the visual representation of the parabola's features. All expected elements from the script are present in the final frame.",
  "confidence_score": 5,
  "verdict": "PASS",
  "overall_critique": "All checks passed with no defects found.",
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

