from pathlib import Path

from langchain_core.documents import Document

from src.ingestion.eob_ingester import EobIngester
from src.ingestion.file_ingester import FileIngester
from src.ingestion.file_reader.pdf_file_reader import PdfFileReader


def test_file_ingester_accepts_zip_and_pdf(mocker):
    mocker.patch(
        "langchain_community.document_loaders.PyPDFLoader.load",
        return_value=[
            Document(page_content="", metadata={"page": 0, "total_pages": 1})
        ],
    )

    ingester = FileIngester()

    temp_path = Path.cwd() / "temp"
    temp_path.mkdir(parents=True, exist_ok=True)
    pdf_path = temp_path / "test_file_path.pdf"
    mocker.patch(
        "src.ingestion.runnables.zip_file_extractor.ZipFileExtractor.invoke",
        return_value=[pdf_path],
    )
    pdf_path.touch(exist_ok=True)
    zip_path = temp_path / "test_file.zip"
    zip_path.touch(exist_ok=True)
    assert ingester.invoke(str(pdf_path.absolute()))
    assert ingester.invoke(str(zip_path.absolute()))


def test_batches_zip(mocker):
    mocker.patch(
        "langchain_community.document_loaders.PyPDFLoader.load",
        return_value=[
            Document(page_content="", metadata={"page": 0, "total_pages": 1})
        ],
    )

    reader_spy = mocker.spy(PdfFileReader, "batch")
    ingester = FileIngester()

    temp_path = Path.cwd() / "temp"
    temp_path.mkdir(parents=True, exist_ok=True)
    pdf_path = temp_path / "test_file_path.pdf"
    mocker.patch(
        "src.ingestion.runnables.zip_file_extractor.ZipFileExtractor.invoke",
        return_value=[pdf_path],
    )

    pdf_path.touch(exist_ok=True)
    zip_path = temp_path / "test_file.zip"
    zip_path.touch(exist_ok=True)

    ingester.invoke(str(zip_path.absolute()))
    reader_spy.assert_called_once()


def test_returns_a_list_of_documents(mocker):
    return_document = Document(page_content="", metadata={"page": 0, "total_pages": 1})
    mocker.patch(
        "langchain_community.document_loaders.PyPDFLoader.load",
        return_value=[return_document],
    )

    temp_path = Path.cwd() / "temp"
    temp_path.mkdir(parents=True, exist_ok=True)
    pdf_path = temp_path / "test_file_path.pdf"
    mocker.patch(
        "src.ingestion.runnables.zip_file_extractor.ZipFileExtractor.invoke",
        return_value=[pdf_path],
    )
    pdf_path.touch(exist_ok=True)
    zip_path = temp_path / "test_file.zip"
    zip_path.touch(exist_ok=True)

    ingester = EobIngester()

    for path in [pdf_path, zip_path]:
        str_path = str(path.absolute())
        results = ingester.invoke(str_path)
        
        for docs in results:
            assert len(docs)

            for doc in docs:
                assert doc == return_document
