import shutil
from pathlib import Path
from typing import Any

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from rich import print

from src.exceptions.file_path import FileDoesNotExistException


class RunnableLog(Runnable):
    def invoke(
        self, input: Any, config: RunnableConfig | None = None, **kwargs: Any
    ) -> Any:
        print(input)
        return input


def zip_directory(source: Path, zip_file_path: Path):
    """
    Zips an existing directory and places the zip file at the provided path.
    """

    if not source.exists():
        raise FileDoesNotExistException(source)

    # Create a zip archive from the temporary directory
    # shutil.make_archive zips the content and gives it a .zip extension
    shutil.make_archive(
        str(zip_file_path.absolute()).removesuffix(zip_file_path.suffix),
        "zip",
        source,
    )
