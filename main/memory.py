# main/memory.py
"""
Simple in-memory conversation store for context.
"""

class MemoryStore:
    def __init__(self):
        self.history = []

    def add_interaction(self, user: str, assistant: str):
        self.history.append((user, assistant))
        if len(self.history) > 20:  # keep last 20
            self.history.pop(0)

    def get_context(self) -> str:
        return "\n".join([f"User: {u}\nAssistant: {a}" for u,a in self.history])
