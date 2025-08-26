from pathlib import Path
from typing import Any, List, Union

from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableSequence
from langchain_core.runnables.base import RunnableLike

type BaseFileReader = Union[FileReader, FileReaderSequence]


class FileReader(Runnable[List[Path], List[List[Document]]]):
    name = "FileReader"


class FileReaderSequence(RunnableSequence[List[Path], List[List[Document]]]):
    name = "FileReaderSequence"

    def __init__(
        self,
        *steps: RunnableLike[Any, Any],
        name: str | None = None,
    ) -> None:
        super().__init__(*steps, name=name)
