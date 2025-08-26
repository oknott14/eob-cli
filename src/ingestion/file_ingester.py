from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_core.runnables.base import RunnableLike

from src.ingestion.file_path_validator.file_path_validator import FilePathValidator
from src.ingestion.file_path_validator.validators.base_validator import (
    BaseFilePathValidator,
)
from src.ingestion.file_type_branch import FileTypeBranch
from src.ingestion.pdf_file_reader import PdfFileReader


@dataclass
class FileIngesterOptions:
    default_file_type_branch: RunnableLike[Path, List[List[Document]]] = field(
        default_factory=lambda: RunnableLambda(lambda x: [x]).pipe(PdfFileReader())
    )
    file_path_validators: List[BaseFilePathValidator] = field(
        default_factory=list[BaseFilePathValidator]
    )
    file_type_branches: Dict[str, RunnableLike[Path, List[List[Document]]]] = field(
        default_factory=dict
    )


class FileIngester(RunnableSequence[str, List[List[Document]]]):
    def __init__(self, config: FileIngesterOptions = FileIngesterOptions()):
        super().__init__(
            FilePathValidator(config.file_path_validators),
            FileTypeBranch[List[List[Document]]](
                config.file_type_branches, config.default_file_type_branch
            ),
            name="FileIngester",
        )
