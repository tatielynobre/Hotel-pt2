from pydantic import BaseModel
from datetime import date

class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: int

    class Config:
        orm_mode = True
        
class QuartoResponse(BaseModel):
    id: int
    numero_quarto: int
    nivel_quarto: str

    class Config:
        orm_mode = True

class ReservaResponse(BaseModel):
    id: int
    data_inicio: date
    data_fim: date
    cliente: ClienteResponse
    quarto: QuartoResponse

    class Config:
        orm_mode = True
