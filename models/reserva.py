from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime
from cliente import Cliente, ClienteBase
from quarto import Quarto

if TYPE_CHECKING:
    from cliente import Cliente
    from quarto import Quarto

class ReservaBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    data_inicio: datetime
    data_fim: datetime

class Reserva(ReservaBase, table= True):
    cliente_id: int = Field(foreign_key="cliente.id")
    id_quarto: int = Field(foreign_key="quarto.id")
    
    cliente: 'Cliente' = Relationship(back_populates="reservas")
    quarto: 'Quarto' = Relationship(back_populates="reservas")

class ReservaBaseWithCliente(ReservaBase):
    user: ClienteBase