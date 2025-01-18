from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .cliente import Cliente


class AtendenteBase(SQLModel):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    nome: str


class Atendente(AtendenteBase, table=True):
    clientes: List["Cliente"] = Relationship(back_populates="atendente")
