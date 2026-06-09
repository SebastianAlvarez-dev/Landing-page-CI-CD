from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr


class RegistroRequest(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str


app = FastAPI(
    title="Landing Page Backend",
    description="Backend independiente para recibir datos desde la landing page.",
    version="1.0.0",
)

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
        "mensaje": "Backend FastAPI activo y listo para recibir peticiones.",
        "estado": "ok",
    }


@app.post("/registro")
def registrar_datos(datos: RegistroRequest):
    return {
        "mensaje": "Registro recibido correctamente.",
        "estado": "success",
        "datos": {
            "nombre": datos.nombre,
            "correo": datos.correo,
            "telefono": datos.telefono,
        },
    }
