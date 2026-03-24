import mysql.connector

def get_raw_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="raw_data_db"
    )

def get_processed_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="processed_data_db"
    )
