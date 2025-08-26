from pathlib import Path
from typing import Iterable, List, Union

from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableSequence

from src.ingestion.file_reader.pdf_file_reader import PdfFileReader
from src.ingestion.zip_file_extractor import ZipFileExtractor


class ZipFileReader(RunnableSequence[List[Path], List[List[Document]]]):
    def __init__(
        self,
        extract_to: Union[str, Path] = Path.cwd() / "extracted_eobs",
        file_reader: Runnable[List[Path], List[List[Document]]] = PdfFileReader(),
        file_types: Iterable[str] = [],
    ):
        super().__init__(
            ZipFileExtractor(extract_to, file_types), file_reader, name="ZipFileReader"
        )
