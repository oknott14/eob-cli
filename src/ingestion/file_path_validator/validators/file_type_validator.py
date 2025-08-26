from pathlib import Path
from typing import Iterable

from src.exceptions.file_path import InvalidFilePathException, InvalidFileTypeException
from src.ingestion.file_path_validator.validators.base_validator import (
    BaseFilePathValidator,
)


class FileTypeValidator(BaseFilePathValidator):
    def __init__(self, supported_types: Iterable[str]):
        self.supported_types = set(supported_types)

    def _validate(self, path: Path) -> bool:
        return path.suffix.lower() in self.supported_types

    def error(self, path: Path) -> InvalidFilePathException:
        return InvalidFileTypeException(path)
