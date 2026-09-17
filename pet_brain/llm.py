import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

@dataclass(frozen=True)
class LLMConfig:
    model: str = os.getenv("PET_LLM_MODEL", "llama3")
    base_url: str = os.getenv("PET_OLLAMA_URL", "http://127.0.0.1:11434")
    timeout: float = float(os.getenv("PET_LLM_TIMEOUT", "30"))

class OllamaClient:
    """Small dependency-free client for the local Ollama HTTP API."""
    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()

    def chat_json(self, system: str, user: str) -> dict:
        payload = {
            "model": self.config.model,
            "stream": False,
            "format": "json",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "options": {"temperature": 0.2},
        }
        request = urllib.request.Request(
            f"{self.config.base_url.rstrip('/')}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Ollama unavailable: {exc}") from exc
        content = body.get("message", {}).get("content", "")
        if not content:
            raise RuntimeError("Ollama returned an empty response")
        try:
            result = json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Ollama returned invalid JSON") from exc
        if not isinstance(result, dict):
            raise RuntimeError("Ollama JSON response must be an object")
        return result
