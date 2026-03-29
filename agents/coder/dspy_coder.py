import dspy
import os
from ..core.rag_retriever import RAGRetriever

class ManimSignature(dspy.Signature):
    """
    Generate executable Manim (Python) code to animate a mathematical concept.
    The code must be a complete, runnable Python script importing `manim`.
    """
    context_examples = dspy.InputField(desc="Relevant Manim code patterns to learn from")
    concept_description = dspy.InputField(desc="The user's description of the animation")
    
    reasoning = dspy.OutputField(desc="Step-by-step logic for how to implement this in Manim")
    manim_code = dspy.OutputField(desc="The complete Python code block")

class DSPyCoder:
    def __init__(self, debug=True):
        self.debug = debug
        
        # 1. Initialize Large Language Model (Groq/DeepSeek via OpenAI interface)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("⚠️ DSPyCoder: GROQ_API_KEY not found. DSPy mode disabled.")
            self.enabled = False
            return
            
        # Use dspy.LM for reliable compatibility
        self.lm = dspy.LM(
            model="openai/llama-3.3-70b-versatile", 
            api_key=api_key, 
            api_base="https://api.groq.com/openai/v1"
        )
        dspy.settings.configure(lm=self.lm)
        
        # 2. Initialize RAG for Dynamic Few-Shot
        self.rag = RAGRetriever()
        
        # 3. Create the Logic Module (Chain of Thought)
        self.generate = dspy.ChainOfThought(ManimSignature)
        self.enabled = True
        
        if self.debug:
            print("🤖 DSPy Coder initialized with Llama-3 (Groq)")

    def generate_code(self, concept: str, reflection_context: str = "") -> str:
        """
        Generate Manim code using DSPy optimization.
        
        Args:
            concept: script JSON or animation description
            reflection_context: Task 12 — 格式化的過去教訓字串（來自 _format_reflection_memory）
        """
        if not self.enabled:
            return "# Error: DSPy not enabled"
            
        print(f"\n🧠 [DSPy] Thinking about: {concept}")
        
        # 1. Retrieve "Golden Examples" + API Rules from RAG
        retrieved = self.rag.retrieve_examples(concept, limit=2)
        retrieved += self.rag.retrieve_rules(concept, limit=2)

        # Format retrieval for context
        context_str = self.rag.format_for_prompt(retrieved) if retrieved else ""
        
        # Task 12: 注入 reflection 記憶（若有）
        if reflection_context:
            context_str += f"\n{reflection_context}"
        
        # 2. Run Generation
        try:
            prediction = self.generate(
                context_examples=context_str,
                concept_description=concept
            )
            
            if self.debug:
                print(f"🔍 [DSPy Reasoning]: {prediction.reasoning}")
                
            code = prediction.manim_code
            
            # Clean up markdown code blocks if present
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].strip()
                
            return code
            
        except Exception as e:
            print(f"⚠️ [DSPy Error]: {e}")
            return f"# Error generating code: {e}"

