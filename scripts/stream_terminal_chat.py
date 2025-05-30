#!/usr/bin/env python3
# scripts/stream_terminal_chat.py

import sys, os

# Add project root to sys.path
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from main.mcp import MCP
from tools.summarize import summarize_tool
from main.personas import PERSONA_MAP

def stream_terminal_chat():
    mcp = MCP(persona_name='generalist', tools=[summarize_tool])

    try:
        while True:
            user = input("You: ")
            if user.lower() in {'exit','quit'}:
                print("Goodbye!"); break
            resp = mcp.respond(user)
            print("AI:", resp)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting…")

if __name__ == '__main__':
    stream_terminal_chat()

