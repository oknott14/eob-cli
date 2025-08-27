from pathlib import Path
from typing import Any, Optional, Union

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel


class FileOutput(Runnable[BaseModel, BaseModel]):
    files_dumped = 0

    def __init__(
        self, output_dir: Union[str, Path], file_name_key: Optional[str] = None
    ):
        self.file_name_key = file_name_key
        self.output_dir = Path(output_dir).absolute()

    def invoke(
        self, input: BaseModel, config: RunnableConfig | None = None, **kwargs: Any
    ) -> BaseModel:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"eob_{self.files_dumped}.json"

        if self.file_name_key:
            file_name = f"{str(input.__getattribute__(self.file_name_key))}.json"
        else:
            self.files_dumped += 1

        file_path = self.output_dir / file_name
        file_path.touch(exist_ok=False)

        file = open(file_path, "w")

        file.write(input.model_dump_json(indent=2))

        file.close()

        return input
