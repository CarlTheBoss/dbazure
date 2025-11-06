import pyodbc
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def get_db_connection():
    """
    Crea y devuelve una conexión a la base de datos utilizando las variables de entorno.
    """
    try:
        connection_string = (
            f"DRIVER={os.getenv('DB_DRIVER')};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USERNAME')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None