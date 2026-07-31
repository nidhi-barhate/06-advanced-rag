from schemas.search_result import SearchResult

class PromptBuilderService:
    def build(
        self,
        question: str,
        search_results: list[SearchResult]
    ) -> str:

        context = "\n\n".join(
            result.text
            for result in search_results
        )

        return f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer:
"""