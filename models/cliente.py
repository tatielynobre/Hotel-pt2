from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .quarto import Quarto
    from .reserva import Reserva

class ClienteBase(SQLModel): 
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: int

class Cliente(ClienteBase, table=True):
    reserva: list['Reserva'] = Relationship(back_populates="cliente")
    quarto: list['Quarto'] = Relationship(back_populates="cliente")