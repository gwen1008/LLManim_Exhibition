
import dspy
import os
from dotenv import load_dotenv

# 1. Setup Environment
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Please check your .env for GROQ_API_KEY")

# Configure DSPy to use Groq Llama3 via dspy.LM (OpenAI-compatible interface)
lm = dspy.LM(model="openai/llama-3.3-70b-versatile", api_key=api_key, api_base="https://api.groq.com/openai/v1")
dspy.settings.configure(lm=lm)

# 2. Define the Goal (Signature)
class ManimGenerator(dspy.Signature):
    """Generate Manim/Python code to animate a mathematical concept."""
    concept_description = dspy.InputField(desc="The mathematical concept to animate")
    manim_code = dspy.OutputField(desc="Executable Python code using Manim library")

# 3. Create the Module (Chain of Thought)
# This module will automatically think step-by-step before generating code
generator = dspy.ChainOfThought(ManimGenerator)

# 4. Create a small "Training Set" (Golden Examples)
# DSPy will learn from these to optimize the prompt
trainset = [
    dspy.Example(
        concept_description="Draw a red circle",
        manim_code="Circle(color=RED)"
    ).with_inputs("concept_description"),
    dspy.Example(
        concept_description="Show text 'Hello World' fading in",
        manim_code="text = Text('Hello World')\nself.play(FadeIn(text))"
    ).with_inputs("concept_description"),
]

# 5. Optimize the Prompt (Compile)
from dspy.teleprompt import BootstrapFewShot

# This "compiler" will test different few-shot combinations to find the best prompt
# Since we don't have a validation logic here, we just use it to "bootstrap" examples into the prompt
teleprompter = BootstrapFewShot(metric=None) 
optimized_generator = teleprompter.compile(generator, trainset=trainset)

# 6. Run the Optimized Agent
user_request = "Create a blue square transforming into a yellow circle"
print(f"\n🚀 User Request: {user_request}")

print("\n🤖 DSPy Agent is Thinking (Chain of Thought)...")
pred = optimized_generator(concept_description=user_request)

print(f"\n🧠 Prediction Object:\n{pred}")
# print(f"\n🧠 Reasoning (Hidden Thought Process):\n{pred.rationale}")
try:
    print(f"\n🧠 Reasoning:\n{pred.reasoning}")
except:
    pass
print(f"\n💻 Generated Code:\n{pred.manim_code}")
# 7. Inspect the "Perfect Prompt" DSPy created
print("\n📝 The Actual Prompt DSPy sent to the LLM:")
lm.inspect_history(n=1)
