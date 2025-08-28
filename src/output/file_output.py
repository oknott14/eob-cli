from pathlib import Path
from typing import Any, Optional, Union

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel


class FileOutput(Runnable[BaseModel, BaseModel]):
    files_dumped = 0

    def __init__(
        self,
        output_dir: Union[str, Path],
        file_name_key: Optional[str] = None,
        overwrite: bool = False,
    ):
        self.file_name_key = file_name_key
        self.output_dir = Path(output_dir).absolute()
        self.overwrite = overwrite

    def invoke(
        self, input: BaseModel, config: RunnableConfig | None = None, **kwargs: Any
    ) -> BaseModel:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"eob_{self.files_dumped}.json"

        if self.file_name_key:
            model_file_name = Path(input.__getattribute__(self.file_name_key))
            name = model_file_name.name.removesuffix(model_file_name.suffix)
            file_name = f"{name}.json"
        else:
            self.files_dumped += 1

        file_path = self.output_dir / file_name
        file_path.touch(exist_ok=self.overwrite)

        file = open(file_path, "w")

        file.write(input.model_dump_json(indent=2))

        file.close()

        return input
