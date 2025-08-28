import typer

from src import cli
from src.config import config

if __name__ == "__main__":
    config()
    typer.run(cli.process_eob)
