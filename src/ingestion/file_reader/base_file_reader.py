from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.runnables import Runnable

type FileReader = Runnable[Path, List[Document]]
