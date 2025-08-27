from langchain_core.runnables import RunnableLambda

from src.ingestion.file_ingester import FileIngester, FileIngesterOptions
from src.ingestion.file_path_validator.validators.file_exists_validator import (
    FileExistsValidator,
)
from src.ingestion.file_path_validator.validators.file_type_validator import (
    FileTypeValidator,
)
from src.ingestion.file_reader.pdf_file_reader import PdfFileReader
from src.ingestion.runnables.zip_file_extractor import ZipFileExtractor


class EobIngester(FileIngester):
    def __init__(self, zipFileDestination: str):
        file_reader = PdfFileReader()
        super().__init__(
            FileIngesterOptions(
                file_path_validators=[
                    FileExistsValidator(),
                    FileTypeValidator({".pdf", ".zip"}),
                ],
                file_type_branches={
                    ".pdf": RunnableLambda(lambda x: [x]).pipe(file_reader),
                    ".zip": ZipFileExtractor(zipFileDestination, {".pdf"}).pipe(
                        file_reader
                    ),
                },
            )
        )
