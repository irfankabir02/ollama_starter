# main/mcp.py
"""
Model Context Protocol: orchestrates persona, memory, tools, and model calls.
"""

import time
from typing import Any, Dict, List, Optional, Callable
from ollama import chat, ResponseError
from main.memory import MemoryStore
from main.personas import get_persona

class MCP:
    def __init__(
        self,
        persona_name: str = 'generalist',
        tools: Optional[List[Callable[[str], str]]] = None,
        llm_params: Optional[Dict[str, Any]] = None,
        debug: bool = False
    ):
        persona = get_persona(persona_name)
        self.persona_name = persona.name
        self.persona_prompt = persona.system_prompt
        self.model = persona.model
        self.history: List[Dict[str, Any]] = []
        self.memory = MemoryStore()
        self.tools = tools or []
        self.llm_params = llm_params or {'temperature': 0.7, 'top_p': 0.9}
        self.debug = debug

    def add_user(self, text: str):
        self.history.append({'role':'user','content':text,'time':time.time()})

    def add_assistant(self, text: str):
        self.history.append({'role':'assistant','content':text,'time':time.time()})

    def build_messages(self) -> List[Dict[str,str]]:
        # System persona
        msgs = [{'role':'system','content': self.persona_prompt}]
        # Inject recent memory if any
        context = self.memory.get_context()
        if context:
            msgs.append({'role':'system','content': f"[Memory]\n{context}"})
        # Conversation history (last 10 turns)
        for turn in self.history[-10:]:
            msgs.append({'role':turn['role'],'content':turn['content']})
        return msgs

    def detect_tool(self, user_input: str) -> Optional[Dict[str,str]]:
        # syntax: tool_name: payload
        if ':' in user_input:
            name, payload = user_input.split(':',1)
            for tool in self.tools:
                if tool.__name__ == f"{name.strip()}_tool":
                    return {'tool': tool, 'payload': payload.strip()}
        return None

    def call_tool(self, tool: Callable[[str], str], payload: str) -> str:
        try:
            return tool(payload)
        except Exception as e:
            return f"[ToolError] {e}"

    def call_llm(self, messages: List[Dict[str,str]]) -> str:
        try:
            resp = chat(model=self.model, messages=messages, **self.llm_params)
            return resp.message.content
        except ResponseError as e:
            return f"[LLM Error {e.status_code}] {e.error}"

    def respond(self, user_input: str) -> str:
        self.add_user(user_input)

        tool_call = self.detect_tool(user_input)
        if tool_call:
            result = self.call_tool(tool_call['tool'], tool_call['payload'])
            self.add_assistant(result)
            self.memory.add_interaction(user_input, result)
            return result

        messages = self.build_messages()
        if self.debug:
            print("→ Prompt messages:", messages)
        reply = self.call_llm(messages)
        self.add_assistant(reply)
        self.memory.add_interaction(user_input, reply)
        return reply
