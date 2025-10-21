from sqlalchemy.orm import Session
from src.models import AppointmentModel, PersonModel
from src.schemas import PatientCreate, ProviderCreate


def get_by_id(table, id: int, db: Session):
    return db.query(table).filter(table.id == id).first()

def search_resource(table, filters: dict, db: Session):
    query = db.query(table)
    for column_name, filter_value in filters.items():
        column = getattr(table, column_name)
        if filter_value == "null":
            query = query.filter(column.is_(None))
        elif filter_value == "not_null":
            query = query.filter(column.isnot(None))
        else:
            query = query.filter(column == filter_value)
    
    return query.first()

def verify_active_appointments(filter_id_column, id: int, db: Session):
    status_values = ['scheduled', 'confirmed', 'in_progress']

    return (
        db.query(AppointmentModel)
        .filter(
            AppointmentModel.status.in_(status_values), filter_id_column == id
        )
        .first()
    )


def create_person(resource: PatientCreate | ProviderCreate, db: Session):
    db_person = PersonModel(
        name=resource.name,
        birth_date=resource.birth_date,
        document=resource.document,
        gender=resource.gender,
        phone_number=resource.phone_number,
        email=resource.email,
    )

    db.add(db_person)
    db.commit()

    db.refresh(db_person)
    return db_person
