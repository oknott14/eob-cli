from pathlib import Path

from src.ingestion.file_path_validator.validators.file_type_validator import (
    FileTypeValidator,
)


def test_uses_passed_file_types():
    exts = [".py", ".pdf", ".zip"]

    validator = FileTypeValidator(exts)

    for ext in exts:
        assert ext in validator.supported_types

        path = Path(f"test_file{ext}")

        assert validator._validate(path)
