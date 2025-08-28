from pathlib import Path
from typing import Optional

import typer
from rich import print
from typing_extensions import Annotated

from src.exceptions.file_path import InvalidFilePathException
from src.extraction.eob_extractor import EobExtractor, EobExtractorOptions
from src.ingestion.eob_ingester import EobIngester
from src.output.console_output import ConsoleOutput
from src.output.file_output import FileOutput
from src.util import zip_directory

cli = typer.Typer()


@cli.command(help="A command for extracting locally stored EOB PDF document(s)")
def process_eob(
    file: Annotated[
        str,
        typer.Option(
            "--file",
            "-f",
            help="The absolute file path to either a single EOB pdf or a Zip file containing many EOB pdfs.",
            dir_okay=False,
            file_okay=True,
        ),
    ],
    output_dir: Annotated[
        Optional[str],
        typer.Option(
            "--output",
            "-o",
            help="Output directory for extracted json files",
            dir_okay=True,
            file_okay=False,
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            "-ov",
            help="When `-o` or `--output` is specified: Whether output files can be overwritten.",
        ),
    ] = False,
    temperature: Annotated[
        float,
        typer.Option(
            "--temperature",
            "-t",
            help="The temperature to use for the LLM.",
        ),
    ] = 0.4,
    unzipTo: Annotated[
        Optional[str],
        typer.Option(
            "--unzipTo",
            "-z",
            help="The directory to unzip the contents of a passed zip file to.",
            file_okay=False,
            dir_okay=True,
        ),
    ] = None,
):
    try:
        print(
            f"[green]Begining EOB File Processing[/green]\t([yellow]File[/yellow]: {file})"
        )

        # Runnable for formatting and presenting output
        output_runnable = (
            FileOutput(
                output_dir, file_name_key="source_file_path", overwrite=overwrite
            )
            if output_dir
            else ConsoleOutput()
        )

        # Chain for formatting documents into a prompt, calling the LLM and collecting output.
        extraction_chain = EobExtractor(
            EobExtractorOptions(model_kwargs={"temperature": temperature})
        ).pipe(output_runnable)

        # Unzip Location
        if not unzipTo:
            unzipTo = "./temp/extracted_eobs"
        # EOB Processing Chain
        chain = EobIngester(  # EobIngester validates the file path and reads / parses the file(s)
            extraction_chain,
            Path(unzipTo).absolute(),
        )

        results = chain.invoke(file)  # Call chain on file path
        print(f"[green]EOB Processing Complete[/green]: {len(results)} files processed")
        return

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
