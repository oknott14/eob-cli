from dataclasses import dataclass, field
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableSequence

from src.extraction.llm.gemini_flash import GoogleGeminiFlash
from src.extraction.prompt.extract_data_prompt_template import ExtractDataPromptTemplate
from src.extraction.structured_output.extraction_structured_output import (
    ExtractionOutput,
)


@dataclass
class EobExtractorOptions:
    model_kwargs: Dict[str, Any] = field(default_factory=dict)


class EobExtractor(RunnableSequence[List[Document], List[ExtractionOutput]]):
    """
    Runnable class that extracts structured data from a single EOB document.

    Attributes:
    model_kwargs: The configuration parameters passed to the LLM Model
    """

    def __init__(self, **options: EobExtractorOptions):
        extractor_options = EobExtractorOptions(options)
        super().__init__(
            lambda doc_list: {"documents": doc_list},
            ExtractDataPromptTemplate(),
            GoogleGeminiFlash(**extractor_options.model_kwargs).with_structured_output(
                ExtractionOutput, method="json_mode"
            ),
        )
