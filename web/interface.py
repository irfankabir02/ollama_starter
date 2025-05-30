# web/interface.py
from main.mcp import MCP

def talk(prompt: str, persona: str) -> str:
    mcp = MCP(persona_name=persona, tools=[])
    return mcp.respond(prompt)

