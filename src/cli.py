import typer
from typing_extensions import Annotated

from src.ingestion.file_ingester import FileIngester


def extract_eob(
    file: Annotated[
        str,
        typer.Argument(
            help="The absolute file path to either a single EOB pdf or a Zip file of many EOB pdfs."
        ),
    ],
):
    return FileIngester().invoke(file)
