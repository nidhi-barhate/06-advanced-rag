from pathlib import Path

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

            Answer the question ONLY using the provided context.
            If the answer cannot be found in the context, reply exactly:
            "I couldn't find enough information in the provided knowledge base."
            Do not use your own knowledge.
            Do not make assumptions.
            Do not invent an answer.

            Context:
            {context}

            Question:
            {question}

            Answer:
            """

    def build_rerank_prompt(
            self,
            question: str,
            document: str
    ) -> str:
        prompt = Path(
            "prompts/rerank.txt"
        ).read_text(
            encoding="utf-8"
        )
        prompt = prompt.replace(
            "{question}",
            question
        )
        prompt = prompt.replace(
            "{document}",
            document
        )
        return prompt