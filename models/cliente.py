from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .quarto import quarto
    from .reserva import reserva

class ClienteBase(SQLModel): 
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: int

class Cliente(ClienteBase, table=True):
    reserva: 
    quarto: