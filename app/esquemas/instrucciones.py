from pydantic import BaseModel, Field

class ComandoCrear(BaseModel):
    id_vehiculo: int
    nombre: str = Field(..., example="SUBIR_PLATAFORMA")
    codigo: int = Field(..., example=5)
    descripcion: str = Field(..., example="Eleva la plataforma del montacargas")

class ComandoActualizar(BaseModel):
    nombre: str
    codigo: int
    descripcion: str
    activo: bool = True

class SolicitarMovimiento(BaseModel):
    id_comando: int = Field(..., description="ID del comando a ejecutar 🚜✨")