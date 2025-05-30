# main/mcp.py
"""
Model Context Protocol (MCP): Routes user input to personas and tools, manages context,
and streams AI responses using Ollama. Enhanced for advanced tag parsing, reasoning, and caching.
"""
import re
import json
from typing import Dict, List, Generator, Optional, Any
from functools import lru_cache
import requests

from .personas import Persona
from .tools import Tool
from .memory import Memory
from .ollama_assistant import OllamaAssistant


@dataclass
class ToolCall:
    """Represents a tool invocation with input and optional parameters."""
    tool_name: str
    input: str
    params: Dict[str, str]


class MCP:
    """Coordinates input routing, persona selection, tool execution, and response streaming."""
    
    def __init__(self, personas: List[Persona], tools: List[Tool], memory: Memory):
        """
        Initialize MCP with personas, tools, and memory backend.
        
        Args:
            personas: List of Persona instances.
            tools: List of Tool instances.
            memory: Memory backend for context storage.
        """
        self.personas = {persona.name.lower(): persona for persona in personas}
        self.tools = {tool.name.lower(): tool for tool in tools}
        self.memory = memory
        self.ollama = OllamaAssistant()
        self.response_cache = {}  # In-memory cache for repeated queries

    def process_input(self, user_input: str, context: Dict[str, Any]) -> Generator[str, None, None]:
        """
        Process user input, route to persona/tools, and yield response chunks.
        
        Args:
            user_input: Raw user input string.
            context: Dictionary with current persona and session state.
            
        Yields:
            Response chunks as plain text.
        """
        # Handle persona switch
        if self._is_switch_command(user_input):
            new_persona = self._extract_persona_from_command(user_input)
            if new_persona in self.personas:
                context['current_persona'] = new_persona
                self.memory.store_context(new_persona, {"last_switch": user_input, "timestamp": time.time()})
                yield f"Switched to persona '{new_persona}'"
            else:
                yield f"Persona '{new_persona}' not found"
            return

        # Default persona
        current_persona_name = context.get('current_persona', 'generalist').lower()
        if current_persona_name not in self.personas:
            current_persona_name = 'generalist'
            context['current_persona'] = current_persona_name
        persona = self.personas[current_persona_name]

        # Check for message tags (e.g., @note priority=high)
        tool_output: Optional[str] = None
        tool_call = self._parse_message_tag(user_input)
        if tool_call:
            if tool_call.tool_name in self.tools:
                tool = self.tools[tool_call.tool_name]
                try:
                    tool_output = tool.execute(tool_call.input, tool_call.params)
                    self.memory.store_context(current_persona_name, {
                        "tool_call": {
                            "tool_name": tool_call.tool_name,
                            "input": tool_call.input,
                            "params": tool_call.params
                        },
                        "output": tool_output,
                        "timestamp": time.time()
                    })
                except Exception as e:
                    yield f"Error executing tool '{tool_call.tool_name}': {str(e)}"
                    return
            else:
                yield f"Tool '{tool_call.tool_name}' not recognized"
                return

        # Prepare state for reasoning
        state = {
            'user_input': user_input,
            'tool_output': tool_output,
            'context': context,
            'memory': self.memory,
            'persona': persona
        }

        # Multi-step reasoning
        prompt = self._reason_multi_step(state)
        cache_key = f"{current_persona_name}:{user_input}"
        if cache_key in self.response_cache:
            yield self.response_cache[cache_key]
            return

        # Stream response
        full_response = ""
        try:
            for chunk in self.ollama.generate_stream(prompt):
                full_response += chunk
                yield chunk
                self.memory.store_context(current_persona_name, {
                    "response_chunk": chunk,
                    "timestamp": time.time()
                })
            self.response_cache[cache_key] = full_response
        except Exception as e:
            yield f"Error generating response: {str(e)}"

        # Experiment: Cross-persona collaboration for complex queries
        if self._is_complex_query(user_input):
            for chunk in self._collaborate_personas(user_input, context):
                yield chunk

    def _parse_message_tag(self, user_input: str) -> Optional[ToolCall]:
        """
        Parse message tags like @note priority=high.
        
        Args:
            user_input: Input string to parse.
            
        Returns:
            ToolCall object or None if no valid tag.
        """
        if not user_input.strip().startswith("@"):
            return None
        match = re.match(r"@(\w+)(?:\s+(.+?))?(?:\s+(.+))?$", user_input.strip())
        if not match:
            return None
        tool_name, input_text, params_str = match.groups()
        params = {}
        if params_str:
            for param in params_str.split():
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key.lower()] = value
        return ToolCall(tool_name=tool_name.lower(), input=input_text or "", params=params)

    def _is_switch_command(self, user_input: str) -> bool:
        """Check if input is a persona switch command."""
        return user_input.strip().lower().startswith("@switch ")

    def _extract_persona_from_command(self, user_input: str) -> str:
        """Extract persona name from switch command."""
        try:
            return user_input.split()[1].lower()
        except IndexError:
            return ""

    def _is_complex_query(self, user_input: str) -> bool:
        """Determine if input requires multi-persona collaboration."""
        return len(user_input.split()) > 10 or any(keyword in user_input.lower() for keyword in ["analyze", "complex", "plan"])

    def _reason_multi_step(self, state: Dict[str, Any]) -> str:
        """
        Implement chain-of-thought reasoning for complex queries.
        
        Args:
            state: Dictionary with user_input, tool_output, context, memory, persona.
            
        Returns:
            Formatted prompt for Ollama.
        """
        user_input = state['user_input']
        persona = state['persona']
        memory = state['memory']
        past_context = memory.retrieve_context(persona.name)

        prompt = f"Persona: {persona.name} (Tone: {persona.tone})\n"
        if past_context:
            prompt += f"Previous context: {json.dumps(past_context)}\n"
        prompt += (
            f"Input: {user_input}\n"
            f"Step 1: Identify key components of the query.\n"
            f"Step 2: Plan a response strategy.\n"
            f"Step 3: Generate a concise, accurate response.\n"
        )
        return prompt

    def _collaborate_personas(self, user_input: str, context: Dict[str, Any]) -> Generator[str, None, None]:
        """
        Experiment: Route complex queries to multiple personas for collaborative response.
        
        Args:
            user_input: User input string.
            context: Current context dictionary.
            
        Yields:
            Collaborative response chunks.
        """
        for persona_name in self.personas:
            if persona_name != context.get('current_persona'):
                temp_context = context.copy()
                temp_context['current_persona'] = persona_name
                yield f"[{persona_name}]: "
                for chunk in self.process_input(user_input, temp_context):
                    yield chunk


if __name__ == "__main__":
    from .personas import Persona
    from .tools import NoteTaker
    from .memory import Memory
    import time
    dummy_persona = Persona(name="generalist", color="#28a745", tone="neutral", tools=[NoteTaker()], memory=Memory())
    dummy_tools = [NoteTaker()]
    mcp = MCP(personas=[dummy_persona], tools=dummy_tools, memory=Memory())
    context = {"current_persona": "generalist"}
    for chunk in mcp.process_input("Hello, @note priority=high Meeting at 3pm", context):
        print(chunk, end="")
