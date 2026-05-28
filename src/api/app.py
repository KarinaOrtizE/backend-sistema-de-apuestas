import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

_default_cors_origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://sistema-de-apuestas-c4610.web.app",
]

_extra = os.getenv("CORS_ORIGINS", "")
_extra_origins = [o.strip() for o in _extra.split(",") if o.strip()]
_cors_allow_origins = list(dict.fromkeys(_default_cors_origins + _extra_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
