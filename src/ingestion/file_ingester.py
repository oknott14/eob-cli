from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableSequence

from src.ingestion.file_path_validator.file_path_validator import FilePathValidator
from src.ingestion.file_path_validator.validators.file_exists_validator import (
    FileExistsValidator,
)
from src.ingestion.file_path_validator.validators.file_type_validator import (
    FileTypeValidator,
)


class FileIngester(RunnableSequence[str, List[Document]]):
    def __init__(self):
        super().__init__(
            FilePathValidator(
                [FileExistsValidator(), FileTypeValidator([".pdf", ".zip"])]
            ),
            
            name="FileIngester",
        )
