from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from src.config import settings
from src.controllers import (
    authenticate,
    create_appointment,
    create_patient,
    create_provider,
    delete_patient,
    delete_provider,
    get_appointments,
    get_patients,
    get_providers,
    update_appointment,
    update_patient,
    update_provider,
    create_user,
)
from src.dependencies import CurrentUser, SessionDep
from src.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AppointmentUpdate,
    PatientCreate,
    PatientResponse,
    PatientUpdate,
    ProviderCreate,
    ProviderResponse,
    ProviderUpdate,
    Token,
    User,
    UserCreate,
)
from src.security import create_access_token

router = APIRouter()

@router.get('/')
def intro_message():
    return "Welcome to 'a clinica' API!"

# Autenticação
@router.post('/login/', response_model=Token)
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate(
        session=session,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post('/singup/', response_model=User)
async def create_user_route(session: SessionDep, user: UserCreate):
    return create_user(session, user)


# Pacientes
@router.post('/patients/', response_model=PatientResponse)
async def create_patient_route(
    patient: PatientCreate, db: SessionDep, _current_user: CurrentUser
):
    return create_patient(db=db, patient_info=patient)


@router.get('/patients/', response_model=list[PatientResponse])
async def read_all_patients_route(db: SessionDep):
    return get_patients(db)


@router.put('/patients/{patient_id}', response_model=PatientResponse)
async def update_patient_route(
    patient_id: int,
    patient: PatientUpdate,
    db: SessionDep,
    _current_user: CurrentUser,
):
    db_patient = update_patient(db, patient_id=patient_id, patient=patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail='Patient not found')
    return db_patient


@router.delete(
    '/patients/{patient_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def delete_patient_route(
    patient_id: int, db: SessionDep, _current_user: CurrentUser
):
    delete_patient(db, patient_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Profissionais
@router.post('/providers/', response_model=ProviderResponse)
async def create_provider_route(
    provider: ProviderCreate, db: SessionDep, _current_user: CurrentUser
):
    return create_provider(db=db, provider_info=provider)


@router.get('/providers/', response_model=list[ProviderResponse])
async def read_all_providers_route(db: SessionDep, _current_user: CurrentUser):
    return get_providers(db)


@router.put('/providers/{provider_id}', response_model=ProviderResponse)
async def update_provider_route(
    provider_id: int,
    provider: ProviderUpdate,
    db: SessionDep,
    _current_user: CurrentUser,
):
    db_provider = update_provider(
        db, provider_id=provider_id, provider=provider
    )
    if db_provider is None:
        raise HTTPException(status_code=404, detail='Provider not found')
    return db_provider


@router.delete(
    '/providers/{provider_id}', status_code=status.HTTP_204_NO_CONTENT
)
async def delete_provider_route(
    provider_id: int, db: SessionDep, _current_user: CurrentUser
):
    delete_provider(db, provider_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Atendimentos
@router.post('/appointments/', response_model=AppointmentResponse)
async def create_appointment_route(
    appointment: AppointmentCreate, db: SessionDep, _current_user: CurrentUser
):
    return create_appointment(db=db, appointment_info=appointment)


@router.get('/appointments/', response_model=list[AppointmentResponse])
async def read_all_appointments_route(
    db: SessionDep, _current_user: CurrentUser
):
    return get_appointments(db)


@router.put(
    '/appointments/{appointment_id}', response_model=AppointmentResponse
)
async def update_appointment_route(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: SessionDep,
    _current_user: CurrentUser,
):
    db_appointment = update_appointment(
        db, appointment_id=appointment_id, appointment=appointment
    )
    if db_appointment is None:
        raise HTTPException(status_code=404, detail='Appointment not found')
    return db_appointment
