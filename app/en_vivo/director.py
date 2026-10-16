from fastapi import WebSocket
from typing import Dict, List
import json
from datetime import datetime

class GestorCanalWebSocket:
    """Administra conexiones concurrentes por vehículo y emite eventos en vivo 📡✨"""
    def __init__(self):
        self.conexiones_activas: Dict[int, List[WebSocket]] = {}

    async def conectar(self, id_vehiculo: int, websocket: WebSocket):
        await websocket.accept()
        if id_vehiculo not in self.conexiones_activas:
            self.conexiones_activas[id_vehiculo] = []
        self.conexiones_activas[id_vehiculo].append(websocket)

    def desconectar(self, id_vehiculo: int, websocket: WebSocket):
        if id_vehiculo in self.conexiones_activas:
            if websocket in self.conexiones_activas[id_vehiculo]:
                self.conexiones_activas[id_vehiculo].remove(websocket)

    async def emitir_evento(self, id_vehiculo: int, evento: dict):
        if id_vehiculo in self.conexiones_activas:
            evento["timestamp"] = datetime.now().isoformat()
            mensaje = json.dumps(evento)
            for conexion in self.conexiones_activas[id_vehiculo]:
                try:
                    await conexion.send_text(mensaje)
                except Exception:
                    pass

gestor_ws = GestorCanalWebSocket()