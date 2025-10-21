from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, validator


class InsuranceProvider(str, Enum):
    amil = 'amil'
    unimed = 'unimed'
    porto = 'porto'
    particular = 'particular'

class Gender(str, Enum):
    male = 'male'
    female = 'female'
    other = 'other'
    not_announced = 'not_announced'

class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"

class ProviderSpeciality(str, Enum):
    psychology = "psychology"
    physiotherapy = "physiotherapy"
    nutrition = "nutrition"
    cardiology = "cardiology"
    dermatology = "dermatology"

class WorkShift(str, Enum):
    morning = "morning"
    afternoon = "afternoon"
    full_day = "full_day"

#pacientes
class PersonBase(BaseModel):
    name: str
    birth_date: date
    gender: Gender
    document: str
    phone_number: str
    email: EmailStr


class PatientBase(PersonBase):
    insurance_provider: InsuranceProvider
    insurance_number: str | None = None
    emergency_contact: str | None = None
    emergency_phone: str | None = None
    blood_type: str | None = None
    organ_donor: bool = False

class PatientCreate(PatientBase):
    pass

class PatientResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
 
class PatientUpdate(PatientBase):
    # person fields
    name: str | None = None
    birth_date: date | None = None
    gender: Gender | None = None
    document: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None

    # patient fields
    insurance_provider: InsuranceProvider | None = None
    insurance_number: str | None = None
    blood_type: str | None = None
    organ_donor: bool | None = None
    emergency_contact: str | None = None
    emergency_phone: str | None = None

    @validator("gender", pre=True, always=True)
    def check_gender(cls, v):
        if v is None:
            return v
        if v in [item.value for item in Gender]:
            return v
        raise ValueError("Invalid gender option.")
    
    @validator("insurance_provider", pre=True, always=True)
    def check_insurance_provider(cls, v):
        if v is None:
            return v
        if v in [item.value for item in InsuranceProvider]:
            return v
        raise ValueError("Invalid insurance provider option.")
    
#profissional
class ProviderBase(PersonBase):
    specialty: ProviderSpeciality
    work_shift: WorkShift
    license_number: str
    active: bool
    availability_notes: str | None = None

class ProviderCreate(ProviderBase):
    pass

class ProviderResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProviderUpdate(ProviderBase):
    # person fields
    name: str | None = None
    birth_date: date | None = None
    gender: Gender | None = None
    document: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None

    # provider fields
    specialty: str | None = None
    work_shift: WorkShift | None = None
    license_number: str | None = None
    active: str | None = None
    availability_notes: str | None = None

    @validator("gender", pre=True, always=True)
    def check_gender(cls, v):
        if v is None:
            return v
        if v in [item.value for item in Gender]:
            return v
        raise ValueError("Invalid gender option.")

# consultas
class AppointmentBase(BaseModel):
    patient_id: int
    provider_id: int
    date_hour: datetime
    status: AppointmentStatus
    reason: str | None = None
    notes: str | None = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AppointmentUpdate(AppointmentBase):
    provider_id: int | None = None
    date_hour: datetime | None = None
    status: AppointmentStatus | None = None
    reason: str | None = None
    notes: str | None = None

    patient_id: None = Field(default=None, exclude=True)

    @validator("status", pre=True, always=True)
    def check_status(cls, v):
        if v is None:
            return v
        if v in [item.value for item in AppointmentStatus]:
            return v
        raise ValueError("Invalid status.")

#autenticacao
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    username: str
    admin: bool

class User(BaseModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int | None = None