from pathlib import Path
from typing import Callable, Dict, List, Tuple

from langchain_core.runnables import RunnableBranch
from langchain_core.runnables.base import RunnableLike

from src.exceptions.file_path import InvalidFileTypeException


class FileTypeBranch(RunnableBranch[Path, List[Path]]):
    def __init__(self, config: Dict[str, RunnableLike[Path, List[Path]]]):
        def branch_runnable(
            file_type: str, runnable: RunnableLike[Path, List[Path]]
        ) -> Tuple[Callable[[Path], bool], RunnableLike[Path, List[Path]]]:
            return lambda x: x.suffix.lower() == file_type, runnable

        branches = [
            branch_runnable(file_type, runnable)
            for file_type, runnable in config.items()
        ]

        def throw_error(path: Path):
            raise InvalidFileTypeException(path)

        super().__init__(*branches, throw_error)
