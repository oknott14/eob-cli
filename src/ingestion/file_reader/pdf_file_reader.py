from pathlib import Path
from typing import Any, List, Type

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.pdf import BasePDFLoader
from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from rich import print


class PdfFileReader(Runnable[Path, List[Document]]):
    def __init__(self, loader: Type[BasePDFLoader] = PyPDFLoader):
        self.loader = loader

    def invoke(
        self, input: Path, config: RunnableConfig | None = None, **kwargs: Any
    ) -> List[Document]:
        print(f"Reading {input}")
        return self.loader(input).load()
