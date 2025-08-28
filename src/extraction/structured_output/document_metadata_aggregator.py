from typing import Any, Callable, Dict, Iterable, List

from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig


class DocumentMetadataAggregator(Runnable[List[Document], Dict[str, Any]]):
    def __init__(
        self,
        fields: Iterable[str],
        document_selector: Callable[[List[Document]], Document] = lambda x: x[0],
        aliases: Dict[str, str] = dict(),
    ):
        self.metadata_fields = set(fields)
        self.document_selector = document_selector
        self.aliases = aliases

    def invoke(
        self, input: List[Document], config: RunnableConfig | None = None, **kwargs: Any
    ) -> Dict[str, Any]:
        if len(input) == 0:
            return {}

        metadata_document = self.document_selector(input)

        metadata = dict()

        for key in self.metadata_fields:
            if key in metadata_document.metadata:
                metadata[self.aliases[key] if key in self.aliases else key] = (
                    metadata_document.metadata[key]
                )

        return metadata
