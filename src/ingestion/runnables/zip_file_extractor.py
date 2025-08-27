import zipfile
from os import walk
from pathlib import Path
from typing import Any, Iterable, List, Union

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from rich import print

from src.exceptions.file_path import FileDoesNotExistException, InvalidZipFileException


class ZipFileExtractor(Runnable[Path, List[Path]]):
    """
    Extracts a zip file and returns a list of files in the zipped directory.
    """

    def __init__(
        self,
        extract_to: Union[str, Path] = Path.cwd().joinpath("extracted_eobs"),
        file_types: Iterable[str] = [],
    ):
        """
        Initializes the FileProcessor with the root directory and file extensions.

        Args:
            extract_to (Path): The root directory to search.
            file_types (Set[str]): A set of file extensions (e.g., {'.txt', '.jpg'}).
        """
        self.extract_to = Path(extract_to)

        self.extract_to.mkdir(
            parents=True, exist_ok=True
        )  # Make extraction directory if it does not exist

        self.file_types = set(file_types)  # Supported File Types

    def invoke(
        self, input: Path, config: RunnableConfig | None = None, **kwargs: Any
    ) -> List[Path]:
        self.extract_zip_file(input)
        return self.get_files()

    def extract_zip_file(self, path: Path):
        """
        Extracts a single zip file to the instance's designated extraction directory.

        This method validates the file's existence and format before attempting to
        extract its contents. Custom exceptions are raised for specific errors.

        Args:
            path (Path): The path to the zip file to be extracted.

        Raises:
            FileDoesNotExistException: If the specified zip file does not exist.
            InvalidZipFileException: If the file is not a valid zip archive.
        """
        print(f"Extracting {path} to {self.extract_to}")
        try:
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(self.extract_to)
        except FileNotFoundError:
            raise FileDoesNotExistException(path)
        except zipfile.BadZipFile:
            raise InvalidZipFileException(path)

    def get_files(self) -> List[Path]:
        """
        Walks through the specified directory and its subdirectories,
        returning a list of paths for files with the target extensions.

        The method uses os.walk() for an efficient traversal of the directory tree.

        Returns:
            List[Path]: An array of Path objects for all matching files.
        """
        print("Parsing Extracted File Paths")
        found_files = []
        # os.walk yields a 3-tuple: (root, directories, files)
        for root, _, files in walk(self.extract_to):
            for file in files:
                file_path = Path(root) / file
                # Check if the file's extension is in our set of target types.
                # Convert the suffix to lowercase to ensure case-insensitive matching.
                if file_path.suffix.lower() in self.file_types:
                    found_files.append(file_path)

        return found_files
