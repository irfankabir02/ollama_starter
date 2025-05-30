# main/personas.py
"""
Define available personas and helper to retrieve them.
"""

from collections import namedtuple

Persona = namedtuple('Persona', ['name','model','system_prompt'])

PERSONA_MAP = {
    'generalist': Persona('generalist', 'llama3.2', "You are a helpful assistant; answer clearly."),
    'zen_monk':   Persona('zen_monk',   'tinyllama', "You are a quiet Zen monk speaking in metaphors."),
    'shakespeare':Persona('shakespeare','gemma3:1b-it-qat',"You speak like Shakespeare: poetic, archaic."),
    'quantum_mentor':Persona('quantum_mentor','gemma3:4b-it-qat',
                             "You are a quantum physicist explaining science simply."),
}

def get_persona(name: str) -> Persona:
    return PERSONA_MAP.get(name, PERSONA_MAP['generalist'])

