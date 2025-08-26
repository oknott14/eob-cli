from pathlib import Path

import typer
from langchain_core.runnables import RunnableLambda
from rich import print
from typing_extensions import Annotated

from src.exceptions.file_path import InvalidFilePathException
from src.ingestion.file_ingester import FileIngester, FileIngesterOptions
from src.ingestion.file_path_validator.validators.file_exists_validator import (
    FileExistsValidator,
)
from src.ingestion.file_path_validator.validators.file_type_validator import (
    FileTypeValidator,
)
from src.ingestion.pdf_file_reader import PdfFileReader
from src.ingestion.zip_file_extractor import ZipFileExtractor


def extract_eob(
    file: Annotated[
        str,
        typer.Option(
            help="The absolute file path to either a single EOB pdf or a Zip file of many EOB pdfs.",
            dir_okay=False,
        ),
    ],
    zipFileDestination: Annotated[
        str,
        typer.Option(
            default=str(Path.cwd() / "temp"),
            help="The directory to extract the zipped EOB PDFs to.",
        ),
    ] = str(Path.cwd() / "temp"),
):
    try:
        print(
            f"[green]Begining EOB File Extraction[/green]\n\t[yellow]File[/yellow]: {file}"
        )

        file_reader = PdfFileReader()

        return FileIngester(
            FileIngesterOptions(
                file_path_validators=[
                    FileExistsValidator(),
                    FileTypeValidator({".pdf", ".zip"}),
                ],
                file_type_branches={
                    ".pdf": RunnableLambda(lambda x: [x]).pipe(file_reader),
                    ".zip": ZipFileExtractor(zipFileDestination, {".pdf"}).pipe(
                        file_reader
                    ),
                },
            )
        ).invoke(file)
    except InvalidFilePathException as e:
        raise e
    except Exception as e:
        raise Exception(f"Failed to Extract EOB - {e}")
