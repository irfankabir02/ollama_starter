# main/personas.py
"""
Defines Persona objects with attributes and dynamic behavior for the AI assistant.
"""
from dataclasses import dataclass
from typing import List, Dict, Any
from .memory import Memory
from .tools.base import Tool  # Corrected import


@dataclass
class Persona:
    """Represents an AI persona with name, color, tone, tools, and memory."""
    name: str
    color: str
    tone: str
    tools: List[Tool]
    memory: Memory

    def process_input(self, state: Dict[str, Any]) -> str:
        """
        Process input with dynamic tone adjustment based on context.
        
        Args:
            state: Dictionary with user_input, tool_output, context, memory, persona.
            
        Returns:
            Formatted prompt string for Ollama.
        """
        user_input = state['user_input']
        context = state['context']
        memory = state['memory']
        
        # Dynamic tone adjustment
        dynamic_tone = self.tone
        if any(keyword in user_input.lower() for keyword in ["formal", "professional", "business"]):
            dynamic_tone = "formal"
        elif "casual" in user_input.lower():
            dynamic_tone = "casual"
        
        # Retrieve relevant context
        past_context = memory.retrieve_context(self.name)
        prompt = (
            f"Persona: {self.name} (Tone: {dynamic_tone})\n"
            f"Context: {json.dumps(past_context) if past_context else 'No prior context'}\n"
            f"Input: {user_input}\n"
            f"Response: "
        )
        return prompt


if __name__ == "__main__":
    from .tools.note_taker import NoteTaker
    from .memory import Memory
    import json
    persona = Persona(
        name="generalist",
        color="#28a745",
        tone="neutral",
        tools=[NoteTaker()],
        memory=Memory()
    )
    state = {
        "user_input": "formal request",
        "context": {},
        "memory": persona.memory,
        "persona": persona
    }
    print(persona.process_input(state))
