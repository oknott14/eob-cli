from pathlib import Path
from time import time

from src.exceptions.file_path import FileDoesNotExistException
from src.ingestion.file_path_validator.validators.file_exists_validator import (
    FileExistsValidator,
)


def test_file_exist_validator_true_when_exists():
    validator = FileExistsValidator()
    path = Path(__file__)
    assert validator._validate(path)
    validator.validate(path)


def test_throws_error_when_path_does_not_exist(mocker):
    validator = FileExistsValidator()
    path = Path(f"{__file__}{time()}")
    assert not validator._validate(path)
    spy = mocker.spy(validator, "error")
    try:
        validator.validate(path)
    except FileDoesNotExistException as e:
        assert isinstance(e, FileDoesNotExistException)

    spy.assert_called_once()
