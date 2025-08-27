from typing import Any

from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from pydantic import BaseModel
from rich import print


class ConsoleOutput(Runnable[BaseModel, BaseModel]):
    def invoke(
        self, input: BaseModel, config: RunnableConfig | None = None, **kwargs: Any
    ) -> BaseModel:
        print(input.model_dump_json(indent=2))
        return input
