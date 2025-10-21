from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.constants import PERSON_FIELDS
from src.helpers import (create_person, get_by_id, search_resource,
                         verify_active_appointments)
from src.models import PersonModel, ProviderModel
from src.schemas import ProviderCreate, ProviderUpdate


def get_providers(db: Session) -> list[ProviderModel]:
    return db.query(ProviderModel).all()


def get_provider(db: Session, provider_name: str) -> ProviderModel | None:
    return db.query(ProviderModel).filter(ProviderModel.name == provider_name)


def create_provider(db: Session, provider_info: ProviderCreate):
    person_exists = search_resource(
        table=PersonModel, filters={'document': provider_info.document}, db=db
    )
    if person_exists:
        provider_exists = search_resource(
            table=ProviderModel,
            filters={'person_id': person_exists.id},
            db=db,
        )
        # se o paciente estiver ativo no sistema, nao cria um novo
        if provider_exists and provider_exists.deleted_at is None:
            raise HTTPException(
            status_code=409,
            detail='Provider already exists.',
        )
        person_id = provider_exists.person_id
        person_exists.deleted_at = None
        db.commit()
    else:   
        person = create_person(resource=provider_info, db=db)
        person_id = person.id
        
    db_provider = ProviderModel(
        person_id=person_id,
        specialty=provider_info.specialty,
        work_shift=provider_info.work_shift,
        license_number=provider_info.license_number,
        active=provider_info.active,
        availability_notes=provider_info.availability_notes,
    )

    db.add(db_provider)
    db.commit()

    db.refresh(db_provider)
    return db_provider


def delete_provider(db: Session, provider_id: int):
    db_provider = get_by_id(table=ProviderModel, id=provider_id, db=db)
    if db_provider is None:
        raise HTTPException(status_code=404, detail='Provider not found')
    active_appointments = verify_active_appointments()
    if active_appointments:
        raise HTTPException(
            status_code=409,
            detail='This provider cannot be deleted because they have an in-progress, scheduled, or confirmed appointment.',
        )
    db_person = get_by_id(table=PersonModel, id=db_provider.person_id, db=db)

    now = datetime.now()
    db_provider.deleted_at = now
    db_person.deleted_at = now

    db.commit()


def update_provider(db: Session, provider_id: int, provider: ProviderUpdate):
    db_provider = get_by_id(table=ProviderModel, id=provider_id, db=db)

    if db_provider is None:
        return None

    db_person = get_by_id(table=PersonModel, id=db_provider.person_id, db=db)

    update_data = provider.dict(exclude_unset=True)

    for field, value in update_data.items():
        if field in PERSON_FIELDS:
            setattr(db_person, field, value)
        else:
            setattr(db_provider, field, value)

    db.commit()
    return db_provider
