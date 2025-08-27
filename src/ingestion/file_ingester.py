from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional, Union

from langchain_core.documents import Document
from langchain_core.runnables import (
    Runnable,
    RunnableBranch,
    RunnableSequence,
)

from src.ingestion.file_path_validator.file_path_validator import FilePathValidator
from src.ingestion.file_path_validator.validators.base_validator import (
    BaseFilePathValidator,
)
from src.ingestion.file_reader.pdf_file_reader import PdfFileReader
from src.ingestion.runnables.zip_file_extractor import ZipFileExtractor


@dataclass
class FileIngesterOptions:
    file_path_validators: List[BaseFilePathValidator] = field(
        default_factory=list[BaseFilePathValidator]
    )

    next: Optional[Runnable[List[Document], Any]] = field(default=None)

    extract_to: Optional[Union[str, Path]] = field(
        default=Path.cwd() / "temp" / "extracted_eobs"
    )


class FileIngester(RunnableSequence[str, List[Any]]):
    def __init__(self, config: FileIngesterOptions = FileIngesterOptions()):
        if not config.extract_to:
            config.extract_to = Path.cwd() / "temp" / "extracted_eobs"

        next_chain = PdfFileReader()

        if config.next is not None:
            next_chain = next_chain.pipe(config.next)

        zip_chain = ZipFileExtractor(config.extract_to, {".pdf"}).pipe(next_chain.batch)
        single_file_chain = next_chain.pipe(lambda x: [x])

        super().__init__(
            FilePathValidator(config.file_path_validators),
            RunnableBranch[Path, List[Any]](
                (
                    FileIngester.is_zip,
                    zip_chain,
                ),  # Batch reading and the post chain if zip
                single_file_chain,  # Single run for non zip files
            ),
            name="FileIngester",
        )

    @classmethod
    def is_zip(cls, path: Path) -> bool:
        return  path.suffix.lower() == ".zip"
