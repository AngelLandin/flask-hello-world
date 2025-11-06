from flask import Flask
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar las variables del archivo .env

# Obtener la cadena de conexión
CONNECTION_STRING = os.getenv("CONN_STRING")

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(CONNECTION_STRING)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/sensor')
def sensor():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT NOW();")
        result = cursor.fetchone()

        cursor.close()
        connection.close()
        return f"Current Time: {result}"

    except Exception as e:
        return f"Failed to connect: {e}"
