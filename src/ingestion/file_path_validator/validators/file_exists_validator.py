from pathlib import Path

from src.exceptions.file_path import FileDoesNotExistException, InvalidFilePathException

from .base_validator import BaseFilePathValidator


class FileExistsValidator(BaseFilePathValidator):
    def _validate(self, path: Path) -> bool:
        return path.exists()

    def error(self, path: Path) -> InvalidFilePathException:
        return FileDoesNotExistException(path)
