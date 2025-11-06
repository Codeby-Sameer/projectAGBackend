# app/schemas/real_estate.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class RealEstateBase(BaseModel):
    # required fields - match SQLAlchemy column names
    file_no: str = Field(..., min_length=1)
    date: date
    farmer_id: str = Field(..., min_length=1)
    aadhar_no: str = Field(..., min_length=12, max_length=12)
    contact: str = Field(..., min_length=10, max_length=10)

    # optional fields
    reference_id: Optional[str] = None
    extent: Optional[str] = None
    survey_no: Optional[str] = None
    location: Optional[str] = None
    village: Optional[str] = None
    mandal: Optional[str] = None
    district: Optional[str] = None
    document_holder: Optional[str] = None
    father_name: Optional[str] = None
    address: Optional[str] = None
    reference_name: Optional[str] = None
    reference_aadhar: Optional[str] = None
    reference_contact1: Optional[str] = None
    reference_contact2: Optional[str] = None
    reference_address: Optional[str] = None
    closure: Optional[str] = None
    farmer_owner_position: Optional[str] = None
    farmer_owner_position_details: Optional[str] = None
    dispute_issue: Optional[str] = None
    dispute_revenue: Optional[bool] = False
    dispute_government: Optional[bool] = False
    dispute_private: Optional[bool] = False

    # document flags
    sfa: Optional[str] = None
    oneb: Optional[str] = None
    adangal: Optional[str] = None
    passbook: Optional[str] = None
    passbook_number: Optional[str] = None
    slr: Optional[str] = None
    mdr: Optional[str] = None
    gilman_record: Optional[str] = None
    gps_survey: Optional[str] = None
    ec_digital: Optional[str] = None
    ec_manual: Optional[str] = None
    fmb_sketch: Optional[str] = None
    document_boundaries_match: Optional[str] = None
    document_convention_copies: Optional[str] = None
    enjoyment: Optional[str] = None
    sale: Optional[str] = None
    number_of_documents: Optional[str] = None
    document_numbers_sale_deed: Optional[str] = None
    legal_heirs: Optional[str] = None
    death_certificates: Optional[str] = None
    note: Optional[str] = None

class RealEstateCreate(BaseModel):
    # For creating - use frontend field names
    fileNo: str = Field(..., min_length=1)
    date: date
    farmerId: str = Field(..., min_length=1)
    aadharNo: str = Field(..., min_length=12, max_length=12)
    contact: str = Field(..., min_length=10, max_length=10)

    # optional fields with frontend names
    referenceId: Optional[str] = None
    extent: Optional[str] = None
    surveyNo: Optional[str] = None
    location: Optional[str] = None
    village: Optional[str] = None
    mandal: Optional[str] = None
    district: Optional[str] = None
    documentHolder: Optional[str] = None
    fatherName: Optional[str] = None
    address: Optional[str] = None
    referenceName: Optional[str] = None
    referenceAadhar: Optional[str] = None
    referenceContact1: Optional[str] = None
    referenceContact2: Optional[str] = None
    referenceAddress: Optional[str] = None
    closure: Optional[str] = None
    farmerOwnerPosition: Optional[str] = None
    farmerOwnerPositionDetails: Optional[str] = None
    disputeIssue: Optional[str] = None
    disputeRevenue: Optional[bool] = False
    disputeGovernment: Optional[bool] = False
    disputePrivate: Optional[bool] = False

    # document flags with frontend names
    sfa: Optional[str] = None
    oneB: Optional[str] = None
    adangal: Optional[str] = None
    passbook: Optional[str] = None
    passbookNumber: Optional[str] = None
    slr: Optional[str] = None
    mdr: Optional[str] = None
    gilmanRecord: Optional[str] = None
    gpsSurvey: Optional[str] = None
    ecDigital: Optional[str] = None
    ecManual: Optional[str] = None
    fmbSketch: Optional[str] = None
    documentBoundariesMatch: Optional[str] = None
    documentConventionCopies: Optional[str] = None
    enjoyment: Optional[str] = None
    sale: Optional[str] = None
    numberOfDocuments: Optional[str] = None
    documentNumbersSaleDeed: Optional[str] = None
    legalHeirs: Optional[str] = None
    deathCertificates: Optional[str] = None
    note: Optional[str] = None

class RealEstateRead(RealEstateBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True  # For SQLAlchemy 2.0