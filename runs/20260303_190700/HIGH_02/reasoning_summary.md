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
**Concept Extraction**: Parabola, vertex form y = (x-h)^2 + k, vertex (h,k) = (2,-3), axis of symmetry x = h = 2, parent function y = x^2, transformations: horizontal shift right by 2, vertical shift down by 3.

**Visual Metaphor**: A coordinate plane as the stage. The parent parabola y=x^2 will be transformed step-by-step into the target parabola.

**Spatial Plan (High-Low Split to Prevent Overflow)**:
- **HEADER Zone (y ~ 3.0)**: Title and step labels.
- **CONTENT Zone (y ~ 0)**: Main coordinate axes and parabolas. This is the primary visual area.
- **FOOTER Zone (y ~ -3.0)**: Explanatory text for the current transformation step.

**Anchors**:
- `global_center`: ORIGIN (0,0,0). This will be the center of the coordinate axes.
- `title_anchor`: UP * 3.0 (HEADER zone).
- `explanation_anchor`: DOWN * 3.0 (FOOTER zone).

**Coordinate System**:
- Axes range: x from -4 to 6, y from -5 to 5. This ensures vertex (2,-3) is well-centered.
- Axes centered at `global_center`.

**Object Definitions & Constraints**:
1.  **Coordinate Axes**: Centered at ORIGIN.
2.  **Parent Parabola (y=x^2)**: Plotted on the axes. Vertex at (0,0).
3.  **Shifted Parabola (y=(x-2)^2)**: Result of horizontal shift. Vertex at (2,0).
4.  **Final Parabola (y=(x-2)^2 - 3)**: Result of vertical shift. Vertex at (2,-3).
5.  **Vertex Dot & Label**: At point (2, -3).
6.  **Axis of Symmetry Line**: Vertical line x=2, dashed style.
7.  **Function Labels**: MathTex objects placed near their respective curves.
8.  **Step Label**: In HEADER zone, updates with each major step.
9.  **Explanation Text**: In FOOTER zone, updates with each step.

**Signal Strategy**:
- Use `Indicate` (color=YELLOW) to highlight the transformation part of the equation (e.g., "-2", "-3").
- Use `Circumscribe` to draw attention to the vertex point.
- Use `Transform` to morph the parabola and its equation.
- Use `ReplacementTransform` for step labels and explanations to avoid overflow.

**Chunking**:
1.  Setup: Show axes and parent function.
2.  Horizontal Shift: Transform parent parabola and equation, show intermediate vertex.
3.  Vertical Shift: Transform to final parabola, show final vertex.
4.  Labeling: Add vertex label and axis of symmetry line.
5.  Recap: Highlight all key features together.
============================================================
```

```text
========================================
👁️  [Vision Agent Audit - CoVT Framework]
----------------------------------------
{
  "visual_rationale": "The final frame displays the completed transformation of the parabola with the vertex labeled at (2, -3) and the axis of symmetry marked at x=2. The explanation text at the bottom summarizes the transformation, while the step label indicates the current step in the process.",
  "temporal_analysis": "From 70% to 95%, the parabola shifts down to its final position, the vertex label appears, and the axis of symmetry is drawn. The explanation text is updated to reflect the final state.",
  "confidence_score": 4,
  "verdict": "PASS",
  "overall_critique": "All elements are present and correctly positioned according to the layout plan, with no significant defects.",
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

