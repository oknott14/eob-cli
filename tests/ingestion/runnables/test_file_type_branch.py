from pathlib import Path

from src.exceptions.file_path import InvalidFileTypeException
from src.ingestion.runnables.file_type_branch import FileTypeBranch


def test_file_type_branch_uses_config(mocker):
    mock = mocker.Mock()
    mock.return_value = []
    runnable = FileTypeBranch({".pdf": mock})
    path = Path("test_file.pdf")
    result = runnable.invoke(path)

    assert result == []
    mock.assert_called_once()


def test_file_type_branch_works_with_many(mocker):
    path_pdf = Path("test_file.pdf")
    path_zip = Path("test_file.zip")
    mock_pdf = mocker.Mock()
    mock_pdf.return_value = [path_pdf]
    mock_zip = mocker.Mock()
    mock_zip.return_value = [path_zip]

    runnable = FileTypeBranch({".pdf": mock_pdf, ".zip": mock_zip})

    assert runnable.invoke(path_pdf) == [path_pdf]
    mock_pdf.assert_called_once()

    assert runnable.invoke(path_zip) == [path_zip]
    mock_zip.assert_called_once()


def test_throws_error_when_file_type_is_invalid(mocker):
    invalid_path = Path("test_file.zip")

    mock_pdf = mocker.Mock()
    mock_pdf.return_value = []

    runnable = FileTypeBranch({".pdf": mock_pdf})

    try:
        runnable.invoke(invalid_path)
    except Exception as e:
        assert isinstance(e, InvalidFileTypeException)
    assert not mock_pdf.called
