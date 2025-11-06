from sqlalchemy.orm import Session
from app.models.real_estate import RealEstate
from app.schemas.real_estate import RealEstateCreate

def create_realestate(db: Session, payload: RealEstateCreate) -> RealEstate:
    obj = RealEstate(
        file_no=payload.fileNo,
        date=payload.date,
        reference_id=payload.referenceId,
        farmer_id=payload.farmerId,
        extent=payload.extent,
        survey_no=payload.surveyNo,
        location=payload.location,
        village=payload.village,
        mandal=payload.mandal,
        district=payload.district,
        document_holder=payload.documentHolder,
        father_name=payload.fatherName,
        address=payload.address,
        aadhar_no=payload.aadharNo,
        contact=payload.contact,
        reference_name=payload.referenceName,
        reference_aadhar=payload.referenceAadhar,
        reference_contact1=payload.referenceContact1,
        reference_contact2=payload.referenceContact2,
        reference_address=payload.referenceAddress,
        closure=payload.closure,
        farmer_owner_position=payload.farmerOwnerPosition,
        farmer_owner_position_details=payload.farmerOwnerPositionDetails,
        dispute_issue=payload.disputeIssue,
        dispute_revenue=payload.disputeRevenue,
        dispute_government=payload.disputeGovernment,
        dispute_private=payload.disputePrivate,
        sfa=payload.sfa,
        oneb=payload.oneB,
        adangal=payload.adangal,
        passbook=payload.passbook,
        passbook_number=payload.passbookNumber,
        slr=payload.slr,
        mdr=payload.mdr,
        gilman_record=payload.gilmanRecord,
        gps_survey=payload.gpsSurvey,
        ec_digital=payload.ecDigital,
        ec_manual=payload.ecManual,
        fmb_sketch=payload.fmbSketch,
        document_boundaries_match=payload.documentBoundariesMatch,
        document_convention_copies=payload.documentConventionCopies,
        enjoyment=payload.enjoyment,
        sale=payload.sale,
        number_of_documents=payload.numberOfDocuments,
        document_numbers_sale_deed=payload.documentNumbersSaleDeed,
        legal_heirs=payload.legalHeirs,
        death_certificates=payload.deathCertificates,
        note=payload.note,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_realestate(db: Session, file_no: str):
    return db.query(RealEstate).filter(RealEstate.file_no == file_no).first()

def list_realestates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RealEstate).offset(skip).limit(limit).all()
