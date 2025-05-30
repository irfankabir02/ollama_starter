# Ollama Starter + MCP

A local, modular assistant framework with:

- Ollama-backed LLM calls  
- Personas & Model Context Protocol (MCP)  
- Terminal & Web UIs  
- Memory & Tools (summarize, search, notes)

## Structure

ollama_starter/
├── main/ # core logic: mcp, memory, personas, direct calls
├── scripts/ # terminal and web entry-points
├── tools/ # plug-in tools
├── web/ # Gradio UI
├── requirements.txt
└── README.md


## Quickstart

```bash
# 1. Install deps
pip install -r requirements.txt

# 2. Start Ollama
ollama serve

# 3. Pull models
ollama pull llama3.2
ollama pull tinyllama
ollama pull gemma3:1b-it-qat
ollama pull gemma3:4b-it-qat

# 4. Terminal chat
python scripts/stream_terminal_chat.py

# 5. Web chat
python scripts/launch_web_ui.py
