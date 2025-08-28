from pathlib import Path
from typing import Any, List, Optional, Union

from langchain_core.documents import Document
from langchain_core.runnables import Runnable

from src.ingestion.file_ingester import FileIngester, FileIngesterOptions
from src.ingestion.file_path_validator.validators.file_exists_validator import (
    FileExistsValidator,
)
from src.ingestion.file_path_validator.validators.file_type_validator import (
    FileTypeValidator,
)


class EobIngester(FileIngester):
    """
    Reads one or many EOB files from the file system and converts them to Langchain Documents. Runs a chain to process the Documents using batching for multiple documents.
    """

    def __init__(
        self,
        next: Optional[Runnable[List[Document], Any]] = None,
        zipFileDestination: Optional[Union[str, Path]] = None,
    ):
        super().__init__(
            FileIngesterOptions(
                file_path_validators=[
                    FileExistsValidator(),
                    FileTypeValidator({".pdf", ".zip"}),
                ],
                extract_to=zipFileDestination,
                next=next,
            )
        )
