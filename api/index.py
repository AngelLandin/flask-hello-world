from flask import Flask
import psycopg2
from dotenv import load_dotenv
import os

#Fetch variables
CONNECTION_STRING = os.getenv("CONN_STRING")

app = Flask(__name__)

# Function for connection to the database
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
    # Connection to the database
   try:
       connection = get_connection()
       print("Connection successful!")
        #Create a cursor to execute SQL queries
        cursor = connection.cursor()




