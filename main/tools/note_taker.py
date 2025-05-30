# tools/note_taker.py
"""
Simple note-taking tool: appends to a local file.
"""

def note_taker_tool(note: str) -> str:
    with open('notes.txt', 'a') as f:
        f.write(note + '\n')
    return "Note saved."
