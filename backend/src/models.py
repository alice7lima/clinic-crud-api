import uuid

from sqlalchemy import Boolean, Column, Date, DateTime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database import Base


class PersonModel(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    document = Column(String)
    gender = Column(String)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
class PatientModel(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)

    medical_record_number = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    insurance_provider = Column(String, nullable=True)
    insurance_number = Column(String, nullable=True)

    blood_type = Column(String, nullable=True) 
    organ_donor = Column(Boolean, default=False, nullable=False)

    emergency_contact = Column(String, nullable=True)
    emergency_phone = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class ProviderModel(Base):
    __tablename__ = "provider"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    specialty = Column(String, nullable=False)
    work_shift = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
    availability_notes = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class AppointmentModel(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patient.id'))
    provider_id = Column(Integer, ForeignKey('provider.id'))
    date_hour = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), default=None, nullable=True)
    is_active = Column(Boolean, default=True)