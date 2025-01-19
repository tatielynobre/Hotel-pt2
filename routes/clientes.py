from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.cliente import Cliente, ClienteBase
from models.reserva import Reserva
from database import get_session
from models.atendente import Atendente

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
)


# Criar cliente
@router.post("/", response_model=Cliente)
def create_cliente(nome: str, email: str, telefone: int, session: Session = Depends(get_session)):
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@router.get("/", response_model=list[Cliente])
def read_clientes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Cliente).offset(offset).limit(limit)).all()


# Buscar cliente por id especifico
@router.get("/{cliente_id}", response_model=Cliente)
def read_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente

# Buscar cliente por nome
@router.get("/busca", response_model=list[Cliente])
def buscar_clientes_por_nome(nome: str, session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente).where(Cliente.nome.ilike(f"%{nome}%"))).all()
    return clientes

@router.get("/clientes/ordenados", response_model=list[Cliente])
def listar_clientes_ordenados(session: Session = Depends(get_session)):
    clientes = session.exec(select(Cliente).order_by(Cliente.nome)).all()
    return clientes



# Atualizar cliente
@router.put("/{cliente_id}", response_model=Cliente)
def update_cliente(
    cliente_id: int, cliente: ClienteBase, session: Session = Depends(get_session)
):
    db_cliente = session.get(ClienteBase, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")

    # Excluir as reservas associadas ao cliente antes de excluir o cliente
    reservas = session.exec(
        select(Reserva).where(Reserva.cliente_id == cliente_id)
    ).all()

    for reserva in reservas:
        session.delete(reserva)

    # Agora, podemos excluir o cliente
    session.delete(cliente)
    session.commit()

    return {"ok": True}

@router.put("/{cliente_id}/associar-atendente/{atendente_id}", response_model=Cliente)
def associar_cliente_a_atendente(cliente_id: int, atendente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    atendente = session.get(Atendente, atendente_id)
    if not atendente:
        raise HTTPException(status_code=404, detail="Atendente não encontrado")

    cliente.atendente_id = atendente.id
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente