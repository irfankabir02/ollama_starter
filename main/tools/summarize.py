# main/tools/summarize.py
"""
Summarization tool for condensing text content.
"""
from .base import Tool
from main.ollama_assistant import OllamaAssistant


class Summarizer(Tool):
    """Tool for summarizing text content."""

    name = "summarize"

    def __init__(self):
        self.ollama = OllamaAssistant()

    def execute(self, input_text: str, params: Dict[str, str] = None) -> str:
        """
        Summarize the input text with optional length control.

        Args:
            input_text: Text to summarize.
            params: Optional parameters (e.g., {'length': 'short'}).

        Returns:
            Summarized text or error message.
        """
        params = params or {}
        length = params.get('length', 'medium').lower()
        max_words = {'short': 50, 'medium': 100, 'long': 200}.get(length, 100)

        if not input_text.strip():
            return "Error: Empty input text"

        prompt = (
            f"Summarize the following text in approximately {max_words} words, "
            f"preserving key points:\n\n{input_text}"
        )
        return self.ollama.generate_sync(prompt)


if __name__ == "__main__":
    summarizer = Summarizer()
    text = "This is a long text about AI assistants. They help users with tasks like note-taking, searching, and summarizing. AI assistants are improving rapidly."
    print(summarizer.execute(text, {"length": "short"}))
