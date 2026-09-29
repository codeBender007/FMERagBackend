# app/routes/__init__.py
from app.routes.auth_routes import router as auth_router
from app.routes.chat_routes import router as chat_router

__all__ = ["auth_router", "chat_router"]