import pandas as pd
import os
import pyodbc
from logger import get_logger
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


logger = get_logger(__name__)

def get_sql_server_connection (driver: str = "SQL Server", 
                               server: str | None = None,
                               database: str | None = None,
                               username: str | None = None,
                               password: str | None = None) -> pyodbc.Connection:
    logger.info("Initializing connection to the Server...")

    server = server or os.getenv("DB_SERVER")
    database = database or os.getenv("DB_NAME")
    username = username or os.getenv("DB_USER")
    password = password or os.getenv("DB_PASSWORD")

    if not all([server, database, username, password]):
        raise ValueError("Missing database credentials in environment variables")
    
    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )
    logger.info("Connection is successful!")
    return pyodbc.connect(conn_str)
    

def load_data_from_file(filepath: str) -> pd.DataFrame:
    # Use chunking if the dataset is large
    return pd.read_csv(filepath)

def load_sql(path):
    with open(path, "r") as file:
        return file.read()


def load_data_from_sql(
        query_path: str,
        engine,
        chunk_size: int | None = None,
        **kwargs):
    
    query = load_sql(query_path)

    return pd.read_sql(
        query,
        engine,
        chunksize=chunk_size,
        **kwargs
    )