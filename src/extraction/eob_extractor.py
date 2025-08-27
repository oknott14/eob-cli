from dataclasses import dataclass, field
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableSequence

from src.extraction.llm.gemini_flash import GoogleGeminiFlash
from src.extraction.prompt.extract_data_prompt_template import ExtractDataPromptTemplate
from src.extraction.structured_output.extraction_structured_output import (
    VerboseExtractionOutput,
)


@dataclass
class EobExtractorOptions:
    model_kwargs: Dict[str, Any] = field(default_factory=dict)


class EobExtractor(RunnableSequence[List[Document], List[VerboseExtractionOutput]]):
    def __init__(self, **options: EobExtractorOptions):
        extractor_options = EobExtractorOptions(options)
        super().__init__(
            ExtractDataPromptTemplate(),
            GoogleGeminiFlash(**extractor_options.model_kwargs).with_structured_output(
                VerboseExtractionOutput
            ),
        )
