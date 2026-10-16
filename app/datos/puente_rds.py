import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    """Crea la conexión segura hacia Amazon RDS 🌉✨"""
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER")
    # Busca tanto DB_PASSWORD como DB_PASS
    password = os.getenv("DB_PASSWORD") or os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")

    if not password:
        raise ValueError("Error: No se encontró la contraseña de RDS en el archivo .env")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )