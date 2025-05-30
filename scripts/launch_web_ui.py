# scripts/launch_web_ui.py
"""
Launches the Gradio UI for the AI assistant system with configurable options.
"""
import gradio as gr
import typer
from typing import Optional
from web.interface import create_interface


def launch_ui(
    host: str = "127.0.0.1",
    port: Optional[int] = 7860,
    debug: bool = False
):
    """
    Launch the Gradio interface for the AI assistant.

    Args:
        host: Host address for the server (default: 127.0.0.1).
        port: Port number (default: 7860).
        debug: Enable debug mode for detailed logs.
    """
    try:
        app = create_interface()
        app.launch(
            server_name=host,
            server_port=port,
            share=False,
            inbrowser=True,
            debug=debug,
            show_error=True,
            quiet=False
        )
    except Exception as e:
        typer.secho(f"Failed to launch UI: {str(e)}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(launch_ui)
