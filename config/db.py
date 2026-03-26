import mysql.connector
import streamlit as st

# connect to db
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",
        database="Sales_Management_System"
    )

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