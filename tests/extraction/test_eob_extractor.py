from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

from src.extraction.eob_extractor import EobExtractor
from src.extraction.llm.gemini_flash import GoogleGeminiFlash
from src.extraction.prompt.extract_data_prompt_template import ExtractDataPromptTemplate
from src.extraction.structured_output.extraction_structured_output import (
    ExtractionOutput,
)


def test_extractor_formats_prompts_to_single_string(mocker):
    return_value = ExtractionOutput(**{})
    mock_runnable = RunnableLambda(lambda _: return_value)
    llm_spy = mocker.spy(mock_runnable, "invoke")
    prompt_spy = mocker.spy(ExtractDataPromptTemplate, "invoke")
    mocker.patch(
        "src.extraction.llm.gemini_flash.GoogleGeminiFlash.with_structured_output",
        return_value=mock_runnable,
    )

    extractor = EobExtractor()

    documents = [
        Document(
            page_content=f"Test Page Content For Document {i}",
            metadata={"page": i, "total_pages": 5},
        )
        for i in range(5)
    ]

    extractor.invoke(documents)
    llm_spy.assert_called_once()
    prompt_spy.assert_called_once()


def test_uses_structured_output(mocker):
    output_spy = mocker.spy(GoogleGeminiFlash, "with_structured_output")
    EobExtractor()

    output_spy.assert_called_once()
