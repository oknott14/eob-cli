from abc import ABC, abstractmethod
from pathlib import Path

from src.exceptions.file_path import InvalidFilePathException


class BaseFilePathValidator(ABC):
    def validate(self, path: Path) -> None:
        if not self._validate(path):
            raise self.error(path)

    @abstractmethod
    def _validate(self, path: Path) -> bool:
        pass

    def error(self, path: Path) -> InvalidFilePathException:
        return InvalidFilePathException(path)
