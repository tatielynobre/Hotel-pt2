from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

class QuartoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nivel_quarto: str
class Quarto(QuartoBase, table=True):
    