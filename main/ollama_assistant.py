# main/ollama_assistant.py
"""
Manages interactions with the local Ollama server for text generation.
Supports streaming and synchronous calls with robust error handling.
"""
import requests
import json
from typing import Generator, Optional
from urllib.parse import urljoin


class OllamaAssistant:
    """Interface for interacting with the Ollama server."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        """
        Initialize the Ollama assistant.

        Args:
            base_url: Ollama server URL (default: http://localhost:11434).
            model: Model name (default: llama3.1).
        """
        self.base_url = base_url
        self.model = model
        self.api_generate = urljoin(base_url, "/api/generate")

    def generate_stream(self, prompt: str, timeout: int = 30) -> Generator[str, None, None]:
        """
        Stream text generation from Ollama.

        Args:
            prompt: Input prompt for the model.
            timeout: Request timeout in seconds.

        Yields:
            Response chunks as strings.

        Raises:
            requests.RequestException: If the request fails.
        """
        try:
            response = requests.post(
                self.api_generate,
                json={"model": self.model, "prompt": prompt, "stream": True},
                stream=True,
                timeout=timeout
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    yield chunk['response']
        except requests.RequestException as e:
            yield f"Error communicating with Ollama: {str(e)}"

    def generate_sync(self, prompt: str, timeout: int = 10) -> str:
        """
        Perform synchronous text generation.

        Args:
            prompt: Input prompt for the model.
            timeout: Request timeout in seconds.

        Returns:
            Complete response as a string.

        Raises:
            requests.RequestException: If the request fails.
        """
        try:
            response = requests.post(
                self.api_generate,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=timeout
            )
            response.raise_for_status()
            return json.loads(response.text)['response']
        except requests.RequestException as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    assistant = OllamaAssistant()
    # Test streaming
    print("Streaming test:")
    for chunk in assistant.generate_stream("Hello, how are you?"):
        print(chunk, end="")
    # Test synchronous
    print("\nSynchronous test:")
    print(assistant.generate_sync("What is 1+1?"))
