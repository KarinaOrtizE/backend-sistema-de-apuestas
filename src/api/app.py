from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables

from . import (
    apuesta,
    billetera,
    bingo,
    loteria,
    metodo_pago,
    ruleta,
    sorteo,
    transaccion,
    usuario,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    import src.entities.apuesta
    import src.entities.billetera
    import src.entities.bingo
    import src.entities.loteria
    import src.entities.metodo_pago
    import src.entities.ruleta
    import src.entities.sorteo
    import src.entities.transaccion
    import src.entities.usuario

    create_tables()
    yield


app = FastAPI(title="API Sistema de Apuestas", version="1.0.0", lifespan=lifespan)

app.include_router(usuario.router)
app.include_router(apuesta.router)
app.include_router(billetera.router)
app.include_router(bingo.router)
app.include_router(loteria.router)
app.include_router(metodo_pago.router)
app.include_router(ruleta.router)
app.include_router(sorteo.router)
app.include_router(transaccion.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
