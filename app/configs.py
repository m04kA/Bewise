import os

USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
PORT = os.getenv("DATABASE_PORT", "5432")


'''
user: str = "admin", password: str = "root", host: str = "127.0.0.1", port: int = 5433,
                  db_name: str = "bewise_db"
                  
                  
                  - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=bewise_db
      - DATABASE_PORT=5433
      - PYTHONUNBUFFERED=True # Убрать при релизе
                  '''
