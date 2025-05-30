# web/interface.py
"""
Enhanced Gradio UI for Multi-Persona AI Assistant
Provides streaming responses, voice I/O, markdown rendering, and persona switching
"""
import gradio as gr
from typing import Generator, List, Tuple, Optional
from main.mcp import MCP
from main.personas import Persona
from main.tools import NoteTaker, Search, Summarizer, TaskManager
from web.ui import UIHelper

# Custom CSS (unchanged from Claude’s version)
CUSTOM_CSS = """
/* Main app styling */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    padding: 0;
}
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
}
/* Header styling */
.header-title {
    background: linear-gradient(90deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 2.5em;
    font-weight: bold;
    margin: 20px 0;
}
/* Chat container */
#chatbot {
    height: 500px !important;
    border: none !important;
    border-radius: 15px !important;
    background: #f8f9fa !important;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.1) !important;
}
/* Message styling */
.message {
    margin: 10px 0;
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 75%;
    word-wrap: break-word;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.message.user {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin-left: auto;
    text-align: right;
    border-bottom-right-radius: 5px;
}
.message.assistant {
    background: #ffffff;
    color: #333;
    margin-right: auto;
    border: 1px solid #e1e5e9;
    border-bottom-left-radius: 5px;
    position: relative;
}
/* Persona-specific colors */
.persona-generalist { border-left: 4px solid #28a745; }
.persona-zen_monk { border-left: 4px solid #6f42c1; }
.persona-shakespeare { border-left: 4px solid #dc3545; }
.persona-quantum_mentor { border-left: 4px solid #007bff; }
/* Voice button styling */
.voice-btn {
    background: none !important;
    border: none !important;
    font-size: 1.2em;
    cursor: pointer;
    padding: 5px 10px;
    border-radius: 50%;
    transition: all 0.3s ease;
    position: absolute;
    top: 10px;
    right: 10px;
}
.voice-btn:hover {
    background: rgba(0,0,0,0.1) !important;
    transform: scale(1.1);
}
/* Input controls */
.input-row {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
/* Button styling */
.gr-button {
    border-radius: 25px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    border: none !important;
}
.gr-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
}
.send-btn {
    background: linear-gradient(135deg, #28a745, #20c997) !important;
    color: white !important;
}
.voice-input-btn {
    background: linear-gradient(135deg, #17a2b8, #138496) !important;
    color: white !important;
}
.clear-btn {
    background: linear-gradient(135deg, #6c757d, #5a6268) !important;
    color: white !important;
}
/* Dropdown styling */
.gr-dropdown {
    border-radius: 10px !important;
    border: 2px solid #e1e5e9 !important;
}
/* Textbox styling */
.gr-textbox {
    border-radius: 10px !important;
    border: 2px solid #e1e5e9 !important;
}
/* Thinking indicator */
.thinking {
    opacity: 0.7;
    font-style: italic;
    color: #6c757d;
}
/* Responsive design */
@media (max-width: 768px) {
    .message {
        max-width: 90%;
    }
    .header-title {
        font-size: 2em;
    }
    #chatbot {
        height: 400px !important;
    }
}
/* Accessibility improvements */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
"""

# JavaScript (unchanged from Claude’s version)
VOICE_JS = """
<script>
let recognition = null;
let synthesis = window.speechSynthesis;

function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            console.log('Voice recognition started');
            const voiceBtn = document.querySelector('.voice-input-btn');
            if (voiceBtn) {
                voiceBtn.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
                voiceBtn.innerHTML = '🔴 Listening...';
            }
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const messageInput = document.querySelector('#message-input textarea');
            if (messageInput) {
                messageInput.value = transcript;
                messageInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        
        recognition.onend = function() {
            const voiceBtn = document.querySelector('.voice-input-btn');
            if (voiceBtn) {
                voiceBtn.style.background = 'linear-gradient(135deg, #17a2b8, #138496)';
                voiceBtn.innerHTML = '🎤 Voice';
            }
        };
        
        recognition.onerror = function(event) {
            console.error('Voice recognition error:', event.error);
            const voiceBtn = document.querySelector('.voice-input-btn');
            if (voiceBtn) {
                voiceBtn.style.background = 'linear-gradient(135deg, #17a2b8, #138496)';
                voiceBtn.innerHTML = '🎤 Voice';
            }
        };
    }
}

function startVoiceInput() {
    if (recognition) {
        recognition.start();
    } else {
        alert('Voice recognition not supported in this browser');
    }
}

function speakText(text) {
    if (synthesis) {
        synthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        synthesis.speak(utterance);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initVoiceRecognition();
});

setInterval(function() {
    if (!recognition) {
        initVoiceRecognition();
    }
}, 1000);
</script>
"""

