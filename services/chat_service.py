from sqlalchemy.orm import Session
from db.models import ChatSession , ChatMessage

def get_or_create_session(db: Session , session_id: str , user_id: int , first_message: str) -> ChatSession:
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        # Question ke pehle 30 characters chat session ka title ban jayenge
        title = first_message[:30] + "..." if len(first_message) > 30 else first_message
        session = ChatSession(id=session_id , user_id = user_id , title = title)
        db.add(session)
        db.commit()
        db.refresh(session)
    return session

def save_chat_turn(db: Session, session_id: str, user_msg: str, bot_msg: str, sql_executed: str):
    user_record = ChatMessage(
        session_id=session_id,
        sender="user",
        message_text=user_msg
    )
    bot_record = ChatMessage(
        session_id=session_id,
        sender="bot",
        message_text=bot_msg,
        sql_executed=sql_executed
    )
    db.add_all([user_record, bot_record])
    db.commit()

def fetch_user_sessions(db: Session, user_id: int):
    return db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc()).all()

def fetch_session_messages(db: Session, session_id: str):
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()

def delete_session(db: Session, session_id: str) -> bool:
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False