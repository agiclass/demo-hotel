"""CLI interface for hotel_chatbot project.
"""
import json

import typer
import wcwidth
from db import HotelDB
from dm import DialogManager
from nlu import nlu
from tabulate import tabulate


def run_typer_chatbot():  # pragma: no cover
    help = """
    ====== hotel chatbot =====
    - input "exit" to exit chat
    - input "create" to create db table schema
    - input "insert" to insert data into db
    - input "delete" to delete db table
    ==========================
    """
    typer.secho(help, fg=typer.colors.GREEN)
    db = HotelDB()
    dm = DialogManager()
    while True:
        user_input = typer.prompt("User: ", prompt_suffix="")
        if user_input.lower() == "exit":
            typer.echo("Chatbot: Goodbye!")
            break
        elif user_input.lower() == "create":
            db.create(name="Hotel")
            typer.secho("created table", fg=typer.colors.RED)
        elif user_input.lower() == "insert":
            with open("../data/hotel.json", "r") as f:
                hotels = json.load(f)
            db.insert(hotels[:200])
            typer.secho("insert table", fg=typer.colors.RED)
        elif user_input.lower() == "delete":
            db.delete(name="Hotel")
            typer.secho("delete table", fg=typer.colors.RED)
        else:
            state = nlu(user_input)
            dm.update_state(state)
            candidates = db.search(
                dm.get_state(), output_fields=["name", "rating", "price"]
            )
            keys = list(candidates[0].keys())
            keys.remove("hotel_id")
            table = [[candidate[k] for k in keys] for candidate in candidates]
            table = [keys] + table
            table = tabulate(table, headers="firstrow", tablefmt="fancy_grid")
            typer.secho(table, fg=typer.colors.BRIGHT_BLUE)


if __name__ == "__main__":  # pragma: no cover
    run_typer_chatbot()
