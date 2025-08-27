import json
import shutil
from pathlib import Path
from typing import Any, List, Union

from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from rich import print

from src.exceptions.file_path import FileDoesNotExistException, InvalidFilePathException


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


class RunnableDump(Runnable):
    def __init__(self, dump_to: Union[str, Path]):
        self.dump_to = Path(dump_to)

        if self.dump_to.suffix != ".json":
            raise InvalidFilePathException(
                self.dump_to,
                f"Failed to initialize RunnableDump: The path {self.dump_to} must point to a JSON file.",
            )

    def invoke(
        self, input: Any, config: RunnableConfig | None = None, **kwargs: Any
    ) -> Any:
        self.dump_to.parent.mkdir(parents=True, exist_ok=True)
        self.dump_to.touch(exist_ok=True)

        file = open(self.dump_to, "w")

        file.write(json.dumps(input, indent=2))

        file.close()

        return input


class DocumentListDump(RunnableDump):
    def invoke(
        self,
        input: List[List[Document]],
        config: RunnableConfig | None = None,
        **kwargs: Any,
    ) -> List[List[Document]]:
        return super().invoke(
            [
                [{"page_content": d.page_content, "metadata": d.metadata} for d in dl]
                for dl in input
            ],
            config,
            **kwargs,
        )
