from typing import Any

from src.extraction.structured_output.extraction_structured_output import (
    ExtractionOutput,
)


def test_can_be_created_with_nothing():
    assert ExtractionOutput(**{})


def test_validator_called_on_multiple_fields():
    dummy_data: Any = {
        "patient_dob": "11/13/2000",
        "processing_date": "11/13/2024",
        "service_date": "12-12-12",
    }

    data_model = ExtractionOutput(**dummy_data)

    assert data_model.patient_dob
    assert data_model.processing_date
    assert data_model.service_date


def test_invalid_dates_are_none():
    dummy_data: Any = {
        "patient_dob": "111/bb131/2000",
        "processing_date": "11s13s2024",
        "service_date": "this is not a date",
    }

    data_model = ExtractionOutput(**dummy_data)

    assert not data_model.patient_dob
    assert not data_model.processing_date
    assert not data_model.service_date


def test_is_json_serializeable():
    assert ExtractionOutput(**{}).model_json_schema()
