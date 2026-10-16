from fastapi import APIRouter, HTTPException
from app.esquemas.flota import VehiculoCrear, VehiculoActualizar
from app.datos.invocador_sp import ejecutar_sp_lectura, ejecutar_sp_escritura

router = APIRouter(prefix="/api/vehiculos", tags=["Gestión de Flota 🚗✨"])

@router.post("")
async def crear_vehiculo(v: VehiculoCrear):
    # SP 1: sp_crear_vehiculo
    nuevo_id = ejecutar_sp_escritura('sp_crear_vehiculo', (v.nombre, v.modelo, v.descripcion, v.microcontrolador))
    return {"mensaje": "Vehículo registrado con éxito 🌸", "id_vehiculo": nuevo_id}

@router.get("")
async def obtener_vehiculos():
    # SP 2: sp_obtener_vehiculos
    return ejecutar_sp_lectura('sp_obtener_vehiculos', ())

@router.get("/{id_vehiculo}")
async def obtener_vehiculo(id_vehiculo: int):
    # SP 3: sp_obtener_vehiculo
    data = ejecutar_sp_lectura('sp_obtener_vehiculo', (id_vehiculo,))
    if not data:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado 💔")
    return data[0]

@router.put("/{id_vehiculo}")
async def actualizar_vehiculo(id_vehiculo: int, v: VehiculoActualizar):
    # SP 4: sp_actualizar_vehiculo
    ejecutar_sp_escritura('sp_actualizar_vehiculo', (id_vehiculo, v.nombre, v.modelo, v.descripcion, v.microcontrolador, v.activo))
    return {"mensaje": "Vehículo actualizado 💅"}

@router.delete("/{id_vehiculo}")
async def eliminar_vehiculo(id_vehiculo: int):
    # SP 5: sp_eliminar_vehiculo
    ejecutar_sp_escritura('sp_eliminar_vehiculo', (id_vehiculo,))
    return {"mensaje": "Vehículo eliminado 🧹"}