from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    # Application Basics
    PROJECT_NAME: str = "Furukawa LMS AI Agent"
    API_V1_STR: str = "/api/v1"
    
    # MSSQL Database Configuration
    DB_SERVER: str = r"DESKTOP-4PEOF64\SQLEXPRESS"
    DB_NAME: str = "FurukawaLMS_Dev"
    DB_DRIVER: str = "ODBC Driver 17 for SQL Server"

    # Ollama Local Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"

    # JWT Auth Configuration
    JWT_SECRET: str = "FurukawaRagAgenticAi"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"
        extra = "ignore"

# YEH LINE ZAROORI HAI (settings object export hona chahiye):
settings = Setting()