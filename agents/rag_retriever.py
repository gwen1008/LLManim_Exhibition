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
                alpha=0.75, 
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

    def format_for_prompt(self, examples: List[Dict]) -> str:
        """Format retrieved examples into a string for the LLM prompt."""
        if not examples:
            return ""
            
        formatted = "\n\n=== 📚 REFERENCE EXAMPLES (RAG) ===\n"
        formatted += "Use these verified snippets to guide your implementation. Do not hallucinate classes.\n"
        
        for i, ex in enumerate(examples, 1):
            formatted += f"\n--- Example {i} ---\n"
            formatted += f"Visual Description: {ex['description']}\n"
            formatted += f"Code:\n```python\n{ex['code']}\n```\n"
            
        return formatted

    def close(self):
        """Close the client connection."""
        if self.client:
            self.client.close()
