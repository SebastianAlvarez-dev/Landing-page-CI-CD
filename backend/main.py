import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import Client, create_client


class Jugador(BaseModel):
    nombre: str
    posicion: str
    dorsal: int


app = FastAPI(
    title="Club ULEAM Backend",
    description="Backend para gestionar jugadores del Club ULEAM con Supabase.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def obtener_cliente_supabase() -> Client:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail="Faltan las variables de entorno SUPABASE_URL y SUPABASE_KEY.",
        )

    return create_client(supabase_url, supabase_key)


@app.get("/")
def inicio():
    return {
        "mensaje": "Backend FastAPI del Club ULEAM activo con Supabase.",
        "estado": "ok",
        "base_datos": "supabase",
    }


@app.get("/jugadores")
def obtener_jugadores():
    supabase = obtener_cliente_supabase()
    respuesta = (
        supabase.table("jugadores")
        .select("nombre,posicion,dorsal")
        .order("dorsal")
        .execute()
    )
    return respuesta.data


@app.post("/jugadores")
def crear_jugador(jugador: Jugador):
    supabase = obtener_cliente_supabase()

    jugador_existente = (
        supabase.table("jugadores")
        .select("dorsal")
        .eq("dorsal", jugador.dorsal)
        .execute()
    )

    if jugador_existente.data:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un jugador con el dorsal {jugador.dorsal}.",
        )

    respuesta = (
        supabase.table("jugadores")
        .insert(jugador.model_dump())
        .execute()
    )

    return {
        "mensaje": "Jugador agregado correctamente.",
        "estado": "success",
        "jugador": respuesta.data[0] if respuesta.data else jugador.model_dump(),
    }


@app.delete("/jugadores/{dorsal}")
def eliminar_jugador(dorsal: int):
    supabase = obtener_cliente_supabase()

    jugador_existente = (
        supabase.table("jugadores")
        .select("dorsal")
        .eq("dorsal", dorsal)
        .execute()
    )

    if not jugador_existente.data:
        raise HTTPException(status_code=404, detail="Jugador no encontrado.")

    supabase.table("jugadores").delete().eq("dorsal", dorsal).execute()

    return {
        "mensaje": f"Jugador con dorsal {dorsal} eliminado correctamente.",
        "estado": "success",
    }
