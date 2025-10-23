from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.constants import PERSON_FIELDS
from src.helpers import (create_person, get_by_id, search_resource,
                         verify_active_appointments)
from src.models import AppointmentModel, PatientModel, PersonModel
from src.schemas import PatientCreate, PatientUpdate


def get_patients(db: Session) -> list[PatientModel]:
    return db.query(PatientModel).all()

def create_patient(db: Session, patient_info: PatientCreate):
    person_exists = search_resource(
        table=PersonModel, filters={'document': patient_info.document}, db=db
    )

    if person_exists:
        patient_exists = search_resource(
            table=PatientModel,
            filters={'person_id': person_exists.id},
            db=db,
        )
        # se o paciente estiver ativo no sistema, nao cria um novo
        if patient_exists and patient_exists.deleted_at is None:
            raise HTTPException(
            status_code=409,
            detail='Patient already exists.',
        )
        person_id = patient_exists.person_id
        person_exists.deleted_at = None
        db.commit()
    else:   
        person = create_person(resource=patient_info, db=db)
        person_id = person.id

    db_patient = PatientModel(
        person_id=person_id,
        insurance_provider=patient_info.insurance_provider,
        insurance_number=patient_info.insurance_number,
        blood_type=patient_info.blood_type,
        organ_donor=patient_info.organ_donor,
    )

    db.add(db_patient)
    db.commit()

    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    db_patient = get_by_id(table=PatientModel, id=patient_id, db=db)
    if db_patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    active_appointments = verify_active_appointments(
        filter_id_column=AppointmentModel.patient_id, id=patient_id, db=db
    )
    if active_appointments:
        raise HTTPException(
            status_code=409,
            detail='This patient cannot be deleted because they have an in-progress, scheduled, or confirmed appointment.',
        )
    db_person = get_by_id(table=PersonModel, id=db_patient.person_id, db=db)

    now = datetime.now()
    db_patient.deleted_at = now
    db_person.deleted_at = now

    db.commit()


def update_patient(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = search_resource(table=PatientModel, filters={'patient_id': patient_id, "deleted_at": "null"}, db=db)
    if db_patient is None or db_patient.deleted_at is not None:
        return None

    db_person = get_by_id(table=PersonModel, id=db_patient.person_id, db=db)

    update_data = patient.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field in PERSON_FIELDS:
            setattr(db_person, field, value)
        else:
            setattr(db_patient, field, value)

    db.commit()
    return db_patient
