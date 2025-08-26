from pathlib import Path
from typing import Any, List, Type

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.pdf import BasePDFLoader
from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig


class PdfFileReader(Runnable[List[Path], List[List[Document]]]):
    def __init__(self, loader: Type[BasePDFLoader] = PyPDFLoader):
        self.loader = loader

    def invoke(
        self, input: List[Path], config: RunnableConfig | None = None, **kwargs: Any
    ) -> List[List[Document]]:
        return [self.loader(path).load() for path in input]
