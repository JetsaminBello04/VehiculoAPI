import asyncio
from fastapi import APIRouter, HTTPException
from app.esquemas.coreografias import (
    DemoCrear, DemoActualizar, MovimientoDemoCrear, MovimientoDemoActualizar
)
from app.datos.invocador_sp import ejecutar_sp_lectura, ejecutar_sp_escritura
from app.en_vivo.director import gestor_ws

router = APIRouter(prefix="/api/demos", tags=["5. Secuencias DEMO 💃✨"])

@router.post("")
async def crear_demo(d: DemoCrear):
    # SP 14: sp_crear_demo
    id_d = ejecutar_sp_escritura('sp_crear_demo', (d.id_vehiculo, d.nombre, d.descripcion))
    return {"mensaje": "Secuencia DEMO registrada 🌸", "id_demo": id_d}

@router.get("/vehiculo/{id_vehiculo}")
async def obtener_demos(id_vehiculo: int):
    # SP 15: sp_obtener_demos
    return ejecutar_sp_lectura('sp_obtener_demos', (id_vehiculo,))

@router.post("/{id_demo}/actualizar")
async def actualizar_demo(id_demo: int, d: DemoActualizar):
    # SP 16: sp_actualizar_demo
    ejecutar_sp_escritura('sp_actualizar_demo', (id_demo, d.nombre, d.descripcion, d.activo))
    return {"mensaje": "DEMO actualizada ✨"}

@router.post("/{id_demo}/eliminar")
async def eliminar_demo(id_demo: int):
    # SP 17: sp_eliminar_demo
    ejecutar_sp_escritura('sp_eliminar_demo', (id_demo,))
    return {"mensaje": "DEMO eliminada 🧹"}

@router.post("/movimiento")
async def agregar_movimiento_demo(m: MovimientoDemoCrear):
    # SP 18: sp_agregar_movimiento_demo
    ejecutar_sp_escritura('sp_agregar_movimiento_demo', (m.id_demo, m.id_comando, m.orden, m.duracion_ms, m.pausa_ms))
    return {"mensaje": "Paso añadido a la DEMO 🎬"}

@router.get("/{id_demo}/movimientos")
async def obtener_movimientos_demo(id_demo: int):
    # SP 19: sp_obtener_movimientos_demo
    return ejecutar_sp_lectura('sp_obtener_movimientos_demo', (id_demo,))

@router.post("/movimiento/{id_demo_movimiento}/actualizar")
async def actualizar_movimiento_demo(id_demo_movimiento: int, m: MovimientoDemoActualizar):
    # SP 20: sp_actualizar_movimiento_demo
    ejecutar_sp_escritura('sp_actualizar_movimiento_demo', (id_demo_movimiento, m.id_comando, m.orden, m.duracion_ms, m.pausa_ms))
    return {"mensaje": "Paso de la DEMO actualizado 🛠️"}

@router.post("/movimiento/{id_demo_movimiento}/eliminar")
async def eliminar_movimiento_demo(id_demo_movimiento: int):
    # SP 21: sp_eliminar_movimiento_demo
    ejecutar_sp_escritura('sp_eliminar_movimiento_demo', (id_demo_movimiento,))
    return {"mensaje": "Paso de la DEMO eliminado ❌"}

@router.post("/vehiculo/{id_vehiculo}/iniciar/{id_demo}")
async def iniciar_ejecucion_demo(id_vehiculo: int, id_demo: int):
    """
    EJECUCIÓN DE DEMO (Regla de negocio 8):
    - Lee N movimientos mediante sp_obtener_movimientos_demo.
    - Emite por WebSocket inicio, cada movimiento (respetando duracion/pausa) y fin.
    - Llama sp_actualizar_estado.
    - NO LLAMA A sp_registrar_historial (0 registros creados en historial).
    """
    movimientos = ejecutar_sp_lectura('sp_obtener_movimientos_demo', (id_demo,))
    if not movimientos:
        raise HTTPException(status_code=404, detail="La DEMO no contiene movimientos 💔")

    # Evento de inicio
    await gestor_ws.emitir_evento(id_vehiculo, {
        "evento": "DEMO_INICIO",
        "id_demo": id_demo,
        "total_movimientos": len(movimientos)
    })

    # Recorrido de los N movimientos
    for mov in movimientos:
        # SP 10: Actualiza estado en RDS
        ejecutar_sp_escritura('sp_actualizar_estado', (id_vehiculo, mov['id_comando'], True))

        # Notifica transmisión por WebSocket
        await gestor_ws.emitir_evento(id_vehiculo, {
            "evento": "DEMO_MOVIMIENTO",
            "orden": mov['orden'],
            "comando": mov['comando'],
            "codigo": mov['codigo'],
            "duracion_ms": mov['duracion_ms'],
            "pausa_ms": mov['pausa_ms']
        })

        # Tiempos de pausa
        await asyncio.sleep(mov['duracion_ms'] / 1000.0)
        if mov['pausa_ms'] > 0:
            await asyncio.sleep(mov['pausa_ms'] / 1000.0)

    # Evento de fin
    await gestor_ws.emitir_evento(id_vehiculo, {
        "evento": "DEMO_FIN",
        "id_demo": id_demo,
        "estado": "COMPLETADO"
    })

    return {"mensaje": "DEMO transmitida exitosamente sin alterar el historial 🌸", "movimientos_procesados": len(movimientos)}