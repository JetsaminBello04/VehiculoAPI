from fastapi import APIRouter, HTTPException
from app.esquemas.instrucciones import SolicitarMovimiento
from app.datos.invocador_sp import ejecutar_sp_lectura, procesar_movimiento_transaccional
from app.en_vivo.director import gestor_ws

router = APIRouter(prefix="/api/telemetria", tags=["3. Estado y Movimientos Individuales 📡✨"])

@router.post("/vehiculo/{id_vehiculo}/movimiento")
async def ejecutar_movimiento_individual(id_vehiculo: int, req: SolicitarMovimiento):
    try:
        # 1. Transacción atómica en RDS (sp_actualizar_estado + sp_registrar_historial)
        procesar_movimiento_transaccional(id_vehiculo, req.id_comando, 'API_POST')

        # 2. Obtener información del comando para notificar por WebSocket
        cmds = ejecutar_sp_lectura('sp_obtener_comandos_vehiculo', (id_vehiculo,))
        nombre_cmd = "COMANDO_EJECUTADO"
        codigo_cmd = req.id_comando
        
        for c in cmds:
            if c.get('id_comando') == req.id_comando:
                nombre_cmd = c.get('nombre', nombre_cmd)
                codigo_cmd = c.get('codigo', codigo_cmd)
                break

        # 3. Transmisión en tiempo real por WebSocket
        await gestor_ws.emitir_evento(id_vehiculo, {
            "evento": "MOVIMIENTO_INDIVIDUAL",
            "id_vehiculo": id_vehiculo,
            "id_comando": req.id_comando,
            "comando": nombre_cmd,
            "codigo": codigo_cmd
        })

        return {
            "mensaje": "Movimiento registrado en RDS y transmitido por WebSocket 🚀✨",
            "estado": "OK"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error al procesar movimiento en RDS: {str(e)}"
        )

@router.get("/vehiculo/{id_vehiculo}/estado")
async def obtener_estado_vehiculo(id_vehiculo: int):
    data = ejecutar_sp_lectura('sp_obtener_estado', (id_vehiculo,))
    return data[0] if data else {}