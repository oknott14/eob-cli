from langchain_core.documents import Document

from src.extraction.prompt.extract_data_prompt_template import ExtractDataPromptTemplate
from src.extraction.prompt.prompts import (
    document_format_prompt,
    extraction_system_message,
)


def test_template_formats_single_doc():
    documents = [
        Document(
            page_content=f"Test Page Content For Document {i}",
            metadata={"page": i, "total_pages": 5},
        )
        for i in range(5)
    ]

    template = ExtractDataPromptTemplate()
    content = template.format(documents=documents)

    assert str(extraction_system_message.format().content) in content
    for test_document in documents:
        assert (
            str(document_format_prompt.format(documents=[test_document]).content)
            in content
        )
