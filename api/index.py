from flask import Flask
import psycopg2
import os
load_dotenv()

app = Flask(__name__)

CONNECTION_STRING = os.getenv("COIN_STRING")

def get_connection():
    if not CONNECTION_STRING:
        raise Exception("CONN_STRING not found in environment variables.")
    return psycopg2.connect(CONNECTION_STRING)

@app.route('/')
def home():
    return 'Hello from Flask + Neon!'

@app.route('/sensor')
def sensor():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return f"✅ Database connected! Current time: {result}"
    except Exception as e:
        return f"❌ Database connection failed: {e}"
