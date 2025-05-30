# main/ollama_assistant.py
"""
Legacy: direct Ollama calls for sync/stream/generate/embed.
(Still available for quick demos.)
"""

import asyncio
import numpy as np
import faiss
from ollama import chat, generate, embed, create, pull, ResponseError

def sync_chat(prompt: str, model: str = 'llama3.2') -> str:
    return chat(model=model, messages=[{'role':'user','content':prompt}]).message.content

def stream_chat_generator(prompt: str, model: str = 'llama3.2'):
    for chunk in chat(model=model, messages=[{'role':'user','content':prompt}], stream=True):
        yield chunk['message']['content']

def generate_text(prompt: str, model: str = 'llama3.2') -> str:
    return generate(model=model, prompt=prompt)['response']

def embed_search(docs: list[str], query: str, top_k: int = 1, model: str = 'llama3.2'):
    vecs = np.array(embed(model=model, input=docs)['embedding'], dtype='float32')
    idx = faiss.IndexFlatL2(vecs.shape[1]); idx.add(vecs)
    qv = np.array(embed(model=model, input=query)['embedding'], dtype='float32')
    dists, idxs = idx.search(qv, k=top_k)
    return [(docs[i], float(dists[0][j])) for j,i in enumerate(idxs[0])]

def setup_persona(name: str, base: str, prompt: str) -> str:
    try:
        create(model=name, from_=base, system=prompt)
        return f"Created persona {name}"
    except ResponseError as e:
        return f"Error: {e.error}"

def pull_model(name: str='llama3.2')->str:
    try:
        pull(name); return f"Pulled {name}"
    except ResponseError as e:
        return f"Pull error: {e.error}"

