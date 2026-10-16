from pydantic import BaseModel, Field

class HistorialRegistro(BaseModel):
    id_vehiculo: int
    id_comando: int
    origen: str = Field(default="MANUAL", example="MANUAL")