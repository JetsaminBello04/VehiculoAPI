from typing import Any, List, Dict
from app.datos.puente_rds import obtener_conexion

def ejecutar_sp_lectura(sp_nombre: str, parametros: tuple = ()) -> List[Dict[str, Any]]:
    """Ejecuta Stored Procedures de lectura (GET) 🌸"""
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc(sp_nombre, parametros)
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        return resultados
    finally:
        cursor.close()
        conn.close()

def ejecutar_sp_escritura(sp_nombre: str, parametros: tuple = ()) -> Any:
    """Ejecuta Stored Procedures de escritura/modificación (POST) 💅"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.callproc(sp_nombre, parametros)
        inserted_id = None
        for result in cursor.stored_results():
            rows = result.fetchall()
            if rows:
                inserted_id = rows[0][0]
        conn.commit()
        return inserted_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def procesar_movimiento_transaccional(id_vehiculo: int, id_comando: int, origen: str = "API") -> bool:
    """Transacción atómica: Llama sp_actualizar_estado y sp_registrar_historial juntas ✨"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        
        # 1. Actualiza estado del montacargas
        cursor.callproc('sp_actualizar_estado', [id_vehiculo, id_comando, True])
        for _ in cursor.stored_results():
            _.fetchall()
            
        # 2. Registra en el historial (SOLO para movimientos individuales)
        cursor.callproc('sp_registrar_historial', [id_vehiculo, id_comando, origen])
        for _ in cursor.stored_results():
            _.fetchall()
            
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()