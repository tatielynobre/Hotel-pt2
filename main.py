from fastapi import FastAPI
from routes import clientes, home, reservas, quartos, atendentes
from contextlib import asynccontextmanager
from database import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


# Substituir o evento de startup pelo gerenciador de ciclo de vida
app = FastAPI(lifespan=lifespan)

app.include_router(clientes.router)
app.include_router(home.router)
app.include_router(quartos.router)
app.include_router(reservas.router)
app.include_router(atendentes.router)