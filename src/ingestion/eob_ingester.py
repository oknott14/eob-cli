from typing import Any, List, Optional

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
    def __init__(
        self,
        next: Optional[Runnable[List[Document], Any]] = None,
        zipFileDestination: Optional[str] = None,
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
