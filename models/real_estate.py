# app/models/real_estate.py
from sqlalchemy import Column, Integer, String, Boolean, Date
from core.database import Base

class RealEstate(Base):
    __tablename__ = "realestate"

    id = Column(Integer, primary_key=True, index=True)
    file_no = Column(String, unique=True, index=True, nullable=False)
    date = Column(Date, nullable=False)

    reference_id = Column(String, nullable=True)
    farmer_id = Column(String, nullable=False)
    extent = Column(String, nullable=True)
    survey_no = Column(String, nullable=True)

    location = Column(String, nullable=True)
    village = Column(String, nullable=True)
    mandal = Column(String, nullable=True)
    district = Column(String, nullable=True)

    document_holder = Column(String, nullable=True)
    father_name = Column(String, nullable=True)
    address = Column(String, nullable=True)

    aadhar_no = Column(String(12), nullable=False)
    contact = Column(String(10), nullable=False)

    reference_name = Column(String, nullable=True)
    reference_aadhar = Column(String(12), nullable=True)
    reference_contact1 = Column(String(10), nullable=True)
    reference_contact2 = Column(String(10), nullable=True)
    reference_address = Column(String, nullable=True)

    closure = Column(String, nullable=True)
    farmer_owner_position = Column(String, nullable=True)
    farmer_owner_position_details = Column(String, nullable=True)

    dispute_issue = Column(String, nullable=True)
    dispute_revenue = Column(Boolean, default=False)
    dispute_government = Column(Boolean, default=False)
    dispute_private = Column(Boolean, default=False)

    sfa = Column(String, nullable=True)
    oneb = Column(String, nullable=True)
    adangal = Column(String, nullable=True)
    passbook = Column(String, nullable=True)
    passbook_number = Column(String, nullable=True)
    slr = Column(String, nullable=True)
    mdr = Column(String, nullable=True)
    gilman_record = Column(String, nullable=True)
    gps_survey = Column(String, nullable=True)

    ec_digital = Column(String, nullable=True)
    ec_manual = Column(String, nullable=True)
    fmb_sketch = Column(String, nullable=True)
    document_boundaries_match = Column(String, nullable=True)
    document_convention_copies = Column(String, nullable=True)
    enjoyment = Column(String, nullable=True)
    sale = Column(String, nullable=True)

    number_of_documents = Column(String, nullable=True)
    document_numbers_sale_deed = Column(String, nullable=True)

    legal_heirs = Column(String, nullable=True)
    death_certificates = Column(String, nullable=True)
    note = Column(String, nullable=True)
