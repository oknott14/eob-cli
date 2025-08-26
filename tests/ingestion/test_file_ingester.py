from src.exceptions.file_path import InvalidFileTypeException
from src.ingestion.file_ingester import FileIngester, FileIngesterOptions


def test_file_ingester_accepts_specified_file_types():
    ingester = FileIngester(
        FileIngesterOptions(
            file_type_branches={".pdf": lambda x: [x], ".zip": lambda x: [x]}
        )
    )

    assert ingester.invoke("test_file_path.pdf")
    assert ingester.invoke("test_file.zip")


def test_file_ingester_does_not_accept_other_file_types():
    ingester = FileIngester(
        FileIngesterOptions(
            file_type_branches={".pdf": lambda x: [x], ".zip": lambda x: [x]}
        )
    )

    try:
        ingester.invoke("test_file_path.other")
    except Exception as e:
        assert isinstance(e, InvalidFileTypeException)
