from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.reserva import Reserva, ReservaBase
from database import get_session
from models.quarto import Quarto

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"],
)

# Criar uma reserva
@router.post("/", response_model=Reserva)
def create_reserva(reserva: ReservaBase, session: Session = Depends(get_session)):  
    quarto = session.get(Quarto, reserva.quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    
    # Criar nova reserva
    nova_reserva = Reserva(**reserva.model_dump())
    session.add(nova_reserva)
    session.commit()
    session.refresh(nova_reserva)
    return nova_reserva

@router.get("/", response_model=list[Reserva])
def list_reservas(
    offset: int = 0, limit: int = Query(default=10, le=100), session: Session = Depends(get_session)
):
    reservas = session.exec(select(Reserva).offset(offset).limit(limit)).all()
    return reservas


# Obter uma reserva específica por ID
@router.get("/{reserva_id}", response_model=Reserva)
def get_reserva(reserva_id: int, session: Session = Depends(get_session)):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


# Atualizar uma reserva
@router.put("/{reserva_id}", response_model=Reserva)
def update_reserva(reserva_id: int, reserva: ReservaBase, session: Session = Depends(get_session)):
    db_reserva = session.get(Reserva, reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    # Verificar se o quarto existe
    if reserva.quarto_id:
        quarto = session.get(Quarto, reserva.quarto_id)
        if not quarto:
            raise HTTPException(status_code=404, detail="Quarto não encontrado")
    
    # Atualizar os dados da reserva
    for key, value in reserva.model_dump(exclude_unset=True).items():
        setattr(db_reserva, key, value)
    
    session.add(db_reserva)
    session.commit()
    session.refresh(db_reserva)
    return db_reserva


# Excluir uma reserva
@router.delete("/{reserva_id}")
def delete_reserva(reserva_id: int, session: Session = Depends(get_session)):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    session.delete(reserva)
    session.commit()
    return {"ok": True}
