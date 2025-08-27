from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


class BaseExtractionOutput(BaseModel):
    """
    A Pydantic model for data extracted from an Explanation of Benefits (EOB)
    document, based on the required fields by the Affordable Care Act (ACA).

    All fields are optional and default to None, allowing the model to be
    created with partial data.
    """

    # Patient and Provider Information
    patient_name: Optional[str] = Field(
        None, description="The full name of the patient on the EOB."
    )
    provider_name: Optional[str] = Field(
        None, description="The full name of the healthcare provider."
    )

    # Service Information
    service_date: Optional[date] = Field(
        None, description="The date the healthcare service was provided."
    )
    service_description: Optional[str] = Field(
        None, description="A description of the service received."
    )

    # Financial Information
    total_billed_amount: Optional[float] = Field(
        None, description="The total amount the provider billed for the service."
    )
    plan_paid_amount: Optional[float] = Field(
        None, description="The amount the insurance plan paid directly to the provider."
    )

    # Patient Responsibility Breakdown
    patient_responsibility: Optional[float] = Field(
        None, description="The total amount the patient is responsible for."
    )
    copay: Optional[float] = Field(
        None, description="The fixed amount a patient pays for a covered service."
    )
    deductible: Optional[float] = Field(
        None,
        description="The amount a patient must pay out-of-pocket before the plan begins to pay.",
    )
    coinsurance: Optional[float] = Field(
        None,
        description="The percentage of costs a patient pays after meeting the deductible.",
    )

    # Denials of Coverage
    denial_explanation: Optional[str] = Field(
        None, description="An explanation for any portion of the claim that was denied."
    )


class ServiceDetail(BaseModel):
    """
    A nested Pydantic model for a single line-item of service details.
    """

    service_date: Optional[date] = Field(
        None, description="The date the service was provided."
    )
    service_description: Optional[str] = Field(
        None, description="A detailed description of the medical service."
    )
    procedure_codes: Optional[List[str]] = Field(
        None, description="A list of CPT codes for the service."
    )
    diagnosis_codes: Optional[List[str]] = Field(
        None, description="A list of ICD codes for the diagnosis."
    )
    place_of_service: Optional[str] = Field(
        None, description="The location where the service was provided."
    )


class VerboseExtractionOutput(BaseExtractionOutput):
    """
    A Pydantic model for data extracted from an Explanation of Benefits (EOB)
    document, based on the required fields by the Affordable Care Act (ACA)
    and additional useful details.

    All fields are optional and default to None, allowing the model to be
    created with partial data.
    """

    # Patient Information
    patient_id: Optional[str] = Field(
        None, description="The patient's member ID or ID number."
    )
    patient_dob: Optional[date] = Field(
        None, description="The patient's date of birth."
    )
    patient_address: Optional[str] = Field(
        None, description="The patient's full address."
    )

    # Provider Information
    provider_id: Optional[str] = Field(
        None, description="The provider's NPI number or ID."
    )
    provider_address: Optional[str] = Field(
        None, description="The provider's full address."
    )
    provider_specialty: Optional[str] = Field(
        None, description="The specialty of the provider (e.g., 'Cardiology')."
    )

    # Service Details (List of line items)
    service_details: Optional[List[ServiceDetail]] = Field(
        None, description="A list of all individual services detailed on the EOB."
    )

    # Financial Information
    out_of_pocket_maximum: Optional[float] = Field(
        None, description="The patient's annual out-of-pocket maximum."
    )
    adjustments_or_discounts: Optional[List[str]] = Field(
        None, description="Any adjustments or discounts applied to the claim."
    )

    # Coverage Decisions
    claim_status: Optional[str] = Field(
        None, description="The status of the claim (e.g., 'Approved', 'Denied')."
    )
    authorization_requirements: Optional[str] = Field(
        None, description="Information about prior authorization requirements."
    )
    appeal_rights_info: Optional[str] = Field(
        None, description="Information on how to appeal the coverage decision."
    )

    # Additional Details
    claim_number: Optional[str] = Field(None, description="The unique claim number.")
    group_number: Optional[str] = Field(
        None, description="The patient's insurance group number."
    )
    plan_name: Optional[str] = Field(
        None, description="The name of the insurance plan."
    )
    processing_date: Optional[date] = Field(
        None, description="The date the claim was processed."
    )
    network_status: Optional[str] = Field(
        None, description="Whether the provider was in-network or out-of-network."
    )
