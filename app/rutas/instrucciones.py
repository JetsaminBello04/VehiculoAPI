from fastapi import APIRouter
from app.esquemas.instrucciones import ComandoCrear, ComandoActualizar
from app.datos.invocador_sp import ejecutar_sp_lectura, ejecutar_sp_escritura

router = APIRouter(prefix="/api/comandos", tags=["2. Catálogo de Comandos 🕹️🎀"])

@router.post("")
async def crear_comando(c: ComandoCrear):
    # SP 6: sp_crear_comando
    nuevo_id = ejecutar_sp_escritura('sp_crear_comando', (c.id_vehiculo, c.nombre, c.codigo, c.descripcion))
    return {"mensaje": "Comando guardado en catálogo ⚡", "id_comando": nuevo_id}

@router.get("/vehiculo/{id_vehiculo}")
async def obtener_comandos_vehiculo(id_vehiculo: int):
    # SP 7: sp_obtener_comandos_vehiculo
    return ejecutar_sp_lectura('sp_obtener_comandos_vehiculo', (id_vehiculo,))

@router.post("/{id_comando}/actualizar")
async def actualizar_comando(id_comando: int, c: ComandoActualizar):
    # SP 8: sp_actualizar_comando
    ejecutar_sp_escritura('sp_actualizar_comando', (id_comando, c.nombre, c.codigo, c.descripcion, c.activo))
    return {"mensaje": "Comando actualizado 🛠️"}

@router.post("/{id_comando}/eliminar")
async def eliminar_comando(id_comando: int):
    # SP 9: sp_eliminar_comando
    ejecutar_sp_escritura('sp_eliminar_comando', (id_comando,))
    return {"mensaje": "Comando eliminado del catálogo 🗑️"}