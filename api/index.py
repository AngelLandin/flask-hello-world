from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import pool  # <--- 1. Importar el pool
from dotenv import load_dotenv
import os

load_dotenv()

# Fetch variables
CONNECTION_STRING = os.getenv("CONN_STRING")

# --- 2. Crear el pool globalmente ---
# (min_conn, max_conn, dsn_string)
# Se crea UNA VEZ cuando la app inicia.
try:
    g_db_pool = pool.SimpleConnectionPool(1, 10, dsn=CONNECTION_STRING)
    if g_db_pool:
        print("Connection pool created successfully")
except psycopg2.Error as e:
    print(f"Error creating connection pool: {e}")
    # Si el pool no se crea, la app no puede funcionar.
    # Podrías querer salir o manejar esto de otra forma.
    g_db_pool = None 

app = Flask(__name__)

def get_connection():
    # --- 3. Pedir una conexión al pool ---
    if g_db_pool:
        return g_db_pool.getconn()
    else:
        # Fallback o error si el pool no está disponible
        raise Exception("Database connection pool is not available")

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route("/sensor/<int:sensor_id>", methods=["POST"])
def insert_sensor_value(sensor_id):
    value = request.args.get("value", type=float)
    if value is None:
        return jsonify({"error": "Missing 'value' query parameter"}), 400

    conn = None # Definir conn aquí para el finally
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO sensors (sensor_id, value) VALUES (%s, %s)",
            (sensor_id, value)
        )
        conn.commit()

        return jsonify({
            "message": "Sensor value inserted successfully",
            "sensor_id": sensor_id,
            "value": value
        }), 201

    except psycopg2.Error as e:
        # Es buena idea hacer rollback si algo falla
        if conn:
            conn.rollback() 
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Capturar el error si el pool falló
        return jsonify({"error": str(e)}), 500

    finally:
        if conn and g_db_pool:
            # --- 4. Devolver la conexión al pool ---
            g_db_pool.putconn(conn) 

if __name__ == "__main__":
    app.run(debug=True)
