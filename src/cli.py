from pathlib import Path

import typer
from typing_extensions import Annotated

from src.ingestion.file_ingester import FileIngester, FileIngesterOptions
from src.ingestion.file_path_validator.validators.file_exists_validator import (
    FileExistsValidator,
)
from src.ingestion.file_path_validator.validators.file_type_validator import (
    FileTypeValidator,
)
from src.ingestion.zip_file_extractor import ZipFileExtractor


def extract_eob(
    file: Annotated[
        str,
        typer.Argument(
            help="The absolute file path to either a single EOB pdf or a Zip file of many EOB pdfs."
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
    return FileIngester(
        FileIngesterOptions(
            file_path_validators=[
                FileExistsValidator(),
                FileTypeValidator({".pdf", ".zip"}),
            ],
            file_type_branches={
                ".pdf": lambda x: [x],
                ".zip": ZipFileExtractor(zipFileDestination, {".pdf"}),
            },
        )
    ).invoke(file)
