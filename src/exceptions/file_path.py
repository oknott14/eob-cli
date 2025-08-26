from pathlib import Path
from typing import Optional


class InvalidFilePathException(Exception):
    """
    Exception raised when ther is an error with the filepath.

    Attributes:
        path -- the Path object that does not exist
        message -- explanation of the error
    """

    def __init__(self, path: Path, message: Optional[str] = None):
        self.path = path
        if message is None:
            message = f"Invalid File Path: {path}"
        self.message = message


class FileDoesNotExistException(InvalidFilePathException):
    def __init__(self, path: Path):
        super().__init__(path, f"File does not exist at {path}")


class InvalidFileTypeException(InvalidFilePathException):
    def __init__(self, path: Path):
        super().__init__(path, f"Invalid File type at {path}")


class InvalidZipFileException(InvalidFilePathException):
    def __init__(self, path: Path):
        super().__init__(path, f"The File {path} is not a valid zip file")
