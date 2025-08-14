from fastapi import FastAPI
from .routes import router

app = FastAPI()

app.include_router(router)

from src.db.crud import create_chat_history_table

@app.on_event("startup")
async def startup_event():
    await create_chat_history_table()
    print("✅ chat_history table ready")
    

@app.get("/health")
async def health_check():
    return {"status": "ok"}