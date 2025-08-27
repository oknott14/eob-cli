from pathlib import Path

from src.ingestion.zip_file_extractor import ZipFileExtractor
from tests.util.file_system import cleanup_dir, create_test_files, create_zip_file


def test_dir_defaults_to_eob_dir():
    extractor = ZipFileExtractor()
    assert extractor.extract_to.absolute() == Path.cwd() / "extracted_eobs"


def test_file_types_is_set_of_passed():
    extractor = ZipFileExtractor(file_types=[".pdf"])
    assert isinstance(extractor.file_types, set)


def test_extractor_extracts_zip_file():
    test_dir = Path.cwd() / "tests" / "temp" / "test_zip_file_extractor"
    temp_dir = test_dir / "temp_dir"
    zip_path = test_dir / "test_zip_file_extractor.zip"
    extraction_dir = test_dir / "extraction_dir"
    create_test_files(temp_dir, "pdf", 3)
    create_zip_file(temp_dir, zip_path)

    extractor = ZipFileExtractor(extract_to=extraction_dir, file_types={".pdf"})
    extracted_files = extractor.invoke(zip_path)

    assert len(extracted_files) == 3

    for path in extracted_files:
        assert path.exists()
        assert (temp_dir / path.name).exists()
        assert path.suffix == ".pdf"

    cleanup_dir(test_dir)


def test_extractor_extracts_only_supported_file_types():
    test_dir = Path.cwd() / "tests" / "temp" / "test_zip_file_extractor"
    temp_dir = test_dir / "temp_dir"
    zip_path = test_dir / "test_zip_file_extractor.zip"
    extraction_dir = test_dir / "extraction_dir"
    create_test_files(temp_dir, "pdf", 3)
    create_test_files(temp_dir, "txt", 3)
    create_zip_file(temp_dir, zip_path)

    extractor = ZipFileExtractor(extract_to=extraction_dir, file_types={".pdf"})
    extracted_files = extractor.invoke(zip_path)

    assert len(extracted_files) == 3

    for path in extracted_files:
        assert path.exists()
        assert (temp_dir / path.name).exists()
        assert path.suffix == ".pdf"

    cleanup_dir(test_dir)
