from datetime import date, datetime
from typing import Annotated, Any, List, Optional

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

    # Patient Information
    patient_name: Annotated[
        Optional[str], Field(description="The full name of the patient on the EOB.")
    ] = Field(None)
    patient_id: Annotated[
        Optional[str], Field(description="The patient's member ID or ID number.")
    ] = Field(None)
    patient_dob: Annotated[
        Optional[datetime],
        Field(description="The patient's date of birth."),
        WrapValidator(flexible_date_validator),
    ] = Field(None)
    patient_address: Annotated[
        Optional[str], Field(description="The patient's full address.")
    ] = Field(None)

    # Provider Information
    provider_name: Annotated[
        Optional[str], Field(description="The full name of the healthcare provider.")
    ] = Field(None)
    provider_id: Annotated[
        Optional[str], Field(description="The provider's NPI number or ID.")
    ] = Field(None)
    provider_address: Annotated[
        Optional[str], Field(description="The provider's full address.")
    ] = Field(None)
    provider_specialty: Annotated[
        Optional[str],
        Field(description="The specialty of the provider (e.g., 'Cardiology')."),
    ] = Field(None)

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
    out_of_pocket_maximum: Annotated[
        Optional[float],
        Field(description="The patient's annual out-of-pocket maximum."),
    ] = Field(None)
    adjustments_or_discounts: Annotated[
        Optional[List[str]],
        Field(description="Any adjustments or discounts applied to the claim."),
    ] = Field(None)

    # Coverage Decisions
    claim_status: Annotated[
        Optional[str],
        Field(description="The status of the claim (e.g., 'Approved', 'Denied')."),
    ] = Field(None)
    denial_explanation: Annotated[
        Optional[str],
        Field(
            description="An explanation for any portion of the claim that was denied."
        ),
    ] = Field(None)
    authorization_requirements: Annotated[
        Optional[str],
        Field(description="Information about prior authorization requirements."),
    ] = Field(None)
    appeal_rights_info: Annotated[
        Optional[str],
        Field(description="Information on how to appeal the coverage decision."),
    ] = Field(None)

    # Additional Required Details
    claim_number: Annotated[
        Optional[str], Field(description="The unique claim number.")
    ] = Field(None)
    group_number: Annotated[
        Optional[str], Field(description="The patient's insurance group number.")
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
        Field(description="Whether the provider was in-network or out-of-network."),
    ] = Field(None)

    service_date: Annotated[
        Optional[datetime],
        Field(description="The date the service was provided."),
        WrapValidator(flexible_date_validator),
    ] = Field(None)
