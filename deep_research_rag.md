# Deep Research Prompt: RAG for Manim Code Generation

**Topic**: Building a Retrieval-Augmented Generation (RAG) System for a Manim Coding Agent.

**Context**:
I have a team collecting "Golden Manim Examples" (Python scripts + MP4 videos).
My goal is to use this data to stop my AI Coder from "hallucinating" (making up fake functions).
I want the AI to "look up" how to implement a specific visual effect before writing code.

**Research Questions for Advanced LLM (DeepSeek-R1 / o1)**:

1.  **Indexing Strategy for Code**:
    *   Should I chunk the code by "Class", "Function", or "Manim Concept"?
    *   Manim code often relies on context (imports, setup). How do I preserve this context in small chunks?

2.  **Retrieval Strategy (The "Visual Gap")**:
    *   User asks: *"Draw a number line that zooms in."*
    *   Code implementation: uses `LinearTransformationScene` or `Camera.frame.animate.scale()`.
    *   *Challenge*: The user's query ("zoom in") doesn't match the code keywords (`camera`, `scale`).
    *   *Question*: How do I bridge this semantic gap? Should I use "HyDE" (Hypothetical Document Embeddings)? Or generate "Synthetic Captions" for every code snippet?

3.  **Prompt Engineering with RAG**:
    *   Once I retrieve 3 relevant code snippets, how do I feed them to the Coder?
    *   Should I say *"Here are examples"*? Or *"Follow this style"*?
    *   What is the optimal context window usage to prevent confusing the model?

**Desired Output**:
A concrete **RAG Architecture Diagram** and a suggested **Tech Stack** (e.g., ChromaDB vs FAISS, LangChain vs LlamaIndex) specifically for a Python Code Agent.
