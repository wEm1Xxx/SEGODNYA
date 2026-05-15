from peewee import MySQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    """Возвращает соединение с БД (используется в моделях через Base)."""
    return MySQLDatabase(
        os.getenv('DB_NAME', 'hotel_db'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306))
    )