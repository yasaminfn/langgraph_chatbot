import psycopg
from dotenv import load_dotenv
import os

load_dotenv()
conn = os.getenv("DATABASE_URL")

# Async connection
async def get_async_connection():
    return await psycopg.AsyncConnection.connect(conn)