from datetime import datetime

from .connection import get_async_connection

async def create_chat_history_table():
    conn = await get_async_connection()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id UUID,
                role VARCHAR(20),
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        await conn.commit()
    await conn.close()


async def save_message_to_db(session_id: str, role: str, content: str):
    conn = await get_async_connection()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO chat_history (session_id, role, content, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (session_id, role, content, datetime.utcnow())
        )
        await conn.commit()
    await conn.close()