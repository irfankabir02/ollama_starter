# 🌌 QuietEdge: Symbolic AI Assistant (Offline, Local-First)

**QuietEdge** is a modular, local-first AI assistant system powered by Ollama. It runs entirely offline with no cloud dependencies, offering symbolic, multi-persona interaction through a Gradio web UI and a streaming terminal interface.

- 🔒 **Privacy-first**: All interactions stay on your machine
- 🔧 **Modular tools**: Note-taking, summarization, search (extensible)
- 🧠 **Multiple personas**: Define styles, memory scope, tools per agent
- 🌀 **Symbolic protocol**: Context-aware routing through the MCP layer
- ✨ **Simple and elegant**: Quiet by design, with an intuitive interface

---

## 📁 Project Structure

```
ollama_starter/
├── main/
│   ├── mcp.py                  # Context coordination layer
│   ├── memory.py               # Long-term and persona memory
│   ├── ollama_assistant.py     # Ollama local model interface
│   ├── personas.py             # Define and switch AI personas
│   └── tools/                  # Modular symbolic tools
├── scripts/
│   ├── stream_terminal_chat.py # Terminal-based streaming chat
│   ├── launch_web_ui.py        # Gradio UI launcher
│   └── clean_structure.sh      # Project cleanup automation
├── web/
│   ├── interface.py            # Gradio logic
│   ├── ui.py                   # Stream handling and formatting
├── README.md
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies

```bash
# Create and activate your environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama if not installed
curl -fsSL https://ollama.com/install.sh | sh
```

---

### 2. Start Ollama (locally)

```bash
ollama serve
ollama run mistral  # Or your preferred model (e.g., llama3)
```

---

## 🚀 Usage

### 🌐 Launch Web UI (Gradio)

```bash
python scripts/launch_web_ui.py
```

Features:
- Persona switching
- Markdown + streaming output
- Interactive tools (note-taking, summarization, search)
- Tag-based prompt parsing (`@note`, `@summarize`, etc.)

---

### 💻 Stream Terminal Chat

```bash
python scripts/stream_terminal_chat.py
```

Use markdown, tags, or CLI-friendly prompts like:

```text
::note summarize today’s meeting
::search how to build local LLM assistant
```

---

## 🧩 Features

- ✅ Symbolic tool system with `@tags` and command triggers
- ✅ Multi-persona support (memory, tone, tool access)
- ✅ Streaming support (both UI and terminal)
- ✅ Modular MCP for intelligent input routing
- ✅ Extensible memory backend (JSON, SQLite optional)
- ✅ Minimal dependencies, low RAM usage

---

## 🤝 Contributing

Pull requests welcome!

```bash
# Fork and clone
git clone https://github.com/yourname/ollama_starter.git
cd ollama_starter

# Make your changes on a new branch
git checkout -b feature/my-improvement
```

To submit:
1. Follow clean Python structure
2. Keep symbolic clarity and naming consistency
3. Test `main/` logic before UI calls it

---

## 🔐 Philosophy

QuietEdge is designed for thinkers, artists, and builders who want powerful AI tools without noise, cloud, or distraction. Each persona reflects a facet of intelligence. The system respects autonomy, creativity, and clarity.

---

## 📜 License

MIT — free to use, remix, build.

---

Made with 🛠️ in a quiet room, far from the cloud.
