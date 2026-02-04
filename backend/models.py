from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Task(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None
    user_id: str

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    actions_taken: Optional[List[str]] = None