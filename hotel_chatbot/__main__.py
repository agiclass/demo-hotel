"""Entry point for hotel_chatbot."""

import typer

from hotel_chatbot.cli import run_typer_chatbot  # pragma: no cover
from hotel_chatbot.web import run_gradio_chatbot  # pragma: no cover

app = typer.Typer()


@app.command()
def web():
    run_gradio_chatbot()


@app.command()
def cli():
    run_typer_chatbot()


if __name__ == "__main__":  # pragma: no cover
    app()
