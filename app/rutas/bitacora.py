from fastapi import APIRouter
from app.esquemas.bitacora import HistorialRegistro
from app.datos.invocador_sp import ejecutar_sp_lectura, ejecutar_sp_escritura

router = APIRouter(prefix="/api/bitacora", tags=["4. Historial y Bitácora 📖🎀"])

@router.post("/historial")
async def registrar_historial_directo(h: HistorialRegistro):
    # SP 12: sp_registrar_historial
    ejecutar_sp_escritura('sp_registrar_historial', (h.id_vehiculo, h.id_comando, h.origen))
    return {"mensaje": "Registro añadido al historial 📝"}

@router.get("/historial/{id_vehiculo}")
async def consultar_historial_limitado(id_vehiculo: int):
    """
    CONSULTA DE HISTORIAL (Regla de negocio 6):
    - Devuelve COMO MÁXIMO los 10 movimientos individuales más recientes.
    - Preserva todo el historial intacto en RDS.
    """
    # SP 13: sp_obtener_historial
    todos = ejecutar_sp_lectura('sp_obtener_historial', (id_vehiculo,))
    ultimos_diez = todos[:10]  # Recorte en memoria
    return {
        "total_mostrados": len(ultimos_diez),
        "total_en_rds": len(todos),
        "historial": ultimos_diez
    }