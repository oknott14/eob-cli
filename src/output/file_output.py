from pathlib import Path
from typing import Any, Union

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel
from rich import print


class FileOutput(Runnable[BaseModel, BaseModel]):
    def __init__(
        self,
        output_dir: Union[str, Path],
        file_name_key: str,
        overwrite: bool = False,
    ):
        self.file_name_key = file_name_key
        self.output_dir = Path(output_dir).absolute()
        self.overwrite = overwrite

    def invoke(
        self, input: BaseModel, config: RunnableConfig | None = None, **kwargs: Any
    ) -> BaseModel:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        model_file_path = Path(input.__getattribute__(self.file_name_key))
        file_name = model_file_path.name.removesuffix(model_file_path.suffix)

        file_path = self.output_dir / f"{file_name}.json"
        file_path.touch(exist_ok=self.overwrite)
        print(f"Writing Results for {model_file_path} to {file_path}")

        file = open(file_path, "w")
        file.write(input.model_dump_json(indent=2))

        file.close()

        return input
