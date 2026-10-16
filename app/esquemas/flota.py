from pydantic import BaseModel, Field

class VehiculoCrear(BaseModel):
    nombre: str = Field(..., example="Montacargas IoT Pro")
    modelo: str = Field(..., example="Modelo Elevador X")
    descripcion: str = Field(..., example="Montacargas con elevador y sensores")
    microcontrolador: str = Field(..., example="ESP8266")

class VehiculoActualizar(BaseModel):
    nombre: str
    modelo: str
    descripcion: str
    microcontrolador: str
    activo: bool = True