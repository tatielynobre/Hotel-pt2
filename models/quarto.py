from sqlmodel import SQLModel, Field, Relationship
from .reserva import Reserva
from typing import Optional, List
from .cliente import Cliente


class QuartoBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_quarto: str
    numero_quarto: int


class Quarto(QuartoBase, table=True):
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.id")
    cliente: "Cliente" = Relationship(back_populates="quartos")
    reservas: List["Reserva"] = Relationship(back_populates="quarto")
