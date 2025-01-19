from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .quarto import Quarto
    from .reserva import Reserva
    from .atendente import Atendente


class ClienteBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: int


class Cliente(ClienteBase, table=True):
    reservas: List["Reserva"] = Relationship(back_populates="cliente")
    quartos: List["Quarto"] = Relationship(back_populates="cliente")
    atendente_id: Optional[int] = Field(default=None, foreign_key="atendente.id")
    atendente: Optional["Atendente"] = Relationship(back_populates="clientes")