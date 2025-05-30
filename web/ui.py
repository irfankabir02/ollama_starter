# web/ui.py
"""
Helper functions for Gradio UI rendering and state management in the AI assistant system.
Supports markdown rendering, persona styling, and voice integration.
"""
import markdown
from typing import List, Tuple, Dict, Optional
from main.personas import Persona
from main.mcp import MCP


class UIHelper:
    """Manages UI rendering and state for the Gradio interface."""

    def __init__(self, personas: List[Persona], mcp: MCP):
        """
        Initialize UI helper with personas and MCP instance.

        Args:
            personas: List of Persona objects from main/personas.py.
            mcp: MCP instance for backend interaction.
        """
        self.personas = {p.name.lower(): p for p in personas}
        self.mcp = mcp
        self.markdown_extensions = ['codehilite', 'fenced_code']

    def format_message(self, content: str, is_user: bool, persona_name: str = None) -> str:
        """
        Format message with HTML styling and persona-specific colors.

        Args:
            content: Message content.
            is_user: True if user message, False for assistant.
            persona_name: Name of the current persona (optional).

        Returns:
            HTML-formatted message string.
        """
        if is_user:
            return f'<div class="message user">{content}</div>'
        else:
            html_content = markdown.markdown(content, extensions=self.markdown_extensions)
            persona_class = f"persona-{persona_name.lower()}" if persona_name else ""
            voice_btn = (
                f'<button class="voice-btn" '
                f'onclick="speakText(`{content.replace("`", "").replace("'", "")}`)" '
                f'title="Speak this message">🔊</button>'
            )
            return f'<div class="message assistant {persona_class}">{html_content}{voice_btn}</div>'

    def get_welcome_message(self, persona_name: str) -> List[Tuple[Optional[str], str]]:
        """
        Generate a welcome message for the selected persona.

        Args:
            persona_name: Name of the current persona.

        Returns:
            List with a single (None, assistant_message) tuple.
        """
        persona_name = persona_name.lower()
        persona = self.personas.get(persona_name, self.personas.get('default'))
        welcome_text = (
            f"Hello! I'm {persona.name.replace('_', ' ').title()}. How can I assist you today?"
        )
        if persona_name == 'zen_monk':
            welcome_text = "🧘 Greetings, seeker. Let our conversation flow like a serene river."
        elif persona_name == 'shakespeare':
            welcome_text = "🎭 Good morrow, gentle soul! What discourse shall we weave today?"
        elif persona_name == 'quantum_mentor':
            welcome_text = "⚛️ Welcome to the realm of knowledge! Ready to unravel the universe?"

        return [(None, self.format_message(welcome_text, is_user=False, persona_name=persona_name))]

    def get_persona_choices(self) -> List[Tuple[str, str]]:
        """
        Get persona choices for dropdown with display names and icons.

        Returns:
            List of (display_name, persona_key) tuples.
        """
        choices = []
        for name, persona in self.personas.items():
            display_name = f"{self._get_persona_icon(name)} {persona.name.replace('_', ' ').title()}"
            choices.append((display_name, name))
        return choices

    def _get_persona_icon(self, persona_name: str) -> str:
        """Map persona names to emoji icons."""
        icons = {
            'generalist': '🤖',
            'zen_monk': '🧘',
            'shakespeare': '🎭',
            'quantum_mentor': '⚛️'
        }
        return icons.get(persona_name.lower(), '🤖')

    def update_persona_info(self, persona_display: str) -> Tuple[str, str]:
        """
        Update persona information display and return persona key.

        Args:
            persona_display: Selected persona display name from dropdown.

        Returns:
            Tuple of (info_text, persona_key).
        """
        persona_key = None
        for display, key in self.get_persona_choices():
            if display == persona_display:
                persona_key = key
                break

        if not persona_key:
            return "Select a persona", "default"

        info_text = {
            'generalist': "**Generalist**: A versatile assistant for all tasks.",
            'zen_monk': "**Zen Monk**: Offers wisdom with a calm, metaphorical tone. 🧘",
            'shakespeare': "**Shakespeare**: Speaks in poetic, Elizabethan English. 🎭",
            'quantum_mentor': "**Quantum Mentor**: Explains complex science clearly. ⚛️"
        }
        return info_text.get(persona_key, "Select a persona"), persona_key


if __name__ == "__main__":
    from main.personas import Persona
    from main.mcp import MCP
    from main.tools import NoteTaker, Search, TaskManager, Summarizer

    dummy_personas = [
        Persona(name="generalist", color="#28a745", tone="neutral", tools=[], memory=None),
        Persona(name="zen_monk", color="#6f42c1", tone="calm", tools=[], memory=None)
    ]
    dummy_tools = [NoteTaker(), Search(), Summarizer(), TaskManager()]
    dummy_mcp = MCP(personas=dummy_personas, tools=dummy_tools, memory=None)
    ui_helper = UIHelper(dummy_personas, dummy_mcp)
    print(ui_helper.get_persona_choices())
    print(ui_helper.get_welcome_message("generalist"))
