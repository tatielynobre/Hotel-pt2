```mermaid
classDiagram
    class reserva{
    id: int
    id_quarto: int
    id_cliente: int
    data_inicio: str
    data_fim: str
}
class quarto{
    id: int
    nivel_quarto: str    
}
class cliente{
    id: int
    nome: str
    email: str
    telefone: int
}
cliente "1"--"1"reserva
quarto "1"--"1" reserva
quarto "1"--"1" cliente
```
