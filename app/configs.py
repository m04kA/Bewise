import os

USER = os.getenv("POSTGRES_USER", "admin")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")
HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_NAME = os.getenv("POSTGRES_DB", "bewise_db")
PORT = os.getenv("DATABASE_PORT", "5433")

