from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi

from app.rutas.flota import router as flota_router
from app.rutas.instrucciones import router as instrucciones_router
from app.rutas.telemetria import router as telemetria_router
from app.rutas.bitacora import router as bitacora_router
from app.rutas.coreografias import router as coreografias_router

from app.datos.invocador_sp import ejecutar_sp_lectura
from app.en_vivo.director import gestor_ws

app = FastAPI(docs_url=None)

# Routers de los 21 Stored Procedures
app.include_router(flota_router)
app.include_router(instrucciones_router)
app.include_router(telemetria_router)
app.include_router(bitacora_router)
app.include_router(coreografias_router)

# WebSocket Endpoint (Servicio en tiempo real)
@app.websocket("/ws/vehiculo/{id_vehiculo}")
async def websocket_endpoint(websocket: WebSocket, id_vehiculo: int):
    await gestor_ws.conectar(id_vehiculo, websocket)
    try:
        # Intentamos obtener el estado inicial de RDS de forma segura
        try:
            estado_inicial = ejecutar_sp_lectura('sp_obtener_estado', (id_vehiculo,))
            if estado_inicial:
                await websocket.send_json({
                    "evento": "ESTADO_INICIAL",
                    "datos": estado_inicial[0]
                })
        except Exception as e:
            # Si falla la BD, notificamos la bienvenida sin tumbar la conexión
            await websocket.send_json({
                "evento": "CONEXION_ESTABLECIDA",
                "mensaje": f"Conectado al vehículo {id_vehiculo} ✨"
            })

        while True:
            await websocket.receive_text()  # Mantiene la conexión abierta
    except WebSocketDisconnect:
        gestor_ws.desconectar(id_vehiculo, websocket)
        
@app.get("/", include_in_schema=False)
async def ir_a_docs():
    return RedirectResponse(url="/docs")

@app.get("/docs", include_in_schema=False)
async def swagger_girly():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <title>Montacargas IoT API - Dev Docs 🌸✨</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" >
    <style>
        .swagger-ui .topbar { background-color: #f3e5f5 !important; border-bottom: 2px solid #e1bee7; }
        .swagger-ui .info .title { color: #8e24aa !important; font-family: 'Comic Sans MS', cursive, sans-serif; }
        .swagger-ui .opblock.opblock-post .opblock-summary { background-color: #fce4ec !important; border-color: #f8bbd0 !important; }
        .swagger-ui .opblock.opblock-get .opblock-summary { background-color: #f3e5f5 !important; border-color: #e1bee7 !important; }
        .swagger-ui .btn.execute { background-color: #ba68c8 !important; color: white !important; border-radius: 20px; }
        body { background-color: #fffafb; }
    </style>
    </head>
    <body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
    window.onload = function() {
        window.ui = SwaggerUIBundle({ url: '/openapi.json', dom_id: '#swagger-ui' });
    }
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

@app.get("/openapi.json", include_in_schema=False)
async def openapi_schema():
    return get_openapi(title="Montacargas IoT API 🌸🏗️", version="1.0.0", routes=app.routes)