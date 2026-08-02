import json
from typing import Any
from typing import Type
from urllib import response
from click import prompt
from pydantic import BaseModel
import requests
from config.settings import Settings

class OllamaClient:
    def embedding(self, prompt: str) -> list[float]:
        url = f"{Settings.OLLAMA_BASE_URL}/api/embed"
        payload = {
            "model": "nomic-embed-text",
            "input": prompt
        }
        response = requests.post(
            url,
            json=payload
        )
        return response.json()["embeddings"][0]

    def chat(self, messages: list, new_chat: bool = True) -> str:
        url = f"{Settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": Settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        }
        print("Request JSON:")
        print(payload)
        response = requests.post(
            url,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        # print("Status Code:", response.status_code)
        # print("Response JSON:")
        # print(response.json())
        return response.json()["message"]["content"]