from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import date

if TYPE_CHECKING:
    from .cliente import Cliente
    from .quarto import Quarto

class ReservaBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_inicio: date
    data_fim: date
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    quarto_id: int = Field(default=None, foreign_key="quarto.id")

class Reserva(ReservaBase, table=True):
    cliente: "Cliente" = Relationship(back_populates="reservas")
    quarto: "Quarto" = Relationship(back_populates="reservas")  


class ReservaBaseWithCliente(ReservaBase):
    cliente: Optional["Cliente"]