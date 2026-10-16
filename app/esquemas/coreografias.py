from pydantic import BaseModel, Field

class DemoCrear(BaseModel):
    id_vehiculo: int
    nombre: str = Field(..., example="Demo Rutina de Carga")
    descripcion: str = Field(..., example="Secuencia automática para mover tarimas")

class DemoActualizar(BaseModel):
    nombre: str
    descripcion: str
    activo: bool = True

class MovimientoDemoCrear(BaseModel):
    id_demo: int
    id_comando: int
    orden: int
    duracion_ms: int = Field(..., example=2000)
    pausa_ms: int = Field(default=300, example=300)

class MovimientoDemoActualizar(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int