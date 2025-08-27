from pathlib import Path
from typing import Callable, Dict, Tuple

from langchain_core.runnables import RunnableBranch
from langchain_core.runnables.base import RunnableLike
from langchain_core.runnables.utils import Output

from src.exceptions.file_path import InvalidFileTypeException


class FileTypeBranch(RunnableBranch[Path, Output]):
    def __init__(
        self,
        config: Dict[str, RunnableLike[Path, Output]],
    ):
        def branch_runnable(
            file_type: str, runnable: RunnableLike[Path, Output]
        ) -> Tuple[Callable[[Path], bool], RunnableLike[Path, Output]]:
            return lambda x: x.suffix.lower() == file_type, runnable

        branches = [
            branch_runnable(file_type, runnable)
            for file_type, runnable in config.items()
        ]

        def throw_error(path: Path):
            raise InvalidFileTypeException(path)

        super().__init__(*branches, throw_error)
