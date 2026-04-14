import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# connect to db
def get_connection():
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME") # comment this line if you want to create database first time
    port = os.getenv("DB_PORT")

    if not user or not password or not database:
        raise EnvironmentError(
            "Database credentials are not fully configured. "
            "Set DB_USER, DB_PASSWORD, and DB_NAME in environment variables."
        )

    connection_args = {
        "host": host,
        "user": user,
        "password": password,
        "database": database, #comment this line if you want to create database first time
    }

    if port:
        connection_args["port"] = int(port)

    return mysql.connector.connect(**connection_args)

# query for one row
def fetch_one(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# query for all row
def fetch_all(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# query for without return value
def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()
