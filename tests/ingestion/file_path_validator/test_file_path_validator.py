from pathlib import Path

from src.exceptions.file_path import InvalidFilePathException
from src.ingestion.file_path_validator.file_path_validator import FilePathValidator
from src.ingestion.file_path_validator.validators.base_validator import (
    BaseFilePathValidator,
)


class TestValidator(BaseFilePathValidator):
    def __init__(self, valid: bool = True):
        self.valid = valid

    def _validate(self, path: Path) -> bool:
        return self.valid


test_validator = TestValidator()


def test_file_path_validator_can_be_created():
    runnable = FilePathValidator([])
    assert isinstance(runnable, FilePathValidator)


def test_uses_provided_validators(mocker):
    spy = mocker.spy(test_validator, "validate")
    runnable = FilePathValidator([test_validator])

    assert test_validator in runnable.validators

    test_file_path = "fake-file-path.pdf"
    result = runnable.invoke(test_file_path)

    assert isinstance(result, Path)
    spy.assert_called_once()


def test_calls_error_when_validation_fails(mocker):
    test_validator = TestValidator(False)
    spy = spy = mocker.spy(test_validator, "error")
    runnable = FilePathValidator([test_validator])
    test_file_path = "fake-file-path.pdf"

    try:
        runnable.invoke(test_file_path)
        assert False
    except Exception as e:
        spy.assert_called_once()
        assert isinstance(e, InvalidFilePathException)
