"""
RAG Retriever Module
====================
Handles retrieval of 'Golden Manim Examples' from Weaviate to ground the Coder agent.
"""

import os
import weaviate
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Optional

class RAGRetriever:
    """Interface for retrieving semantic code examples from vector database."""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        # Connect to local Weaviate instance
        # Note: In docker-compose we set OPENAI_APIKEY env var for the container.
        # Here we rely on the python client using the local env var if needed for client-side operations,
        # but mostly we rely on the server-side text2vec-openai module.
        try:
            self.client = weaviate.connect_to_local(host=host, port=port)
            self._check_connection()
        except Exception as e:
            print(f"⚠️  RAG Warning: Could not connect to Weaviate at {host}:{port}. Error: {e}")
            self.client = None

    def _check_connection(self):
        """Verify connection to Weaviate."""
        if self.client and self.client.is_live():
            print("✅ RAG System: Connected to Weaviate.")
        else:
            print("⚠️  RAG System: Weaviate is not live.")
            self.client = None

    def retrieve_examples(self, query: str, limit: int = 3) -> List[Dict]:
        """
        Retrieve relevant code examples based on natural language query.
        
        Args:
            query: The visual description (e.g., "A rotating red square")
            limit: Number of examples to retrieve
            
        Returns:
            List of dictionaries containing 'code', 'description', and 'score'.
        """
        if not self.client:
            return []

        try:
            collection = self.client.collections.get("ManimGoldenPair")
            
            # Hybrid Search: Combines keyword (BM25) and vector (Semantic) search
            # Alpha 0.75 leans towards vector search (semantic) which is better for "visual descriptions"
            response = collection.query.hybrid(
                query=query,
                limit=limit,
                alpha=0.5,  # Balanced: 0=pure BM25 keyword, 1=pure vector. 0.5 improves Manim API name matching.
                return_metadata=MetadataQuery(score=True)
            )
            
            results = []
            for obj in response.objects:
                results.append({
                    "description": obj.properties.get("video_description", "No description"),
                    "code": obj.properties.get("code_content", ""),
                    "imports": obj.properties.get("imports", ""),
                    "modules": obj.properties.get("manim_modules", ""),
                    "score": obj.metadata.score
                })
                
            print(f"🔍 RAG Search: Found {len(results)} examples for '{query}'")
            return results
            
        except Exception as e:
            print(f"⚠️  RAG Retrieval Failed: {e}")
            return []

    def _prune_code(self, code: str) -> str:
        """
        Extract only the construct() method body from a Manim Scene class.
        Removes imports, class definitions, and other boilerplate to reduce token usage.
        
        Args:
            code: Full Python code including imports and class definition
            
        Returns:
            Just the construct() method body (indented code, min 4 spaces context)
        """
        import ast
        import textwrap

        try:
            tree = ast.parse(code)
            
            # Find the Scene class
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    # Find the construct method
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == 'construct':
                            # Get exact line numbers
                            start_line = item.body[0].lineno - 1
                            end_line = item.body[-1].end_lineno
                            
                            # Extract lines from original code to preserve formatting
                            lines = code.split('\n')[start_line:end_line]
                            
                            # Dedent uniformly
                            pruned = textwrap.dedent('\n'.join(lines)).strip()
                            return pruned
            
            # If no construct method found, fallback to regex as safety net
            import re
            pattern = re.compile(r'def construct\(self\):\s*([\s\S]*?)(?=\n\s*def |\n\s*class |\Z)')
            match = pattern.search(code)
            if match:
                return textwrap.dedent(match.group(1)).strip()
                
        except SyntaxError:
            # Code is not parseable, fallback to original
            pass

        return code

    def format_for_prompt(self, examples: List[Dict]) -> str:
        """Format retrieved examples into a string for the LLM prompt."""
        if not examples:
            return ""
            
        formatted = "\n\n=== 📚 REFERENCE EXAMPLES (RAG - Core Logic Only) ===\n"
        formatted += "Use these verified patterns. Full imports/class structure are in your system prompt.\n"
        
        for i, ex in enumerate(examples, 1):
            formatted += f"\n--- Example {i} ---\n"
            formatted += f"Visual: {ex['description']}\n"
            
            # Prune the code to only construct() body
            pruned_code = self._prune_code(ex['code'])
            formatted += f"Core Logic:\n```python\n{pruned_code}\n```\n"
            
        return formatted

    def close(self):
        """Close the client connection."""
        if self.client:
            self.client.close()
