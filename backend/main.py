from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Jugador(BaseModel):
    nombre: str
    posicion: str
    dorsal: int


app = FastAPI(
    title="Club ULEAM Backend",
    description="Backend para gestionar jugadores del Club ULEAM.",
    version="1.0.0",
)

db_jugadores = [
    {"nombre": "Juan Perez", "posicion": "Portero", "dorsal": 1},
    {"nombre": "Carlos Vera", "posicion": "Defensa", "dorsal": 4},
    {"nombre": "Mauro Lucas", "posicion": "Mediocampista", "dorsal": 8},
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "Backend FastAPI del Club ULEAM activo.",
        "estado": "ok",
    }


@app.get("/jugadores")
def obtener_jugadores():
    return db_jugadores


@app.post("/jugadores")
def crear_jugador(jugador: Jugador):
    db_jugadores.append(jugador.model_dump())
    return {
        "mensaje": "Jugador agregado correctamente.",
        "estado": "success",
        "jugador": jugador,
    }


@app.delete("/jugadores/{dorsal}")
def eliminar_jugador(dorsal: int):
    global db_jugadores

    jugador_existe = any(jugador["dorsal"] == dorsal for jugador in db_jugadores)

    if not jugador_existe:
        raise HTTPException(status_code=404, detail="Jugador no encontrado.")

    db_jugadores = [
        jugador for jugador in db_jugadores if jugador["dorsal"] != dorsal
    ]

    return {
        "mensaje": f"Jugador con dorsal {dorsal} eliminado correctamente.",
        "estado": "success",
    }
