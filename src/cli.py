from pathlib import Path
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from src.exceptions.file_path import InvalidFilePathException
from src.extraction.eob_extractor import EobExtractor
from src.ingestion.eob_ingester import EobIngester
from src.output.console_output import ConsoleOutput
from src.output.file_output import FileOutput
from src.util import zip_directory

cli = typer.Typer()


@cli.command()
def extract_eob(
    file: Annotated[
        str,
        typer.Option(
            help="The absolute file path to either a single EOB pdf or a Zip file of many EOB pdfs.",
            dir_okay=False,
            file_okay=True,
        ),
    ],
    o: Annotated[
        Optional[str],
        typer.Option(
            help="Output directory for extracted json files",
            dir_okay=True,
            file_okay=False,
        ),
    ] = None,
):
    try:
        print(
            f"[green]Begining EOB File Extraction[/green]\n\t[yellow]File[/yellow]: {file}"
        )

        zip_file_destination = str(Path.cwd() / "temp" / "extracted_eobs")

        chain = EobIngester(
            EobExtractor().pipe(FileOutput(o) if o else ConsoleOutput()),
            zip_file_destination,
        )

        return chain.invoke(file)
    except InvalidFilePathException as e:
        raise e
    except Exception as e:
        raise Exception(f"Failed to Extract EOB - {e}")


@cli.command()
def zip(
    source: Annotated[str, typer.Argument(help="The directory to zip")],
    dest: Annotated[
        str, typer.Argument(help="The destination directory to place the zip file")
    ],
):
    source_path = Path(source)
    dest_path = Path(dest)
    zip_path = dest_path / f"{source_path.name}.zip"

    if zip_path.exists():
        response = (
            input("Zip File Already Exists. Do you want to replace if? [y/n]")
            .lower()
            .strip()
        )

        while response not in {"y", "n"}:
            response = (
                input("Zip File Already Exists. Do you want to replace if? [y/n]")
                .lower()
                .strip()
            )

        if response == "n":
            return True

    print(f"[green]Zipping Directory ({source})[/green]")
    zip_directory(source_path, zip_path)
    print("Done")
    return True
