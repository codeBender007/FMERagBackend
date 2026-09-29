from datetime import datetime
from sqlalchemy import Column , Integer , String , Text , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base


class ChatSession(Base):
    __tablename__ = "AIChatSessions"

    id = Column(String(50) , primary_key=True , index=True)
    user_id = Column(Integer , nullable=False , index=True)
    title = Column(String(255) , nullable=False)
    created_at = Column(DateTime , default=datetime.utcnow)

    messages = relationship("ChatMessage" , back_populates="session" , cascade="all, delete-orphan")



class ChatMessage(Base):
    __tablename__ = "AIChatMessage"

    id = Column(Integer , primary_key=True , autoincrement=True)
    session_id = Column(String(50) , ForeignKey("AIChatSessions.id" , ondelete="CASCADE") , nullable=False)
    sender = Column(String(10) , nullable=False) # user message or LLM Message
    message_text = Column(Text , nullable=False)
    sql_executed = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages") 

