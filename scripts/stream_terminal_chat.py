# scripts/stream_terminal_chat.py
"""
Terminal-based chat interface with streaming responses and tool support.
"""
import typer
from typing import Optional
from main.mcp import MCP
from main.personas import Persona
from main.tools import NoteTaker, Search, Summarizer, TaskManager
from main.memory import Memory


def stream_chat(persona: Optional[str] = "generalist"):
    """
    Run a terminal-based chat with streaming responses.

    Args:
        persona: Initial persona name (default: generalist).
    """
    # Initialize MCP
    tools = [NoteTaker(), Search(), Summarizer(), TaskManager()]
    personas = [
        Persona(name="generalist", color="#28a745", tone="neutral", tools=tools, memory=Memory()),
        Persona(name="zen_monk", color="#6f42c1", tone="calm", tools=tools, memory=Memory()),
        Persona(name="shakespeare", color="#dc3545", tone="poetic", tools=tools, memory=Memory()),
        Persona(name="quantum_mentor", color="#007bff", tone="technical", tools=tools, memory=Memory())
    ]
    mcp = MCP(personas=personas, tools=tools, memory=Memory())
    context = {"current_persona": persona.lower()}

    typer.secho(f"Starting chat with {persona}. Type '@switch persona_name' to change personas, or use tool commands like '@note'.", fg=typer.colors.GREEN)
    typer.secho("Type 'exit' to quit.", fg=typer.colors.YELLOW)

    while True:
        try:
            user_input = typer.prompt("You")
            if user_input.lower() == 'exit':
                break

            print(f"{persona}> ", end="", flush=True)
            for chunk in mcp.process_input(user_input, context):
                print(chunk, end="", flush=True)
            print()  # Newline after response
        except KeyboardInterrupt:
            typer.secho("\nExiting chat...", fg=typer.colors.RED)
            break
        except Exception as e:
            typer.secho(f"Error: {str(e)}", fg=typer.colors.RED)


if __name__ == "__main__":
    typer.run(stream_chat)
