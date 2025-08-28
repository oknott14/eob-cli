from dataclasses import dataclass, field
from typing import Any, Dict, List

from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel, RunnableSequence

from src.extraction.llm.gemini_flash import GoogleGeminiFlash
from src.extraction.prompt.extract_data_prompt_template import ExtractDataPromptTemplate
from src.extraction.structured_output.document_metadata_aggregator import (
    DocumentMetadataAggregator,
)
from src.extraction.structured_output.extraction_structured_output import (
    ExtractionOutput,
)
from src.extraction.structured_output.output_merger import OutputMerger


@dataclass
class EobExtractorOptions:
    model_kwargs: Dict[str, Any] = field(
        default_factory=lambda: {
            "temperature": 0.5,
        }
    )


class EobExtractor(RunnableSequence[List[Document], ExtractionOutput]):
    """
    Runnable class that extracts structured data from a single EOB document.

    Attributes:
    model_kwargs: The configuration parameters passed to the LLM Model
    """

    def __init__(self, options: EobExtractorOptions = EobExtractorOptions()):
        super().__init__(
            RunnableParallel(
                {
                    "get_data": EobDataExtractor(options),
                    "get_document_metadata": DocumentMetadataAggregator(
                        {"source"}, aliases={"source": "source_file_path"}
                    ),
                }
            ),
            OutputMerger("get_data", "get_document_metadata"),
        )


class EobDataExtractor(RunnableSequence[List[Document], ExtractionOutput]):
    """
    Runnable class that extracts structured data from a single EOB document.

    Attributes:
    model_kwargs: The configuration parameters passed to the LLM Model
    """

    def __init__(self, options: EobExtractorOptions = EobExtractorOptions()):
        super().__init__(
            lambda doc_list: {"documents": doc_list},
            ExtractDataPromptTemplate(),
            GoogleGeminiFlash(**options.model_kwargs).with_structured_output(
                ExtractionOutput, method="json_mode"
            ),
        )
