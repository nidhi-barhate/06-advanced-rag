from client.ollama_client import OllamaClient

class LLMService:

    def __init__(self):
        self.client = OllamaClient()

    def chat(self, prompt: str, new_chat: bool = True) -> str:

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.client.chat(
            messages=messages,
            new_chat=new_chat
        )