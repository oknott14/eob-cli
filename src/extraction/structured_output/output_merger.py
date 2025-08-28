from typing import Any, Dict, Union

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig

from src.extraction.structured_output.extraction_structured_output import (
    ExtractionOutput,
)


class OutputMerger(
    Runnable[Dict[str, Union[ExtractionOutput, Dict[str, Any]]], ExtractionOutput]
):
    def __init__(self, structured_output_key: str, merge_key: str):
        self.structured_output_key = structured_output_key
        self.merge_key = merge_key

    def invoke(
        self,
        input: Dict[str, ExtractionOutput | Dict[str, Any]],
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> ExtractionOutput:
        self.validate_input(input)
        structured_output: ExtractionOutput = input[self.structured_output_key]
        merge_dict: Dict[str, Any] = input[self.merge_key]
        return structured_output.model_copy(update=merge_dict)

    def validate_input(
        self,
        input: Dict[str, ExtractionOutput | Dict[str, Any]],
    ):
        for key in [self.structured_output_key, self.merge_key]:
            if key not in input:
                raise KeyError(f"{key} was not found in OutputMerger input")
