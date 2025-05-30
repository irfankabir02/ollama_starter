# main/memory.py
"""
Manages persona-specific context storage with SQLite and auto-summarization.
"""
import sqlite3
import json
import time
from typing import Dict, Any
from main.tools.summarize import Summarizer


class Memory:
    """Stores and retrieves persona-specific context using SQLite."""
    
    def __init__(self, db_path: str = "memory.db"):
        """
        Initialize SQLite database for context storage.
        
        Args:
            db_path: Path to SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contexts (
                persona TEXT,
                context_key TEXT,
                context_value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        self.summarizer = Summarizer()
        self.max_contexts = 5  # Threshold for auto-summarization

    def store_context(self, persona: str, context: Dict[str, Any]):
        """
        Store context for a persona.
        
        Args:
            persona: Persona name.
            context: Context dictionary to store.
        """
        try:
            context_json = json.dumps(context)
            self.cursor.execute(
                "INSERT INTO contexts (persona, context_key, context_value) VALUES (?, ?, ?)",
                (persona.lower(), context.get('context_key', f"ctx_{int(time.time())}"), context_json)
            )
            self.conn.commit()
            self._auto_summarize(persona)
        except sqlite3.Error as e:
            print(f"Error storing context: {str(e)}")

    def retrieve_context(self, persona: str) -> Dict[str, Any]:
        """
        Retrieve the latest context for a persona.
        
        Args:
            persona: Persona name.
            
        Returns:
            Latest context dictionary or empty dict if none found.
        """
        try:
            self.cursor.execute(
                "SELECT context_value FROM contexts WHERE persona = ? ORDER BY timestamp DESC LIMIT 1",
                (persona.lower(),)
            )
            result = self.cursor.fetchone()
            return json.loads(result[0]) if result else {}
        except sqlite3.Error as e:
            print(f"Error retrieving context: {str(e)}")
            return {}

    def _auto_summarize(self, persona: str):
        """
        Summarize context if it exceeds max_contexts for a persona.
        
        Args:
            persona: Persona name.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM contexts WHERE persona = ?", (persona.lower(),))
            count = self.cursor.fetchone()[0]
            if count > self.max_contexts:
                self.cursor.execute(
                    "SELECT context_value FROM contexts WHERE persona = ? ORDER BY timestamp",
                    (persona.lower(),)
                )
                contexts = [json.loads(row[0]) for row in self.cursor.fetchall()]
                context_text = "\n".join(str(c) for c in contexts)
                summary = self.summarizer.execute(context_text, {"length": "short"})
                self.cursor.execute("DELETE FROM contexts WHERE persona = ?", (persona.lower(),))
                self.store_context(persona, {
                    "context_key": "summary",
                    "summary": summary,
                    "timestamp": time.time()
                })
                self.conn.commit()
        except (sqlite3.Error, Exception) as e:
            print(f"Error summarizing context: {str(e)}")

    def __del__(self):
        """Close database connection."""
        try:
            self.conn.close()
        except sqlite3.Error:
            pass


if __name__ == "__main__":
    memory = Memory()
    memory.store_context("generalist", {"input": "Test input", "timestamp": time.time()})
    print(memory.retrieve_context("generalist"))
