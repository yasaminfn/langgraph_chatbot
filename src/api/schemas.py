from pydantic import BaseModel
class Question(BaseModel):
    query: str
    session_id : str = None