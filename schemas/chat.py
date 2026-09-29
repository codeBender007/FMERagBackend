# schemas/chat.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sql_executed: Optional[str] = None

class SessionItem(BaseModel):
    session_id: str
    title: Optional[str] = "New conversation"
    created_at: Optional[datetime] = None

class SessionListResponse(BaseModel):
    sessions: List[SessionItem]

class MessageItem(BaseModel):
    id: Optional[int] = None 
    sender: str
    message_text: str
    sql_executed: Optional[str] = None
    created_at: Optional[datetime] = None

class HistoryResponse(BaseModel):
    session_id: str
    messages: List[MessageItem]