from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.helpers import get_by_id, search_resource
from src.models import AppointmentModel, PatientModel, ProviderModel
from src.schemas import AppointmentCreate, AppointmentUpdate


def get_appointments(db: Session) -> list[AppointmentModel]:
    return db.query(AppointmentModel).all()

def get_appointment(db: Session, appointment_id: str) -> AppointmentModel | None:
    return db.query(AppointmentModel).filter(AppointmentModel.id == appointment_id).first()

def create_appointment(db: Session, appointment_info: AppointmentCreate):
    db_appointment = AppointmentModel(**appointment_info.model_dump())

    patient = search_resource(table=PatientModel, filters={"id": appointment_info.patient_id}, db=db)
    provider = search_resource(table=ProviderModel, filters={"id": appointment_info.provider_id}, db=db)

    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    db.add(db_appointment)
    db.commit()

    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = get_by_id(table=AppointmentModel, id=appointment_id, db=db)

    if db_appointment is None:
        return None

    update_data = appointment.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_appointment, field, value)

    db.commit()
    return db_appointment