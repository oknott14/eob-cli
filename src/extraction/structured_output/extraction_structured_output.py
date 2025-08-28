from datetime import date, datetime
from pathlib import Path
from typing import Annotated, Any, List, Optional, Union

from pydantic import (
    BaseModel,
    Field,
    ValidatorFunctionWrapHandler,
    WrapValidator,
)


def flexible_date_validator(
    value: Any, handler: ValidatorFunctionWrapHandler
) -> date | None:
    try:
        return handler(value)
    except Exception:
        if value is None or isinstance(value, datetime):
            return value
        elif not isinstance(value, str):
            return None

        # List of acceptable datetime formats, from most to least specific
        date_formats = [
            "%Y-%m-%d %H:%M:%S",  # 2024-11-13 14:30:00
            "%Y-%m-%d %H:%M",  # 2024-11-13 14:30
            "%m/%d/%Y",  # 11/13/2024
            "%m/%d/%y",  # 11/13/24
            "%B %d, %Y",  # November 13, 2024
            "%Y-%m-%d",  # 2024-11-13
            "%d-%m-%Y",
            "%d-%m-%y",
        ]

        for fmt in date_formats:
            try:
                # Attempt to parse the string with the current format
                return datetime.strptime(value, fmt)
            except ValueError:
                continue

        return None


class ExtractionOutput(BaseModel):
    """
    A Pydantic model for data extracted from an Explanation of Benefits (EOB)
    document, based on the required fields by the Affordable Care Act (ACA)
    and additional useful details.
    """

    # Document Information
    source_file_path: Annotated[Union[str, Path, None], Field()] = Field(None)

    # Patient Information
    patient_name: Annotated[
        Optional[str], Field(description="The full name of the patient on the EOB.")
    ] = Field(None)

    patient_id: Annotated[
        Optional[str],
        Field(
            description="The patient's member ID or ID number.",
            examples=[
                "980598604",
                "ABC123456789",  # Common alphanumeric format
                "WXYZ987654321",  # Example with a mix of letters and numbers
                "012345678901",  # All numeric, typically 10-12 digits
                "JD-112233-44",  # Hyphenated format
                "P1234567-89",  # Numeric with a leading letter and hyphen
                "E123456789A",
            ],
        ),
    ] = Field(None)

    # Provider Information
    provider_name: Annotated[
        Optional[str],
        Field(
            description="The full name of the healthcare provider or person / organization specified as the service provider.",
        ),
    ] = Field(None)

    provider_id: Annotated[
        Optional[str],
        Field(
            description="The provider's NPI number or ID.",
            examples=[
                "1234567890",  # A typical 10-digit NPI number
                "9876543210",
                "G87654321",  # Example with a leading letter
                "A-555555",  # Hyphenated format
                "MED-343434",  # Prefix with a numeric ID
                "1029384756",
            ],
        ),
    ] = Field(None)
    provider_address: Annotated[
        Optional[str], Field(description="The provider's full address.")
    ] = Field(None)

    # provider_specialty: Annotated[
    #     Optional[str],
    #     Field(description="The specialty of the provider (e.g., 'Cardiology')."),
    # ] = Field(None)

    # Financial Information
    total_billed_amount: Annotated[
        Optional[float],
        Field(description="The total amount the provider billed for the service."),
    ] = Field(None)
    plan_paid_amount: Annotated[
        Optional[float],
        Field(
            description="The amount the insurance plan paid directly to the provider."
        ),
    ] = Field(None)
    patient_responsibility: Annotated[
        Optional[float],
        Field(description="The total amount the patient is responsible for."),
    ] = Field(None)
    copay: Annotated[
        Optional[float],
        Field(description="The fixed amount a patient pays for a covered service."),
    ] = Field(None)
    deductible: Annotated[
        Optional[float],
        Field(
            description="The amount a patient must pay out-of-pocket before the plan begins to pay."
        ),
    ] = Field(None)
    coinsurance: Annotated[
        Optional[float],
        Field(
            description="The percentage of costs a patient pays after meeting the deductible."
        ),
    ] = Field(None)

    adjustments_or_discounts: Annotated[
        Optional[List[str]],
        Field(description="Any adjustments or discounts applied to the claim."),
    ] = Field(None)

    # Coverage Decisions
    claim_status: Annotated[
        Optional[str],
        Field(
            description="The status of the claim.",
            examples=["Approved", "Denied"],
        ),
    ] = Field(None)

    denial_explanation: Annotated[
        Optional[str],
        Field(
            description="An explanation for any portion of the claim that was denied."
        ),
    ] = Field(None)

    # Additional Required Details
    claim_number: Annotated[
        Optional[str], Field(description="The unique claim number.")
    ] = Field(None)

    group_number: Annotated[
        Optional[str],
        Field(
            description="The patient's insurance group number.",
            examples=[
                "5678-ABC-90",  # Alphanumeric with hyphens
                "A-123456",  # Common format with leading letter and numbers
                "GRP-7890",  # A prefix followed by a numeric ID
                "123456",  # Numeric-only format
                "G12345678",  # Numeric with a leading letter
                "9999-9999",  # Hyphenated numeric format
            ],
        ),
    ] = Field(None)

    plan_name: Annotated[
        Optional[str], Field(description="The name of the insurance plan.")
    ] = Field(None)

    processing_date: Annotated[
        Optional[datetime],
        Field(description="The date the claim was processed."),
        WrapValidator(flexible_date_validator),
    ] = Field(None)

    network_status: Annotated[
        Optional[str],
        Field(
            description="Whether the provider was in-network or out-of-network. If the provider paid a portion of the claim, assume they are in-network",
            examples=["in-network", "out-of-network"],
        ),
    ] = Field(None)

    service_date: Annotated[
        Optional[datetime],
        Field(description="The date the service was provided."),
        WrapValidator(flexible_date_validator),
    ] = Field(None)
