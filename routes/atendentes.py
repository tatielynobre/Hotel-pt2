from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.atendente import Atendente
from database import get_session
from sqlalchemy.orm import joinedload


router = APIRouter(
    prefix="/atendentes",
    tags=["Atendentes"],
)


# Atendente
@router.post("/", response_model=Atendente)
def create_atendente(nome: str, session: Session = Depends(get_session)):
    atendente = Atendente(nome=nome)
    session.add(atendente)
    session.commit()
    session.refresh(atendente)
    return atendente


@router.get("/", response_model=list[Atendente])
def read_atendentes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Atendente).offset(offset).limit(limit)).all()


@router.get("/{atendente_id}", response_model=Atendente)
def read_atendente(atendente_id: int, session: Session = Depends(get_session)):
    atendente = session.get(Atendente, atendente_id)
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente not found")
    return atendente


@router.put("/{atendente_id}", response_model=Atendente)
def update_atendente(
    atendente_id: int, atendente: Atendente, session: Session = Depends(get_session)
):
    db_atendente = session.get(Atendente, atendente_id)
    if not db_atendente:
        raise HTTPException(status_code=404, detail="Atendente not found")
    for key, value in atendente.model_dump(exclude_unset=True).items():
        setattr(db_atendente, key, value)
    session.add(db_atendente)
    session.commit()
    session.refresh(db_atendente)
    return db_atendente


@router.delete("/{atendente_id}")
def delete_atendente(atendente_id: int, session: Session = Depends(get_session)):
    atendente = session.get(Atendente, atendente_id)
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente not found")
    session.delete(atendente)
    session.commit()
    return {"ok": True}

@router.get("/clientes", response_model=Atendente)
def listar_atendentes_com_clientes(session: Session = Depends(get_session)):
    atendentes = session.exec(select(Atendente).options(joinedload(Atendente.clientes))).all()
    return atendentes