def create_interface():
    """Create the Gradio interface for the AI assistant."""
    # Initialize MCP and UI helper
    tools = [NoteTaker(), Search(), Summarizer(), TaskManager()]
    personas = [
        Persona(name="generalist", color="#28a745", tone="neutral", tools=tools, memory=None),
        Persona(name="zen_monk", color="#6f42c1", tone="calm", tools=tools, memory=None),
        Persona(name="shakespeare", color="#dc3545", tone="poetic", tools=tools, memory=None),
        Persona(name="quantum_mentor", color="#007bff", tone="technical", tools=tools, memory=None)
    ]
    mcp = MCP(personas=personas, tools=tools, memory=None)
    ui_helper = UIHelper(personas, mcp)

    # Custom theme
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="slate",
        font=("Segoe UI", "system-ui", "sans-serif")
    )

    with gr.Blocks(css=CUSTOM_CSS, theme=theme, title="Multi-Persona AI Assistant", head=VOICE_JS) as app:
        gr.HTML('<div class="header-title">🧠 Multi-Persona AI Assistant</div>')
        gr.Markdown("""
        Welcome to your intelligent assistant! Choose a persona, type your message, or use voice input.
        Use commands like `@note priority=high`, `@search query`, `@summarize text`, or `@task description`.
        """)

        # State management
        current_persona = gr.State("generalist")

        # Main interface
        with gr.Row():
            with gr.Column(scale=1, min_width=200):
                persona_selector = gr.Dropdown(
                    choices=ui_helper.get_persona_choices(),
                    value="🤖 Generalist",
                    label="🎭 Choose Persona",
                    elem_id="persona-selector"
                )
                persona_info = gr.Markdown(
                    "**Generalist**: A versatile assistant for all tasks.",
                    elem_id="persona-info"
                )

            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    value=ui_helper.get_welcome_message("generalist"),
                    elem_id="chatbot",
                    height=500,
                    show_label=False,
                    container=True,
                    render_markdown=False
                )

        # Input controls
        with gr.Row(elem_classes=["input-row"]):
            with gr.Column(scale=4):
                message_input = gr.Textbox(
                    placeholder="Type your message or use @note, @task, @search, @summarize...",
                    show_label=False,
                    elem_id="message-input",
                    container=False
                )
            with gr.Column(scale=1, min_width=100):
                with gr.Row():
                    voice_btn = gr.Button("🎤 Voice", elem_classes=["voice-input-btn"], size="sm")
                    send_btn = gr.Button("Send", variant="primary", elem_classes=["send-btn"], size="sm")

        with gr.Row():
            clear_btn = gr.Button("🗑️ Clear Chat", elem_classes=["clear-btn"], size="sm")
            gr.Markdown("**Tips**: Use Enter to send • Click 🔊 to hear responses • Try voice input with 🎤")

        # Event handlers
        def send_message_wrapper(message: str, history: List[Tuple[str, str]], persona_display: str):
            if not message.strip():
                yield history, ""
                return

            # Get persona key
            persona_key = "generalist"
            for display, key in ui_helper.get_persona_choices():
                if display == persona_display:
                    persona_key = key
                    break

            # Add user message
            user_msg = ui_helper.format_message(message, is_user=True)
            history.append((user_msg, None))
            yield history, ""

            # Show thinking indicator
            thinking_msg = ui_helper.format_message("🤔 Assistant is thinking...", is_user=False, persona_name=persona_key)
            history[-1] = (history[-1][0], thinking_msg)
            yield history, ""

            try:
                # Stream response
                full_response = ""
                for chunk in mcp.process_input(message, {"current_persona": persona_key}):
                    full_response += chunk
                    history[-1] = (history[-1][0], ui_helper.format_message(full_response, is_user=False, persona_name=persona_key))
                    yield history, ""
            except Exception as e:
                error_msg = ui_helper.format_message(f"❌ Error: {str(e)}", is_user=False, persona_name=persona_key)
                history[-1] = (history[-1][0], error_msg)
                yield history, ""

        persona_selector.change(
            fn=ui_helper.update_persona_info,
            inputs=persona_selector,
            outputs=[persona_info, current_persona]
        ).then(
            fn=ui_helper.get_welcome_message,
            inputs=current_persona,
            outputs=chatbot
        )

        send_btn.click(
            fn=send_message_wrapper,
            inputs=[message_input, chatbot, persona_selector],
            outputs=[chatbot, message_input]
        )

        message_input.submit(
            fn=send_message_wrapper,
            inputs=[message_input, chatbot, persona_selector],
            outputs=[chatbot, message_input]
        )

        clear_btn.click(
            fn=ui_helper.clear_chat,
            outputs=[chatbot, message_input]
        ).then(
            fn=ui_helper.get_welcome_message,
            inputs=current_persona,
            outputs=chatbot
        )

        voice_btn.click(fn=None, js="startVoiceInput")

    return app


if __name__ == "__main__":
    create_interface().launch()
