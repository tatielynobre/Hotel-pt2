from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime
from cliente import cliente
from quarto import Quarto

class ReservaBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    data_inicio: datetime
    data_fim: datetime

class Reserva(ReservaBase, table= True):
    cliente_id: int = Field(foreign_key="cliente.id")
    id_quarto: int = Field(foreign_key="quarto.id")
    