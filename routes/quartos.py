from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.quarto import Quarto, QuartoBase
from database import get_session

router = APIRouter(
    prefix="/quartos",
    tags=["Quartos"],
)


# Criar um novo quarto
@router.post("/", response_model=Quarto)
def create_quarto(quarto: QuartoBase, session: Session = Depends(get_session)):
    novo_quarto = Quarto(**quarto.model_dump())
    session.add(novo_quarto)
    session.commit()
    session.refresh(novo_quarto)
    return novo_quarto


@router.get("/", response_model=list[Quarto])
def list_quartos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    quartos = session.exec(select(Quarto).offset(offset).limit(limit)).all()
    return quartos


# Buscar quarto por id especifico
@router.get("/{quarto_id}", response_model=Quarto)
def get_quarto(quarto_id: int, session: Session = Depends(get_session)):
    quarto = session.get(Quarto, quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")
    return quarto


# Atualizar um quarto
@router.put("/{quarto_id}", response_model=Quarto)
def update_quarto(
    quarto_id: int, quarto: QuartoBase, session: Session = Depends(get_session)
):
    db_quarto = session.get(Quarto, quarto_id)
    if not db_quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")

    for key, value in quarto.model_dump(exclude_unset=True).items():
        setattr(db_quarto, key, value)

    session.add(db_quarto)
    session.commit()
    session.refresh(db_quarto)
    return db_quarto


# Excluir um quarto
@router.delete("/{quarto_id}")
def delete_quarto(quarto_id: int, session: Session = Depends(get_session)):
    quarto = session.get(Quarto, quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto não encontrado")

    session.delete(quarto)
    session.commit()
    return {"ok": True}
