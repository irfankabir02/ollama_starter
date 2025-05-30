# main/tools/search.py
"""
Search tool for finding notes and tasks by keywords or tags.
"""
import json
from typing import Dict, Optional
from .base import Tool


class Search(Tool):
    """Tool for searching stored notes and tasks."""

    name = "search"

    def execute(self, query: str, params: Dict[str, str] = None) -> str:
        """
        Search notes and tasks by query or tags.

        Args:
            query: Search query string.
            params: Optional parameters (e.g., {'tag': 'work'}).

        Returns:
            Formatted search results or error message.
        """
        params = params or {}
        tag_filter = params.get('tag', '').lower()
        results = []

        # Search notes
        try:
            with open('notes.json', 'r') as f:
                for line in f:
                    note = json.loads(line.strip())
                    if (query.lower() in note['content'].lower() or
                            (tag_filter and tag_filter in [t.lower() for t in note.get('tags', [])])):
                        results.append(f"Note: {note['content']} (Priority: {note.get('priority', 'medium')}, Tags: {note.get('tags', [])})")
        except FileNotFoundError:
            pass

        # Search tasks
        try:
            with open('tasks.json', 'r') as f:
                for line in f:
                    task = json.loads(line.strip())
                    if query.lower() in task['description'].lower():
                        results.append(f"Task: {task['description']} (Priority: {task.get('priority', 'medium')})")
        except FileNotFoundError:
            pass

        if results:
            return "\n".join(f"{i+1}. {result}" for i, result in enumerate(results))
        return f"No results found for query '{query}'" + (f" with tag '{tag_filter}'" if tag_filter else "")


if __name__ == "__main__":
    search = Search()
    print(search.execute("meeting", {"tag": "work"}))
