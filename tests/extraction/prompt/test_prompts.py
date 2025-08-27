from langchain_core.documents import Document

from src.extraction.prompt.prompts import (
    document_format_prompt,
    extraction_system_message,
)


def test_document_formatting_prompt_formats_list_of_one_documents():
    test_document = Document(
        page_content="Test Document Page Content",
        metadata={"page": 0, "total_pages": 1},
    )

    formatted = document_format_prompt.format(documents=[test_document])
    content = str(formatted.content)
    assert test_document.page_content in content
    assert "0" in content
    assert "1" in content


def test_document_formatting_prompt_formats_list_of_documents():
    documents = [
        Document(
            page_content=f"Test Page Content For Document {i}",
            metadata={"page": i, "total_pages": 5},
        )
        for i in range(5)
    ]

    formatted = document_format_prompt.format(documents=documents)
    content = str(formatted.content)
    assert "5" in content
    for idx, test_document in enumerate(documents):
        assert test_document.page_content in content
        assert str(idx) in content


def test_system_prompt_formats():
    formatted = extraction_system_message.format()
    assert formatted
    assert formatted.content
