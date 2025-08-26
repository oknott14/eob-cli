import typer

from src import cli

if __name__ == "__main__":
    typer.run(cli.extract_eob)
