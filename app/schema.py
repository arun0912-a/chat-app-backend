from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    type: str
    username: str
    content: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
