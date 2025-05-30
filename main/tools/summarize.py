# tools/summarize.py
"""
A simple summarization tool stub.
"""

def summarize_tool(text: str) -> str:
    if len(text) < 30:
        return "Too short to summarize."
    return f"[Summary] {text[:100]}…"
