import gradio as gr
from web.constants import PERSONAS, DEFAULT_PERSONA
from web.interface import talk

def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# 🧠 Ollama Starter — Web Chat")
        with gr.Row():
            inp = gr.Textbox(label="Your message", placeholder="Type your message here...", lines=3)
            per = gr.Dropdown(choices=PERSONAS, value=DEFAULT_PERSONA, label="Persona")
        out = gr.Textbox(label="AI response", interactive=False, lines=10)
        btn = gr.Button("Send")
        error_message = gr.Textbox(label="Error", interactive=False, visible=False)

        def wrapped_talk(message, persona):
            try:
                response = talk(message, persona)
                error_message.visible = False
                return response, ""
            except Exception as e:
                error_message.visible = True
                return "", f"Error: {str(e)}"

        btn.click(fn=wrapped_talk, inputs=[inp, per], outputs=[out, error_message])

    demo.launch()

