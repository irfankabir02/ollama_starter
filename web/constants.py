# web/constants.py
"""
Constants for UI and backend configuration.
"""
# Persona configurations
PERSONA_COLORS = {
    'generalist': '#28a745',
    'zen_monk': '#6f42c1',
    'shakespeare': '#dc3545',
    'quantum_mentor': '#007bff'
}

PERSONA_ICONS = {
    'generalist': '🤖',
    'zen_monk': '🧘',
    'shakespeare': '🎭',
    'quantum_mentor': '⚛️'
}

# UI configurations
DEFAULT_PERSONA = 'generalist'
CHATBOT_HEIGHT = 500
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 7860

# Tool command prefixes
TOOL_PREFIXES = {
    'note': '@note',
    'search': '@search',
    'summarize': '@summarize',
    'task': '@task'
}
