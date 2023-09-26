"""Entry point for hotel_chatbot."""

from cli import run_typer_chatbot  # pragma: no cover
from web import run_gradio_chatbot  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    # TODO add args to select web ui and cli ui
    # run_gradio_chatbot()
    run_typer_chatbot()
