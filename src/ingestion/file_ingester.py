from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableSequence
from langchain_core.runnables.base import RunnableLike

from src.ingestion.file_path_validator.file_path_validator import FilePathValidator
from src.ingestion.file_path_validator.validators.base_validator import (
    BaseFilePathValidator,
)
from src.ingestion.file_type_branch import FileTypeBranch


@dataclass
class FileIngesterOptions:
    file_path_validators: List[BaseFilePathValidator] = []
    file_type_branches: Dict[str, RunnableLike[Path, List[Path]]] = {}


class FileIngester(RunnableSequence[str, List[Document]]):
    def __init__(self, config: FileIngesterOptions = FileIngesterOptions()):
        super().__init__(
            FilePathValidator(config.file_path_validators),
            FileTypeBranch(config.file_type_branches),
            name="FileIngester",
        )
