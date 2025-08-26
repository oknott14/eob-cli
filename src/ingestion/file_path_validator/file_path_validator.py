from pathlib import Path
from typing import Any, List

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig

from src.ingestion.file_path_validator.validators.base_validator import (
    BaseFilePathValidator,
)


class FilePathValidator(Runnable[str, Path]):
    def __init__(self, validators: List[BaseFilePathValidator]):
        self.validators = validators
        super()

    def invoke(
        self, input: str, config: RunnableConfig | None = None, **kwargs: Any
    ) -> Path:
        path = Path(input)

        for validator in self.validators:
            validator.validate(path)

        return path
