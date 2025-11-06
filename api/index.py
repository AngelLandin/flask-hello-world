from flask import Flask
import psycopg2
import os

# ❌ LÍNEA CORREGIDA: Comentamos load_dotenv()
load_dotenv() 
# Si esta línea estuviera activa, podría cargar un archivo .env local
# que contenga una conexión de "socket" o "localhost" incorrecta,
# lo cual es incompatible con el entorno de Vercel.

# Fetch variables
# Usamos la variable de entorno 'CONN_STRING' inyectada por Vercel.
CONNECTION_STRING = os.getenv("CONN_STRING")

# Si por alguna razón la variable no se carga, detenemos la app
if not CONNECTION_STRING:
    raise ValueError("CONNECTION_STRING no está configurada. Asegúrate de definirla en Vercel.")

app = Flask(__name__)

def get_connection():
    # La cadena de conexión debe ser una URL completa de red (ej: postgresql://user:pass@host:5432/db?sslmode=require)
    return psycopg2.connect(CONNECTION_STRING)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/sensor')
def sensor():
    # Conectar a la base de datos
    try:
        connection = get_connection()
        
        # Crear un cursor para ejecutar consultas SQL
        cursor = connection.cursor()
        
        # Ejemplo query
        cursor.execute("SELECT * FROM sensores;")
        result = cursor.fetchone()
        
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()
        return f"Datos del sensor: {result}"
    
    except psycopg2.OperationalError as e:
        # Esto capturará el error específico de conexión de PostgreSQL (incluido el error del socket o SSL)
        return f"🚨 Error de Operación de BD: Verifica la CONN_STRING (URL y SSL): {e}"
        
    except Exception as e:
        # Para otros errores inesperados
        return f"❌ Fallo inesperado: {e}"

if __name__ == "__main__":
    app.run(debug=True)
