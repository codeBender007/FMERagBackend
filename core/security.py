import re
from datetime import datetime , timedelta , timezone
from typing import Optional
from jose import jwt , JWTError
from passlib.context import CryptContext
from core.config import settings

# password hashing Setup
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Dectructive SQL pattern backlist
DANGEROUS_SQL_PATTERNS = [
    r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b", r"\bDROP\b",
    r"\bALTER\b", r"\bTRUNCATE\b", r"\bEXEC\b", r"\bCREATE\b",
    r"\bMERGE\b", r"\bGRANT\b", r"\bREVOKE\b"
]

# 1) SQL Guardrail Function = this function SQL query will not effect data in database
def sanitize_and_validate_sql(query:str) -> tuple[bool , str]:
    """
    Ensures query is strictly a read-only SELECT statement.
    Returns: (is_valid: bool, cleaned_query_or_error_msg: str)
    """

    cleaned = query.strip()

    # sometime LLM give sql middle of query 
    cleaned = re.sub(r"^```(sql)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    # Rule 1: Query must be a SELECT statement or CTE culminating in SELECT
    upper_cleaned = cleaned.upper()
    if not (upper_cleaned.startswith("SELECT") or (upper_cleaned.startswith("WITH") and "SELECT" in upper_cleaned)):
        return False, "Security Error: only Allow Select query."

    for pattern in DANGEROUS_SQL_PATTERNS:
        if re.search(pattern, cleaned, flags=re.IGNORECASE):
            return False, f"Security Error: Forbidden Keyword '{pattern}'"

    return True, cleaned

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password , hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict , expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exe':expire})
    return jwt.encode(to_encode , settings.JWT_SECRET , algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None