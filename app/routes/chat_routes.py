# app/routes/chat_routes.py
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from schemas.chat import ChatRequest, ChatResponse, SessionListResponse, HistoryResponse
from services.ai_engine.graph import lms_rag_agent
from services.chat_service import (
    get_or_create_session,
    save_chat_turn,
    fetch_user_sessions,
    fetch_session_messages,
    delete_session
)

router = APIRouter(prefix="/chat", tags=["Chat"])

def detect_conversational_intent(message: str) -> str | None:
    """Quickly detects greetings and non-database conversational intents to respond instantly without database/LLM overhead."""
    msg = message.strip().lower()
    
    # 1. Greetings
    if re.search(r'^(hi|hello|hey|heya|hola|namaste|hlo|hii|hiii|good\s+(morning|afternoon|evening|day))\b', msg):
        return "Hello! I am your Furukawa LMS & Shop-Floor AI Assistant. How can I help you today? You can ask me about employee records, departments, attendance, training courses, skill matrices, or daily 5M reports."
    
    # 2. Identity / Capabilities / Help
    if re.search(r'^(who\s+are\s+you|what\s+can\s+you\s+do|help\s*me|help)\b', msg) or msg in ["?", "help"]:
        return "I am the AI Assistant for Furukawa LMS & Shop-Floor Operations. I can help you search and analyze employee records, attendance punches, course enrollments, evaluation tests, skill matrices, and daily production reports."
    
    # 3. Gratitude
    if re.search(r'^(thanks|thank\s+you|thx|ty|dhanyawad|shukriya|great\s+thanks)\b', msg):
        return "You're very welcome! Feel free to ask if you need any other information from LMS."
    
    # 4. Farewells
    if re.search(r'^(bye|goodbye|cya|see\s+you|tata)\b', msg):
        return "Goodbye! Have a productive and safe day on the shop floor."

    return None

@router.post("/send", response_model=ChatResponse)
def send_chat_message(payload: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_id = 1  # Default admin ID until user token is injected
        try:
            get_or_create_session(db, payload.session_id, user_id, payload.message)
        except Exception as db_init_err:
            print(f"Warning: Could not create/verify chat session in DB: {db_init_err}")

        # 1. Check for conversational / greeting intents first
        conversational_reply = detect_conversational_intent(payload.message)
        if conversational_reply:
            try:
                save_chat_turn(db, payload.session_id, payload.message, conversational_reply, None)
            except Exception as save_err:
                print(f"Warning: Failed to save greeting turn: {save_err}")
            
            return ChatResponse(
                session_id=payload.session_id,
                answer=conversational_reply,
                sql_executed=None
            )

        # 2. Dispatch to AI Engine for database query generation
        state_input = {
            "question": payload.message,
            "session_id": payload.session_id,
            "selected_tables": [],
            "schema_context": "",
            "sql_query": "",
            "query_result": None,
            "error": None,
            "retry_count": 0,
            "final_answer": ""
        }
        
        output = lms_rag_agent.invoke(state_input)

        answer = output.get("final_answer", "No answer could be generated.")
        sql_used = output.get("sql_query", "")

        # Save turn to database safely
        try:
            save_chat_turn(db, payload.session_id, payload.message, answer, sql_used)
        except Exception as save_err:
            print(f"Warning: Failed to save chat turn: {save_err}")

        return ChatResponse(
            session_id=payload.session_id,
            answer=answer,
            sql_executed=sql_used
        )
    except Exception as e:
        print(f"Error in send_chat_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=SessionListResponse)
def get_sessions(db: Session = Depends(get_db)):
    try:
        user_id = 1
        sessions = fetch_user_sessions(db, user_id)
        return {
            "sessions": [
                {
                    "session_id": str(s.id),
                    "title": str(s.title) if s.title else "New conversation",
                    "created_at": s.created_at
                } 
                for s in sessions
            ]
        }
    except Exception as e:
        print(f"Error in get_sessions: {e}")
        return {"sessions": []}

@router.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str, db: Session = Depends(get_db)):
    try:
        messages = fetch_session_messages(db, session_id)
        return {
            "session_id": session_id,
            "messages": [
                {
                    "id": m.id,
                    "sender": str(m.sender),
                    "message_text": str(m.message_text),
                    "sql_executed": m.sql_executed,
                    "created_at": m.created_at
                }
                for m in messages
            ]
        }
    except Exception as e:
        print(f"Error in get_history for {session_id}: {e}")
        return {"session_id": session_id, "messages": []}

@router.delete("/session/{session_id}")
def remove_session(session_id: str, db: Session = Depends(get_db)):
    try:
        success = delete_session(db, session_id)
        return {"success": success}
    except Exception as e:
        print(f"Error deleting session {session_id}: {e}")
        return {"success": False}