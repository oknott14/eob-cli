from pathlib import Path

from src.ingestion.file_reader.pdf_file_reader import PdfFileReader
from tests.util.file_system import cleanup_dir, create_test_files, write_to_pdf_file


def test_reader_reads_single_pdf():
    temp_dir = Path.cwd() / "tests" / "temp"
    test_dir = temp_dir / "test_reader_reads_pdfs"

    paths = create_test_files(test_dir, "pdf", 1)

    for path in paths:
        write_to_pdf_file(path, f"This is the content for pdf file {path.absolute()}")

    reader = PdfFileReader()

    result = reader.invoke(paths[0])

    assert len(result)

    for document in result:
        assert len(document.page_content)
    cleanup_dir(test_dir)


def test_reader_reads_many_pdfs():
    temp_dir = Path.cwd() / "tests" / "temp"
    test_dir = temp_dir / "test_reader_reads_pdfs"

    paths = create_test_files(test_dir, "pdf", 10)

    for path in paths:
        write_to_pdf_file(path, f"This is the content for pdf file {path.absolute()}")

    reader = PdfFileReader()

    results = reader.batch(paths)

    assert len(results) == len(paths)
    for result in results:
        assert len(result)

        for document in result:
            assert len(document.page_content)

    cleanup_dir(test_dir)
