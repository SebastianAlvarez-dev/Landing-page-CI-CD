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

    supabase_url = supabase_url.rstrip("/")
    if supabase_url.endswith("/rest/v1"):
        supabase_url = supabase_url.removesuffix("/rest/v1")

    return create_client(supabase_url, supabase_key)


def manejar_error_supabase(error: Exception):
    raise HTTPException(
        status_code=500,
        detail=f"Error consultando Supabase: {str(error)}",
    )


@app.get("/")
def inicio():
    return {
        "mensaje": "Backend FastAPI del Club ULEAM activo con Supabase.",
        "estado": "ok",
        "base_datos": "supabase",
        "supabase_configurado": bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY")),
    }


@app.get("/jugadores")
def obtener_jugadores():
    supabase = obtener_cliente_supabase()
    try:
        respuesta = (
            supabase.table("jugadores")
            .select("nombre,posicion,dorsal")
            .order("dorsal")
            .execute()
        )
    except Exception as error:
        manejar_error_supabase(error)

    return respuesta.data


@app.post("/jugadores")
def crear_jugador(jugador: Jugador):
    supabase = obtener_cliente_supabase()

    try:
        jugador_existente = (
            supabase.table("jugadores")
            .select("dorsal")
            .eq("dorsal", jugador.dorsal)
            .execute()
        )
    except Exception as error:
        manejar_error_supabase(error)

    if jugador_existente.data:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe un jugador con el dorsal {jugador.dorsal}.",
        )

    try:
        respuesta = (
            supabase.table("jugadores")
            .insert(jugador.model_dump())
            .execute()
        )
    except Exception as error:
        manejar_error_supabase(error)

    return {
        "mensaje": "Jugador agregado correctamente.",
        "estado": "success",
        "jugador": respuesta.data[0] if respuesta.data else jugador.model_dump(),
    }


@app.delete("/jugadores/{dorsal}")
def eliminar_jugador(dorsal: int):
    supabase = obtener_cliente_supabase()

    try:
        jugador_existente = (
            supabase.table("jugadores")
            .select("dorsal")
            .eq("dorsal", dorsal)
            .execute()
        )
    except Exception as error:
        manejar_error_supabase(error)

    if not jugador_existente.data:
        raise HTTPException(status_code=404, detail="Jugador no encontrado.")

    try:
        supabase.table("jugadores").delete().eq("dorsal", dorsal).execute()
    except Exception as error:
        manejar_error_supabase(error)

    return {
        "mensaje": f"Jugador con dorsal {dorsal} eliminado correctamente.",
        "estado": "success",
    }
