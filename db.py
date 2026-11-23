"""Connessione a MariaDB. I parametri arrivano dalle variabili d'ambiente PANTRY_DB_*."""

import os

import pymysql
from pymysql.cursors import DictCursor


def connect():
    return pymysql.connect(
        host=os.environ.get("PANTRY_DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("PANTRY_DB_PORT", "3306")),
        user=os.environ.get("PANTRY_DB_USER", "pantry"),
        password=os.environ.get("PANTRY_DB_PASSWORD", ""),
        database=os.environ.get("PANTRY_DB_NAME", "pantry"),
        charset="utf8mb4",
        cursorclass=DictCursor,  # ogni riga è un dict: row["name"]
    )
